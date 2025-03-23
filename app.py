from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import os
from algorithm import parse_receipt_image
from PIL import Image, UnidentifiedImageError
import logging
from werkzeug.utils import secure_filename
import json
from decimal import Decimal, ROUND_HALF_UP
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session and flash messages

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def round_decimal(value: Decimal) -> Decimal:
    """Round decimal to 2 places using ROUND_HALF_UP."""
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

@app.before_request
def make_session_permanent():
    session.permanent = True

def get_session_data():
    """Get required session data or return None if missing."""
    try:
        return {
            'parsed_data': session.get('parsed_data'),
            'people_names': session.get('people_names', [])
        }
    except Exception as e:
        logger.error(f"Error getting session data: {str(e)}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'receipt' not in request.files:
            flash('No file uploaded', 'warning')
            return redirect(request.url)
            
        file = request.files['receipt']
        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(request.url)
            
        if not allowed_file(file.filename):
            flash('Invalid file type. Please upload a PNG, JPG, or GIF file.', 'warning')
            return redirect(request.url)
            
        try:
            # Save the file
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            logger.info(f"Processing receipt: {filename}")
            
            # Process the receipt
            parsed_data = parse_receipt_image(filepath)
            
            # Store results in session
            session['parsed_data'] = parsed_data
            
            # Clean up the file
            os.remove(filepath)
            
            return redirect(url_for('safety'))
            
        except Exception as e:
            logger.error(f"Error processing receipt: {str(e)}")
            flash(f'An error occurred while processing the receipt: {str(e)}', 'danger')
            return redirect(request.url)
            
    return render_template('index.html')

@app.route("/safety", methods=["GET", "POST"])
def safety():
    # Get session data
    session_data = get_session_data()
    
    # Initialize empty data if coming from manual input
    if not session_data or not session_data['parsed_data']:
        session['parsed_data'] = {
            'items': [],
            'subtotal': 0.00,
            'tax': 0.00,
            'tip': 0.00,
            'total': 0.00
        }
        parsed_data = session['parsed_data']
    else:
        parsed_data = session_data['parsed_data']
    
    if request.method == "POST":
        try:
            num_people = int(request.form.get("num_people", 1))
            if num_people < 1:
                raise ValueError("Number of people must be at least 1")
                
            session["num_people"] = num_people
            people_names = [request.form.get(f"person_name_{i}") for i in range(num_people)]
            
            # Validate people names
            if not all(name and name.strip() for name in people_names):
                flash("Please provide names for all people")
                return render_template("safety.html", parsed_data=parsed_data)
                
            session["people_names"] = people_names
            
            # Get all form keys that start with "item_name_" to determine number of items
            item_keys = [k for k in request.form.keys() if k.startswith("item_name_")]
            
            # Update items
            edited_items = []
            calculated_subtotal = Decimal('0')
            
            # Process each item
            for key in item_keys:
                try:
                    # Extract index from the key (item_name_X)
                    idx = key.split('_')[-1]
                    
                    # Get corresponding values
                    item_name = request.form.get(f"item_name_{idx}").strip()
                    if not item_name:
                        continue
                        
                    quantity = int(request.form.get(f"item_quantity_{idx}", 1))
                    if quantity < 1:
                        continue
                        
                    price_str = request.form.get(f"item_price_{idx}", '0')
                    # Remove any currency symbols and whitespace
                    price_str = price_str.replace('$', '').strip()
                    price = Decimal(price_str)
                    if price <= 0:
                        continue
                        
                    # Add to edited items
                    edited_items.append({
                        "name": item_name,
                        "quantity": quantity,
                        "price": float(price)  # Store as float for JSON serialization
                    })
                    
                    # Add to subtotal
                    calculated_subtotal += price
                        
                except (ValueError, KeyError, TypeError) as e:
                    logger.error(f"Error processing item {key}: {str(e)}")
                    flash("Please enter valid numbers for quantity and price")
                    return render_template("safety.html", parsed_data=parsed_data)
            
            # Update totals
            try:
                submitted_subtotal = Decimal(request.form.get("subtotal", '0').replace('$', '').strip())
                tax = Decimal(request.form.get("tax", '0').replace('$', '').strip())
                tip = Decimal(request.form.get("tip", '0').replace('$', '').strip())
                total = Decimal(request.form.get("total", '0').replace('$', '').strip())
                
                # Round all values consistently
                calculated_subtotal = round_decimal(calculated_subtotal)
                submitted_subtotal = round_decimal(submitted_subtotal)
                tax = round_decimal(tax)
                tip = round_decimal(tip)
                total = round_decimal(total)
                
                # Debug logging
                logger.info(f"Items processed: {len(edited_items)}")
                logger.info(f"Calculated subtotal: {calculated_subtotal}")
                logger.info(f"Submitted subtotal: {submitted_subtotal}")
                logger.info(f"Individual items: {[(item['name'], item['price']) for item in edited_items]}")
                
                # Validate totals with exact decimal comparison
                if calculated_subtotal != submitted_subtotal:
                    flash("Subtotal doesn't match item prices")
                    return render_template("safety.html", parsed_data=parsed_data)
                
                calculated_total = round_decimal(submitted_subtotal + tax + tip)
                if calculated_total != total:
                    flash("Total doesn't match subtotal + tax + tip")
                    return render_template("safety.html", parsed_data=parsed_data)
                
            except ValueError as e:
                logger.error(f"Value error in totals: {str(e)}")
                flash("Please enter valid numbers for totals")
                return render_template("safety.html", parsed_data=parsed_data)
            
            # Update session data
            parsed_data.update({
                "items": edited_items,
                "subtotal": float(submitted_subtotal),  # Convert to float for JSON
                "tax": float(tax),
                "tip": float(tip),
                "total": float(total)
            })
            session["parsed_data"] = parsed_data
            session.modified = True
            
            return redirect(url_for('assign_items'))
            
        except Exception as e:
            logger.error(f"Error in safety page: {str(e)}")
            flash("An error occurred. Please try again.")
            return render_template("safety.html", parsed_data=parsed_data)
            
    return render_template("safety.html", parsed_data=parsed_data)

@app.route("/assign_items", methods=["GET", "POST"])
def assign_items():
    # Ensure we have session data
    session_data = get_session_data()
    if not session_data:
        flash('Please enter receipt details first.', 'warning')
        return redirect(url_for('safety'))

    if request.method == 'POST':
        try:
            # Get item assignments
            item_assignments = {}
            for i, item in enumerate(session_data['parsed_data']['items']):
                assigned_to = request.form.getlist(f'item_{i}[]')
                if not assigned_to:
                    flash('Please assign all items to at least one person.', 'warning')
                    return redirect(url_for('assign_items'))
                item_assignments[item['name']] = assigned_to

            # Calculate individual costs
            individual_costs = defaultdict(Decimal)
            tax_rate = Decimal(session_data['parsed_data']['tax']) / Decimal(session_data['parsed_data']['subtotal'])
            tip_rate = Decimal(session_data['parsed_data']['tip']) / Decimal(session_data['parsed_data']['subtotal'])

            # Calculate base costs
            for item in session_data['parsed_data']['items']:
                item_price = Decimal(str(item['price']))
                assigned_to = item_assignments[item['name']]
                price_per_person = item_price / Decimal(len(assigned_to))
                
                # Add base price
                for person in assigned_to:
                    individual_costs[person] += round_decimal(price_per_person)

                # Add tax and tip for this item
                item_tax = round_decimal(item_price * tax_rate)
                item_tip = round_decimal(item_price * tip_rate)
                tax_per_person = item_tax / Decimal(len(assigned_to))
                tip_per_person = item_tip / Decimal(len(assigned_to))
                
                for person in assigned_to:
                    individual_costs[person] += round_decimal(tax_per_person)
                    individual_costs[person] += round_decimal(tip_per_person)

            # Round final amounts
            for person in individual_costs:
                individual_costs[person] = round_decimal(individual_costs[person])

            # Store results in session
            session['individual_costs'] = {k: str(v) for k, v in individual_costs.items()}
            session['item_assignments'] = item_assignments

            return redirect(url_for('results'))

        except Exception as e:
            app.logger.error(f"Error in assign_items: {str(e)}")
            flash('An error occurred while processing item assignments. Please try again.', 'danger')
            return redirect(url_for('assign_items'))

    return render_template(
        'assign_items.html',
        people_names=session_data['people_names'],
        parsed_data=session_data['parsed_data']
    )

@app.route('/results')
def results():
    # Ensure we have all required session data
    session_data = get_session_data()
    if not session_data:
        flash('Please enter receipt details first.', 'warning')
        return redirect(url_for('safety'))

    individual_costs = session.get('individual_costs')
    item_assignments = session.get('item_assignments')
    
    if not individual_costs or not item_assignments:
        flash('Please assign items to people first.', 'warning')
        return redirect(url_for('assign_items'))

    return render_template(
        'results.html',
        parsed_data=session_data['parsed_data'],
        individual_costs=individual_costs,
        item_assignments=item_assignments
    )

@app.route("/share", methods=["POST"])
def share():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Here you would implement your sharing logic
        # For example, generating a shareable link or sending an email
        
        return jsonify({"message": "Share functionality implemented here"})
        
    except Exception as e:
        logger.error(f"Error in share: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route("/manual_entry")
def manual_entry():
    # Clear only the receipt-related session data
    session['parsed_data'] = {
        'items': [],
        'subtotal': 0.00,
        'tax': 0.00,
        'tip': 0.00,
        'total': 0.00
    }
    return redirect(url_for('safety'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port) 
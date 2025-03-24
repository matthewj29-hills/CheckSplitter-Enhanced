# Check Splitter Enhanced

A modern web application that helps users split restaurant bills effortlessly using OCR technology. This enhanced version features improved receipt parsing accuracy, a beautiful user interface, and better user experience.

## Project Status
'''
The heroku hosting sight has ran out of memory, the heroku webspage is currently out of order while I search for alternate hosting/viewing alternatives. 

### Home Page
<img width="638" alt="image" src="https://github.com/user-attachments/assets/733e2a33-3243-477a-bc01-deb60dacadb8" />


### Receipt Processing
<img width="626" alt="image" src="https://github.com/user-attachments/assets/11d58749-2bc1-4a4c-8907-e5d7d54040f2" />


### Split Configuration
<img width="639" alt="image" src="https://github.com/user-attachments/assets/41f7bfde-b3d7-47b6-acaa-850c62e930ff" />


### Results Page
<img width="639" alt="image" src="https://github.com/user-attachments/assets/175123a1-c380-4d40-be13-0801e10292cd" />



### Sample Receipt
<img width="242" alt="Screenshot 2025-01-13 195025" src="https://github.com/user-attachments/assets/72865599-80a4-467a-bb66-268102972de9" />



## Features

- 📸 Upload receipt photos with drag-and-drop support
- 🔍 Dual OCR engine system (Tesseract + EasyOCR) for enhanced text extraction
- ✨ Clean, modern Bootstrap 5 interface
- 📱 Responsive design for all devices
- 🔄 Intelligent receipt parsing with pattern recognition
- 📊 Automatic item detection and price extraction
- 🧮 Smart quantity detection and price splitting
- 💰 Support for multiple items with quantity > 1
- 📝 Automatic restaurant name detection
- 🔍 Built-in receipt validation and error handling

## Technology Stack

- **Backend:**
  - Python 3.x
  - Flask web framework
  - OpenCV (opencv-python-headless) for image preprocessing
  - Tesseract OCR for primary text extraction
  - EasyOCR for secondary text extraction and validation
  - NumPy for numerical operations
  - Pillow for image processing

- **Frontend:**
  - Bootstrap 5 for responsive design
  - Font Awesome for icons
  - HTML5/CSS3 for layout and styling

- **Deployment:**
  - Heroku platform
  - Gunicorn production server
  - Ubuntu 24.04 (Heroku-24 stack)


## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CheckSplitter-Enhanced.git
cd CheckSplitter-Enhanced
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Tesseract OCR:
- Windows: Download and install from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

5. Run the application:
```bash
python app.py
```

## Deployment to Heroku

1. Create a new Heroku app:
```bash
heroku create check-splitter-enhanced
```

2. Add the Tesseract buildpack:
```bash
heroku buildpacks:add https://github.com/heroku/heroku-buildpack-apt
```

3. Push to Heroku:
```bash
git push heroku main
```

4. Set environment variables:
```bash
heroku config:set TESSDATA_PREFIX=/app/vendor/tesseract-ocr/share/tessdata
```

## Usage

1. Visit the application URL
2. Upload a receipt photo
3. Verify the extracted data
4. Add people and assign items
5. View the split results
6. Share or print the results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Tesseract OCR team
- EasyOCR team
- Flask team
- Bootstrap team 

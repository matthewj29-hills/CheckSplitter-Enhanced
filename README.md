# Check Splitter Enhanced

A modern web application that helps users split restaurant bills effortlessly using OCR technology. This enhanced version features improved receipt parsing accuracy, a beautiful user interface, and better user experience.

## Features

- 📸 Upload receipt photos with drag-and-drop support
- 🔍 Advanced OCR with multiple engines for better accuracy
- ✨ Modern, responsive user interface
- 📱 Mobile-friendly design
- 🔄 Real-time data validation
- 📊 Detailed split calculations
- 🖨️ Print-friendly results
- 🔗 Share functionality
- 💰 Support for shared items
- 🧮 Automatic tax and tip calculations

## Technology Stack

- Python/Flask
- OpenCV for image processing
- Tesseract OCR + EasyOCR for text extraction
- Bootstrap 5 for responsive design
- Font Awesome for icons
- Heroku for deployment

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
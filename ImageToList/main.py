from flask import Flask, render_template, request, redirect, url_for, send_file
import cv2
import pytesseract
import os

# Initialize the Flask application
app = Flask(__name__)

# Path to the Tesseract-OCR installation (only needed for Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust this path as needed

# Function to rearrange lines in a text file
def rearrange_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Strip whitespace and remove empty lines
    lines = [line.strip() for line in lines if line.strip()]

    # Prepare a list to hold the rearranged lines
    rearranged_lines = []

    # Iterate through the lines two at a time
    for i in range(0, len(lines), 2):
        # Check if there's a next line to pair with
        if i + 1 < len(lines):
            rearranged_lines.append(f"{lines[i]} - {lines[i + 1]}")
        else:
            rearranged_lines.append(lines[i])  # For odd number of lines

    # Write the rearranged content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        for line in rearranged_lines:
            file.write(line + '\n')

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle file upload and text extraction
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'files' not in request.files:
        return redirect(request.url)
    
    files = request.files.getlist('files')
    extracted_texts = []

    for file in files:
        if file.filename == '':
            continue
        
        # Save the uploaded file
        image_path = os.path.join('uploads', file.filename)
        file.save(image_path)
        
        # Process the image and extract text
        extracted_text = extract_text_from_image(image_path)
        extracted_texts.append(extracted_text)

        # Optionally, remove the uploaded file after processing
        os.remove(image_path)

    # Combine the extracted texts into a single string
    combined_text = "\n\n".join(extracted_texts)

    # Save the combined text to a temporary input file
    input_filename = 'input.txt'
    with open(input_filename, 'w', encoding='utf-8') as input_file:
        input_file.write(combined_text)

    # Rearrange the text and save to the output file
    output_filename = 'extracted_text.txt'
    rearrange_file(input_filename, output_filename)

    # Optionally remove the temporary input file
    os.remove(input_filename)

    return render_template('index.html', download_file=output_filename)

def extract_text_from_image(image_path):
    # Read the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Optionally apply some image processing techniques
    gray_image = cv2.GaussianBlur(gray_image, (5, 5), 0)
    
    # Use Tesseract to extract text
    extracted_text = pytesseract.image_to_string(gray_image)
    
    return extracted_text

# Route to download the text file
@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    # Create uploads directory if it doesn't exist
    os.makedirs('uploads', exist_ok=True)
    app.run(debug=True)

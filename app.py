from flask import Flask, render_template, request, redirect, send_file, url_for, after_this_request
from margin import margin_content_check, draw_border
from pdf2image import convert_from_path, convert_from_bytes
import numpy as np
import base64
import cv2
from PyPDF2 import PdfWriter, PdfReader
from PIL import Image
import io

app = Flask(__name__, static_url_path='/static', static_folder='static')

def custom_b64encode(value):
    encoded_bytes = base64.b64encode(value)
    return encoded_bytes.decode('utf-8')

# Register the custom filter with Jinja2
app.jinja_env.filters['custom_b64encode'] = custom_b64encode

@app.route("/")
def hello_one():
    return render_template("main.html")


@app.route("/margin", methods = ['GET','POST'])
def margin_detector():
   if request.method == 'POST':
        pdffile = request.files["pdfFile"]
        images = convert_from_bytes(pdffile.read(),size=1000)
        doubleside = 0 if request.form.get('checkboxOption') == None else int(request.form.get('checkboxOption'))
        fault_page_list = []
        fault_page_images = []
        for i in range(len(images)):
            if doubleside == 1 and i%2!=0:
                image = np.array(images[i])
                image = np.rot90(image , k=2)
            else:
                image = np.array(images[i])

            fl, image = margin_content_check(image)
            if fl == 1:
                fault_page_list.append(i)
                fault_page_images.append(image)
        
        
        if len(fault_page_list)==0:
            print("Document is well formated")
            flag = 1
            msg = "Document is well formatted"
            return render_template('pdf.html')
        else:
            print("Pages of the Document "+ str(fault_page_list) + " has to be verified")
            flag = 2
            msg = ", ".join(str(num+1) for num in fault_page_list)

            pdf_writer = PdfWriter()
            for i in range(len(fault_page_images)):
                new_image = draw_border(fault_page_images[i])
                pdf_image = Image.fromarray(new_image)
                pdf_buffer = io.BytesIO()
                pdf_image.save(pdf_buffer, format='PDF')
                pdf_buffer.seek(0)
                pdf_page = PdfReader(pdf_buffer).pages[0]
                pdf_writer.add_page(pdf_page)

            # Create an in-memory buffer to hold the PDF data 
                output_pdf_buffer = io.BytesIO()

            # Save the PDF data to the buffer
                pdf_writer.write(output_pdf_buffer)

            # Seek to the beginning of the buffer
                output_pdf_buffer.seek(0)

            #return send_file(output_pdf_buffer, as_attachment=True,mimetype="application/pdf",download_name="Corrections.pdf",conditional=False), render_template('main.html',msg=msg,flag=flag)
        
        return send_file(output_pdf_buffer, as_attachment=True,mimetype="application/pdf",download_name="Corrections.pdf",conditional=False)
   else:
       return redirect(url_for("hello_one"))
    

    
if __name__ == "__main__":
  app.run(debug=True)


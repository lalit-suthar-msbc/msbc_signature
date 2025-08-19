from datetime import datetime
from logging.handlers import RotatingFileHandler
from flask import Flask, request, send_file, redirect, url_for, render_template
from create_docs_signature import create_docs_file
import logging
app = Flask(__name__, template_folder='templates',static_folder='static')

handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.ERROR)
app.logger.addHandler(handler)




@app.route('/signature/<page_name>', methods=['GET', 'POST'])
def signature_link(page_name):
    if request.method == "POST":
        print("post method is hitted")
        first_name = request.form['First name']
        last_name = request.form['Last name']
        email = request.form['Email address']
        designation = request.form['Designation']
        number_type=request.form['number_type']
        if number_type=="uk":
            telephone="+44 (0) 870 850 0470"
        else:
            telephone="+91 (079) 470 16 666"
        
        need_extension =request.form.get('need_extension')=="true"
        if need_extension:
            extension = request.form['extension']
        else:
            extension=""
        create_docs_file(page_name,first_name, last_name, designation, email,telephone,extension)
        output_file = "{}_{}.docx".format(str(datetime.today().date()),page_name)
        return send_file(output_file,
                            download_name=output_file, as_attachment=True)

    return render_template(f"{page_name}.html")

@app.route('/', methods=['GET'])
def home_page():
    return render_template("MSBC Signature Portal.html")
# @app.route('/test', methods=['GET','POST'])
# def home():
#     if request.method == "POST":
#         print(request.files["file"])
#         print(request.files["file"].filename)
#     return render_template("form.html")

if __name__ == "__main__":
    app.run(port=5100,host="0.0.0.0",debug=True)

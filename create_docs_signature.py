from datetime import datetime
import zipfile
import os
import shutil
from lxml import etree
temp_dir = 'temp'

# output_file = r'C:\Users\lalit.suthar\Downloads\PB-MSBC-Signature-Modified_test.docx'



# Function to unzip the DOCX file
def unzip_docx(docx_file, temp_dir):
    with zipfile.ZipFile(docx_file, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)


# Function to zip the modified files back into a DOCX file
def zip_docx(temp_dir, modified_docx):
    with zipfile.ZipFile(modified_docx, 'w') as zipf:
        for root, dirs, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, temp_dir))


# Function to replace text in the XML
def replace_text(element, replacements, namespaces,new_email,msbc):
    for elem in element.xpath('.//w:t', namespaces=namespaces):
        if elem.text:
            for old_text, new_text in replacements.items():
                if old_text in elem.text:
                    print(new_text,"*****************")
                    elem.text = elem.text.replace(old_text, new_text)
    mail = 'mailto:{}{}'
    
    # if msbc:
    #     namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    #     elements = element.xpath('.//w:hyperlink', namespaces=namespaces)
    #     print(elements,"**&*&*&*&*&*&*&*&*")
    #     # Check if elements were found
    #     if elements:
    #         element = elements[0]  # Assume you want to modify the first found element
    #         # Note: Use the correct namespace URI for the 'tooltip' attribute
    #         element.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tooltip', mail.format(new_email,'@msbcgroup.com'))
    # else:
    #     content_xml_path = os.path.join(temp_dir, 'word/_rels', 'document.xml.rels')
    #     parser = etree.XMLParser(recover=True)
    #     tree = etree.parse(content_xml_path, parser)
    #     element = tree.getroot()
    #     # Define the namespace (if any)
    #     namespace = {'ns': 'http://schemas.openxmlformats.org/package/2006/relationships'}
    #     print(element.findall('ns:Relationship', namespaces=namespace),"********************")
    #     # Find the specific Relationship element by its Type
    #     for relationship in element.findall('ns:Relationship', namespaces=namespace):
    #        if relationship.get('Type') == 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink':
    #         target = relationship.get('Target')
    #         if target == 'mailto:firstletter.surname@qtech365.com':
    #             print(f"Updating Target from {target} to {new_email}")
    #             # Update the Target attribute
    #             relationship.set('Target', mail.format(new_email,"@qtech365.com"))
    #         if target == 'mailto:firstletter.surname@remoratech.io':
    #             print(f"Updating Target from {target} to {new_email}")
    #             # Update the Target attribute
    #             relationship.set('Target', mail.format(new_email,"@remoratech.io"))
    #     tree.write(content_xml_path, encoding='UTF-8', xml_declaration=True)



# Main function to demonstrate usage
def create_docs_file(sign_name,new_first_name, new_last_name, new_designation, email_new,new_telephone,new_extension):
   
    all_docx_path=os.path.join(os.path.dirname(__file__),"docx_sample")
    file_path=os.path.join(all_docx_path,f"Faizal Deraiya- 10-03-2025f.docx")
    print(file_path)
    first_name = "Faizal"
    last_name = "Deraiya"
    email = "faizal.deraiya@msbcgroup.com"
    hyperlink="faizal.deraiya@msbcgroup.com"
    designation = "UI - UX Designer"
    telephone_num='+91 (079) 470 16 666'
    extension='| EXT : 219'
    docx_file = file_path
    
    # Ensure temp directory exists and is empty
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    os.makedirs(temp_dir)

    # Unzip the DOCX file
    unzip_docx(docx_file, temp_dir)

    # Define replacements
    replacements = {
        first_name: new_first_name,
        last_name: new_last_name,
        designation: new_designation,
        telephone_num: new_telephone,
        extension: f'| EXT : {new_extension}' if new_extension else "",hyperlink:email,email: f"{email_new}"
    }

    output_file="{}_{}.docx".format(str(datetime.today().date()),sign_name)

    # Parse XML with namespaces
    content_xml_path = os.path.join(temp_dir, 'word', 'document.xml')
    parser = etree.XMLParser(recover=True)
    tree = etree.parse(content_xml_path, parser)
    root = tree.getroot()

    # Get namespaces
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    msbc=True if sign_name.__contains__("MSBC") else None
   
    # Replace text in the XML
    replace_text(root, replacements=replacements, namespaces=namespaces,new_email=email_new,msbc=msbc)

    # Print modified XML for debugging
    # print(etree.tostring(root, pretty_print=True, encoding='unicode'))

    # Write the modified XML back to file
    tree.write(content_xml_path, xml_declaration=True, encoding='UTF-8', method='xml')

    # Zip the modified files back into a new DOCX file
    modified_docx = output_file
    zip_docx(temp_dir, modified_docx)

    # Cleanup
    shutil.rmtree(temp_dir)
 
    print(f'Modified DOCX file saved to: {modified_docx}')
    return output_file


# if __name__=="__main__":
#     create_docs_file("MSBC","lalit", "suthar", "python developer", "msbv@gmailc.om","9878799","54545")
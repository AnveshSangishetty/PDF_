#Used Libraries Tika,PyMuPDF(fitz)
from tika import parser
import fitz
import os



file_path=r"path_to_file"
corrupted=None
images_count=0
hidden_layers=False
locked_layers=False


try:
    pdf = fitz.open(file_path)
    layers=pdf.layer_ui_configs()
    for i in layers:
        if i['locked']==True:
            locked_layers=True
        if i['on']==False:
            hidden_layers=True
    parsed_pdf = parser.from_file(file_path)
    data = parsed_pdf['metadata']
    corrupted=False
    content = parsed_pdf['content']
    if content==None:
        content_copying="Not allowed"
        print("No text available")
    else:
        content_copying="Allowed"
    print("is Encrypted:", data["pdf:encrypted"])
    print("Corrupted:", False)
    print("Contains hidden layers:",hidden_layers)
    print("Locked layers:",locked_layers)
    print("Created on:",data["Creation-Date"])
    print("Printing: Allowed") if data["access_permission:can_print"] == True else print("Printing: Not Allowed")
    print("Content copying:",content_copying)
    print("Filling of form fields: Allowed") if data["access_permission:fill_in_form"] == True else print("Filling in form fields: Not Allowed")
    print("Document assemble: Allowed") if data["access_permission:assemble_document"]==True else print("Document assemble: Not Allowed")
    print("Content copying for accessibility: Allowed") if data["access_permission:extract_for_accessibility"] == True else print("Content copying for accessibility: Not Allowed")
    print("Changing the document: Allowed") if data["access_permission:can_modify"]==True else print("Changing the document: Not Allowed")
except:
    corrupted=True
    print("Corrupted",True)

#To highlight non-text objects in PDF
for page in range(pdf.page_count):
    image_list = pdf.get_page_images(page,full=True)
    for inst in image_list:
        images_count+=1
        Pagee=pdf.load_page(page)
        bbox=Pagee.get_image_bbox(inst)
        x0,y0,x1,y1=bbox.x0,bbox.y0,bbox.x1,bbox.y1
        print("{}) Left: {:.2f}, Top: {:.2f}, Right: {:.2f}, Bottom: {:.2f}, Height: {:.2f}, Width: {:.2f}".format(images_count,x0,y0,x1,y1,bbox.height,bbox.width))

        #noting numbers of images:

        shape=Pagee.new_shape()
        rect = fitz.Rect(x0-20, y0, x0, y0+20)
        ht = Pagee.add_circle_annot(rect)
        ht.update(fill_color=[1, 0, 0])
        ht.set_blendmode(fitz.PDF_BM_Multiply)
        ht.set_opacity(0.5)
        ht.update()
        shape.insert_textbox(rect,str(images_count),align=1,)
        shape.finish()
        shape.commit()

        highlight = Pagee.add_rect_annot(bbox)

#saving the highlighted output
output_path=os.path.dirname(file_path)+"\\"+os.path.basename(file_path)[:-4]+"_highlighted_output.pdf"
pdf.save(output_path, garbage=4, deflate=True, clean=True)
print("Highlighted pdf saved at ",output_path)

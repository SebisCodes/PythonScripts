''' 
    This code is based on the code from niqiu (link below) and slightly edited by sebiscodes.

    A program to convert AutoCAD SHX PDF annotation text to searchable text
    Source: https://niqiu.livejournal.com/153083.html?utm_source=3userpost

    PIP Dependencies: PyPDF2, reportlab
    Version: Required 3.5

    Contact: sebiscodes@gmail.com / niqiu@livejournal.com 
    Creators Website: http://www.livejournal.com/~niqiu
    My Github: https://github.com/SebisCodes
'''

import io,os
import tkinter
import sys
from tkinter import messagebox
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape, A3, A2, A1
from datetime import date, time, datetime,timedelta


def convert_annot(pdf_name):
    #Open PDF
    pdfFile = open(pdf_name, "rb")
    pdf = PdfFileReader(pdfFile, strict=False)
    output = PdfFileWriter() 
    #Go through all pages
    for page_num in range(pdf.getNumPages()):
        page = pdf.getPage(page_num) 
        
        objs=[]
        if "/Annots" in page:
            for annot in page['/Annots'] :
                obj=annot.getObject()
                if 'AutoCAD SHX Text' in obj.values():
                    #Get annot objects
                    objs.append(obj)

            
        page_size=pdf.getPage(0).mediaBox.upperRight
        w, h =page_size
        packet = io.BytesIO()
        c = canvas.Canvas(packet,pagesize=page_size)
        c.setFillColor(colors.transparent)
        #c.setFillColor(colors.red)
        #Rewrite Text for each annot object
        for obj in objs:
            if '/Contents' in obj:
                xy=tuple(obj['/Rect']) 
                llx,lly,urx,ury=xy   #LowerLeftX,LowerLeftY,UpperRightX, UpperRightY
                text=obj['/Contents']
                x1=int(urx)
                y1=int(ury-(ury-lly)/2)
                if ury-lly > 1.5*(llx-urx):
                    c.setFont('Helvetica',(llx-urx)/2)
                    c.saveState()
                    c.translate(x1,y1)
                    c.rotate(90)
                    c.drawString(-(ury-lly)/2,-(llx-urx)/2,text)
                    c.restoreState()
                else:
                    c.setFont('Helvetica',(ury-lly)/2)
                    c.drawString(x1,y1,text)
                    c.saveState()
        c.save()
        

        #buffer start from 0
        packet.seek(0)
        new_pdf = PdfFileReader(packet)
        page=None
        new_pdf_file_name=None

        page = pdf.getPage(page_num)
        page.compress_content_streams(packet)
        #Put old PDF over new transparent text
        new_pdf.getPage(0).mergePage(page)

        #Add new page to output file
        output.addPage(new_pdf.getPage(0))
    output.removeLinks()

    # Finally output new pdf
    try:
        new_pdf_file_name=os.path.splitext(pdf_name)[0]+".annot.pdf"
        #new_pdf_file_name=pdf_name
        outputStream = open(new_pdf_file_name, "wb")
        output.write(outputStream)
        outputStream.close()
        pdfFile.close()
    except:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Error!", "Error: Saving failed!")
    
    try:
        os.remove(pdf_name)
    except:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Error!", "Error: Delete failed, file is open!")
    try:
        os.rename(new_pdf_file_name, pdf_name)
    except:
        root = tkinter.Tk()
        root.withdraw()
        messagebox.showinfo("Error!", "Error: Renaming failed, file is open!")

if __name__ == '__main__':
    if len(sys.argv) > 0:
        for i, arg in enumerate(sys.argv):
            if i == 1:
                pdf_name=arg
        
        if pdf_name != "":
            print("Starting...")
            convert_annot(pdf_name)
        else:
            print("Not enough arguments! Exit...")
            exit

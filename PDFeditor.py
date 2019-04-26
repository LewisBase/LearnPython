# -*- coding: utf-8 -*-
"""
Created on Fri Apr 19 13:00:22 2019

@author: lewisbase
* Extract document infromation from a PDF in Python
* Rotate pages
* Merge PDFs
* split PDFs
* Add watermarks
* Encrypt a PDF
"""

from PyPDF4 import PdfFileReader,PdfFileWriter

def extract_information(pdf_path):
    with open(pdf_path,'rb') as f:
        pdf=PdfFileReader(f)
        information=pdf.getDocumentInfo()
        number_of_pages=pdf.getNumPages()
        
    txt=f"""
    Information about {pdf_path}
    
    Author: {information.author}
    Creator: {information.creator}
    Producer: {information.producer}
    Subject: {information.subject}
    Title: {information.title}
    Number of pages: {number_of_pages}
    """
    print(txt)
    return information

def rotate_pages(pdf_path,pages=[0],direction='right'):
    """Parameters: filename, pages want to rotate and rotate direction"""
    pdf_writer=PdfFileWriter()
    pdf_reader=PdfFileReader(pdf_path)
    outputname=pdf_path[:-4]+'-rotate.pdf'
    for page in pages:
        # Rotate page 90 degrees to the right
        if direction=='right':
            page_r=pdf_reader.getPage(page).rotateClockwise(90)
            pdf_writer.addPage(page_r)
        # Rotate page 90 degrees to the left
        elif direction=='left':
            page_r=pdf_reader.getPage(page).rotateCounterClockwise(90)
            pdf_writer.addPage(page_r)
        else:
            print("Encountered an improper argument! Input right or left.")
    
    with open(outputname,'wb') as fh:
        pdf_writer.write(fh)
    
def merge_pdfs(paths,output):
    pdf_writer=PdfFileWriter()
    for path in paths:
        pdf_reader=PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
            
    with open(output,'wb') as out:
        pdf_writer.write(out)
        
def split(pdf_path,name_of_split):
    pdf_reader=PdfFileReader(pdf_path)
    for page in range(pdf_reader.getNumPages()):
        pdf_reader=PdfFileReader(pdf_path)
        pdf_writer=PdfFileWriter()
        pdf_writer.addPage(pdf_reader.getPage(page))
        output=f'{name_of_split}{page}.pdf'
        with open(output,'wb') as output_pdf:
            pdf_writer.write(output_pdf)

def main():
    pass

if __name__ == '__main__':
    main()
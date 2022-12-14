from glob import glob
from PyPDF2 import PdfFileMerger

def pdf_merge():
    ''' Merges all the pdf files in current directory '''
    merger = PdfFileMerger()
    allpdfs = [a for a in glob("./PDFs/*.pdf")]
    [merger.append(pdf) for pdf in allpdfs]
    with open("./Result/merged.pdf", "wb") as new_file:
        merger.write(new_file)

if __name__ == "__main__":
    pdf_merge()

exit()
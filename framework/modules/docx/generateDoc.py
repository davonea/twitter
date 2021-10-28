from docx import Document
import time
from framework.modules.bases.singleton import singleton


@singleton
class Docx(object):
    def __init__(self):
        self._document = Document()
        self.p = None

    def addTitle(self, title):
        self._document.add_heading(title, 0)

    def addCountinfo(self, countinfo):
        self._document.add_paragraph(countinfo)

    def addnewsTitle(self, newsTitle, description):
        self._document.add_heading(newsTitle, level=1)
        self._document.add_paragraph(description, style='Intense Quote')

    def addbaseinfo(self, info):
        self._document.add_paragraph(
            info, style='List Bullet'
        )

    def saveDocx(self, name=None):
        if name is None:
            name = time.time()
        self._document.save("{}.docx".format(name))


def main():
    document = Document()

    document.add_heading('Document Title', 0)

    p = document.add_paragraph('A plain paragraph having some ')
    p.add_run('bold').bold = True
    p.add_run(' and some ')
    p.add_run('italic.').italic = True

    document.add_heading('Heading, level 1', level=1)
    document.add_paragraph('Intense quote', style='Intense Quote')

    document.add_paragraph(
        'first item in unordered list', style='List Bullet'
    )
    document.add_paragraph(
        'first item in ordered list', style='List Number'
    )

    # document.add_picture('monty-truth.png', width=Inches(1.25))

    records = (
        (3, '101', 'Spam'),
        (7, '422', 'Eggs'),
        (4, '631', 'Spam, spam, eggs, and spam')
    )

    table = document.add_table(rows=1, cols=3)
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Qty'
    hdr_cells[1].text = 'Id'
    hdr_cells[2].text = 'Desc'
    for qty, id, desc in records:
        row_cells = table.add_row().cells
        row_cells[0].text = str(qty)
        row_cells[1].text = id
        row_cells[2].text = desc

    document.add_page_break()

    document.save('demo.docx')


if __name__ == '__main__':
    main()

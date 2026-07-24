import fitz


def extract_text(pdf_path):

    document = fitz.open(pdf_path)


    pages=[]


    for index,page in enumerate(document):

        pages.append({

            "page":
            index+1,


            "text":
            page.get_text()

        })


    return pages
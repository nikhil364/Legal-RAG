from database import SessionLocal
from models import Document



def get_document(filepath):

    db = SessionLocal()

    doc = (
        db.query(Document)
        .filter(
            Document.filepath==filepath
        )
        .first()
    )

    db.close()

    return doc



def register_document(metadata, file_hash):

    db = SessionLocal()


    doc = Document(

        filepath=metadata["filepath"],

        filename=metadata["filename"],

        sha256=file_hash,

        folder_path="/".join(
            metadata["folder_path"]
        ),

        indexed=False

    )


    db.add(doc)

    db.commit()

    db.close()
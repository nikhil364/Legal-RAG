from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler



from extractor import extract_text
from chunker import chunk_text
from metadata import extract_metadata
from rabbitmq_client import send_chunk

from hash import calculate_hash
from registry import get_document, register_document


class PDFHandler(
    FileSystemEventHandler
):


    def process(self,path):

        if not path.endswith(".pdf"):
            return


        file_hash = calculate_hash(path)


        metadata = extract_metadata(path)


        existing = get_document(
            metadata["filepath"]
        )


        if existing:

            if existing.sha256 == file_hash:

                print(
                "No change detected"
                )

                return


            print(
            "Document modified"
            )


        else:

            print(
            "New document"
            )


            register_document(
                metadata,
                file_hash
            )



        pages = extract_text(path)


        chunks = chunk_text(
            pages
        )


        for chunk in chunks:

            payload={

                **metadata,

                **chunk,

                "hash":file_hash

            }


            send_chunk(payload)



    def on_created(self,event):

        self.process(
            event.src_path
        )


    def on_modified(self,event):

        self.process(
            event.src_path
        )



def start():

    observer=Observer()


    observer.schedule(

        PDFHandler(),

        "/app/docs",

        recursive=True

    )


    observer.start()


    print(
    "Watching docs directory..."
    )


    observer.join()
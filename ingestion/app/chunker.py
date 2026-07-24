def chunk_text(
        pages,
        size=1000,
        overlap=200
):

    chunks=[]


    for page in pages:

        text=page["text"]


        start=0


        while start < len(text):

            end=start+size


            chunks.append({

                "page":
                page["page"],


                "text":
                text[start:end]

            })


            start=end-overlap


    return chunks
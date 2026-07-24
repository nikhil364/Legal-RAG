def build_prompt(question, chunks):


    context = ""


    for i, chunk in enumerate(chunks):

        context += f"""

SOURCE {i+1}

File:
{chunk['payload'].get('filename')}

Page:
{chunk['payload'].get('page')}


Content:

{chunk['payload'].get('text')}

"""



    prompt=f"""

You are a legal document assistant.

Answer only using the provided context.

If the answer is not available,
say:
"I could not find this information."


Context:

{context}


Question:

{question}


Answer:

"""


    return prompt
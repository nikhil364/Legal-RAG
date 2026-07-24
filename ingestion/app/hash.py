import hashlib



def calculate_hash(path):

    sha = hashlib.sha256()


    with open(path,"rb") as f:

        while chunk := f.read(1024*1024):

            sha.update(chunk)


    return sha.hexdigest()
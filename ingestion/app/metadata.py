from pathlib import Path


def extract_metadata(file_path):

    root = Path("/app/docs")

    path = Path(file_path)


    relative = path.relative_to(root)


    folders = list(relative.parts[:-1])


    return {

        "filename":
            path.name,


        "filepath":
            str(relative),


        "folder_path":
            folders,


        "depth":
            len(folders),


        "root_category":
            folders[0]
            if len(folders)
            else None,


        "parent_category":
            folders[-1]
            if len(folders)
            else None,


        "file_type":
            path.suffix.replace(".","")

    }
import os
import sys
import json
import zipfile


def get_json_file(file_name):
    try:
        return json.loads(open(file_name).read())
    except FileNotFoundError:
        print("File \"" + file_name + "\" does not exist")
        sys.exit(1)


def set_json_file(file_name, json_arr, indents=True):
    if indents:
        indents = 2
    else:
        indents = None

    return open(file_name, 'w').write(json.dumps(json_arr, indent=indents))


def print_line(w):
    sys.stdout.write(w)
    sys.stdout.flush()


def zip_directory(directory, zip_location, verbose=False, very_verbose=False):
    if not os.path.exists(os.path.dirname(zip_location)):
        os.makedirs(os.path.dirname(zip_location))
    zip_file = zipfile.ZipFile(zip_location, "w", zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(directory):
        if verbose:
            print(root)

        for file in files:
            if very_verbose:
                print(file)

            zip_file.write(os.path.join(root, file))
    zip_file.close()


class colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'

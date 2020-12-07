import argparse
import json
import shutil

from bokeh.core.property.bases import DeserializationError
from bokeh.document import Document
from bokeh.plotting import Figure

def replace_colour(json_string, colour):
    doc = json.loads(json_string.replace('\\"', '"'))
    tlk = list(doc.keys())[0]
    bdoc = Document.from_json(doc[tlk])
    for model in bdoc.select({"type": Figure}):
        model.background_fill_color = colour
        model.border_fill_color = colour
    doc[tlk] = bdoc.to_json()
    final = json.dumps(doc).replace('"', '\\"')
    #print(json_string)
    #print(final)
    return final


def main():
    parser = argparse.ArgumentParser(description="Change background colour of all bokeh Figures in a notebook.")
    parser.add_argument("colour", help='hexstring for background colour.')
    parser.add_argument("notebooks", nargs='+', help='notebook files.')
    parser.add_argument("--backup", default='.bck', help='backup file extension.')
    args = parser.parse_args()

    CHECK = "var docs_json = "
    ENDSWITH=';\\n",'

    colour = '#' + args.colour.replace('#', '').upper()
    for notebook in args.notebooks:
        shutil.move(notebook, notebook + args.backup)
        with open(notebook + args.backup, 'r') as filein, open(notebook, 'w') as fileout:
            for line in filein:
                line = line.strip()
                if CHECK in line:
                    start, data = line.split(CHECK, 1)
                    if not data.endswith(ENDSWITH):
                        raise IOError("Could not parse data line, <<{}>>".format(data[-5:]))
                    data = data.strip(ENDSWITH)
                    try:
                        new_doc = replace_colour(data, colour)
                    except DeserializationError:
                        new_doc = data
                    new_line = start + CHECK + new_doc + ENDSWITH
                    fileout.write(new_line + "\n")
                else:
                    fileout.write(line + "\n")




if __name__ == "__main__":
    main()

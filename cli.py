import sys
from typing import Tuple
from os.path import join
from os.path import isdir
from os.path import isfile
from ntpath import basename
from shutil import move
from pybtex.database import parse_string
from pybtex.database import parse_file
from pybtex.database import BibliographyData
from pybtex.database import Entry

BIBTEX_DIR='tmp/library.bib'
PDF_DIR='/home/ffff/Programs/mendeley-replacer/tmp/pdf-dir/'
PDF_FILE='tmp/my-pdf.pdf'

# Check that BIBTEX_DIR exists and is readable
biblib = parse_file(BIBTEX_DIR)

# check that PDF_DIR exists and is a directory
assert(isdir(PDF_DIR))

# check that PDF_FILE exists and is a file
assert(isfile(PDF_FILE))

PDF_FILE = sys.argv[1]

print(f'Adding {PDF_FILE} to library.')

def add_file_to_entry (bibtex_entry: str) -> Tuple[str, BibliographyData]:
    '''
    Returns a citation key + a bibtex entry (dict) with the PDF associated.
    '''
    def mendeleyify (pth):
        full_path = join(PDF_DIR, pth)
        # make sure path starts with a  : instead of a /
        return ':' + full_path[1:] + ":pdf"

    def citation_key (parsed_entry):
        return list(parsed_entry.entries)[0]

    parsed: BibliographyData = parse_string(bibtex_entry, 'bibtex')
    ckey = citation_key(parsed)
    entry: Entry = parsed.entries[ckey]
    entry.fields['file'] = mendeleyify(PDF_FILE)
    parsed.entries[ckey] = entry
    return ckey, parsed


print("Paste the bibtext entry for this PDF. Ctrl-D or Ctrl-Z ( windows ) to save it.")
my_bibtex_entry = '\n'.join(sys.stdin.readlines())

citekey, entry = add_file_to_entry(my_bibtex_entry)

# check for citation key collisions.
libkeys = list(biblib.entries)
if citekey in libkeys:
    raise Exception(f'Cite key {citekey} already in bibtex db! Choose a unique citekey. Not adding entry or moving PDF.')

# if no collision, move PDF to directory
dest = join(PDF_DIR, basename(PDF_FILE))
move(PDF_FILE, dest)
print(f'Copied {PDF_FILE} to {PDF_DIR}')

# if ok, append to bibfile
with open (BIBTEX_DIR, 'a') as f:
    appendage = entry.to_string('bibtex')
    f.write(appendage)
    f.write('\n')

print(f'Added {citekey} to {BIBTEX_DIR}')

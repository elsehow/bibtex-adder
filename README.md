# bibtex-adder

Add bibtex entries to a bib database.

# install

Requires pybtex:

- `pip install pybtex`

# example

```
rm -rf tmp/
cp -r test-static/ tmp/
python cli.py tmp/my-pdf.pdf
```

Copy and paste some valid bibtex in. (See `tmp/example-bibtex.bib` for an example).

The PDF will be moved to tmp/pdf-dir, and the entry will be added to tmp/library.bib.

Configure the script to reflect your preferred paths.

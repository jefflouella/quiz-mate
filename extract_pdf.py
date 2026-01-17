#!/usr/bin/env python3
import sys
import os

# Try different PDF libraries
try:
    import pypdf
    def extract_with_pypdf(filename):
        with open(filename, 'rb') as pdf_file:
            reader = pypdf.PdfReader(pdf_file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
            return text
    print(extract_with_pypdf(sys.argv[1]))
except ImportError:
    try:
        import PyPDF2
        def extract_with_pypdf2(filename):
            with open(filename, 'rb') as pdf_file:
                reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text()
                return text
        print(extract_with_pypdf2(sys.argv[1]))
    except ImportError:
        try:
            import pdfplumber
            def extract_with_pdfplumber(filename):
                with pdfplumber.open(filename) as pdf:
                    text = ''
                    for page in pdf.pages:
                        text += page.extract_text()
                    return text
            print(extract_with_pdfplumber(sys.argv[1]))
        except ImportError:
            print("ERROR: No PDF library available. Please install one: pip install pypdf", file=sys.stderr)
            sys.exit(1)

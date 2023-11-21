#!/bin/bash
pdflatex monografia.tex
bibtex monografia
pdflatex monografia.tex
pdflatex monografia.tex

rm *.aux
rm *.bbl
rm *.blg
rm *.brf
rm *.idx
rm *.lof
rm *.log
rm *.toc
# Compilacion condicional del plan de proyecto.
#
#   make v1 .. v4   genera GdP_Vera_Lautaro_VN.pdf con las secciones de esa entrega
#   make all        genera las cuatro
#   make            compila charter.pdf con la revision por defecto de charter.tex
#   make clean      borra los auxiliares y los PDF de entrega

NOMBRE  := GdP_Vera_Lautaro
LATEXMK := latexmk -pdf -synctex=1 -interaction=nonstopmode -file-line-error
REV      = $(patsubst v%,%,$@)

.PHONY: all default v1 v2 v3 v4 clean

default:
	$(LATEXMK) charter.tex

all: v1 v2 v3 v4

v1 v2 v3 v4:
	$(LATEXMK) -jobname=$(NOMBRE)_V$(REV) \
	  -pdflatex='pdflatex %O "\def\revision{$(REV)}\input{%S}"' charter.tex

clean:
	latexmk -c charter.tex
	rm -f $(NOMBRE)_V*.aux $(NOMBRE)_V*.log $(NOMBRE)_V*.out $(NOMBRE)_V*.toc \
	      $(NOMBRE)_V*.fls $(NOMBRE)_V*.fdb_latexmk $(NOMBRE)_V*.synctex.gz

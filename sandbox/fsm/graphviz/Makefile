TARGET=vni

SRC=$(TARGET).gv
PNG=$(TARGET).png
SVG=$(TARGET).svg

all: $(PNG) $(SVG)

$(PNG): $(SRC)
	dot -Tpng $(SRC) -o $(PNG)

$(SVG): $(SRC)
	dot -Tsvg $(SRC) -o $(SVG)

feh: $(PNG)
	feh $(PNG)

inkview: $(SVG)
	inkview $(SVG)

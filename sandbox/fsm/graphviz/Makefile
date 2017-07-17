SRC=fw_dplex.gv
PNG=fw_dplex.png
SVG=fw_dplex.svg

all: $(PNG) $(SVG)

$(PNG): $(SRC)
	dot -Tpng $(SRC) -o $(PNG)

$(SVG): $(SRC)
	dot -Tsvg $(SRC) -o $(SVG)

feh: $(PNG)
	feh $(PNG)

inkview: $(SVG)
	inkview $(SVG)

IN_XML := $(wildcard configs/*.xml)
OUT_MD = $(IN_XML:%.xml=%.md)
OUT_YAML = $(IN_XML:%.xml=%.yaml)
OUT_BBCODE = $(IN_XML:%.xml=%.bbcode)

all: md yaml bbcode
clean:
	rm -f $(OUT_MD) $(OUT_YAML) $(OUT_BBCODE)

md: $(OUT_MD)
yaml: $(OUT_YAML)
bbcode: $(OUT_BBCODE)

%.md: %.xml
	coverage run ../format.py -i $< -f md -o $@
	coverage report -m

%.yaml: %.xml
	coverage run ../format.py -i $< -f yaml -o $@
	coverage report -m

%.bbcode: %.xml
	coverage run ../format.py -i $< -f bbcode -o $@
	coverage report -m

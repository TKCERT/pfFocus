IN_XML := $(wildcard configs/*.xml)
OUT_MD = $(IN_XML:%.xml=%.md)
OUT_YAML = $(IN_XML:%.xml=%.yaml)

all: md yaml
clean:
	rm -f $(OUT_MD) $(OUT_YAML)

md: $(OUT_MD)
yaml: $(OUT_YAML)

%.md: %.xml
	coverage run ../format.py -i $< -f md -o $@
	coverage report -m

%.yaml: %.xml
	coverage run ../format.py -i $< -f yaml -o $@
	coverage report -m

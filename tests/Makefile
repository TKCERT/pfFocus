IN_XML := $(wildcard configs/*.xml)
OUT_MD = $(IN_XML:%.xml=%.md)
OUT_YAML = $(IN_XML:%.xml=%.yaml)

all: md yaml report
clean:
	rm -f $(OUT_MD) $(OUT_YAML)

md: $(OUT_MD)
yaml: $(OUT_YAML)

%.md: %.xml
	coverage run ../format.py -i $< -f md -o $@

%.yaml: %.xml
	coverage run ../format.py -i $< -f yaml -o $@

report:
	coverage report -m

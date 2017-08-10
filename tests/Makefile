IN_XML := $(wildcard configs/*.xml)
OUT_MD = $(IN_XML:%.xml=%.md)
OUT_YAML = $(IN_XML:%.xml=%.yaml)

all: md yaml
clean:
	rm $(OUT_MD) $(OUT_YAML)

md: $(OUT_MD)
yaml: $(OUT_YAML)

%.md: %.xml
	../format.py -i $< -f md -o $@

%.yaml: %.xml
	../format.py -i $< -f yaml -o $@

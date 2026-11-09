PICODECK_ROOT ?= $(HOME)/Projects/PicoDeck/picodeck
export PICODECK_ROOT
VERSION := $(shell python3 -c 'import json; print(json.load(open("app.json"))["version"])')

.PHONY: e2e zip clean

# Simulator tests: needs PicoDeck's simulator (make simulator in $(PICODECK_ROOT)).
e2e:
	SDL_VIDEODRIVER=dummy python3 -m pytest tests/e2e -v

# The release zip, as CI builds it, from files.txt.
zip:
	mkdir -p build
	rm -f build/picodeck-editor-*.zip
	zip -9 build/picodeck-editor-v$(VERSION).zip $$(cat files.txt)

clean:
	rm -rf build

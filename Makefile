.PHONY: serve build default buildimage

default: buildimage serve

buildimage:
	docker build -t raphiz/raphaelli docker/

build:
	docker run --rm --name raphaelli -v $(shell pwd):/src/ -p 4000:4000 raphiz/raphaelli build

serve:
	docker run --rm --name raphaelli -v $(shell pwd):/src/ -p 4000:4000 raphiz/raphaelli serve

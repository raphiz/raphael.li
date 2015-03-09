.PHONY: serve build default build-image

default: buildimage serve

buildimage:
	docker build -t raphiz/jekyll docker/

build:
	docker run --rm --name jekyll -v $(shell pwd):/src/ -p 4000:4000 raphiz/jekyll build

serve:
	docker run --rm --name jekyll -v $(shell pwd):/src/ -p 4000:4000 raphiz/jekyll serve

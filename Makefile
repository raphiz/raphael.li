.PHONY: serve build default build-image

default: buildimage serve

buildimage:
	docker build -t raphiz/raphael.li docker/

build:
	docker run --rm --name raphael.li -u jekyll -v $(shell pwd):/src/ -e "JEKYLL_ENV=production" raphiz/raphael.li jekyll build

serve:
	docker run --rm --name raphael.li -u jekyll -v $(shell pwd):/src/ -p 4000:4000 raphiz/raphael.li jekyll serve

deploy:
	docker run -i -t --rm --name raphael.li -v $(shell pwd):/src/  -e "HOST=$(HOST)" -e "USER=$(USER)" -e "PASSWORD=$(PASSWORD)" -e "DIRECTORY=$(DIRECTORY)" raphiz/raphael.li /src/deploy.sh

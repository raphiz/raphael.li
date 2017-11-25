.PHONY: serve build default build-image

default: buildimage serve

buildimage:
	docker build -t raphiz/raphael.li docker/

build:
	docker run --rm --name raphael.li -u jekyll -v $(shell pwd):/src/:z raphiz/raphael.li jekyll build

serve:
	docker run --rm --name raphael.li -u jekyll -v $(shell pwd):/src/:z -p 4000:4000 raphiz/raphael.li jekyll server

deploy:
	docker run -i -t --rm --name raphael.li -v $(shell pwd):/src/  -e "FTP_HOST=$(FTP_HOST)" -e "FTP_USER=$(FTP_USER)" -e "FTP_PASSWORD=$(FTP_PASSWORD)" -e "FTP_DIRECTORY=$(FTP_DIRECTORY)" raphiz/raphael.li /src/deploy.py

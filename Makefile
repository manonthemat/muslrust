SHELL := /bin/bash

.PHONY: build run test push

build:
	docker build -t manonthemat/muslrust .
run:
	docker run -v $$PWD/test:/volume  -w /volume -it manonthemat/muslrust /bin/bash

test-plain:
	./test.sh plain
test-curl:
	./test.sh curl
test-ssl:
	./test.sh ssl
test-zlib:
	./test.sh zlib
test-hyper:
	./test.sh hyper

clean-docker:
	docker images manonthemat/muslrust -q | xargs -r docker rmi -f
clean-lock:
	sudo find . -iname Cargo.lock -exec rm {} \;
clean-builds:
	sudo find . -mindepth 3 -maxdepth 3 -name target -exec rm -rf {} \;
clean: clean-docker clean-lock clean-builds

test: test-plain test-ssl test-curl test-zlib test-hyper
.PHONY: test-plain test-curl test-ssl test-zlib test-hyper


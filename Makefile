WSGI_REPO := spdata/chatgpt-wsgi-server
WSGI_VERSION := v240812

WEB_REPO := spdata/chatgpt-web-server
WEB_VERSION := v240812

build: build-wsgi build-web

build-wsgi:
	docker build \
	-t $(WSGI_REPO):$(WSGI_VERSION) \
	-f Dockerfile.wsgi-server .

build-web:
	docker build \
	-t $(WEB_REPO):$(WEB_VERSION) \
	-f Dockerfile.web-server .


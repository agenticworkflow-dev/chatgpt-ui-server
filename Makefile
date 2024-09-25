WSGI_REPO := agenticworkflow/chatgpt-wsgi-server
WSGI_VERSION := v240924

WEB_REPO := agenticworkflow/chatgpt-web-server
WEB_VERSION := v240924

build: build-wsgi build-web

build-wsgi:
	docker build \
	-t $(WSGI_REPO):$(WSGI_VERSION) \
	-f Dockerfile.wsgi-server .

build-web:
	docker build \
	-t $(WEB_REPO):$(WEB_VERSION) \
	-f Dockerfile.web-server .


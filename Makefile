build:
	docker-compose build

# Prepare for zipping
clean: stop
	rm -r ./python/__pycache__/ ./python/venv/
	rm -r ./test/__pycache__/ ./test/venv/

# Run the app and all its dependencies
run: build
	docker-compose up cap-app

# Runs a bash shell in a container. Good for messing with python packages.
# Ex:
# APP=cap-test make shell
shell:
	docker-compose run $(APP) /bin/bash

# Stop all running apps
stop:
	docker-compose down

int-test:
	docker-compose up cap-test

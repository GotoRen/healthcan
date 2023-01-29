PYTHON=python3
TEST=$(PYTHON) -m unittest

all: test/project test/healthcan test/user

test/project: ## unittest model/project.py
	$(TEST) tests.test_project.test_project

test/healthcan: ## unittest model/healthcan.py
	$(TEST) tests.test_healthcan.test_healthcan

test/user: ## unittest model/user.py
	$(TEST) tests.test_user.test_user

help: ## display this help screen
	@grep -E '^[a-zA-Z/_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

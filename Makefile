.PHONY: all
all: test build

define with-context
cd $$(git rev-parse --show-toplevel) && $(1)
endef

define poetry-run
$(call with-context,poetry run $(1))
endef

.PHONY: install
install:
	$(call with-context,poetry install)

.PHONY: test
test:
	$(call poetry-run,pytest)

.PHONY: build
build:
	$(call poetry-run,build)

.PHONY: shell
shell:
	$(call with-context,poetry shell)

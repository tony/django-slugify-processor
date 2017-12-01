WATCH_FILES= find . -type f -not -path '*/\.*' | grep -i '.*[.]py$$' 2> /dev/null


entr_warn:
	@echo "----------------------------------------------------------"
	@echo "     ! File watching functionality non-operational !      "
	@echo "                                                          "
	@echo "Install entr(1) to automatically run tasks on file change."
	@echo "See http://entrproject.org/                               "
	@echo "----------------------------------------------------------"

build_docs:
	cd doc && $(MAKE) html

watch_docs:
	cd doc && $(MAKE) watch_docs

flake8:
	flake8 django_slugify_processors tests

watch_flake8:
	if command -v entr > /dev/null; then ${WATCH_FILES} | entr -c $(MAKE) flake8; else $(MAKE) flake8 entr_warn; fi

test:
	py.test --reuse-db --nomigrations $(test)

watch_test:
	if command -v entr > /dev/null; then ${WATCH_FILES} | entr -c $(MAKE) test; else $(MAKE) test entr_warn; fi

yapf:
	yapf --exclude='*settings*' --parallel --in-place -r .

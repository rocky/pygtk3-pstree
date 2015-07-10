# Compatibility for us old-timers.
# Note: This makefile include remake-style target comments.
# These comments before the targets start with #:
# remake --tasks to shows the targets and the comments

GIT2CL ?= git2cl
PYTHON ?= python
PYTHON3 ?= python3
RM      ?= rm
LINT    = flake8

PHONY=check clean dist distclean clean_pyc nosetests

#: Default target - same as "check"
all: check

# FIXME: get these done
#: Same as "check"
# test: check

#: Same as "check"
#nosetests: check

#: Clean up temporary files and .pyc files
clean: clean_pyc
	$(PYTHON) ./setup.py $@

#: Create source (tarball) and binary (egg) distribution
dist:
	$(PYTHON) ./setup.py sdist bdist_egg

#: Remove .pyc files
clean_pyc:
	$(RM) -f */*.pyc *.pyc

#: Create source tarball
sdist:
	$(PYTHON) ./setup.py sdist


#: Style check. Set env var LINT to pyflakes, flake, or flake8
lint:
	$(LINT) gtkPstree

#: Create binary egg distribution
bdist_egg:
	$(PYTHON) ./setup.py bdist_egg


# It is too much work to figure out how to add a new command to distutils
# to do the following. I'm sure distutils will someday get there.
DISTCLEAN_FILES = build dist *.pyc

#: Remove ALL derived files
distclean: clean
	-rm -fr $(DISTCLEAN_FILES) || true
	-find . -name \*.pyc -exec rm -v {} \;
	-find . -name \*.egg-info -exec rm -vr {} \;

#: Install package locally
verbose-install:
	$(PYTHON) ./setup.py install

#: Install package locally without the verbiage
install:
	$(PYTHON) ./setup.py install >/dev/null

.PHONY: $(PHONY)

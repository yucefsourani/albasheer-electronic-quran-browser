DESTDIR?=/
PREFIX?=$(DESTDIR)/usr
datadir?=$(PREFIX)/share
INSTALL=install
PYTHON=/usr/bin/python3
SOURCES=$(wildcard *.desktop.in)
TARGETS=${SOURCES:.in=}
#TEST_DEPS=0

all: $(TARGETS) icons

icons:
	install -d icons; 
	for i in 96 72 64 48 36 32 24 22 16; do \
		convert albasheer-128.png -resize $${i}x$${i} icons/albasheer$${i}.png; \
	done

albasheer-data/ix.db: albasheer-data/quran.db
	rm albasheer-data/ix.db || :
	$(PYTHON) gen-index.py

pos:
	make -C po all

install: all
	#[ $(TEST_DEPS) == "1" ] && $(PYTHON) -c 'import gi; gi.require_version("Gtk", "3.0")'
	rm albasheer-data/quran-kareem.png || :
	$(PYTHON) setup.py install --prefix=$(PREFIX)
	$(INSTALL) -d $(datadir)/applications/
	$(INSTALL) -m 0644 albasheer.desktop $(datadir)/applications/
	for i in 96 72 64 48 36 32 24 22 16; do \
		install -d $(datadir)/icons/hicolor/$${i}x$${i}/apps; \
		$(INSTALL) -m 0644 -D icons/albasheer-$${i}.png $(datadir)/icons/hicolor/$${i}x$${i}/apps/albasheer.png; \
	done
	install -d $(datadir)/pixmaps
	$(INSTALL) -m 0644 -D albasheer-128.png $(datadir)/pixmaps/albasheer.png
	
%.desktop: %.desktop.in pos
	echo "updating .desktop"
	intltool-merge -d po $< $@

clean:
	rm -f albasheer-data/ix.db


POTFILE=$(shell cat POTFILES.in)
SOURCES=$(addprefix ../, $(POTFILE))
POFILES=$(wildcard *.po)
MOFILES=$(patsubst %.po,%.mo,$(POFILES))
all: $(MOFILES)

albasheer.pot: $(SOURCES)
	intltool-update -g albasheer -p

%.mo: %.po
	msgfmt $*.po -o $*.mo
	mkdir -p ../locale/$*/LC_MESSAGES/ || :
	cp $*.mo ../locale/$*/LC_MESSAGES/albasheer.mo
	touch ../*.desktop.in

%.po: albasheer.pot
	intltool-update -g albasheer -d $*


#! /usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import print_function

import sys, os, os.path, time
from albasheer.core import albasheerCore, searchIndexer

for d in os.listdir("albasheer-data"):
    d = os.path.join("albasheer-data",d)
    if os.path.isdir(d):
        l_ = os.path.join(d,"quran.db")
        if os.path.isfile(l_):
            q = albasheerCore(False,qurandb=l_)
            ix = searchIndexer(True,ix=os.path.join(d,"ix.db"))
            wc = 0
            for n,(o,i) in enumerate(q.getAyatIter(1, 6236)):
                for w in i.split():
                    ix.addWord(w,n+1)
                    wc += 1
            d = os.path.dirname(sys.argv[0])
            ix.save()
            print("got %d words, %d terms (max term length=%d character, term vectors size=%d bytes)." % (wc, ix.terms_count, ix.maxWordLen, ix.term_vectors_size))



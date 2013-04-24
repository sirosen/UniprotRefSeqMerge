#1/usr/bin/env python

from __future__ import print_function, division
import csv, os

files = [fname for fname in os.listdir('.')
                if fname.endswith('.csv')]

prots_to_fs = {}
#map val to (val,[vals],[vals])
uniprot_to_refandprotsandfs = {}
refseq_to_uniandprotsandfs = {}

all_cols = set()

prot_key = 'Protein'
uniprot_key = 'Uniprot'
refseq_key = 'RefSeq'
map_file = 'mapping.csv'

for fname in files:
    with open(fname) as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='"')
        for row in reader:
            all_cols.update(set(row.keys()))
            ref, uni, prot = None, None, None
            if prot_key in row:
                prot = row[prot_key]
                if prot not in prots_to_fs:
                    prots_to_fs[prot] = set()
                prots_to_fs[prot].add(fname)
            if uniprot_key in row:
                uni = row[uniprot_key]
            if refseq_key in row:
                ref = row[refseq_key]

            if (uni and not ref) and uni in uniprot_to_refandprotsandfs:
                ref = uniprot_to_refandprots[uni][0]
            if (ref and not uni) and ref in refseq_to_uniandprotsandfs:
                uni = refseq_to_uniandprotsandfs[ref][0]

            if ref and ref not in refseq_to_uniandprotsandfs:
                refseq_to_uniandprotsandfs[ref] = (None,set(),set())
            if uni and uni not in uniprot_to_refandprotsandfs:
                uniprot_to_refandprotsandfs[uni] = (None,set(),set())

            if ref:
                if fname != map_file:
                    refseq_to_uniandprotsandfs[ref][2].add(fname)
                if prot:
                    refseq_to_uniandprotsandfs[ref][1].add(prot)
            if uni:
                if fname != map_file:
                    uniprot_to_refandprotsandfs[uni][2].add(fname)
                if prot:
                    uniprot_to_refandprotsandfs[uni][1].add(prot)

            if ref and uni:
                refseq_to_uniandprotsandfs[ref] = (uni,refseq_to_uniandprotsandfs[ref][1],refseq_to_uniandprotsandfs[ref][2])
                uniprot_to_refandprotsandfs[uni] = (ref,uniprot_to_refandprotsandfs[uni][1],uniprot_to_refandprotsandfs[uni][2])


rowkeys = []
for uni in uniprot_to_refandprotsandfs:
    (ref,ps,fs) = uniprot_to_refandprotsandfs[uni]
    rowkeys.append((uni,ref,ps,fs))
    if len(ps) == 0:
        for p in ps:
            prots_to_fs.pop(p,None)
for ref in refseq_to_uniandprotsandfs:
    (uni,ps,fs) = refseq_to_uniandprotsandfs[ref]
    rowkeys.append((uni,ref,ps,fs))
    if len(ps) == 0:
        for p in ps:
            prots_to_fs.pop(p,None)
for p in prots_to_fs:
    rowkeys.append((None,None,[p],list(prots_to_fs[p])))


def printkey((uni,ref,ps,fs)):
    print(('| %15s | %15s | ' % (uni,ref)) + ', '.join(fs) + ' | ' + ', '.join(ps))

print('| %15s | %15s | File Names | Protein Names' % ('Uniprot','RefSeq'))
for k in rowkeys:
    printkey(k)

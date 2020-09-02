```

$ pubchemmer
Usage: pubchemmer [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dbimport
  dbquery                       session.bind.execute("select column_name,...
  dumpconfig
  find
  generate-sqlalchemy-model
  update-sdf-tags-from-pubchem

$ pubchemmer dbimport ~/pubchem/new/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/* --simulate |& head -n 5
ic| pubchemmer.py:186 in dbimport()- BASE: <class 'sqlalchemy.ext.declarative.api.Base'>
ic| pubchemmer.py:202 in dbimport()- index: 0, path: PosixPath('/home/user/pubchem/new/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_000000001_000500000.sdf.gz')
ic| pubchemmer.py:202 in dbimport()- index: 1, path: PosixPath('/home/user/pubchem/new/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_000000001_000500000.sdf.gz.md5')
ic| pubchemmer.py:202 in dbimport()- index: 2, path: PosixPath('/home/user/pubchem/new/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_000500001_001000000.sdf.gz')
ic| pubchemmer.py:202 in dbimport()- index: 3, path: PosixPath('/home/user/pubchem/new/ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_000500001_001000000.sdf.gz.md5')

$ pubchemmer find '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide'
ic| pubchemmer.py:310 in find()- index: 0, match: (False, 41252806, True, Decimal('465'), True, True, True, 'AAADceB7MAAAAAAAAAAAAAAAAAAAAAAAAAA8YIAAAAAAAAABQAAAHgAQAAAADAzhmAYzxoPABACIAiRCUACCCAAhIgAIiIAObIiOZiLEsZuXOCjs1hPY6AeQwJAOgAABQAASAAAAAAKAACQAAAAAAAAAAA==', '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide', '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]-1-piperazinecarboxamide', '4-(2,3-dimethylphenyl)-<I>N</I>-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide', '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide', '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide', '4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide', 'InChI=1S/C22H29N3O2/c1-17-6-4-8-20(16-17)27-15-10-23-22(26)25-13-11-24(12-14-25)21-9-5-7-18(2)19(21)3/h4-9,16H,10-15H2,1-3H3,(H,23,26)', 'VUDRQTIWWOQCKA-UHFFFAOYSA-N', Decimal('3.9'), Decimal('367.225977'), 'C22H29N3O2', Decimal('367.5'), 'CC1=CC(=CC=C1)OCCNC(=O)N2CCN(CC2)C3=CC=CC(=C3C)C', 'CC1=CC(=CC=C1)OCCNC(=O)N2CCN(CC2)C3=CC=CC(=C3C)C', Decimal('44.8'), Decimal('367.225977'), 0, 27, 0, 0, 0, 0, 0, 1, -1, '1
5
255', '10  11  8
10  13  8
11  14  8
13  16  8
14  17  8
16  17  8
21  22  8
21  23  8
22  24  8
23  25  8
24  26  8
25  26  8', '8 17 32 33 31 40 40 39 39 27 30 26 22 29 34 21 25 37 36 38 19 24 18 28 20 23 35 15 15 15 15 16 16 16 16 2 9 12 12 12 4 7 14 14 11 11 11 13 13 5 1 3 6 10 10 10', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None)

$ 


```

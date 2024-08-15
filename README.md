```
Usage: pubchemmer [OPTIONS] COMMAND [ARGS]...

Options:
  --verbose
  --dict
  --verbose-inf
  --help         Show this message and exit.

Commands:
  dbimport                      import pubchem sdf files
  dbquery                       session.bind.execute("select column_name,...
  describe                      list database table columns
  dumpconfig
  find                          search for compound in pubchem_iupac_name...
  find-numeric-field-by-range   search for compound with the specified...
  generate-sqlalchemy-model
  humanize-stdin-dicts          humanize field names from messagepacked...
  indexes                       list table indexes
  last-cid                      get last compound id (pubchem CID) in...
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

# hunt for isobars between m/z 13.4 and 14.1:
$ pubchemmer find-numeric-field-by-range generated_mass_to_charge 13.4 14.1 | pubchemmer humanize-stdin-dicts | mpdictkeydrop xlogp3_aa symmetry_classes iupac_name_markup tpsa heavy_atoms hbond_acceptor hbond_d
onor cactvs_complexity iupac_openeye_name iupac_cas_name iupac_traditional_name nonstandardbond inchi                                   
ic| 1723715187.235 16560 pubchemmer:12<click>→ ''/pubchemmer.py:526→ 3.12/contextlib.py:137→ ''/sqlalchemytool.py:111<RTOE>＠ database_already_exists():79→ db_url: 'postgresql+psycopg://postgres@localhost/pubchemmer'
{'cid': 58013676, 'iupac_name': 'carbanylium', 'mass': '14.034908', 'formula': 'CH3+', 'smiles': '[11CH3+]', 'charge': 1, 'm/z': 14.03491}
{'cid': 5460520, 'mass': '14.03278', 'formula': 'BH3+', 'smiles': '[BH3+]', 'charge': 1, 'm/z': 14.03278}
{'cid': 135971918, 'mass': '14.01565', 'formula': 'CH2+', 'smiles': '[CH2+]', 'charge': 1, 'm/z': 14.01565}
{'cid': 21932468, 'iupac_name': 'azanium;magnesium', 'mass': '42.019416', 'formula': 'H4MgN+3', 'smiles': '[NH4+].[Mg+2]', 'charge': 3, 'm/z': 14.00647}
{'cid': 10396793, 'mass': '56.016152', 'formula': 'AlB2Li+4', 'smiles': '[Li+].[B].[B].[Al+3]', 'charge': 4, 'm/z': 14.00404}
{'cid': 57347672, 'iupac_name': 'nitrogen(1+)', 'mass': '14.003074', 'formula': 'N+', 'smiles': '[N+]', 'charge': 1, 'm/z': 14.00307}
{'cid': 16204531, 'iupac_name': 'aluminum;hydride', 'mass': '27.989363', 'formula': 'AlH+2', 'smiles': '[H-].[Al+3]', 'charge': 2, 'm/z': 13.99468}
{'cid': 115281, 'iupac_name': 'aluminum(2+) monohydride', 'mass': '27.989363', 'formula': 'AlH+2', 'smiles': '[AlH+2]', 'charge': 2, 'm/z': 13.99468}
{'cid': 71587901, 'iupac_name': 'magnesium-28(2+)', 'mass': '27.98388', 'formula': 'Mg+2', 'smiles': '[28Mg+2]', 'charge': 2, 'm/z': 13.99194}
{'cid': 153907748, 'iupac_name': 'chromium(5+);hydrate', 'mass': '69.95107', 'formula': 'CrH2O+5', 'smiles': 'O.[Cr+5]', 'charge': 5, 'm/z': 13.99021}
{'cid': 16207196, 'iupac_name': 'silicon(2+)', 'mass': '27.976927', 'formula': 'Si+2', 'smiles': '[Si+2]', 'charge': 2, 'm/z': 13.98846} 
{'cid': 9833933, 'iupac_name': 'technetium(7+)', 'mass': '97.90721', 'formula': 'Tc+7', 'smiles': '[Tc+7]', 'charge': 7, 'm/z': 13.98674}
{'cid': 11963629, 'iupac_name': 'iron(4+)', 'mass': '55.934936', 'formula': 'Fe+4', 'smiles': '[Fe+4]', 'charge': 4, 'm/z': 13.98373}
{'cid': 91868465, 'iupac_name': 'beryllium;germanium(4+)', 'mass': '82.933361', 'formula': 'BeGe+6', 'smiles': '[Be+2].[Ge+4]', 'charge': 6, 'm/z': 13.82223}
{'cid': 21889120, 'iupac_name': 'aluminum;iron(3+)', 'mass': '82.916474', 'formula': 'AlFe+6', 'smiles': '[Al+3].[Fe+3]', 'charge': 6, 'm/z': 13.81941}
{'cid': 21707918, 'iupac_name': 'aluminum;magnesium;hydrate', 'mass': '68.977145', 'formula': 'AlH2MgO+5', 'smiles': 'O.[Mg+2].[Al+3]', 'charge': 5, 'm/z': 13.79543}
{'cid': 22056513, 'iupac_name': 'magnesium;scandium(3+)', 'mass': '68.940949', 'formula': 'MgSc+5', 'smiles': '[Mg+2].[Sc+3]', 'charge': 5, 'm/z': 13.78819}
{'cid': 20202011, 'iupac_name': 'dialuminum;iron(2+)', 'mass': '109.898012', 'formula': 'Al2Fe+8', 'smiles': '[Al+3].[Al+3].[Fe+2]', 'charge': 8, 'm/z': 13.73725}
{'cid': 154082653, 'iupac_name': 'titanium(3+);titanium(4+)', 'mass': '95.895882', 'formula': 'Ti2+7', 'smiles': '[Ti+3].[Ti+4]', 'charge': 7, 'm/z': 13.69941}
{'cid': 21225614, 'iupac_name': 'potassium;hydron', 'mass': '40.979357', 'formula': 'H2K+3', 'smiles': '[H+].[H+].[K+]', 'charge': 3, 'm/z': 13.65979}
{'cid': 18679089, 'iupac_name': 'calcium;hydron', 'mass': '40.970416', 'formula': 'CaH+3', 'smiles': '[H+].[Ca+2]', 'charge': 3, 'm/z': 13.65681}
{'cid': 18378042, 'iupac_name': 'beryllium;hydrate', 'mass': '27.022748', 'formula': 'BeH2O+2', 'smiles': '[Be+2].O', 'charge': 2, 'm/z': 13.51137}
{'cid': 21881329, 'iupac_name': 'lithium;magnesium;sodium', 'mass': '53.990814', 'formula': 'LiMgNa+4', 'smiles': '[Li+].[Na+].[Mg+2]', 'charge': 4, 'm/z': 13.4977}
{'cid': 91868432, 'iupac_name': 'aluminum;lithium;germanium(4+)', 'mass': '107.91872', 'formula': 'AlGeLi+8', 'smiles': '[Li+].[Al+3].[Ge+4]', 'charge': 8, 'm/z': 13.48984}
{'cid': 46830027, 'iupac_name': 'technetium-94(7+)', 'mass': '93.90965', 'formula': 'Tc+7', 'smiles': '[94Tc+7]', 'charge': 7, 'm/z': 13.41566}
{'cid': 20349122, 'iupac_name': 'trilithium;disodium', 'mass': '67.027549', 'formula': 'Li3Na2+5', 'smiles': '[Li+].[Li+].[Li+].[Na+].[Na+]', 'charge': 5, 'm/z': 13.40551}



```

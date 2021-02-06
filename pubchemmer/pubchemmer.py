#!/usr/bin/env python3

# pylint: disable=C0111     # docstrings are always outdated and wrong
# pylint: disable=W0511     # todo is encouraged
# pylint: disable=C0301     # line too long
# pylint: disable=R0902     # too many instance attributes
# pylint: disable=C0302     # too many lines in module
# pylint: disable=C0103     # single letter var names, func name too descriptive
# pylint: disable=R0911     # too many return statements
# pylint: disable=R0912     # too many branches
# pylint: disable=R0915     # too many statements
# pylint: disable=R0913     # too many arguments
# pylint: disable=R1702     # too many nested blocks
# pylint: disable=R0914     # too many local variables
# pylint: disable=R0903     # too few public methods
# pylint: disable=E1101     # no member for base
# pylint: disable=W0201     # attribute defined outside __init__

import hashlib
import os
import pprint
import re
import sys
import time
from decimal import Decimal
from pathlib import Path

import click
import pandas
import requests
from enumerate_input import enumerate_input
from icecream import ic
from kcl.configops import click_read_config
from kcl.configops import click_write_config_entry
from kcl.sqlalchemy.delete_database import \
    delete_database as really_delete_database
from kcl.sqlalchemy.model.BaseMixin import BASE
from kcl.sqlalchemy.self_contained_session import self_contained_session
from structure_data_file_sdf_parser.structure_data_file_sdf_parser import \
    molecule_dict_generator

from pubchemmer.PubChem import PubChem
from pubchemmer.sdf_field_types import SDF_FIELD_TYPES

ic.configureOutput(includeContext=True)

APP_NAME = 'pubchemmer'


def md5_hash_file(path, block_size=256 * 128 * 2):
    md5 = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(block_size), b''):
            md5.update(chunk)
    return md5.hexdigest()


@click.group()
@click.pass_context
def cli(ctx):
    pass


def parse_pubchem_sdtags(content, verbose=False):
    assert isinstance(content, bytes)
    content = content.decode('utf8')
    if verbose:
        ic(content)

    preamble = True
    body = False
    changelog = False
    sdf_format_dict = {"preamble": '', "body": '', "changelog": ''}
    sdf_keys_dict = {}
    for line in content.splitlines():
        line = line + '\r\n'
        #print(line)
        assert isinstance(line, str)
        if line.startswith("PubChem Substance Associated SD Fields"):
            preamble = False
            body = True
            changelog = False
            continue
        if line.startswith("Document Version History"):
            preamble = False
            body = False
            changelog = True
            continue

        if preamble:
            sdf_format_dict['preamble'] += line
        if body:
            sdf_format_dict['body'] += line
        if changelog:
            sdf_format_dict['changelog'] += line

    body = False
    current_key = False
    for line in sdf_format_dict['body'].splitlines():
        #print(line)
        if re.match(r"    [A-Z]", line):
            #print(line)
            new_key = line.strip()
            new_key = new_key.replace(' ', '_')
            current_key = new_key
            sdf_keys_dict[new_key] = ''
            body = True
            continue
        if body:
            assert current_key
            sdf_keys_dict[current_key] += line

    #assert 'mol_chiral_flag' in sdf_keys_dict.keys()
    return sdf_keys_dict


@cli.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
def update_sdf_tags_from_pubchem(verbose: bool,
                                 debug: bool,
                                 ipython: bool,):
    global APP_NAME

    url = "https://ftp.ncbi.nlm.nih.gov/pubchem/data_spec/pubchem_sdtags.txt"
    response = requests.get(url)
    content = response.content
    if ipython:
        import IPython; IPython.embed()

    sdf_keys_dict = parse_pubchem_sdtags(content, verbose=False)

    if verbose:
        pprint.pprint(sdf_keys_dict)

    section = "sdf_keys"
    for key in sdf_keys_dict.keys():
        #ic(key)
        config, config_mtime = click_write_config_entry(click_instance=click,
                                                        app_name=APP_NAME,
                                                        section=section,
                                                        key=key,
                                                        value=sdf_keys_dict[key],
                                                        keep_case=True,
                                                        verbose=verbose,
                                                        debug=debug,)

@cli.command(help="import pubchem sdf files")
@click.argument("paths", type=str, nargs=-1)
@click.option('--add', is_flag=True)
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option('--simulate', is_flag=True)
@click.option('--count', type=int)
@click.option('--start-cid', type=int)
@click.option('--delete-database', is_flag=True)
@click.option("--null", is_flag=True)
def dbimport(paths,
             add,
             verbose,
             debug,
             ipython,
             simulate,
             count,
             start_cid,
             delete_database,
             null):

    total_records = 155000000

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME
    if delete_database:
        if not simulate:
            really_delete_database(database)


    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    #primary_key_created = False
    with self_contained_session(db_url=database) as session:
        if verbose:
            ic(session)

        ic(BASE)
        BASE.metadata.create_all(session.bind)

        if not paths:
            ic('waiting for input')

        all_sdf_keys = config['sdf_keys'].keys()
        assert "PUBCHEM_XLOGP3" in all_sdf_keys

        #mdict_df = pandas.DataFrame()
        for index, path in enumerate_input(iterator=paths,
                                           null=null,
                                           debug=debug,
                                           skip=None,
                                           head=None,
                                           tail=None,
                                           verbose=verbose):
            path = Path(path)
            last_cid_in_file = int(path.name.split("_")[-1].split('.')[0])
            ic(last_cid_in_file)
            if start_cid:
                if last_cid_in_file < start_cid:
                    ic('skipping:', path)
                    continue

            ic(index, path)
            if simulate:
                continue

            import_start_time = time.time()  # per sdf.gz
            md5_hash = md5_hash_file(path)
            expected_md5 = Path(path.as_posix() + '.md5').read_text().split()[0]
            ic(md5_hash)
            ic(expected_md5)
            assert md5_hash == expected_md5
            for mindex, mdict in enumerate(molecule_dict_generator(path=path.as_posix(),
                                                                   verbose=verbose)):
                if start_cid:
                    if int(mdict['PUBCHEM_COMPOUND_CID']) < start_cid:
                        continue

                if count:
                    if count > (mindex + 1):
                        ic(count)
                        sys.exit(1)

                for key in all_sdf_keys:
                    if key not in mdict.keys():
                        mdict[key] = ''

                if verbose:
                    ic(mdict)

                mdict = {k.lower(): v for k, v in mdict.items()}
                mdict = {k.replace(' ', '_'): v for k, v in mdict.items()}
                for key in mdict.keys():
                    #assert key in SDF_FIELD_TYPES.keys()
                    key_type = SDF_FIELD_TYPES[key]
                    if mdict[key]:
                        if key_type in ['Integer', 'Boolean']:
                            mdict[key] = int(mdict[key])
                        if key_type in ['Boolean']:
                            mdict[key] = bool(mdict[key])
                    else:  # ''
                        mdict[key] = None

                pubchem_row = PubChem(**mdict)
                #ic(pubchem_row)
                cid = mdict['pubchem_compound_cid']
                elapsed_time = max(int(time.time() - import_start_time), 1)
                records_per_sec = max(int((mindex + 1) / elapsed_time), 1)
                records_remaning = total_records - cid
                seconds_eta = records_remaning / records_per_sec
                hours_eta = seconds_eta / (60*60)
                days_eta = round(hours_eta / 24, 3)

                session.add(pubchem_row)
                if mindex % 1000 == 0:
                    session.commit()
                    name = mdict['pubchem_iupac_name']
                    ic(days_eta, records_per_sec, records_remaning, mindex, cid, name)

            if ipython:
                import IPython; IPython.embed()
                break


@cli.command(help="get last compound id (pubchem CID) in database")
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
def last_cid(verbose,
             debug,
             ipython):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    #query = "SELECT pubchem.pubchem_compound_cid from pubchem ORDER BY pubchem.pubchem_compound_cid"
    query = "SELECT MAX(pubchem.pubchem_compound_cid) from pubchem"

    with self_contained_session(db_url=database) as session:
        for index, match in enumerate(session.bind.execute(query).fetchone()):
            ic(index, match)

        if ipython:
            import IPython; IPython.embed()

@cli.command(help="list table indexes")
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
def indexes(verbose,
            debug,
            ipython):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    #query = "SELECT pubchem.pubchem_compound_cid from pubchem ORDER BY pubchem.pubchem_compound_cid"
    query = "SELECT * FROM pg_indexes WHERE tablename = 'pubchem';"

    #ic('column_name, data_type, character_maximum_length, column_default, is_nullable')
    with self_contained_session(db_url=database) as session:
        for index, match in enumerate(session.bind.execute(query).fetchall()):
            ic(index, match)

        if ipython:
            import IPython; IPython.embed()

@cli.command(help="list database table columns")
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
def describe(verbose,
             debug,
             ipython):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    #query = "SELECT pubchem.pubchem_compound_cid from pubchem ORDER BY pubchem.pubchem_compound_cid"
    query = "select column_name, data_type, character_maximum_length, column_default, is_nullable from INFORMATION_SCHEMA.COLUMNS where table_name = 'pubchem';"

    ic('column_name, data_type, character_maximum_length, column_default, is_nullable')
    with self_contained_session(db_url=database) as session:
        for index, match in enumerate(session.bind.execute(query).fetchall()):
            ic(index, match)

        if ipython:
            import IPython; IPython.embed()


def humanize_result_dict(result_dict):
    humanized_result_dict = {}
    anchored_name = result_dict['pubchem_iupac_name']
    anchored_mass = result_dict['pubchem_exact_mass']
    anchored_count = result_dict['pubchem_component_count']
    #smiles_anchor = result_dict['pubchem_openeye_iso_smiles']
    for k, v in result_dict.items():
        if not v:
            continue
        if k in ['pubchem_cactvs_subskeys', 'pubchem_iupac_inchikey', 'pubchem_cactvs_tauto_count', 'pubchem_molecular_weight']:
            continue
        if k == 'pubchem_compound_canonicalized':
            if v:
                continue
        if k == 'openbabel_symmetry_classes':
            if v == '1':
                continue
        if '_name' in k and (k != 'pubchem_iupac_name'):
            if v == anchored_name:
                continue
        if k.endswith('_weight'):
            if str(anchored_mass).startswith(str(v)):
                continue
        if k.endswith('_count'):
            if v == anchored_count:
                continue
        if k == 'pubchem_openeye_can_smiles':
            continue  # it's seemingly never more useful than the ISO smiles
            #if v == smiles_anchor:
            #    continue
        if k == 'pubchem_exact_mass':
            v = str(v)
        if k == 'pubchem_coordinate_type':
            if v == '1\n5\n255':
                continue
        k = k.replace('pubchem_', '')
        k = k.replace('compound_cid', 'cid')
        k = k.replace('molecular_formula', 'formula')
        k = k.replace('openeye_iso_smiles', 'smiles')
        k = k.replace('iupac_inchi', 'inchi')
        k = k.replace('exact_mass', 'mass')
        if isinstance(v, Decimal):
            v = str(v)
        humanized_result_dict[k] = v

    return humanized_result_dict


@cli.command(help="search for compound in pubchem_iupac_name column")
@click.argument('match', type=str, nargs=1)
@click.option('--verbose', is_flag=True)
@click.option('--cid', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
def find(match,
         verbose,
         cid,
         debug,
         ipython):

    assert match

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    if not cid:
        query = "SELECT * from pubchem WHERE pubchem.pubchem_iupac_name LIKE '%%{}%%' ORDER BY pubchem_exact_mass DESC".format(match)
    else:
        query = "SELECT * from pubchem WHERE pubchem_compound_cid = '{}'".format(match)

    with self_contained_session(db_url=database) as session:
        result = session.bind.execute(query)
        result_keys = result.keys()
        for index, match in enumerate(result.fetchall()):
            result_zip = zip(result_keys, match)
            #result_dict = {k.replace('pubchem_', ''): v for (k, v) in result_zip if v}
            result_dict = {k: v for (k, v) in result_zip if v}
            humanized_result_dict = humanize_result_dict(result_dict)
            ic(index, humanized_result_dict)

        #ic(result_keys)

        if ipython:
            import IPython; IPython.embed()

@cli.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option("--null", is_flag=True)
def dumpconfig(verbose,
               debug,
               ipython,
               null):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    pprint.pprint(config)
    with self_contained_session(db_url=database) as session:
        query = "select * from INFORMATION_SCHEMA.COLUMNS where table_name = 'pubchem'"
        for index, match in enumerate(session.bind.execute(query).fetchall()):
            ic(index, match)

        if ipython:
            import IPython; IPython.embed()

@cli.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option("--null", is_flag=True)
def generate_sqlalchemy_model(verbose,
                              debug,
                              ipython,
                              null):
    output_template = '''#!/usr/bin/env python3

### AUTO GENERATED FILE ###
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import Text
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import Numeric

Base = declarative_base()


class PubChem(Base):
    __tablename__ = 'pubchem'
'''
    #pprint.pprint(SDF_FIELD_TYPES)
    for key, value in SDF_FIELD_TYPES.items():
        key = key.replace(' ', '_')

        column_type = 'Text'
        if value:
            column_type = value

        primary_key = ''
        if key == 'pubchem_compound_cid':
            primary_key = ', primary_key=True'

        line = "    {column} = Column({column_type}(){primary_key})\n".format(column=key,
                                                                              primary_key=primary_key,
                                                                              column_type=column_type)
        output_template += line

    print(output_template)

    if ipython:
        import IPython; IPython.embed()

@cli.command()
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option("--null", is_flag=True)
def dbquery(verbose,
            debug,
            ipython,
            null):

    '''
    session.bind.execute("select column_name,
                          data_type,
                          character_maximum_length from INFORMATION_SCHEMA.COLUMNS where table_name = 'pubchem'").fetchall()
    '''

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose,
                                             debug=debug,)
    if verbose:
        ic(config, config_mtime)

    with self_contained_session(db_url=database) as session:
        if verbose:
            ic(session)

        if ipython:
            import IPython; IPython.embed()

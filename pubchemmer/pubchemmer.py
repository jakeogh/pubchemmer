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
## pylint: disable=W0703     # catching too general exception

import os
import sys
import time
import requests
import re
import pprint
import pandas
import hashlib
import click
from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path
from icecream import ic
from kcl.configops import click_read_config
from kcl.configops import click_write_config_entry
from kcl.inputops import enumerate_input
from pubchemmer.sdf_field_types import SDF_FIELD_TYPES
from kcl.sqlalchemy.model.BaseMixin import BASE

#Base = declarative_base()
from pubchemmer.PubChem import PubChem

from sqlalchemy_utils.functions import create_database
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.delete_database import delete_database as really_delete_database
from structure_data_file_sdf_parser.structure_data_file_sdf_parser import molecule_dict_generator

ic.configureOutput(includeContext=True)

APP_NAME = 'pubchemmer'


def md5_hash_file(path, block_size=256*128*2):
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
    sdf_format_dict = {"preamble":'', "body":'', "changelog":''}
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
        if body == True:
            assert current_key
            sdf_keys_dict[current_key] += line

    #assert 'mol_chiral_flag' in sdf_keys_dict.keys()
    return sdf_keys_dict


@cli.command()
@click.option('--verbose', is_flag=True)
@click.option('--ipython', is_flag=True)
def update_sdf_tags_from_pubchem(verbose, ipython):
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
                                                        verbose=verbose)

@cli.command()
@click.argument("paths", type=str, nargs=-1)
@click.option('--add', is_flag=True)
@click.option('--verbose', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option('--simulate', is_flag=True)
@click.option('--count', type=str)
@click.option('--delete-database', is_flag=True)
@click.option("--null", is_flag=True)
def dbimport(paths,
             add,
             verbose,
             debug,
             ipython,
             simulate,
             count,
             delete_database,
             null):

    total_records = 155000000

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME
    if delete_database:
        really_delete_database(database)


    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose)
    if verbose:
        ic(config, config_mtime)

    primary_key_created = False
    with self_contained_session(db_url=database) as session:
        if verbose:
            ic(session)

        ic(BASE)
        BASE.metadata.create_all(session.bind)

        if not paths:
            ic('waiting for input')

        all_sdf_keys = config['sdf_keys'].keys()
        assert "PUBCHEM_XLOGP3" in all_sdf_keys

        mdict_df = pandas.DataFrame()
        for index, path in enumerate_input(iterator=paths,
                                           null=null,
                                           debug=debug,
                                           verbose=verbose):
            path = Path(path)

            if verbose or simulate:
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
                records_per_sec = int((mindex + 1) / elapsed_time)
                records_remaning = total_records - cid
                #records_per_sec = int( cid / elapsed_time)
                #seconds_eta = total_records / records_per_sec
                seconds_eta = records_remaning / records_per_sec
                hours_eta = seconds_eta / (60*60)
                days_eta = round(hours_eta / 24, 3)

                session.add(pubchem_row)
                if mindex % 1000 == 0:
                    session.commit()
                    name = mdict['pubchem_iupac_name']
                    ic(days_eta, records_per_sec, records_remaning, mindex, cid, name)

                #mdict_df = pandas.DataFrame(mdict, index=[0])
                ## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_sql.html?highlight=to_sql
                ##mdict_df.to_sql('pubchem', con=session.bind, if_exists='append', index_label='PUBCHEM_COMPOUND_CID')
                #mdict_df.to_sql('pubchem',
                #                con=session.bind,
                #                if_exists='append',
                #                index=False)  # data frame index is always 0

                ##  'PUBCHEM_COMPOUND_CID':
                ##       PubChem Compound ID (CID) is the non-zero unsigned integer PubChem accession ID for a unique chemical structure.
                #if not primary_key_created:
                #    session.bind.execute("ALTER TABLE pubchem ADD PRIMARY KEY (pubchem_compound_cid);")
                #    primary_key_created = True
                #if debug:
                #    if ipython:
                #        import IPython; IPython.embed()
                #        break

            if ipython:
                import IPython; IPython.embed()
                break

@cli.command()
@click.argument('match', type=str)
@click.option('--verbose', is_flag=True)
@click.option('--cid', is_flag=True)
@click.option('--debug', is_flag=True)
@click.option('--ipython', is_flag=True)
@click.option("--null", is_flag=True)
def find(match,
         verbose,
         cid,
         debug,
         ipython,
         null):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose)
    if verbose:
        ic(config, config_mtime)

    if not cid:
        query = "SELECT * from pubchem WHERE pubchem.pubchem_iupac_name LIKE '%%{}%%' ORDER BY pubchem_exact_mass".format(match)
    else:
        query = "SELECT * from pubchem WHERE pubchem_compound_cid = '{}'".format(match)

    with self_contained_session(db_url=database) as session:
        for index, match in enumerate(session.bind.execute(query).fetchall()):
            ic(index, match)

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
                                             verbose=verbose)
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
                                             verbose=verbose)
    if verbose:
        ic(config, config_mtime)

    with self_contained_session(db_url=database) as session:
        if verbose:
            ic(session)

        if ipython:
            import IPython; IPython.embed()

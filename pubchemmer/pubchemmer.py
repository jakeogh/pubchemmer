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
import requests
import re
import pprint
import pandas
import click
from pathlib import Path
from icecream import ic
from kcl.configops import click_read_config
from kcl.configops import click_write_config_entry
from kcl.inputops import enumerate_input

from sqlalchemy_utils.functions import create_database
from kcl.sqlalchemy.self_contained_session import self_contained_session
from kcl.sqlalchemy.delete_database import delete_database as really_delete_database
from structure_data_file_sdf_parser.structure_data_file_sdf_parser import molecule_dict_generator


ic.configureOutput(includeContext=True)
# import IPython; IPython.embed()
# import pdb; pdb.set_trace()
# from pudb import set_trace; set_trace(paused=False)

APP_NAME = 'pubchemmer'


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
            current_key = new_key
            sdf_keys_dict[new_key] = ''
            body = True
            continue
        if body == True:
            assert current_key
            sdf_keys_dict[current_key] += line

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
@click.option('--delete-database', is_flag=True)
@click.option("--null", is_flag=True)
def dbimport(paths,
             add,
             verbose,
             debug,
             ipython,
             delete_database,
             null):

    global APP_NAME
    database = 'postgres://postgres@localhost/' + APP_NAME
    if delete_database:
        really_delete_database(database)

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose)
    if verbose:
        ic(config, config_mtime)

    #if add:
    #    section = "test_section"
    #    key = "test_key"
    #    value = "test_value"
    #    config, config_mtime = click_write_config_entry(click_instance=click,
    #                                                    app_name=APP_NAME,
    #                                                    section=section,
    #                                                    key=key,
    #                                                    value=value,
    #                                                    keep_case=False,
    #                                                    verbose=verbose)
    #    if verbose:
    #        ic(config)

    with self_contained_session(db_url=database) as session:
        if verbose:
            ic(session)
        if not paths:
            ic('waiting for input')

        all_sdf_keys = config['sdf_keys'].keys()
        assert "PUBCHEM_XLOGP3" in all_sdf_keys

        for index, path in enumerate_input(iterator=paths,
                                           null=null,
                                           debug=debug,
                                           verbose=verbose):
            if verbose:
                ic(index, path)

            for mindex, mdict in enumerate(molecule_dict_generator(path=path,
                                                                   verbose=verbose)):

                for key in all_sdf_keys:
                    if key not in mdict.keys():
                        mdict[key] = ''

                if verbose:
                    ic(mdict)
                mdict_df = pandas.DataFrame(mdict, index=[0])
                #mdict_df.to_sql('pubchem', con=session.bind, if_exists='append', index_label='PUBCHEM_COMPOUND_CID')
                mdict_df.to_sql('pubchem', con=session.bind, if_exists='append')
                ic(mdict['PUBCHEM_IUPAC_NAME'])
                if mindex > 4:
                    break
                #break
                if debug:
                    if ipython:
                        import IPython; IPython.embed()
                        break

            if ipython:
                import IPython; IPython.embed()
                break

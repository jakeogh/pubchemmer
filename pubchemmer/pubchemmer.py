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
import click
from pathlib import Path
from icecream import ic
from kcl.configops import click_read_config
from kcl.configops import click_write_config_entry
from kcl.inputops import enumerate_input


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
@click.option("--null", is_flag=True)
def dbimport(paths,
             add,
             verbose,
             debug,
             ipython,
             null):

    global APP_NAME

    config, config_mtime = click_read_config(click_instance=click,
                                             app_name=APP_NAME,
                                             verbose=verbose)
    if verbose:
        ic(config, config_mtime)

    if add:
        section = "test_section"
        key = "test_key"
        value = "test_value"
        config, config_mtime = click_write_config_entry(click_instance=click,
                                                        app_name=APP_NAME,
                                                        section=section,
                                                        key=key,
                                                        value=value,
                                                        keep_case=False,
                                                        verbose=verbose)
        if verbose:
            ic(config)

    for index, path in enumerate_input(iterator=paths,
                                       null=null,
                                       debug=debug,
                                       verbose=verbose):
        if verbose:
            ic(index, path)

        with open(path, 'rb') as fh:
            path_bytes_data = fh.read()

        if ipython:
            import IPython; IPython.embed()



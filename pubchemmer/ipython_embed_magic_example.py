#!/usr/bin/env python

import os
import sys
import click
from traitlets.config.loader import Config
from IPython.core.magic import register_line_magic
from IPython.terminal.prompts import Prompts, Token
from IPython.terminal.embed import InteractiveShellEmbed
from icecream import ic

from IPython.core.magic import (Magics, magics_class, line_magic, cell_magic, line_cell_magic)
from IPython.core.magic_arguments import (argument, magic_arguments, parse_argstring)
from IPython.core.magic import needs_local_scope


class CustomPrompt(Prompts):
    def in_prompt_tokens(self, cli=None):
        return [(Token.Prompt, 'In ['),
                (Token.PromptNum, str(self.shell.execution_count)),
                (Token.Prompt, ']: '),
                (Token, os.getcwd()),
                (Token.Prompt, ' >>>: ')]

try:
    get_ipython
except NameError:
    nested = 0
    cfg = Config()
    cfg.TerminalInteractiveShell.prompts_class=CustomPrompt

    # why wont this execute?
    # https://github.com/ipython/ipython/blob/master/IPython/core/shellapp.py#L103
    cfg.InteractiveShellApp.exec_lines = [
    'print("\\nimporting some things\\n")',
    'import math',
    "math"
    ]

else:
    print("Running nested copies of IPython.")
    print("The prompts for the nested copy have been modified")
    cfg = Config()
    nested = 1

ipyshell = InteractiveShellEmbed(config=cfg,
                                 banner1='Dropping into IPython',
                                 exit_msg='Leaving Interpreter.')




# The class MUST call this class decorator at creation time
@magics_class
class MyMagics(Magics):

    @needs_local_scope
    @line_magic
    @magic_arguments()
    @argument('-o', '--option', help='An optional argument.')
    @argument('arg', type=int, help='An integer positional argument.')
    def magic_cool(self, arg, **kwargs):
        """ A really cool magic command."""
        #print("local_ns:", local_ns)
        ic(arg)
        ic(kwargs)
        args = parse_argstring(self.magic_cool, arg)
        ic(args)


    @line_magic
    def lmagic(self, line):
        "my line magic"
        print("Full access to the main IPython object:", self.shell)
        print("Variables in the user namespace:", list(self.shell.user_ns.keys()))
        return line

    @needs_local_scope
    @line_magic
    @magic_arguments()
    @argument('arg', type=str)
    def click_invoke(self, arg, **kwargs):
        ic(arg)
        ic(kwargs)
        #match='4-(2,3-dimethylphenyl)-N-[2-(3-methylphenoxy)ethyl]piperazine-1-carboxamide')
        return kwargs['local_ns']['ctx'].invoke(kwargs['local_ns']['find'], match=arg)

    @cell_magic
    def cmagic(self, line, cell):
        "my cell magic"
        return line, cell

    @line_cell_magic
    def lcmagic(self, line, cell=None):
        "Magic that works both as %lcmagic and as %%lcmagic"
        if cell is None:
            print("Called as line magic")
            return line
        else:
            print("Called as cell magic")
            return line, cell


ipyshell.register_magics(MyMagics)


# Goal: execute this after the IPython shell starts, embedded in the local namespace (so ctx (see below) is in locals()"
#START = '''
#@register_line_magic
#def click_invoke(ctx, f, *args, **kwargs):
#    return ctx.invoke(f, *args, **kwargs)
#'''

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):

    ipyshell()

    print('\nBack in caller program, moving along...\n')
    sys.exit(0)


if __name__ == '__main__':
    cli()



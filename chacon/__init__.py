from chacon.classes import CheckedItem, CheckedItemContract
from chacon.utils import _outputs_from_tsv
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--summary', required=True, type=str)
@click.option('-o', '--output', required=True, type=str)
def create(summary, output):
    fps = _outputs_from_tsv(summary)
    contract = CheckedItemContract.from_filepaths(fps)
    #print(CheckedItemContract.from_dict(contract.as_dict())) #TODO test this...
    contract.to_yaml(output)

@cli.command()
@click.option('-i', '--contract','input', required=True, type=str)
@click.option('--silent', is_flag=True)
def verify(input, silent):
    contract = CheckedItemContract.from_yaml(input)
    is_ok = contract.verify(verbose=not silent)
    exit(0 if is_ok else 1)
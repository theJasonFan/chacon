from snakecheck.classes import CheckedItem, CheckedItemContract
from snakecheck.utils import _outputs_from_snakemake_sumary
import click

@click.group()
def cli():
    pass

@cli.command()
@click.option('-i', '--summary', required=True, type=str)
@click.option('-o', '--output', required=True, type=str)
def create(summary, output):
    fps = _outputs_from_snakemake_sumary(summary)
    contract = CheckedItemContract.from_filepaths(fps)
    #print(CheckedItemContract.from_dict(contract.as_dict())) #TODO test this...
    contract.to_yaml(output)

@cli.command()
@click.option('-i', '--contract','input', required=True, type=str)
def verify(input):
    contract = CheckedItemContract.from_yaml(input)
    is_ok = contract.verify(verbose=True)
    exit(0 if is_ok else 1) # nice exit code
import snakecheck
import pandas as pd
import click
import hashlib
import yaml

__outputs = 'output_file'

@click.command()
@click.argument('snake_summary')
def main(snake_summary):
    outputs = _extract_outputs(snake_summary)
    checked_item_dicts = [CheckedItem(fp).as_dict() for fp in outputs]
    print(checked_item_dicts)

def _extract_outputs(fp):
    df = pd.read_csv(fp, sep='\t')
    outputs = df[__outputs].values
    return outputs

class CheckedItem(object):
    def __init__(self, fp, md5=None):
        self.fp = fp
        self.md5 = md5 if md5 is not None else self._calc_md5(fp)
    
    @staticmethod
    def _calc_md5(fp):
        with open(fp, 'rb') as f:
            hexhash = hashlib.md5(f.read()).hexdigest()
        return hexhash
    
    def as_dict(self):
        return dict(path=self.fp, md5=self.md5)
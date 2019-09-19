import pandas as pd
__outputs = 'output_file'

def _outputs_from_tsv(fp):
    df = pd.read_csv(fp, sep='\t')
    outputs = df.iloc[:, 0].values
    return outputs

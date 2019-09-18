import pandas as pd
__outputs = 'output_file'

def _outputs_from_snakemake_sumary(fp):
    df = pd.read_csv(fp, sep='\t')
    outputs = df[__outputs].values
    return outputs

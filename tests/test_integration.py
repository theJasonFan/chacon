from chacon import create, verify
from click.testing import CliRunner

import tempfile
from os import path

def test_create_verify():
    runner = CliRunner()
    with runner.isolated_filesystem():
        checked_file = 'hello.txt'
        checked_file_list = 'summary.tsv'
        contract_file = 'contract.yml'
        
        # Write a file
        with open(checked_file, 'w') as f:
            f.write('Hello world!')

        # Write TSV of files to track
        with open(checked_file_list, 'w') as f:
            f.write('outputs\n%s\n' % checked_file)
        
        create_result = runner.invoke(create, ['-i', checked_file_list, '-o', contract_file])
        assert create_result.exit_code == 0

        verify_result = runner.invoke(verify, ['-i', contract_file])
        assert verify_result.exit_code == 0

def test_create_verify_fails():
    runner = CliRunner()
    with runner.isolated_filesystem():
        checked_file = 'hello.txt'
        checked_file_list = 'summary.tsv'
        contract_file = 'contract.yml'
        
        # Write a file
        with open(checked_file, 'w') as f:
            f.write('Hello world!')

        # Write TSV of files to track
        with open(checked_file_list, 'w') as f:
            f.write('outputs\n%s\n' % checked_file)
        
        with open(contract_file, 'w') as f:
            f.write('%s: bad_hash' % checked_file)

        verify_result = runner.invoke(verify, ['-i', contract_file])
        assert verify_result.exit_code == 1
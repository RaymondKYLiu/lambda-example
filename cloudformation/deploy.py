import os
import subprocess
from configparser import SafeConfigParser
import shlex
# import boto3

config = SafeConfigParser()
config.optionxform = str # # preserve case
config.read(os.path.join(os.path.dirname(__file__), 'parameters.ini'))

parameters = []
# [('prefix', 'hw2-cf'), ('appversion', '1.0.0-9')]
for item in config.items('Parameters'):
    key = item[0]
    val = item[1]
    parameters.append(f'{key}={val}')

template_file = os.path.join(os.path.dirname(__file__), 'hw2.yml')
param_strs = ' '.join(parameters)
cmd = (
    f'aws cloudformation deploy --stack-name hw2 --template-file {template_file} '
    f'--capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM --parameter-overrides {param_strs}'
)
print('deploy command: ' + cmd)
subprocess.check_call(shlex.split(cmd))

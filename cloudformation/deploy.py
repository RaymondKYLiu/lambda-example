import os
import subprocess
import configparser
import shlex

class EnvInterpolation(configparser.BasicInterpolation):
    """Interpolation which expands environment variables in values.
        https://stackoverflow.com/a/49529659
    """

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

config = configparser.ConfigParser(interpolation=EnvInterpolation())
config.optionxform = str # preserve case
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

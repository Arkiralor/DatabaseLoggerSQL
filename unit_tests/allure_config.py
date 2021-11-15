import os
import sys
import platform as pl

REPORT_PATH = 'reports/environment.properties'

def config_retrieve():
    arch = pl.architecture()
    mac = pl.machine()
    name = pl.node()
    platform = pl.platform()
    version = pl.python_version_tuple()
    proc_name = pl.processor()
    return arch[0], proc_name, mac, name, platform, version

def config_writer(report_path:str = REPORT_PATH):
    
    architecture, processor, machine, machine_name, platform, version = config_retrieve()

    data = f'Architecture={architecture}\nProcessor={processor}\nMachine={machine}\nMachineName={machine_name}\nPlatform={platform}\nPythonVersion={version[0]}.{version[1]}.{version[2]}'

    
    with open(report_path, 'wt') as config_file:
        config_file.write(data)

if __name__ == "__main__":
    config_writer()
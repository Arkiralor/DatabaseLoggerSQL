import platform as pl

# Just declaring a variable to the path to the env variable file to make my life a bit easier:
REPORT_PATH = 'AllureReports/environment.properties'


# Method to retrieve platform details:
def config_retrieve():
    arch = pl.architecture() # Retrieve the platform architecture
    mac = pl.machine() # Retrieve the platform nachine
    name = pl.node() # Retrieve the machine name as per the LAN policy
    platform = pl.platform() # Retrieve the platform
    version = pl.python_version_tuple() # Retrieve the python MajorVersion, MinorVersion and PatchLevel in a tuple
    proc_name = pl.processor() # Retrieve the type of the processor
    sys_name = pl.system()

    return arch[0], proc_name, sys_name, mac, name, platform, version


# Method to write platform details to 'environment.properties' file:
def config_writer(report_path:str = REPORT_PATH):
    
    architecture, processor, system_details, machine, machine_name, platform, version = config_retrieve()

    # Constructing 'data' variable as a string to be written to the file:
    data = f'Architecture={architecture}\n'+\
    f'Processor={processor}\n'+\
    f'SystemDetails={system_details}\n'+\
    f'Machine={machine}\n'+\
    f'MachineName={machine_name}\n'+\
    f'Platform={platform}\n'+\
    f'PythonVersion={version[0]}.{version[1]}.{version[2]}'

    # Over-writing data in file with new contents:
    with open(report_path, 'wt') as config_file:
        config_file.write(data)

# Please don't make me explain this; I still have no idea wtf '__main__' means 😭:
if __name__ == "__main__":
    config_writer()
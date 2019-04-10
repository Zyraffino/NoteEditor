import os
import data_structure

LIB_NAME = 'meta.json'

def _make_dir(dir):
    if not os.path.exists(dir):
        print('{} not  exists'.format('\\'.join(dir.split('\\')[-2:])))
        os.mkdir(dir)
    else:
        print('{} dose exists'.format('\\'.join(dir.split('\\')[-2:])))


def _build_config(config_path):
    mother_path = '/'.join(config_path.split('/')[:-2])
    config_dict = {'mother_dir': mother_path,
                   'src_dir': os.path.join(mother_path, 'src'),
                   'meta_dir': os.path.join(mother_path, 'src', 'meta'),
                   'meta_path' : os.path.join(mother_path, 'src', 'meta', 'meta.json'),
                   'intell_dir': os.path.join(mother_path, 'src', 'intell'),
                   'script_path': os.path.join(mother_path, 'script'),
                   'config_path': config_path,
                   'log_path': os.path.join(mother_path, 'src', 'event.log')
                   }
    with open(config_path, 'w') as config:
        for key, value in config_dict.items():
            config.write('{};{}\n'.format(key,value))
    return config_dict


def _load_config(config_path):
    with open(config_path, 'r') as config:
        config_dict = {}
        for property in config.readlines():
            config_dict[property.split(';')[0]] = property.split(';')[1][:-1]
    return config_dict


def edit_config(config_path, edit_dict):
    original_dict = _load_config(config_path)
    for key, value in edit_dict.items():
        original_dict[key] = value

    with open(config_path, 'w') as config:
        for o_key, o_value in original_dict.items():
            config.write('{};{}\n'.format(o_key,o_value))

    return original_dict


def check_config():
    current_dir = os.getcwd()
    mother_dir = '/'.join(current_dir.split('/')[:-1])
    config_dir = os.path.join(mother_dir, 'src')
    config_path = os.path.join(mother_dir, 'src', 'setting.config')
    is_config_exist = os.path.exists(config_path)

    if is_config_exist:
        config_dict = _load_config(config_path)
        print('config file loaded')
    else:
        _make_dir(config_dir)
        config_dict = _build_config(config_path)
        _make_dir(config_dict['meta_dir'])
        _make_dir(config_dict['intell_dir'])
        print('config file built')

    return config_dict


def load_library(lib_dir):
    lib_path = os.path.join(lib_dir,LIB_NAME)
    if os.path.exists(lib_path):
        instance = data_structure.Library('load', lib_path)
        print('LIB EXISTED')
        for key, dict in instance.state_dict.items():
            print(key)
            print(dict)
    else:
        instance = data_structure.Library('new', lib_path)
        print('LIB CREATED')
    return instance


def initiate_project():
    config_dict = check_config()
    lib_instance = load_library(config_dict['meta_dir'])
    log_instance = data_structure.Logger(config_dict)
    flow_dict = {
        'config': config_dict,
        'meta_data' : lib_instance,
        'log_instance' : log_instance
    }
    return flow_dict


def terminate_project(flow_dict):
    flow_dict['meta_data'].close()
    flow_dict['log_instance'].close()

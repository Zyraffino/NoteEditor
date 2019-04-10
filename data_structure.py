import os
from collections import OrderedDict
import json

class Disease_oriented_object:
    def __init__(self, mode, contents, flow_dict):
        assert mode in ['new','load']
        self.ordered_category_list = ['CAUSE', 'SYMPTOM', 'DIAGNOSTICS/RESULT', 'TREATMENT']
        if mode == 'new':
            self.state_dict = OrderedDict({
                'NAME': contents[0],
                'CAUSE': contents[1],
                'SYMPTOM': contents[2],
                'DIAGNOSTICS/RESULT': contents[3],
                'TREATMENT': contents[4],
                'NOTE': contents[5]
            })
            self.instance_to_json(flow_dict)
            self.meta_update(flow_dict)
            print('created_\n', self.format_representation())
        elif mode == 'load':
            self.state_dict = self.json_to_instance(flow_dict, contents)
            print('loaded_\n', self.format_representation())

    def meta_update(self,flow_dict):
        meta_instance = flow_dict['meta_data']
        logger_instance = flow_dict['log_instance']
        log_format = 'LibUpdate:: {} update, {}<={} ({})'
        disease_name = self.state_dict['NAME']
        for category in self.ordered_category_list:
            target_dict = meta_instance.state_dict[category]
            for key in self.state_dict[category].keys():
                try:
                    if not target_dict[key].count(disease_name):
                        target_dict[key].append(disease_name)
                        mode = 'append'
                    else:
                        mode = 'existed'
                except:
                    target_dict[key] = [disease_name]
                    mode = 'create'
                finally:
                    logger_instance.log(log_format.format(category, key, disease_name, mode))

        if not meta_instance.state_dict['NAME'].count(disease_name):
            meta_instance.state_dict['NAME'].append(disease_name)
            mode_name = 'create'
        else:
            mode_name = 'existed'
        logger_instance.log(log_format.format('NAME', 'DS_LIST', disease_name, mode_name))

    def instance_to_json(self, flow_dict):
        json_path = os.path.join(flow_dict['config']['intell_dir'],
                                 '{}.json'.format(self.state_dict['NAME']))
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(self.state_dict, json_file, ensure_ascii=False)
        print('Intell file json-ed in {}'.format('/'.join(json_path.split('/')[-3:])))
        return json_path

    def json_to_instance(self, flow_dict, name):
        intell_dir = flow_dict['config']['intell_dir']
        json_path = os.path.join(intell_dir, '{}.json'.format(name))
        return json.load(open(json_path), object_pairs_hook=OrderedDict)

    def format_representation(self):
        text = '''[Disease]\n{}\n\n[Cause]\n{}\n[Symptom / Sign]\n{}\n[Diagnostic tool / Result]\n{}\n[Treatment]\n{}\n[extra NOTE]\n{}'''
        format_content = []
        for category in self.ordered_category_list:
            content = self.state_dict[category]
            format_text = ''
            for key, value in content.items():
                format_text += '   {} : {}\n'.format(key, value)
            format_content.append(format_text)
        return text.format(self.state_dict['NAME'], *format_content, self.state_dict['NOTE'])


class Library:
    def __init__(self, mode, meta_path):
        assert mode in ['new', 'load']
        self.path = meta_path
        if mode == 'new':
            self.category_list = ['CAUSE', 'SYMPTOM', 'DIAGNOSTICS/RESULT', 'TREATMENT']
            self.state_dict = OrderedDict({category: {} for category in self.category_list})
            self.state_dict['NAME'] = []
        elif mode == 'load':
            self.category_list = ['CAUSE', 'SYMPTOM', 'DIAGNOSTICS/RESULT', 'TREATMENT']
            self.state_dict = self.json_to_instance()
        self.count = 0
        self.instance_to_json()


    def close(self):
        self.instance_to_json()

    def instance_to_json(self):
        with open(self.path, 'w', encoding='utf-8') as json_file:
            json.dump(self.state_dict, json_file, ensure_ascii=False)
        self.count +=1
        print('Metafile safely json-ed {} times'.format(self.count))

    def json_to_instance(self):
        return json.load(open(self.path), object_pairs_hook=OrderedDict)

    def restore_disease_instance(self, name_ds, flow_dict):
        disease_instance = Disease_oriented_object('load', name_ds, flow_dict)
        return disease_instance


class Logger:
    def __init__(self, config_dict):
        self.log_path = config_dict['log_path']
        log_mode = 'a' if os.path.exists(self.log_path) else 'w'
        print('Logging file open \'{}\' mode'.format(log_mode))
        self.log_file = open(self.log_path, log_mode)

    def log(self, str):
        self.log_file.write(str+'\n')
        print(str)

    def close(self):
        print('Logfile safely closed')
        self.log_file.close()


def input_trimmer(input_list):
    for ind in range(1,5):
        tmp_dict = OrderedDict()
        for tmp_item in input_list[ind].split('\n'):
            if not tmp_item: continue
            key = tmp_item.split(':')[0].lstrip().rstrip()
            value = tmp_item.split(':')[1].lstrip().rstrip() if len(tmp_item.split(':')) == 2 else ''
            tmp_dict[key] = value
        input_list[ind] = tmp_dict

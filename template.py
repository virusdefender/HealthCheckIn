#!/usr/bin/env python3
import argparse
import json
import re
import requests

def traverse(node):
    componentName = node['componentName']
    if componentName.endswith('Field'):
        print()
        print('#', node['props']['label']['zh_CN'])
        if componentName in ('RadioField', 'SelectField'):
            dataSource = node['props']['dataSource']
            if dataSource['complexType'] == 'custom':
                for option in dataSource['options']:
                    print('#', node['props']['fieldId'], json.dumps(option['value'], ensure_ascii=False))
            else:
                print('#', node['props']['fieldId'], 'unsupported')
        elif componentName == 'CheckboxField':
            dataSource = node['props']['dataSource']
            if dataSource['complexType'] == 'custom':
                print('#', node['props']['fieldId'], json.dumps([option['value'] for option in dataSource['options']], ensure_ascii=False))
            else:
                print('#', node['props']['fieldId'], 'unsupported')
        elif componentName in ('TextField', 'TextareaField'):
            print('#', node['props']['fieldId'], '"placeholder"')
        elif componentName == 'DateField':
            print('#', node['props']['fieldId'], '1582992000000')
        elif componentName == 'CitySelectField':
            print('#', node['props']['fieldId'], '["110000", "110100"]')
        else:
            print('#', node['props']['fieldId'], 'unsupported')
    if node['children']:
        for child in node['children']:
            traverse(child)

def main():
    parser = argparse.ArgumentParser(description='Health Check-In')
    parser.add_argument('form_url', help='URL to form')
    args = parser.parse_args()
    form_url = args.form_url

    session = requests.Session()
    base_url = '/'.join(form_url.split('/', 3)[:3])
    form_body = session.get(form_url).text
    form_uuid = re.search(r'formUuid: "(FORM-[0-9A-Z]+)"', form_body).group(1)
    schema_url = base_url + re.search(r'GET_FORM_SCHEMA: "(/[^"]+)"', form_body).group(1)
    schema_body = session.post(schema_url, data={'formUuid': form_uuid}).json()
    assert schema_body['success']
    schema = schema_body['content']
    schema_version = schema['version']
    schema_pages = schema['pages']
    assert len(schema_pages) == 1
    schema_page = schema_pages[0]
    schema_layout = schema_page['layout']

    print(form_url)
    print(form_uuid)
    print('version', schema_version)
    traverse(schema_layout)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import argparse
import json
import re
import requests

def main():
    parser = argparse.ArgumentParser(description='Health Check-In')
    parser.add_argument('answer_file', help='path/URL to answer file')
    args = parser.parse_args()
    
    answer_file = args.answer_file
    if answer_file.startswith('http://') or answer_file.startswith('https://'):
        rsp = requests.get(answer_file)
        assert rsp.status_code == 200, f'{rsp.status_code} {rsp.reason}'
        answer_data = rsp.text
    else:
        with open(answer_file, 'r') as f:
            answer_data = f.read()
    answer_data = answer_data.replace('\r', '') # in case of Windows user
    it = iter(answer_data.split('\n'))

    form_url = next(it)
    assert re.match(r'https?://', form_url), 'invalid form URL'
    base_url = '/'.join(form_url.split('/', 3)[:3])
    answer_uuid = next(it)
    match = re.fullmatch('version (\d+)', next(it))
    assert match, 'invalid answer file'
    answer_version = int(match.group(1))

    session = requests.Session()
    form_body = session.get(form_url).text
    form_uuid = re.search(r'formUuid: "([^"]+)"', form_body).group(1)
    submit_url = base_url + re.search(r'RECEIPT_SAVE_FORM_DATA: "(/[^"]+)"', form_body).group(1)
    schema_url = base_url + re.search(r'GET_FORM_SCHEMA: "(/[^"]+)"', form_body).group(1)
    schema_body = session.post(schema_url, data={'formUuid': form_uuid}).json()
    assert schema_body['success'], 'unable to fetch form schema'
    schema = schema_body['content']
    schema_version = schema['version']

    assert answer_uuid == form_uuid, f'form mismatch, got {answer_uuid}, expect {form_uuid}'

    value = []
    for line in it:
        if not line or line.startswith('#'): continue
        field_id, field_value = line.split(' ', 1)
        value.append({
            'fieldId': field_id,
            'fieldData': { 'value': json.loads(field_value) },
        })
    assert value, 'nothing to submit'

    rsp = session.post(submit_url, data={
        'formUuid': form_uuid,
        'value': json.dumps(value, ensure_ascii=False, separators=(',', ':')),
    })
    assert rsp.status_code == 200, f'{rsp.status_code} {rsp.reason}'
    result = rsp.json()
    assert result['success'], rsp.text
    print('提交成功', result['content']['formInstId'])

    # best effort
    assert answer_version == schema_version, f'version mismatch, got {answer_version}, expect {schema_version}'

if __name__ == '__main__':
    main()

import re

def clean_data(ti):
    data = ti.xcom_pull(task_ids='fetch_data')

    for item in data:
        item['text'] = re.sub(r'@[^\s]+', '', item['text'])
        item['text'] = re.sub(r'\s+', ' ', item['text'])
        item['text'] = item['text'].strip()

    return data
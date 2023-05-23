import csv
import json
from pprint import pprint

try:
    with open('fields.txt', 'r') as f:
        data = f.read().lower()
        fields = data.split()
except:
    with open('fields.txt', 'w') as f:
        fields = []

datadict = {}

for index in range(len(fields)):
    try:
        with open(f'words/{fields[index]}.json', 'r') as f:
            data = json.loads(f.read())
            texts = []
            for text in data:
                if text and text != '---':
                    texts.append(text.lower().strip())
                    if '’' in text:
                        texts.append(text.replace('’', '\''))
                    elif '‘' in text:
                        texts.append(text.replace('‘', '\''))
                    elif 'ʻ' in text:
                        texts.append(text.replace('ʻ', '\''))
                    elif '"' in text:
                        texts.append(text.replace('"', ""))
                    elif '\n' in text:
                        texts.append(text.replace('\n', " "))
            datadict[f'{fields[index].lower().strip()}'] = texts
    except:
        with open(f'words/{fields[index]}.json', 'w') as f:
            f.write(json.dumps([]))
pprint(datadict)


# CSV faylini yozish rejimida ochish
with open('negPosWords.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # sarlavhani yozish
    writer.writerow(['text', 'label'])

    # ma'lumotlarni qatorma-qator yozish
    for key, values in datadict.items():
        for value in values:
            writer.writerow([value, key])

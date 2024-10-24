import re
import json

with open('text.txt') as file:
    text = file.read()

# get words
words = [w.lower() for w in re.split(r'\W+', text) if w]

# dict key=verb, value=set(noun)
d = {}

# if verb find next nearest noun and add to dictionary d
for i, w in enumerate(words):
    if(w.endswith('s')):
        # change verb to present tense
        present = w[:-2] + 'as'
        for j in range(i, i+4):
            if words[j].endswith(('o', 'on', 'oj' 'ojn')):
                if present not in d:
                    d[present] = set()
                d[present].add(words[j].rstrip('jn'))

# Take 100 with the most verbs
result = sorted(d, key=lambda x: len(d[x]), reverse=True)[:100]

with open('result.json', 'w') as file:
    json.dump({k: sorted(v) for k, v in d.items()}, file, indent=4)
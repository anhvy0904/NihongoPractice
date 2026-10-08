import json
from pathlib import Path
from collections import Counter

bank = json.loads((Path(__file__).parent / 'dist/questions.json').read_text(encoding='utf-8'))
assert [u['id'] for u in bank['units']] == [9, 10, 11, 12]
ids = set()
for unit in bank['units']:
    for section in ('vocabulary', 'grammar'):
        questions = unit[section]
        assert len(questions) == 40
        assert sum(bool(q.get('suppliedSample')) for q in questions) == (12 if section=='vocabulary' else 10)
        assert [q['group'] for q in questions] == sorted(q['group'] for q in questions)
        signatures = set()
        for q in questions:
            assert q['id'] not in ids
            ids.add(q['id'])
            signature = (q['type'], q['target'])
            assert signature not in signatures
            signatures.add(signature)
            assert len(q['options']) == len(set(q['options'])) == 4
            assert isinstance(q['answer'], int) and 0 <= q['answer'] < 4
            assert q['prompt'] and q['explanation']
            assert q['prompt'].startswith('問題')
            if q['type'] in ('reading','kanji','synonym'):
                assert q['target'] in q['sentence']
            if q['type'] == 'order':
                assert q['options'][q['answer']] == q['orderedFragments'][2]
                assert set(q['options']) == set(q['orderedFragments'])
                assert q['fullSentence']
        print(f"Unit {unit['id']} {section}: {len(questions)}; {dict(Counter(q['type'] for q in questions))}")
assert len(ids) == 320
print('PASS: 320 unique IDs, balanced sections, options, answer keys and star positions.')

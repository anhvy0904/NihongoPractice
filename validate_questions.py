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
common=bank['commonVocabulary']
assert len(common['words'])==118
assert len({w['word'] for w in common['words']})==118
assert Counter(w['category'] for w in common['words'])=={'noun':47,'verb':36,'adjective':11,'adverb':12,'katakana':12}
assert {q['word'] for q in common['questions']}=={w['word'] for w in common['words']}
assert Counter(q['type'] for q in common['questions'])['context']>=10
for q in common['questions']:
    assert q['id'] not in ids
    ids.add(q['id'])
    assert len(q['options'])==len(set(q['options']))==4
    assert 0<=q['answer']<4 and q['explanation']
    if 'sentence' in q: assert q['target'] in q['sentence']
print(f"PASS: {len(common['questions'])} common questions cover all 118 unique words across five categories.")

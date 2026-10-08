import fs from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const bank=JSON.parse(fs.readFileSync('dist/questions.json','utf8'));
const ctx=vm.createContext({document:{querySelector:()=>({})}});
vm.runInContext(fs.readFileSync('dist/app.js','utf8').split("document.addEventListener('change'")[0],ctx);ctx.data=bank;vm.runInContext('bank=data',ctx);
const questions=[...bank.units.flatMap(u=>[...u.vocabulary,...u.grammar]),...bank.commonVocabulary.questions];
for(const q of questions){
 const entry=q.studyPattern?bank.learning.grammar[q.studyPattern]:bank.learning.vocabulary[q.studyKey];
 assert.ok(entry,`Missing ${q.id}`);
 assert.ok(entry.meaning&&entry.translation&&entry.sentence);
 assert.equal(entry.exampleRuby.map(p=>p.text).join(''),entry.sentence);
 for(const p of entry.exampleRuby)if(/[一-龯々]/.test(p.text))assert.ok(p.reading&&p.reading!=='*',`${q.id}: ${p.text}`);
 assert.ok(entry.synonyms.length&&entry.antonyms.length);
 if(q.studyKey)assert.ok(entry.reading&&entry.hanViet&&entry.wordRuby.length);
 ctx.q=q;const html=vm.runInContext('studyPanel(q)',ctx);
 assert.match(html,/Câu ví dụ/);assert.match(html,/Trái nghĩa \/ đối chiếu/);
 assert.ok(!html.includes('undefined'));
}
assert.equal(bank.learning.vocabulary['出荷'].hanViet,'xuất hà');
assert.equal(bank.learning.vocabulary['出荷'].reading,'しゅっか');
assert.ok(bank.learning.vocabulary['朝会'].exampleRuby.some(p=>p.text==='九時'&&p.reading==='くじ'));
assert.ok(bank.learning.vocabulary['発注する'].exampleRuby.some(p=>p.text==='仕入先'&&p.reading==='しいれさき'));
console.log(`PASS: all ${questions.length} questions have complete study cards, Japanese readings, translated examples and labeled relations.`);

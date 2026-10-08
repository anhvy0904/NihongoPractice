import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import assert from 'node:assert/strict';
const bank=JSON.parse(readFileSync(new URL('./dist/questions.json',import.meta.url),'utf8'));
const code=readFileSync(new URL('./dist/app.js',import.meta.url),'utf8').split("document.addEventListener('change'")[0];
const context=vm.createContext({document:{querySelector:()=>({})},__bank:bank});
vm.runInContext(code,context);
vm.runInContext('bank=__bank',context);
const expected={reading:10,kanji:8,context:10,synonym:6,usage:6};
const draws=new Set();
for(let i=0;i<20;i++){
 const questions=vm.runInContext('chooseCommon()',context);
 assert.equal(questions.length,40);
 assert.equal(new Set(questions.map(q=>q.id)).size,40);
 const counts={};
 for(const q of questions)counts[q.type]=(counts[q.type]||0)+1;
 assert.deepEqual(counts,expected);
 assert.ok(questions.every((q,j)=>j===0||q.group>=questions[j-1].group));
 draws.add(questions.map(q=>q.id).join(','));
}
assert.ok(draws.size>1);
console.log('PASS: Actual sampler draws 40 unique questions across all five formats; repeated sessions vary.');

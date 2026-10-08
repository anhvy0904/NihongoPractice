'use strict';
const $ = selector => document.querySelector(selector);
const main = $('#main');
const nav = $('#navigation');
const names = { vocabulary: 'Từ vựng', grammar: 'Ngữ pháp' };
const types = { reading:'Cách đọc', kanji:'Chữ Hán', context:'Điền từ', synonym:'Gần nghĩa', usage:'Cách dùng', fill:'Điền ngữ pháp', order:'Sắp xếp ★' };
let bank, activeUnit = null, session = null, pendingAction = null;
const escapeHTML = str => String(str).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const shuffle = items => { const a = [...items]; for(let i=a.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[a[i],a[j]]=[a[j],a[i]];} return a; };
const sectionLabel = s => s.unit==='common'?'Từ vựng chung':`Unit ${s.unit}`;
function commonCard(){const c=bank.commonVocabulary;return `<article class="common-card"><div><p class="eyebrow">ÔN TẬP CHUNG</p><h2>Từ vựng chung</h2><p>${c.words.length} từ · Danh từ, động từ, tính từ, phó từ và katakana.</p><small>${c.questions.length} câu trong ngân hàng · Mỗi lượt 40 câu</small></div><button class="primary" data-common-start>Bắt đầu luyện</button></article>`;}
function chooseCommon(){
 const c=bank.commonVocabulary;
 const quotas={reading:10,kanji:8,context:10,synonym:6,usage:6};const result=[];const seen=new Set();
 for(const [type,count] of Object.entries(quotas)){
   let choices=shuffle(c.questions.filter(q=>q.type===type));
   choices.sort((a,b)=>Number(seen.has(a.word))-Number(seen.has(b.word)));
   for(const q of choices.slice(0,count)){result.push(q);seen.add(q.word);}
 }
 return result.sort((a,b)=>a.group-b.group);
}
function showCommon(){session=null;activeUnit='common';renderNav();document.title='Từ vựng chung · Nihongo Practice';const c=bank.commonVocabulary;
 main.innerHTML=`<button class="back" data-home>Tổng quan</button><p class="eyebrow">ÔN TẬP CHUNG</p><h1>Từ vựng chung</h1><p class="common-description">Toàn bộ ${c.words.length} từ trong bảng bạn cung cấp, luyện theo 5 dạng đề.</p>${commonCard()}<p class="source-note">Mỗi lượt chọn 40 câu từ ngân hàng ${c.questions.length} câu. Các lượt có thể trùng một số từ. Có chấm điểm, giải thích và luyện lại câu chưa đúng.</p>`;focusMain();}
function questionText(q){
 if(!q.sentence)return escapeHTML(q.target);
 const at=q.sentence.lastIndexOf(q.target);
 if(at<0)return escapeHTML(q.sentence);
 return escapeHTML(q.sentence.slice(0,at))+`<strong class="tested-word">${escapeHTML(q.target)}</strong>`+escapeHTML(q.sentence.slice(at+q.target.length));
}
function focusMain(){ main.focus({preventScroll:true}); window.scrollTo({top:0,behavior:'instant'}); }
function renderNav(){
  nav.innerHTML = `<button class="nav-btn ${activeUnit === null?'active':''}" data-home ${activeUnit===null?'aria-current="page"':''}><span class="nav-icon">▦</span>Tổng quan</button>` + bank.units.map(u=>`<button class="nav-btn ${activeUnit===u.id?'active':''}" data-unit="${u.id}" ${activeUnit===u.id?'aria-current="page"':''}><span class="nav-number">${u.id}</span>Unit ${u.id}</button>`).join('')+`<button class="nav-btn ${activeUnit==='common'?'active':''}" data-common ${activeUnit==='common'?'aria-current="page"':''}><span class="nav-icon" lang="ja">語</span>Từ vựng chung</button>`;
}
function unitCards(){ return bank.units.map(u=>`<article class="unit-card"><div class="unit-top"><span class="unit-kicker">UNIT ${u.id}</span><small>80 câu hỏi</small></div><h3>${escapeHTML(u.title)}</h3><p class="patterns" lang="ja">${u.patterns.map(escapeHTML).join(' · ')}</p><div class="launch-row"><button class="launch" data-start="vocabulary" data-unit="${u.id}"><span><span class="launch-icon" lang="ja">字</span> Từ vựng</span><small>40 câu · 5 dạng bài</small></button><button class="launch" data-start="grammar" data-unit="${u.id}"><span><span class="launch-icon" lang="ja">文</span> Ngữ pháp</span><small>40 câu · 2 dạng bài</small></button></div></article>`).join(''); }
function home(){ session = null; activeUnit = null; renderNav(); document.title = 'Nihongo Practice · Unit 9–12';
 main.innerHTML = `<div class="intro"><div><p class="eyebrow">LUYỆN TẬP TIẾNG NHẬT</p><h1>Sẵn sàng cho bài kiểm tra.</h1><p>Chọn một unit hoặc phần từ vựng chung để bắt đầu luyện tập.</p></div><div class="intro-count">${320+bank.commonVocabulary.questions.length}<span>CÂU HỎI ĐỂ LUYỆN TẬP</span></div></div><div class="overview-stats"><span><b>4</b> unit</span><span><b>160</b> câu từ vựng</span><span><b>160</b> câu ngữ pháp</span></div>${commonCard()}<div class="section-heading"><h2>Bắt đầu luyện tập</h2><span>Mỗi phần · 40 câu hỏi</span></div><div class="units-grid">${unitCards()}</div><div class="format-strip"><span><b>Từ vựng</b> &nbsp; Cách đọc · Chữ Hán · Điền từ · Gần nghĩa · Cách dùng</span><span><b>Ngữ pháp</b> &nbsp; Điền mẫu câu · Sắp xếp ★</span></div><p class="source-note">Bám theo đề mẫu Unit 9–12 bạn cung cấp, bổ sung câu luyện cùng dạng.</p>`; focusMain(); }
function showUnit(id){ session=null; activeUnit=id;renderNav();const u=bank.units.find(u=>u.id===id);document.title=`Unit ${id} · Nihongo Practice`;
 main.innerHTML=`<button class="back" data-home>Tổng quan</button><p class="eyebrow">UNIT ${id}</p><h1>${escapeHTML(u.title)}</h1><p style="color:var(--muted)">Chọn phần bạn muốn luyện tập.</p><div class="unit-detail"><h2>Các mẫu ngữ pháp</h2><p class="patterns" lang="ja">${u.patterns.map(escapeHTML).join(' · ')}</p></div><div class="section-cards">${['vocabulary','grammar'].map(section=>`<article class="practice-card"><h2>${names[section]}</h2><div class="count">40<small>câu hỏi</small></div><p>${section==='vocabulary'?'Luyện cách đọc, viết chữ Hán, điền từ, từ gần nghĩa và cách sử dụng.':'Luyện chọn mẫu câu và sắp xếp các mảnh vào vị trí ★.'}</p><button class="primary" data-start="${section}" data-unit="${id}">Luyện ${names[section].toLowerCase()}</button></article>`).join('')}</div>`;focusMain(); }
function start(id,section,subset){ const u=bank.units.find(u=>u.id===id); activeUnit=id; const originals=subset||(id==='common'?chooseCommon():u[section]);
 const questions=originals.map((q,originalIndex)=>{const order=shuffle([0,1,2,3]);return {...q,originalIndex,options:order.map(i=>q.options[i]),answer:order.indexOf(q.answer)};});
 session={unit:id,section,questions,answers:Array(questions.length).fill(null),graded:Array(questions.length).fill(false),lastFeedback:null,masterQuestions:questions,masterAnswers:Array(questions.length).fill(null),firstScore:null,retryRound:0,index:0,submitted:false,isRetry:!!subset};renderNav();renderQuiz();focusMain(); }
function countAnswered(){return session.answers.filter(a=>a!==null).length;}
function mapPanel(){const s=session; const done=s.graded.filter(Boolean).length;const n=s.questions.length;
 return `<aside class="map-panel" aria-label="Danh sách câu hỏi"><h2>${s.submitted?'Xem lại từng câu':'Tiến độ làm bài'}</h2><p class="map-counter" aria-live="polite">${s.submitted?`${s.answers.filter((a,i)=>a===s.questions[i].answer).length} / ${n} câu đúng`:`Đã chấm ${done} / ${n}`}</p><div class="progress-track"><div class="progress-fill" style="width:${done/n*100}%"></div></div><div class="question-map">${s.questions.map((q,i)=>{const result=(s.submitted||s.graded[i])?(s.answers[i]===q.answer?'right':'wrong'):(s.answers[i]!==null?'answered':'');return `<button class="map-button ${result} ${i===s.index?'current':''}" data-jump="${i}" aria-label="Câu ${i+1}, ${(s.submitted||s.graded[i])?(result==='right'?'đúng':s.answers[i]===null?'chưa trả lời':'sai'):(s.answers[i]===null?'chưa trả lời':'đã trả lời')}" ${i===s.index?'aria-current="step"':''}>${i+1}</button>`;}).join('')}</div><div class="map-key"><span class="status-good">Đúng</span><span class="status-bad">Sai</span><span>Chưa chấm</span></div>${s.submitted?'<button class="secondary" data-results style="width:100%">Về kết quả</button>':'<p class="quiz-note">Chọn đáp án là chấm ngay. Bấm Câu tiếp để chuyển câu. Làm hết bài, các câu sai sẽ tự chuyển sang lượt làm lại.</p>'}</aside>`; }
function questionCard(){const s=session,q=s.questions[s.index],selected=s.answers[s.index],locked=s.submitted||s.graded[s.index];
 return `<section><div class="question-card"><div class="question-meta"><span class="type-badge">問題${q.group} · ${types[q.type]}</span><span>${s.retryRound?`Câu gốc ${q.originalIndex+1} · `:''}Câu ${s.index+1} / ${s.questions.length}</span></div><h2 id="question-prompt" lang="ja">${escapeHTML(q.prompt)}</h2><div id="question-stem" class="question-text ${!q.sentence&&q.type==='usage'?'short':''}" lang="ja">${questionText(q)}</div><fieldset class="choices" aria-labelledby="question-prompt" aria-describedby="question-stem"><legend class="sr-only">Chọn một trong bốn đáp án</legend>${q.options.map((o,i)=>{const cls=locked?(i===q.answer?'correct':i===selected?'incorrect':''):i===selected?'selected':'';const mark=locked?(i===q.answer?'Đáp án đúng':i===selected?'Bạn chọn':''):'';return `<label class="choice ${cls} ${locked?'review':''}"><input type="radio" name="answer" value="${i}" ${selected===i?'checked':''} ${locked?'disabled':''}><span class="choice-letter" aria-hidden="true">${i+1}</span><span lang="ja">${escapeHTML(o)}</span>${mark?`<span class="answer-mark">${mark}</span>`:''}</label>`;}).join('')}</fieldset>${locked?`<div class="explanation"><h3 class="${selected===q.answer?'status-good':'status-bad'}">${selected===q.answer?'Chính xác':selected===null?'Bạn chưa trả lời câu này':'Cần ôn lại'}</h3>${q.pattern?`<p lang="ja"><b>${escapeHTML(q.pattern)}</b></p>`:''}<p>${escapeHTML(q.explanation)}</p>${q.fullSentence?`<p class="sentence" lang="ja">${escapeHTML(q.fullSentence)}</p><p>Thứ tự đúng: <span lang="ja">${q.orderedFragments.map(escapeHTML).join(' → ')}</span><br>Mảnh ở vị trí ★: <b lang="ja">${escapeHTML(q.options[q.answer])}</b></p>`:''}</div>`:''}</div><div class="quiz-controls"><button class="secondary" data-prev ${s.index===0?'disabled':''}>Câu trước</button>${!s.submitted?`<button class="primary" data-check ${selected===null?'disabled':''}>Câu tiếp</button>`:`<button class="secondary" ${s.index===s.questions.length-1?(s.submitted?'data-results':'data-next-pending'):'data-next'}>${s.index===s.questions.length-1?(s.submitted?'Về kết quả':'Câu chưa chấm'):'Câu tiếp'}</button>`}</div></section>`; }
function renderQuiz(){const s=session; document.title=`${names[s.section]} · ${sectionLabel(s)} · Nihongo Practice`;
main.innerHTML=`<div class="quiz-heading"><div><p class="eyebrow">${sectionLabel(s).toUpperCase()} ${s.retryRound?`· LÀM LẠI LƯỢT ${s.retryRound}`:s.isRetry?'· ÔN LẠI':''}</p><h1 lang="ja">${s.section==='vocabulary'?'ミニテスト①（漢字・語彙）':'ミニテスト②（文法）'}</h1><p>${s.submitted?'Xem đáp án và giải thích chi tiết.':`${names[s.section]} · Chọn đáp án 1–4 để xem đúng/sai và đáp án đúng ngay.`}</p></div><button class="secondary" data-leave>Chọn bài khác</button></div>${s.retryRound&&!s.submitted?`<div class="instant-feedback bad"><b>Làm lại ${s.questions.length} câu chưa đúng · Lượt ${s.retryRound}</b><p class="retry-note">Lượt đầu: ${s.firstScore} / ${s.masterQuestions.length} câu đúng. Tiếp tục làm lại đến khi đúng hết.</p></div>`:''}${feedbackPanel()}<div class="quiz-layout">${questionCard()}${mapPanel()}</div>`; }
function updateAnswer(value){
 const s=session;if(!s||s.submitted||s.graded[s.index]||![0,1,2,3].includes(value))return;
 const index=s.index;s.answers[index]=value;s.graded[index]=true;s.masterAnswers[s.questions[index].originalIndex]=value;s.lastFeedback={index,correct:value===s.questions[index].answer};
 renderQuiz();
 $('[data-check]').focus({preventScroll:true});
}
function feedbackPanel(){
 const f=session.lastFeedback;if(!f)return '';
 const q=session.questions[f.index];
 return `<div class="instant-feedback ${f.correct?'good':'bad'}" role="status" aria-live="polite"><b>Câu ${f.index+1}: ${f.correct?'Đúng!':'Chưa đúng.'}</b> Đáp án đúng: <span lang="ja">${escapeHTML(q.options[q.answer])}</span><details><summary>Xem giải thích câu ${f.index+1}</summary><p>${escapeHTML(q.explanation)}</p>${q.fullSentence?`<p lang="ja">${escapeHTML(q.fullSentence)}</p>`:''}</details></div>`;
}
function checkAnswer(){
 const s=session;if(!s||s.submitted||!s.graded[s.index])return;
 const index=s.index;
 const next=s.graded.findIndex((g,i)=>!g&&i>index);
 if(s.graded.every(Boolean)){submit();return;}
 s.index=next<0?s.graded.findIndex(g=>!g):next;renderQuiz();focusMain();
}
function confirmAction(title,message,accept,fn){ pendingAction=fn;$('#confirm-title').textContent=title;$('#confirm-message').textContent=message;$('#accept-confirm').textContent=accept;$('#confirm-dialog').showModal(); }
function requestSubmit(){
 if(!session||session.submitted)return;
 const missing=session.graded.findIndex(g=>!g);
 if(missing>=0){session.index=missing;renderQuiz();focusMain();return;}
 submit();
}
function submit(){
 const s=session;if(!s||s.submitted||s.graded.some(g=>!g))return;
 const wrong=s.questions.filter((q,i)=>s.answers[i]!==q.answer);
 if(s.firstScore===null)s.firstScore=s.questions.length-wrong.length;
 if(wrong.length){
   s.retryRound++;s.questions=wrong;s.answers=Array(wrong.length).fill(null);s.graded=Array(wrong.length).fill(false);s.index=0;s.lastFeedback=null;s.isRetry=true;
   renderQuiz();focusMain();return;
 }

 s.questions=s.masterQuestions;s.answers=[...s.masterAnswers];s.graded=Array(s.questions.length).fill(true);s.index=0;s.submitted=true;

 s.lastFeedback=null;renderResults();focusMain();
}
function renderResults(){const s=session,n=s.questions.length,correct=s.answers.filter((a,i)=>a===s.questions[i].answer).length,blank=s.answers.filter(a=>a===null).length,wrong=n-correct-blank;
 main.innerHTML=`${feedbackPanel()}<section class="result-header"><p class="eyebrow">${sectionLabel(s).toUpperCase()} · ${names[s.section].toUpperCase()}</p><h1>${correct===n?'Bạn đã hoàn thành xuất sắc!':correct/n>=.8?'Làm tốt lắm, tiếp tục luyện nhé.':'Bài luyện đã hoàn thành.'}</h1><div class="score">${correct}<span> / ${n}</span></div><p class="result-sub">${s.firstScore} / ${n} câu đúng ở lượt đầu${s.retryRound?` · Đã làm lại ${s.retryRound} lượt`:""}. Hiện bạn đã trả lời đúng toàn bộ ${n} câu.</p><div class="score-stats"><span><b class="status-good">${correct}</b>Đúng</span><span><b class="status-bad">${wrong}</b>Sai</span><span><b>${blank}</b>Chưa trả lời</span></div><div class="result-actions"><button class="primary" data-review>Xem đáp án</button>${correct<n?'<button class="secondary" data-retry-wrong>Luyện câu chưa đúng</button>':''}<button class="secondary" data-restart>Làm lại bài</button><button class="text-button" data-leave>Chọn bài khác</button></div></section>`; }
function go(fn){if(session&&!session.submitted&&(countAnswered()>0||session.retryRound>0))confirmAction('Rời bài đang làm?', 'Đáp án của bài hiện tại sẽ bị xóa khi bạn chọn bài khác.', 'Rời bài',fn);else fn();}
document.addEventListener('change', e=>{if(e.target.matches('input[name="answer"]')&&session&&!session.submitted) updateAnswer(Number(e.target.value));});
document.addEventListener('click',e=>{const b=e.target.closest('button,a.brand');if(!b||!bank)return;
 if(b.matches('a.brand')){e.preventDefault();go(home);}
 else if(b.hasAttribute('data-common-start'))go(()=>start('common','vocabulary'));
 else if(b.hasAttribute('data-common'))go(showCommon);
 else if(b.hasAttribute('data-start'))go(()=>start(Number(b.dataset.unit),b.dataset.start));
 else if(b.hasAttribute('data-home'))go(home);
 else if(b.hasAttribute('data-unit'))go(()=>showUnit(Number(b.dataset.unit)));
 else if(b.hasAttribute('data-leave'))go(()=>activeUnit==='common'?showCommon():showUnit(activeUnit));
 else if(b.hasAttribute('data-check'))checkAnswer();
 else if(b.hasAttribute('data-next-pending')){session.index=session.graded.findIndex(g=>!g);renderQuiz();focusMain();}
 else if(b.hasAttribute('data-submit'))requestSubmit();
 else if(b.hasAttribute('data-jump')){session.index=Number(b.dataset.jump);renderQuiz();focusMain();}
 else if(b.hasAttribute('data-prev')){session.index--;renderQuiz();focusMain();}
 else if(b.hasAttribute('data-next')){session.index++;renderQuiz();focusMain();}
 else if(b.hasAttribute('data-results')){renderResults();focusMain();}
 else if(b.hasAttribute('data-review')){session.index=0;renderQuiz();focusMain();}
 else if(b.hasAttribute('data-restart'))start(session.unit,session.section);
 else if(b.hasAttribute('data-retry-wrong')){const s=session;start(s.unit,s.section,s.questions.filter((q,i)=>s.answers[i]!==q.answer));}
});
$('#sources-button').addEventListener('click',()=>$('#source-dialog').showModal());
$('#close-sources').addEventListener('click',()=>$('#source-dialog').close());
$('#cancel-confirm').addEventListener('click',()=>{$('#confirm-dialog').close();pendingAction=null;});
$('#accept-confirm').addEventListener('click',()=>{const action=pendingAction;pendingAction=null;$('#confirm-dialog').close();if(action)action();});
$('#confirm-dialog').addEventListener('cancel',()=>{pendingAction=null;});
window.addEventListener('beforeunload',e=>{if(session&&!session.submitted&&(countAnswered()>0||session.retryRound>0)){e.preventDefault();e.returnValue='';}});
fetch('questions.json').then(r=>{if(!r.ok)throw new Error('Không tải được câu hỏi');return r.json();}).then(data=>{if(!Array.isArray(data.units)||data.units.length!==4||data.units.some(u=>u.vocabulary.length!==40||u.grammar.length!==40))throw new Error('Bộ câu hỏi không hợp lệ');if(!data.commonVocabulary||data.commonVocabulary.questions.length<40)throw new Error("Thiếu câu hỏi chung");bank=data;$(".top-tag").textContent=`4 UNIT · ${bank.commonVocabulary.words.length} TỪ CHUNG`;home();}).catch(()=>{main.innerHTML='<div class="error" role="alert"><h1>Chưa tải được bộ câu hỏi</h1><p>Vui lòng kiểm tra kết nối và tải lại trang.</p><button class="primary" id="reload">Tải lại</button></div>';$('#reload').addEventListener('click',()=>location.reload());});

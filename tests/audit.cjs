'use strict';
const assert=require('node:assert/strict');
const E=require('../app.js');
let checks=0;
function eq(a,b,message){assert.ok(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<1e-5,message+` (${a} ≠ ${b})`);checks++}
function derivative(f,x){const d=1e-5;return(f(x+d)-f(x-d))/(2*d)}
assert.equal(E.TEMPLATES.length,28);
assert.equal(E.TEMPLATES.filter(t=>t.exam==='oge').length,14);
assert.equal(E.TEMPLATES.filter(t=>t.exam==='ege').length,14);
assert.deepEqual(new Set(E.TEMPLATES.map(t=>t.id)).size,28);
assert.equal(E.parseAnswer('−3,5'),-3.5);
assert.equal(E.parseAnswer('3/2'),1.5);
assert.equal(E.parseAnswer('2/0'),null);
assert.equal(E.parseAnswer('1 + 2'),null);
assert.equal(E.isNumberCorrect('-1,5',-1.5),true);
assert.equal(E.isNumberCorrect('0.5',2),false);
assert.equal(E.isPointsCorrect([{x:1,y:2},{x:3,y:4}],[{x:3,y:4},{x:1,y:2}]),true);
assert.equal(E.isPointsCorrect([{x:1,y:2},{x:3,y:5}],[{x:3,y:4},{x:1,y:2}]),false);
for(const t of E.TEMPLATES){
 for(let seed=1;seed<=100;seed++){
  const x=E.makeTask(t.id,seed), f=x.chart.functions[0]?.fn;
  assert.equal(x.id,t.id);assert.equal(x.exam,t.exam);assert.equal(x.level,t.level);
  assert.ok(x.formula&&x.prompt&&x.hint&&x.solution&&x.chart);
  if(x.format==='points'){
   assert.equal(x.targets.length,2);
   assert.ok(E.isPointsCorrect(x.targets,x.targets));
   for(const p of x.targets){eq(x.solutionFunctions[0].fn(p.x),p.y,`${t.id} point @${seed}`)}
  }else{
   assert.equal(typeof x.answer,'number');assert.ok(Number.isFinite(x.answer));
   assert.ok(E.isNumberCorrect(String(x.answer).replace('.',','),x.answer));
  }
  switch(t.id){
   case 'og-line-root':case 'og-para-roots':case 'ege-stationary':case 'ege-cubic-derivative':eq(f(x.answer),0,t.id);break;
   case 'og-para-vertex':case 'og-abs-min':case 'ege-quadratic-range':{
    if(t.id==='og-para-vertex')eq(derivative(f,x.answer),0,t.id);
    else if(t.id==='og-abs-min')assert.ok(Array.from({length:101},(_,i)=>f((i-50)/10)).every(y=>y>=x.answer-1e-9));
    else assert.ok(Array.from({length:101},(_,i)=>f((i-50)/10)).every(y=>y<=x.answer+1e-9));
    break;
   }
   case 'og-line-cross':case 'ege-rational-line':eq(f(x.answer),x.chart.functions[1].fn(x.answer),t.id);break;
   case 'og-hyper-asymptote':assert.ok(!Number.isFinite(f(x.answer)));break;
   case 'ege-derivative-max':assert.ok(f(x.answer-.01)>0&&f(x.answer+.01)<0);break;
   case 'ege-derivative-min':assert.ok(f(x.answer-.01)<0&&f(x.answer+.01)>0);break;
   case 'ege-tangent-parallel':{
    const slope=Number(x.prompt.match(/y = ([+\-]?\d+)x/)[1]);eq(derivative(f,x.answer),slope,t.id);break;
   }
   case 'ege-tangent-slope':{
    const at=Number(x.prompt.match(/x = ([+\-]?\d+)/)[1]);eq(derivative(f,at),x.answer,t.id);break;
   }
   case 'ege-exp-value':{
    const at=Number(x.prompt.match(/f\(([+\-]?\d+)\)/)[1]);eq(f(at),x.answer,t.id);break;
   }
   case 'ege-log-root':eq(f(x.answer),x.chart.horizontal[0],t.id);break;
   case 'ege-derivative-integral':{
    const interval=x.chart.vertical,from=interval[0],to=interval[1],N=1000,dx=(to-from)/N;
    let sum=0;for(let i=0;i<N;i++)sum+=f(from+(i+.5)*dx)*dx;
    eq(sum,x.answer,t.id);break;
   }
   case 'og-para-horizontal':case 'og-abs-count':case 'og-piecewise':case 'og-hyper-count':case 'ege-parameter-quadratic':case 'ege-derivative-parameter':{
    const m=x.chart.horizontal[0];
    assert.ok(Number.isFinite(m));assert.ok([0,1,2].includes(x.answer));break;
   }
   case 'ege-cubic-parameter':{
    const m=x.chart.horizontal[0],cnt=Math.abs(m)>2?1:Math.abs(m)===2?2:3;assert.equal(x.answer,cnt);break;
   }
   case 'og-hole':{
    const h=x.chart.holes[0],m=x.chart.horizontal[0];eq(f(h.x),h.y,t.id);assert.equal(x.answer,m===h.y?0:1);break;
   }
   default:break;
  }
  checks++;
 }
}
console.log(`✓ ${E.TEMPLATES.length} шаблонов · 100 seeds каждый · ${checks} проверок пройдены`);

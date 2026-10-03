'use client';

import {useEffect,useMemo,useState} from 'react';

function makeSteps(solution:string){
  const normalized=solution.replace(/\s+/g,' ').trim();
  if(!normalized)return ['Решение пока не добавлено.'];
  const parts=(normalized.match(/[^.!?;]+[.!?;]?/g)||[normalized]).map(x=>x.trim()).filter(Boolean);
  const steps:string[]=[];
  for(const part of parts){
    if(steps.length&&part.length<28){steps[steps.length-1]+=' '+part;}
    else steps.push(part);
  }
  return steps;
}

export default function SolutionBoard({solution}:{solution:string}){
  const steps=useMemo(()=>makeSteps(solution),[solution]);
  const[visible,setVisible]=useState(0);
  const[playing,setPlaying]=useState(false);

  useEffect(()=>{
    if(!playing)return;
    if(visible>=steps.length){setPlaying(false);return;}
    const timer=window.setTimeout(()=>setVisible(v=>Math.min(steps.length,v+1)),1800);
    return()=>window.clearTimeout(timer);
  },[playing,visible,steps.length]);

  const next=()=>setVisible(v=>Math.min(steps.length,v+1));
  const reset=()=>{setPlaying(false);setVisible(0)};

  return <div className="solutionBoard">
    <div className="solutionBoardHead">
      <div>
        <div className="solutionBoardTitle">Интерактивная доска решения</div>
        <div className="solutionBoardSub">Решение открывается по шагам — как объяснение у доски.</div>
      </div>
      <div className="solutionBoardCounter">{visible}/{steps.length}</div>
    </div>

    <div className="solutionBoardScreen">
      {visible===0?<div className="solutionBoardEmpty">Нажмите «Показать первый шаг» или запустите автопоказ.</div>:
      steps.slice(0,visible).map((step,i)=><div className="solutionStep" key={i}>
        <span className="solutionStepNo">{i+1}</span>
        <div>{step}</div>
      </div>)}
      {visible===steps.length&&<div className="solutionBoardDone">✓ Решение показано полностью</div>}
    </div>

    <div className="solutionBoardControls">
      <button className="btn" onClick={next} disabled={visible>=steps.length}>{visible===0?'Показать первый шаг':'Следующий шаг →'}</button>
      <button className="btn secondary" onClick={()=>setVisible(steps.length)} disabled={visible>=steps.length}>Показать всё</button>
      <button className="btn secondary" onClick={()=>setPlaying(p=>!p)} disabled={visible>=steps.length}>{playing?'⏸ Пауза':'▶ Автопоказ'}</button>
      <button className="btn ghost" onClick={reset} disabled={visible===0&&!playing}>↺ Сначала</button>
    </div>
  </div>
}

'use client';

import {useEffect,useRef,useState} from 'react';

export default function WhiteBoard({problemId}:{problemId:number}){
  const canvasRef=useRef<HTMLCanvasElement|null>(null);
  const drawing=useRef(false);
  const [mode,setMode]=useState<'pen'|'eraser'>('pen');
  const storageKey=`math-olympiad-whiteboard-${problemId}`;

  useEffect(()=>{
    const canvas=canvasRef.current;
    if(!canvas)return;
    const resize=()=>{
      const rect=canvas.getBoundingClientRect();
      const dpr=window.devicePixelRatio||1;
      const saved=canvas.toDataURL();
      canvas.width=Math.max(1,Math.round(rect.width*dpr));
      canvas.height=Math.max(1,Math.round(rect.height*dpr));
      const ctx=canvas.getContext('2d');
      if(!ctx)return;
      ctx.scale(dpr,dpr);
      ctx.lineCap='round';
      ctx.lineJoin='round';
      ctx.fillStyle='#fff';
      ctx.fillRect(0,0,rect.width,rect.height);
      const source=localStorage.getItem(storageKey)||saved;
      if(source&&source!=='data:,'){
        const img=new Image();
        img.onload=()=>ctx.drawImage(img,0,0,rect.width,rect.height);
        img.src=source;
      }
    };
    resize();
    window.addEventListener('resize',resize);
    return()=>window.removeEventListener('resize',resize);
  },[storageKey]);

  const point=(e:React.PointerEvent<HTMLCanvasElement>)=>{
    const canvas=canvasRef.current!;
    const rect=canvas.getBoundingClientRect();
    return {x:e.clientX-rect.left,y:e.clientY-rect.top};
  };

  const start=(e:React.PointerEvent<HTMLCanvasElement>)=>{
    const canvas=canvasRef.current!;
    canvas.setPointerCapture(e.pointerId);
    const ctx=canvas.getContext('2d');
    if(!ctx)return;
    drawing.current=true;
    const p=point(e);
    ctx.beginPath();
    ctx.moveTo(p.x,p.y);
  };

  const move=(e:React.PointerEvent<HTMLCanvasElement>)=>{
    if(!drawing.current)return;
    const canvas=canvasRef.current!;
    const ctx=canvas.getContext('2d');
    if(!ctx)return;
    const p=point(e);
    ctx.globalCompositeOperation='source-over';
    ctx.strokeStyle=mode==='pen'?'#101828':'#ffffff';
    ctx.lineWidth=mode==='pen'?3:22;
    ctx.lineTo(p.x,p.y);
    ctx.stroke();
  };

  const finish=()=>{
    if(!drawing.current)return;
    drawing.current=false;
    const canvas=canvasRef.current;
    if(canvas)localStorage.setItem(storageKey,canvas.toDataURL('image/png'));
  };

  const clear=()=>{
    const canvas=canvasRef.current;
    if(!canvas)return;
    const ctx=canvas.getContext('2d');
    if(!ctx)return;
    const rect=canvas.getBoundingClientRect();
    ctx.globalCompositeOperation='source-over';
    ctx.fillStyle='#fff';
    ctx.fillRect(0,0,rect.width,rect.height);
    localStorage.removeItem(storageKey);
  };

  return <section className="whiteBoard">
    <div className="whiteBoardHead">
      <div>
        <div className="whiteBoardTitle">Белая доска</div>
        <div className="whiteBoardSub">Черновик для решения — пишите мышью, стилусом или пальцем.</div>
      </div>
      <div className="whiteBoardTools">
        <button className={`boardTool ${mode==='pen'?'active':''}`} onClick={()=>setMode('pen')} type="button">✎ Ручка</button>
        <button className={`boardTool ${mode==='eraser'?'active':''}`} onClick={()=>setMode('eraser')} type="button">⌫ Ластик</button>
        <button className="boardTool danger" onClick={clear} type="button">Очистить</button>
      </div>
    </div>
    <div className="whiteBoardCanvasWrap">
      <canvas
        ref={canvasRef}
        className="whiteBoardCanvas"
        onPointerDown={start}
        onPointerMove={move}
        onPointerUp={finish}
        onPointerCancel={finish}
        onPointerLeave={finish}
      />
    </div>
    <div className="whiteBoardNote">Записи сохраняются в этом браузере для данной задачи.</div>
  </section>;
}

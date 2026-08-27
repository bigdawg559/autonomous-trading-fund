'use client';

import { useEffect, useState } from 'react';

const API = process.env.NEXT_PUBLIC_SIGNAL_API_URL || '';

type State = { signal?: string; reason_codes?: string[]; entry?: number; stop_loss?: number; tp1?: number; tp2?: number; risk_reward?: number; model_status?: string };

export default function Home() {
  const [state, setState] = useState<State>({});
  const [error, setError] = useState('');

  useEffect(() => {
    let active = true;
    const load = async () => {
      try {
        const r = await fetch(`${API}/api/signal/current`, { cache: 'no-store' });
        if (!r.ok) throw new Error(`API ${r.status}`);
        const data = await r.json();
        if (active) { setState(data); setError(''); }
      } catch (e) {
        if (active) setError(e instanceof Error ? e.message : 'DATA_UNAVAILABLE');
      }
    };
    load();
    const id = setInterval(load, 15000);
    return () => { active = false; clearInterval(id); };
  }, []);

  return (
    <main style={{maxWidth: 900, margin: '0 auto', padding: 24, fontFamily: 'system-ui'}}>
      <h1>BTCUSDT Adaptive Signal Engine</h1>
      <p>15-minute decision support · paper/research only</p>
      <section style={{border: '1px solid #ccc', borderRadius: 12, padding: 20}}>
        <h2>{state.signal || (error ? 'DATA UNAVAILABLE' : 'LOADING')}</h2>
        <p>Model status: {state.model_status || 'UNKNOWN'}</p>
        <p>Reasons: {(state.reason_codes || []).join(' · ') || '—'}</p>
        <dl>
          <dt>Entry</dt><dd>{state.entry ?? '—'}</dd>
          <dt>Stop</dt><dd>{state.stop_loss ?? '—'}</dd>
          <dt>TP1</dt><dd>{state.tp1 ?? '—'}</dd>
          <dt>TP2</dt><dd>{state.tp2 ?? '—'}</dd>
          <dt>R:R</dt><dd>{state.risk_reward ?? '—'}</dd>
        </dl>
      </section>
    </main>
  );
}

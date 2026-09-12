'use client';

import { useState, useEffect, useRef } from 'react';

interface BatteryStats {
  percent: number;
  plugged: boolean;
  face: string;
  color: string;
  category: string;
  roast: string;
  score: number;
}

interface LogEntry {
  timestamp: string;
  category: string;
  message: string;
}

interface MinecraftFrameProps {
  onToggleDeadScreen: () => void;
}

export default function MinecraftFrame({ onToggleDeadScreen }: MinecraftFrameProps) {
  const [stats, setStats] = useState<BatteryStats | null>(null);
  const [mode, setMode] = useState<'mild' | 'savage' | 'toxic'>('savage');
  const [logs, setLogs] = useState<LogEntry[]>([
    {
      timestamp: new Date().toLocaleTimeString(),
      category: 'SYSTEM',
      message: 'World spawned. Monitoring laptop sensors...',
    },
  ]);
  const [lastRoast, setLastRoast] = useState('');
  const logRef = useRef<HTMLDivElement>(null);

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/stats', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mode }),
      });
      const data: BatteryStats = await response.json();
      setStats(data);

      if (data.roast !== lastRoast) {
        setLastRoast(data.roast);
        const newLog: LogEntry = {
          timestamp: new Date().toLocaleTimeString(),
          category: data.category,
          message: data.roast,
        };
        setLogs((prev) => [...prev, newLog]);
      }
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  useEffect(() => {
    fetchStats();
    const interval = setInterval(fetchStats, 2500);
    return () => clearInterval(interval);
  }, [mode]);

  useEffect(() => {
    if (logRef.current) {
      logRef.current.scrollTop = logRef.current.scrollHeight;
    }
  }, [logs]);

  const simulate = async (percent: number, plugged: boolean) => {
    try {
      await fetch('/api/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ percent, plugged, mode }),
      });
      fetchStats();
    } catch (error) {
      console.error('Simulation failed:', error);
    }
  };

  const reset = async () => {
    try {
      await fetch('/api/reset', { method: 'POST' });
      fetchStats();
    } catch (error) {
      console.error('Reset failed:', error);
    }
  };

  const triggerSpeak = async () => {
    try {
      await fetch('/api/speak', { method: 'POST' });
    } catch (error) {
      console.error('Speak failed:', error);
    }
  };

  const triggerNotify = async () => {
    try {
      await fetch('/api/notify', { method: 'POST' });
    } catch (error) {
      console.error('Notify failed:', error);
    }
  };

  if (!stats) {
    return (
      <div className="mc-frame text-center">
        <div className="pixel-face">...</div>
        <p className="text-gray-700 font-minecraft text-sm">Initializing sensors...</p>
      </div>
    );
  }

  return (
    <div className="mc-frame">
      {/* Header */}
      <div className="flex justify-between items-center mb-4 text-gray-800 text-sm font-minecraft font-bold" style={{ textShadow: '2px 2px white' }}>
        <span>MINECRAFT BATTERY HUD</span>
        <span className={`text-xs ${stats.plugged ? 'text-green-600' : 'text-red-600'}`}>
          {stats.plugged ? '⚡ AC CONNECTED' : '🔋 ON BATTERY'}
        </span>
      </div>

      {/* Face Slot */}
      <div className="mc-slot text-center">
        <div className="pixel-face" style={{ color: stats.color }}>
          {stats.face}
        </div>
        <div className="text-xs text-white font-minecraft" style={{ textShadow: '1px 1px #000' }}>
          DURABILITY: {stats.score}%
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 gap-2.5 mb-3.5">
        <div className="mc-slot text-center">
          <div className="text-xs text-gray-900 font-minecraft mb-1" style={{ textShadow: '1px 1px white' }}>
            REDSTONE CHARGE
          </div>
          <div className="text-xl text-white font-minecraft" style={{ textShadow: '2px 2px #000' }}>
            {stats.percent}%
          </div>
        </div>
        <div className="mc-slot text-center">
          <div className="text-xs text-gray-900 font-minecraft mb-1" style={{ textShadow: '1px 1px white' }}>
            CELL INTEGRITY
          </div>
          <div className="text-xl text-white font-minecraft" style={{ textShadow: '2px 2px #000' }}>
            {stats.score}/100
          </div>
        </div>
      </div>

      {/* Roast Box */}
      <div
        className="bg-gray-900 border-4 border-black p-3.5 mb-3.5 text-minecraft-yellow font-minecraft text-sm leading-relaxed min-h-12"
        style={{ textShadow: '1px 1px #000' }}
      >
        "{stats.roast}"
      </div>

      {/* Log Box */}
      <div
        ref={logRef}
        className="bg-black border-4 border-gray-500 p-2 h-20 overflow-y-auto text-gray-400 font-minecraft text-xs mb-3.5"
        style={{ fontSize: '10px' }}
      >
        {logs.map((log, idx) => (
          <div key={idx}>
            [{log.timestamp}] {log.category}: {log.message}
          </div>
        ))}
      </div>

      {/* Mode Select */}
      <select
        value={mode}
        onChange={(e) => setMode(e.target.value as 'mild' | 'savage' | 'toxic')}
        className="w-full bg-gray-500 border-4 border-gray-700 border-r-white border-b-white text-white p-1.5 font-minecraft text-xs mb-3.5 cursor-pointer"
        style={{ textShadow: '1px 1px #000' }}
      >
        <option value="mild">Difficulty: Peaceful (Gentle Reminders)</option>
        <option value="savage">Difficulty: Hard (Savage Roasts)</option>
        <option value="toxic">Difficulty: Hardcore (Full Creeper Rage)</option>
      </select>

      {/* Simulation Buttons */}
      <div className="grid grid-cols-4 gap-1.5 mb-2.5">
        <button className="mc-btn" onClick={() => simulate(100, true)}>
          100% Cook
        </button>
        <button className="mc-btn" onClick={() => simulate(85, true)}>
          85% Stress
        </button>
        <button className="mc-btn" onClick={() => simulate(4, false)}>
          4% Panic
        </button>
        <button className="mc-btn" onClick={reset}>
          Live Real
        </button>
      </div>

      {/* Action Buttons */}
      <div className="grid grid-cols-2 gap-2">
        <button
          className="mc-btn bg-blue-900 hover:bg-blue-800"
          onClick={triggerSpeak}
          title="Text-to-speech (requires local environment)"
        >
          🔊 Say Roast
        </button>
        <button
          className="mc-btn bg-red-700 hover:bg-red-800"
          onClick={triggerNotify}
          title="Desktop notification (requires local environment)"
        >
          Trigger Popup
        </button>
        <button
          className="mc-btn col-span-2 bg-gray-900 text-red-400 border-red-500 hover:bg-gray-800"
          onClick={onToggleDeadScreen}
        >
          ⚠️ Toggle Screen Error (Blind Mode)
        </button>
      </div>
    </div>
  );
}

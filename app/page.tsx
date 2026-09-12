'use client';

import { useEffect, useState } from 'react';
import MinecraftFrame from '@/components/MinecraftFrame';

export default function Home() {
  const [isDeadScreen, setIsDeadScreen] = useState(false);

  return (
    <>
      {isDeadScreen && (
        <div
          onClick={() => setIsDeadScreen(false)}
          className="fixed inset-0 bg-minecraft-dred bg-opacity-95 z-50 flex flex-col items-center justify-center text-white text-center cursor-pointer"
        >
          <div className="text-6xl mb-4 font-minecraft text-red-400" style={{ textShadow: '4px 4px #000' }}>
            ☠ DISPLAY BLINDNESS ☠
          </div>
          <div className="text-2xl mb-6 font-minecraft text-minecraft-yellow" style={{ textShadow: '2px 2px #000' }}>
            BATTERY HARDWARE FAILURE // SCREEN DESTROYED
          </div>
          <div
            className="text-base leading-8 max-w-2xl mb-8 font-minecraft"
            style={{ textShadow: '2px 2px #000' }}
          >
            ALL SYSTEM STATUS METRICS ARE HIDDEN & INACCESSIBLE.
            <br />
            CANNOT READ OS TRAY OR PERCENTAGE LEVELS.
            <br />
            ONLY EMERGENCY AUDIO SYNTHESIS IS ACTIVE.
          </div>
          <button className="mc-btn bg-gray-500">[ CLICK ANYWHERE TO RESTORE HUD ]</button>
        </div>
      )}

      <MinecraftFrame onToggleDeadScreen={() => setIsDeadScreen(!isDeadScreen)} />
    </>
  );
}

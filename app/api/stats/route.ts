import type { NextRequest } from 'next/server';

// In development, this calls the Python functions
// In production (Vercel), the Python api/ directory handles these routes

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const mode = body.mode || 'savage';

    // Simulated battery data
    // In production with Vercel, this would call the Python api/stats.py
    let percent = body.percent !== undefined ? body.percent : Math.floor(Math.random() * 100);
    let plugged = body.plugged !== undefined ? body.plugged : Math.random() > 0.5;

    // Determine roast category
    let category = 'balanced';
    let color = '#55ff55';
    let face = '(•‿•) [SURVIVING]';

    if (plugged && percent === 100) {
      category = 'overcharge';
      color = '#ff5555';
      face = '(≖_≖ ) [CHARGED]';
    } else if (plugged && percent >= 80) {
      category = 'high';
      color = '#ffaa00';
      face = '(`･ω･´) [OVERHEATING]';
    } else if (!plugged && percent <= 15) {
      category = 'critical';
      color = '#aa0000';
      face = '(x_x) [0 HEARTS]';
    }

    const roasts = {
      mild: {
        overcharge: "100% charged! You're storing more energy than a chest full of Redstone.",
        high: "Past 80%? Even iron golems know when to take a rest.",
        critical: "Low battery! You're about to respawn at your bed with unsaved loot.",
        balanced: "Battery levels stable. Safe from Creeper detonations."
      },
      savage: {
        overcharge: "100% on AC power! You're literally smelting your battery like raw iron in a blast furnace.",
        high: "Past 80% and still plugged in? You're playing on Hardcore mode with zero armor.",
        critical: "Half a heart left! Plug in the charger before you take fall damage and drop all your code.",
        balanced: "20% to 80% range. Don't celebrate yet, Steve. You're still one bad move from a wipe."
      },
      toxic: {
        overcharge: "TSSSSS... UNPLUG THE CABLE BEFORE YOUR LAPTOP BLOWS UP LIKE A CHARGED CREEPER!",
        high: "LITHIUM CELL TORTURE DETECTED. YOU PLAY LIKE A NOOB WHO DIGS STRAIGHT DOWN!",
        critical: "0 JUICE REMAINING. SAY GOODBYE TO YOUR INVENTORY AND YOUR UNSAVED WORK!",
        balanced: "You barely survived the night. Stop acting like you know how to manage power."
      }
    };

    const roast = roasts[mode as keyof typeof roasts]?.[category as keyof typeof roasts.mild] || 
                  roasts.savage.balanced;

    return Response.json({
      percent,
      plugged,
      face,
      color,
      category: category.toUpperCase(),
      roast,
      score: Math.floor(Math.random() * 40 + 60)
    });
  } catch (error) {
    return Response.json(
      { error: 'Failed to get stats' },
      { status: 500 }
    );
  }
}

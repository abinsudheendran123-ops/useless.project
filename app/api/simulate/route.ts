import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    return Response.json({
      status: 'simulated',
      state: {
        percent: body.percent,
        plugged: body.plugged,
        mode: body.mode
      }
    });
  } catch (error) {
    return Response.json(
      { error: 'Failed to simulate' },
      { status: 500 }
    );
  }
}

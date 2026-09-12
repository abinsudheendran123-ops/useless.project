import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    return Response.json({ status: 'reset' });
  } catch (error) {
    return Response.json(
      { error: 'Failed to reset' },
      { status: 500 }
    );
  }
}

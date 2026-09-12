import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Desktop notifications only work in local development with plyer installed
    // On Vercel, this will return a skipped status
    return Response.json({
      status: 'skipped',
      message: 'Desktop notifications not available. Install plyer locally for full features.'
    });
  } catch (error) {
    return Response.json(
      { error: 'Failed to notify' },
      { status: 500 }
    );
  }
}

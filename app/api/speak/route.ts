import type { NextRequest } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Text-to-speech only works in local development with pyttsx3 installed
    // On Vercel, this will return a skipped status
    return Response.json({
      status: 'skipped',
      message: 'Text-to-speech not available. Install pyttsx3 locally for full features.'
    });
  } catch (error) {
    return Response.json(
      { error: 'Failed to speak' },
      { status: 500 }
    );
  }
}

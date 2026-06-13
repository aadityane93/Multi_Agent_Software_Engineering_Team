import type { CreateRunPayload, Run } from '../types/run'

const API_BASE_URL = 'http://localhost:8000'

async function parseRunResponse(res: Response): Promise<Run> {
  if (!res.ok) {
    throw new Error(await res.text())
  }

  return res.json() as Promise<Run>
}

export async function createRun(payload: CreateRunPayload): Promise<Run> {
  const res = await fetch(`${API_BASE_URL}/runs`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      accept: 'application/json',
    },
    body: JSON.stringify(payload),
  })

  return parseRunResponse(res)
}

export async function getRun(runId: string): Promise<Run> {
  const res = await fetch(`${API_BASE_URL}/runs/${runId}`, {
    headers: {
      accept: 'application/json',
    },
  })

  return parseRunResponse(res)
}

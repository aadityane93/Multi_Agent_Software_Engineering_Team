export type RunStatus =
  | 'planning'
  | 'awaiting_approval'
  | 'implementing'
  | 'completed'
  | 'rejected'
  | 'failed'
  | 'unknown'
  | string

export type AgentArtifact = {
  name: string
  content: string
}

export type Run = {
  run_id: string
  status: RunStatus
  product_idea: string
  artifacts: AgentArtifact[]
}

export type CreateRunPayload = {
  title: string
  description: string
}

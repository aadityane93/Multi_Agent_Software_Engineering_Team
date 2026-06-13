import type { Run } from '../types/run'

type RunStatusCardProps = {
  run: Run | null
  loading: boolean
}

const statusMessages: Record<string, string> = {
  started: 'Run accepted by the backend.',
  requirements_done: 'Requirements artifact is ready.',
  awaiting_approval: 'Planning is complete and awaiting backend approval.',
  approved: 'Implementation agents are starting.',
  backend_done: 'Backend plan is ready.',
  frontend_done: 'Frontend plan is ready.',
  tests_done: 'Test plan is ready.',
  docs_done: 'Documentation is ready.',
  completed: 'All artifacts are ready.',
  rejected: 'Run was rejected.',
  failed: 'Run failed.',
}

function getStatusLabel(status: string) {
  return status.replaceAll('_', ' ')
}

function getStatusTone(status: string) {
  if (status === 'completed') {
    return 'is-success'
  }

  if (status === 'failed' || status === 'rejected') {
    return 'is-danger'
  }

  if (status === 'awaiting_approval') {
    return 'is-warning'
  }

  return 'is-active'
}

export function RunStatusCard({ run, loading }: RunStatusCardProps) {
  const status = run?.status ?? (loading ? 'starting' : 'idle')
  const artifactCount = run?.artifacts.length ?? 0
  const message =
    run && statusMessages[run.status]
      ? statusMessages[run.status]
      : loading
        ? 'Creating run...'
        : 'Ready.'

  return (
    <section className="status-panel" aria-label="Run status">
      <div className="status-panel__topline">
        <p className="eyebrow">Status</p>
        <span className={`status-badge ${getStatusTone(status)}`}>{getStatusLabel(status)}</span>
      </div>

      <dl className="status-grid">
        <div>
          <dt>Run ID</dt>
          <dd>{run?.run_id ?? 'Not started'}</dd>
        </div>
        <div>
          <dt>Artifacts</dt>
          <dd>{artifactCount}</dd>
        </div>
      </dl>

      <p className="progress-message">{message}</p>
    </section>
  )
}

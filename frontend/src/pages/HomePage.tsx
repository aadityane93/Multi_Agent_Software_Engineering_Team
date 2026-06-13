import { useEffect, useMemo, useState } from 'react'
import { createRun, getRun } from '../api/runsApi'
import { ArtifactList } from '../components/ArtifactList'
import { ArtifactViewer } from '../components/ArtifactViewer'
import { RunForm } from '../components/RunForm'
import { RunStatusCard } from '../components/RunStatusCard'
import type { AgentArtifact, CreateRunPayload, Run } from '../types/run'

const POLL_INTERVAL_MS = 2500
const terminalStatuses = new Set(['awaiting_approval', 'completed', 'failed', 'rejected'])

function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    return error.message
  }

  return 'Something went wrong.'
}

function getFirstArtifact(run: Run | null) {
  return run?.artifacts[0] ?? null
}

export function HomePage() {
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [run, setRun] = useState<Run | null>(null)
  const [selectedArtifact, setSelectedArtifact] = useState<AgentArtifact | null>(null)

  async function handleSubmit(payload: CreateRunPayload) {
    setLoading(true)
    setError(null)

    try {
      const createdRun = await createRun(payload)
      setRun(createdRun)
      setSelectedArtifact(getFirstArtifact(createdRun))
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (!run?.run_id || terminalStatuses.has(run.status)) {
      return
    }

    let cancelled = false

    const intervalId = window.setInterval(async () => {
      try {
        const nextRun = await getRun(run.run_id)

        if (cancelled) {
          return
        }

        setRun(nextRun)
        setSelectedArtifact((currentArtifact) => {
          if (currentArtifact && nextRun.artifacts.some((artifact) => artifact.name === currentArtifact.name)) {
            return currentArtifact
          }

          return getFirstArtifact(nextRun)
        })
      } catch (err) {
        if (!cancelled) {
          setError(getErrorMessage(err))
        }
      }
    }, POLL_INTERVAL_MS)

    return () => {
      cancelled = true
      window.clearInterval(intervalId)
    }
  }, [run?.run_id, run?.status])

  const selectedArtifactName = selectedArtifact?.name ?? null
  const selectedArtifactForRun = useMemo(() => {
    if (!run || !selectedArtifactName) {
      return getFirstArtifact(run)
    }

    return run.artifacts.find((artifact) => artifact.name === selectedArtifactName) ?? getFirstArtifact(run)
  }, [run, selectedArtifactName])

  return (
    <main className="app-shell">
      <section className="top-grid">
        <RunForm
          title={title}
          description={description}
          loading={loading}
          onTitleChange={setTitle}
          onDescriptionChange={setDescription}
          onSubmit={handleSubmit}
        />
        <RunStatusCard run={run} loading={loading} />
      </section>

      {error ? (
        <div className="error-banner" role="alert">
          {error}
        </div>
      ) : null}

      <section className="workspace-grid">
        <ArtifactList
          artifacts={run?.artifacts ?? []}
          selectedArtifactName={selectedArtifactForRun?.name ?? null}
          onSelect={setSelectedArtifact}
        />
        <ArtifactViewer artifact={selectedArtifactForRun} />
      </section>
    </main>
  )
}

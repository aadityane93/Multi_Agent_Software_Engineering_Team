import type { AgentArtifact } from '../types/run'

type ArtifactViewerProps = {
  artifact: AgentArtifact | null
}

export function ArtifactViewer({ artifact }: ArtifactViewerProps) {
  if (!artifact) {
    return (
      <section className="artifact-viewer artifact-viewer--empty" aria-label="Artifact viewer">
        <p>No artifact selected.</p>
      </section>
    )
  }

  return (
    <section className="artifact-viewer" aria-label={`${artifact.name} artifact`}>
      <header className="artifact-viewer__header">
        <p className="eyebrow">Selected artifact</p>
        <h2>{artifact.name}</h2>
      </header>

      <pre>{artifact.content}</pre>
    </section>
  )
}

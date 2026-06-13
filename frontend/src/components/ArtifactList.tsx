import type { AgentArtifact } from '../types/run'

type ArtifactListProps = {
  artifacts: AgentArtifact[]
  selectedArtifactName: string | null
  onSelect: (artifact: AgentArtifact) => void
}

const artifactOrder = [
  {
    key: 'requirements',
    label: 'Requirements',
    names: ['Requirements'],
  },
  {
    key: 'architecture',
    label: 'Architecture',
    names: ['Architecture'],
  },
  {
    key: 'backend-plan',
    label: 'Backend plan',
    names: ['Backend Code', 'Backend Plan', 'Backend'],
  },
  {
    key: 'frontend-plan',
    label: 'Frontend plan',
    names: ['Frontend Code', 'Frontend Plan', 'Frontend'],
  },
  {
    key: 'tests',
    label: 'Tests',
    names: ['Tests'],
  },
  {
    key: 'docs',
    label: 'Docs',
    names: ['Documentation', 'Docs'],
  },
  {
    key: 'review',
    label: 'Review',
    names: ['Review Report', 'Review'],
  },
] as const

function findArtifact(artifacts: AgentArtifact[], names: readonly string[]) {
  return artifacts.find((artifact) => names.includes(artifact.name))
}

export function ArtifactList({ artifacts, selectedArtifactName, onSelect }: ArtifactListProps) {
  const orderedRows = artifactOrder.map((definition) => ({
    ...definition,
    artifact: findArtifact(artifacts, definition.names),
  }))

  const orderedNames = new Set<string>(artifactOrder.flatMap((definition) => definition.names))
  const extraArtifacts = artifacts.filter((artifact) => !orderedNames.has(artifact.name))

  return (
    <aside className="artifact-list" aria-label="Generated artifacts">
      <div className="artifact-list__header">
        <p className="eyebrow">Artifacts</p>
        <span>{artifacts.length}/7</span>
      </div>

      <div className="artifact-list__items">
        {orderedRows.map(({ key, label, artifact }) => {
          const isSelected = artifact?.name === selectedArtifactName

          return (
            <button
              className={`artifact-row ${isSelected ? 'is-selected' : ''}`}
              disabled={!artifact}
              key={key}
              type="button"
              onClick={() => artifact && onSelect(artifact)}
            >
              <span>{label}</span>
              <small>{artifact ? 'Ready' : 'Pending'}</small>
            </button>
          )
        })}

        {extraArtifacts.map((artifact) => (
          <button
            className={`artifact-row ${
              artifact.name === selectedArtifactName ? 'is-selected' : ''
            }`}
            key={artifact.name}
            type="button"
            onClick={() => onSelect(artifact)}
          >
            <span>{artifact.name}</span>
            <small>Ready</small>
          </button>
        ))}
      </div>
    </aside>
  )
}

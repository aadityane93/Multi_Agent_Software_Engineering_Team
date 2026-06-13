import type { FormEvent } from 'react'
import type { CreateRunPayload } from '../types/run'

type RunFormProps = {
  title: string
  description: string
  loading: boolean
  onTitleChange: (title: string) => void
  onDescriptionChange: (description: string) => void
  onSubmit: (payload: CreateRunPayload) => void
}

export function RunForm({
  title,
  description,
  loading,
  onTitleChange,
  onDescriptionChange,
  onSubmit,
}: RunFormProps) {
  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    onSubmit({
      title: title.trim(),
      description: description.trim(),
    })
  }

  const canSubmit = title.trim().length >= 3 && description.trim().length >= 10

  return (
    <form className="run-form" onSubmit={handleSubmit}>
      <div className="section-heading">
        <p className="eyebrow">New run</p>
        <h1>Multi-agent run console</h1>
      </div>

      <label className="field">
        <span>Title</span>
        <input
          type="text"
          value={title}
          minLength={3}
          required
          placeholder="Inventory planning assistant"
          onChange={(event) => onTitleChange(event.target.value)}
        />
      </label>

      <label className="field">
        <span>Description</span>
        <textarea
          value={description}
          minLength={10}
          required
          rows={7}
          placeholder="A lightweight tool that helps small shops forecast demand, plan purchases, and review stock risks."
          onChange={(event) => onDescriptionChange(event.target.value)}
        />
      </label>

      <button className="primary-button" type="submit" disabled={loading || !canSubmit}>
        {loading ? 'Starting run...' : 'Start run'}
      </button>
    </form>
  )
}

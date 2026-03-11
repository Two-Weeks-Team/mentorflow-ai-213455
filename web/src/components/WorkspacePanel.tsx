"use client";

type WorkspacePanelProps = {
  query: string;
  preferences: string;
  onQueryChange: (value: string) => void;
  onPreferencesChange: (value: string) => void;
  onGenerate: () => void;
  loading: boolean;
  features: string[];
};

export default function WorkspacePanel({
  query,
  preferences,
  onQueryChange,
  onPreferencesChange,
  onGenerate,
  loading,
  features,
}: WorkspacePanelProps) {
  return (
    <section className="workspace-panel">
      <span className="eyebrow">Primary Workspace</span>
      <div className="controls">
        <textarea value={query} onChange={(event) => onQueryChange(event.target.value)} placeholder="Describe the session you want to generate." />
        <textarea value={preferences} onChange={(event) => onPreferencesChange(event.target.value)} placeholder="Add constraints, style cues, or priorities." />
        <div className="button-row">
          <button className="primary-button" onClick={onGenerate} disabled={loading}>
            {loading ? "Generating..." : "Generate showcase plan"}
          </button>
        </div>
      </div>
      <div className="feature-chips">
        {features.map((feature) => (
          <span className="feature-chip" key={feature}>{feature}</span>
        ))}
      </div>
    </section>
  );
}

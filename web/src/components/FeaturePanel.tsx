type FeaturePanelProps = {
  features: string[];
  proofPoints: string[];
};

export default function FeaturePanel({ features, proofPoints }: FeaturePanelProps) {
  return (
    <section className="feature-panel">
      <span className="eyebrow">Secondary Supporting Panel</span>
      <h2>Demo talking points</h2>
      <ul className="feature-list">
        {features.concat(proofPoints).map((entry) => (
          <li key={entry}>{entry}</li>
        ))}
      </ul>
    </section>
  );
}

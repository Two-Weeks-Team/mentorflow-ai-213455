type SavedPlan = {
  summary: string;
  score: number;
  items: Array<{ title: string; detail: string; score: number }>;
};

export default function CollectionPanel({ saved }: { saved: SavedPlan[] }) {
  return (
    <section className="collection-panel">
      <div className="section-heading">
        <span className="eyebrow">Saved Library and Recent Activity</span>
        <h2>Outputs stay visible for a live walkthrough.</h2>
      </div>
      <div className="saved-grid">
        {saved.length ? (
          saved.map((entry, index) => (
            <article className="saved-card" key={`${entry.summary}-${index}`}>
              <span className="saved-score">Score {entry.score}</span>
              <h3>{entry.summary}</h3>
              <ul>
                {entry.items.slice(0, 2).map((item) => (
                  <li key={item.title}>{item.title}</li>
                ))}
              </ul>
            </article>
          ))
        ) : (
          <article className="saved-card">
            <span className="saved-score">Empty state</span>
            <h3>Generate the first output</h3>
            <p>The saved library and recent activity surface will fill after the first successful run.</p>
          </article>
        )}
      </div>
    </section>
  );
}

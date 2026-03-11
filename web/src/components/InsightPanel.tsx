type PlanPayload = {
  summary: string;
  score: number;
  items: Array<{ title: string; detail: string; score: number }>;
  insights?: { insights: string[]; next_actions: string[]; highlights: string[] };
};

export default function InsightPanel({ plan }: { plan: PlanPayload }) {
  return (
    <section className="insight-panel">
      <span className="eyebrow">Insight or Result Panel</span>
      <span className="score-pill">Readiness score {plan.score}</span>
      <h2>{plan.summary}</h2>
      {plan.items.map((item) => (
        <article className="item-card" key={item.title}>
          <h3>{item.title}</h3>
          <p>{item.detail}</p>
        </article>
      ))}
      {plan.insights ? (
        <ul className="insight-list">
          {plan.insights.highlights.concat(plan.insights.next_actions).map((entry) => (
            <li key={entry}>{entry}</li>
          ))}
        </ul>
      ) : null}
    </section>
  );
}

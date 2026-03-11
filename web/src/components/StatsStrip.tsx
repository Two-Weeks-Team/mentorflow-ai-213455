type StatsStripProps = {
  stats: Array<{ label: string; value: string }>;
};

export default function StatsStrip({ stats }: StatsStripProps) {
  return (
    <section className="stats-strip">
      {stats.map((stat) => (
        <article className="stat-chip" key={stat.label}>
          <span className="eyebrow">{stat.label}</span>
          <strong>{stat.value}</strong>
        </article>
      ))}
    </section>
  );
}

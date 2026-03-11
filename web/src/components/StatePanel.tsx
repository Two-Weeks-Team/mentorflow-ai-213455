export default function StatePanel({
  title,
  detail,
  tone,
}: {
  title: string;
  detail: string;
  tone: "neutral" | "error";
}) {
  return (
    <section className="status-panel">
      <span className="eyebrow">{tone === "error" ? "Attention" : "Ready"}</span>
      <h2>{title}</h2>
      <p>{detail}</p>
    </section>
  );
}

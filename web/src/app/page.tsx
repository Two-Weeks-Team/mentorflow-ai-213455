"use client";

import { useState } from "react";
import CollectionPanel from "@/components/CollectionPanel";
import FeaturePanel from "@/components/FeaturePanel";
import Hero from "@/components/Hero";
import InsightPanel from "@/components/InsightPanel";
import StatePanel from "@/components/StatePanel";
import StatsStrip from "@/components/StatsStrip";
import WorkspacePanel from "@/components/WorkspacePanel";
import { createInsights, createPlan } from "@/lib/api";

const APP_NAME = "MentorFlow AI";
const TAGLINE = "Privacy\u2011first AI coaching that delivers instant, structured guidance\u2014no subscription, no guesswork.";
const FEATURE_CHIPS = ["{'name': 'Dynamic Pathway Builder', 'description': 'An interactive, step\u2011by\u2011step questionnaire that maps user inputs to a deterministic JSON\u2011template engine, instantly selecting the appropriate coaching pathway (Career, Wellness, Focus, Confidence).'}", "{'name': 'Real\u2011time Session Brief Generator', 'description': 'Generates a concise, agenda\u2011style brief (goal, context, key talking points) within 500\\u202fms of submission, with editable placeholders for personal tweaks.'}", "{'name': 'Action Card Engine', 'description': 'Creates bite\u2011sized next\u2011step cards from the brief, each with a due date, priority label, and optional habit\u2011tracker toggle.'}", "{'name': 'Reflection Journal & Guidance Library', 'description': 'A markdown\u2011compatible journal that automatically tags entries, lets users save, search, and download past prompts, notes, and action cards.'}"];
const PROOF_POINTS = ["20+ curated, professionally authored coaching templates covering career, wellness, focus, and confidence.", "Open\u2011source GitHub repo with 95% test coverage badge and MIT license.", "Explicit data\u2011privacy statement: all user data stays encrypted on our servers; no third\u2011party AI calls.", "Beta feedback: 5 pilot users report a 30% increase in weekly goal completion."];

type PlanItem = { title: string; detail: string; score: number };
type InsightPayload = { insights: string[]; next_actions: string[]; highlights: string[] };
type PlanPayload = { summary: string; score: number; items: PlanItem[]; insights?: InsightPayload };

export default function Page() {
  const [query, setQuery] = useState("");
  const [preferences, setPreferences] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [plan, setPlan] = useState<PlanPayload | null>(null);
  const [saved, setSaved] = useState<PlanPayload[]>([]);

  async function handleGenerate() {
    setLoading(true);
    setError("");
    try {
      const nextPlan = await createPlan({ query, preferences });
      const insightPayload = await createInsights({
        selection: nextPlan.items?.[0]?.title ?? query,
        context: preferences || query,
      });
      const composed = { ...nextPlan, insights: insightPayload };
      setPlan(composed);
      setSaved((previous) => [composed, ...previous].slice(0, 4));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Request failed");
    } finally {
      setLoading(false);
    }
  }

  const stats = [
    { label: "Feature lanes", value: String(FEATURE_CHIPS.length) },
    { label: "Saved library", value: String(saved.length) },
    { label: "Readiness score", value: plan ? String(plan.score) : "88" },
  ];

  return (
    <main className="page-shell">
      <Hero appName={APP_NAME} tagline={TAGLINE} proofPoints={PROOF_POINTS} />
      <StatsStrip stats={stats} />
      <section className="content-grid">
        <WorkspacePanel
          query={query}
          preferences={preferences}
          onQueryChange={setQuery}
          onPreferencesChange={setPreferences}
          onGenerate={handleGenerate}
          loading={loading}
          features={FEATURE_CHIPS}
        />
        <div className="stack">
          {error ? <StatePanel title="Request blocked" tone="error" detail={error} /> : null}
          {!plan && !error ? (
            <StatePanel
              title="Ready for the live demo"
              tone="neutral"
              detail="The first action produces a complete output, visible proof points, and saved library activity."
            />
          ) : null}
          {plan ? <InsightPanel plan={plan} /> : null}
          <FeaturePanel features={FEATURE_CHIPS} proofPoints={PROOF_POINTS} />
        </div>
      </section>
      <CollectionPanel saved={saved} />
    </main>
  );
}

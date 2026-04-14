"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { DiagnosticResult } from "@/types";
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from "recharts";

const GRADE_LEVELS = [
  { value: "6ano", label: "6º Ano" },
  { value: "7ano", label: "7º Ano" },
  { value: "8ano", label: "8º Ano" },
  { value: "9ano", label: "9º Ano" },
  { value: "1em", label: "1ª Série EM" },
  { value: "2em", label: "2ª Série EM" },
  { value: "3em", label: "3ª Série EM" },
  { value: "vestibular", label: "Vestibulando" },
  { value: "concurso", label: "Concurseiro" },
];

const LEVEL_COLORS: Record<string, string> = {
  abaixo_basico: "text-red-600 bg-red-50",
  basico: "text-yellow-700 bg-yellow-50",
  adequado: "text-green-700 bg-green-50",
  avancado: "text-brand-700 bg-brand-50",
};

export default function DiagnosticPage() {
  const [diagnostics, setDiagnostics] = useState<DiagnosticResult[]>([]);
  const [selected, setSelected] = useState<DiagnosticResult | null>(null);
  const [gradeLevel, setGradeLevel] = useState("6ano");
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    api.get("/diagnostics/").then((r) => {
      setDiagnostics(r.data);
      const completed = r.data.filter((d: DiagnosticResult) => d.status === "concluido");
      if (completed.length > 0) setSelected(completed[completed.length - 1]);
    });
  }, []);

  async function startDiagnostic() {
    setStarting(true);
    try {
      const res = await api.post("/diagnostics/start", { grade_level: gradeLevel });
      alert(`Diagnóstico iniciado! ID: ${res.data.id}\n\nResponda os exercícios e volte para completar.`);
    } finally {
      setStarting(false);
    }
  }

  const radarData = selected
    ? Object.entries(selected.scores).map(([topic, data]) => ({
        topic: topic.replace(/_/g, " ").slice(0, 15),
        score: data.score,
      }))
    : [];

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Diagnóstico</h1>
      <p className="text-slate-500 mb-8">Identifique suas defasagens com precisão</p>

      {!selected ? (
        <div className="bg-white rounded-2xl border border-slate-100 p-8 text-center max-w-md mx-auto">
          <div className="text-5xl mb-4">🎯</div>
          <h2 className="text-2xl font-bold text-slate-800 mb-2">Iniciar diagnóstico</h2>
          <p className="text-slate-500 mb-6">
            Responda exercícios calibrados e receba um relatório completo das suas defasagens.
          </p>
          <div className="mb-4">
            <label className="block text-sm font-medium text-slate-700 mb-2">Sua série</label>
            <select
              value={gradeLevel}
              onChange={(e) => setGradeLevel(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-brand-500"
            >
              {GRADE_LEVELS.map((g) => (
                <option key={g.value} value={g.value}>{g.label}</option>
              ))}
            </select>
          </div>
          <button
            onClick={startDiagnostic}
            disabled={starting}
            className="w-full bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 rounded-xl transition disabled:opacity-50"
          >
            {starting ? "Iniciando..." : "Começar diagnóstico"}
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Overview */}
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: "Nota geral", value: `${selected.overall_score?.toFixed(1)}%` },
              { label: "Nível", value: selected.overall_level?.replace(/_/g, " ") ?? "-" },
              { label: "Questões", value: `${selected.correct_answers}/${selected.total_questions}` },
            ].map((s) => (
              <div key={s.label} className="bg-white rounded-2xl border border-slate-100 p-5 text-center">
                <p className="text-3xl font-bold text-slate-800">{s.value}</p>
                <p className="text-sm text-slate-400 mt-1">{s.label}</p>
              </div>
            ))}
          </div>

          {/* Radar */}
          {radarData.length > 0 && (
            <div className="bg-white rounded-2xl border border-slate-100 p-6">
              <h2 className="text-lg font-bold text-slate-800 mb-4">Desempenho por tópico</h2>
              <ResponsiveContainer width="100%" height={280}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="topic" tick={{ fontSize: 11 }} />
                  <Radar dataKey="score" stroke="#2563eb" fill="#2563eb" fillOpacity={0.2} />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          )}

          {/* Gaps */}
          {selected.gaps.length > 0 && (
            <div className="bg-white rounded-2xl border border-slate-100 p-6">
              <h2 className="text-lg font-bold text-slate-800 mb-4">Defasagens identificadas</h2>
              <div className="space-y-3">
                {selected.gaps.map((gap) => (
                  <div key={gap.topic} className="flex items-center justify-between p-4 rounded-xl bg-slate-50">
                    <div>
                      <p className="font-medium text-slate-800 capitalize">
                        {gap.topic.replace(/_/g, " ")}
                      </p>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium mt-1 inline-block ${LEVEL_COLORS[gap.level] || "bg-slate-100 text-slate-600"}`}>
                        {gap.level.replace(/_/g, " ")}
                      </span>
                    </div>
                    <div className="text-right">
                      <p className="text-2xl font-bold text-slate-800">{gap.score.toFixed(0)}%</p>
                      <p className="text-xs text-slate-400">Prioridade {gap.priority}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Learning path */}
          {selected.learning_path.length > 0 && (
            <div className="bg-white rounded-2xl border border-slate-100 p-6">
              <h2 className="text-lg font-bold text-slate-800 mb-4">Plano de estudos personalizado</h2>
              <div className="space-y-3">
                {selected.learning_path.map((item, i) => (
                  <div key={i} className="flex items-center gap-4 p-4 rounded-xl border border-slate-100">
                    <div className="w-8 h-8 rounded-full bg-brand-600 text-white flex items-center justify-center font-bold text-sm flex-shrink-0">
                      {i + 1}
                    </div>
                    <div className="flex-1">
                      <p className="font-medium text-slate-800 capitalize">{item.topic.replace(/_/g, " ")}</p>
                      <p className="text-xs text-slate-400">{item.estimated_hours}h estimadas</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          <button
            onClick={() => setSelected(null)}
            className="border border-brand-500 text-brand-600 font-medium px-6 py-2 rounded-xl hover:bg-brand-50 transition text-sm"
          >
            Novo diagnóstico
          </button>
        </div>
      )}
    </div>
  );
}

"use client";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import type { Exercise, ExerciseAttemptResponse } from "@/types";
import { CheckCircle, XCircle, Clock } from "lucide-react";

const TOPICS = [
  { value: "", label: "Todos os tópicos" },
  { value: "numeros_e_operacoes", label: "Números e Operações" },
  { value: "algebra", label: "Álgebra" },
  { value: "geometria", label: "Geometria" },
  { value: "estatistica_e_probabilidade", label: "Estatística e Probabilidade" },
  { value: "grandezas_e_medidas", label: "Grandezas e Medidas" },
  { value: "raciocinio_logico", label: "Raciocínio Lógico" },
];

const DIFFICULTIES = [
  { value: "", label: "Todas as dificuldades" },
  { value: "abaixo_basico", label: "Abaixo do Básico" },
  { value: "basico", label: "Básico" },
  { value: "adequado", label: "Adequado" },
  { value: "avancado", label: "Avançado" },
];

const DIFFICULTY_COLORS: Record<string, string> = {
  abaixo_basico: "bg-red-100 text-red-700",
  basico: "bg-yellow-100 text-yellow-700",
  adequado: "bg-green-100 text-green-700",
  avancado: "bg-brand-100 text-brand-700",
};

export default function ExercisesPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [current, setCurrent] = useState<Exercise | null>(null);
  const [selectedAnswer, setSelectedAnswer] = useState("");
  const [result, setResult] = useState<ExerciseAttemptResponse | null>(null);
  const [topic, setTopic] = useState("");
  const [difficulty, setDifficulty] = useState("");
  const [loading, setLoading] = useState(false);
  const [startTime, setStartTime] = useState<number | null>(null);

  useEffect(() => {
    loadExercises();
  }, [topic, difficulty]);

  async function loadExercises() {
    const params: Record<string, string> = {};
    if (topic) params.topic = topic;
    if (difficulty) params.difficulty = difficulty;
    const res = await api.get("/exercises/", { params });
    setExercises(res.data);
    setCurrent(null);
    setResult(null);
  }

  function startExercise(ex: Exercise) {
    setCurrent(ex);
    setSelectedAnswer("");
    setResult(null);
    setStartTime(Date.now());
  }

  async function submitAnswer() {
    if (!current || !selectedAnswer) return;
    setLoading(true);
    const timeSpent = startTime ? Math.floor((Date.now() - startTime) / 1000) : undefined;
    try {
      const res = await api.post("/exercises/attempt", {
        exercise_id: current.id,
        answer: selectedAnswer,
        time_spent_seconds: timeSpent,
      });
      setResult(res.data);
    } finally {
      setLoading(false);
    }
  }

  if (current) {
    return (
      <div className="max-w-2xl mx-auto">
        <button
          onClick={() => setCurrent(null)}
          className="text-slate-400 hover:text-slate-600 text-sm mb-6 flex items-center gap-1"
        >
          ← Voltar para lista
        </button>

        <div className="bg-white rounded-2xl border border-slate-100 p-8">
          <div className="flex items-center gap-2 mb-6">
            <span className={`text-xs px-3 py-1 rounded-full font-medium ${DIFFICULTY_COLORS[current.difficulty]}`}>
              {current.difficulty.replace(/_/g, " ")}
            </span>
            <span className="text-xs text-slate-400">{current.exam_source}</span>
          </div>

          <p className="text-lg text-slate-800 leading-relaxed mb-8">{current.statement}</p>

          {current.options && (
            <div className="space-y-3 mb-8">
              {current.options.map((opt) => (
                <button
                  key={opt.id}
                  onClick={() => !result && setSelectedAnswer(opt.id)}
                  disabled={!!result}
                  className={`w-full text-left px-5 py-4 rounded-xl border-2 transition font-medium ${
                    result
                      ? opt.id === result.correct_answer
                        ? "border-green-500 bg-green-50 text-green-800"
                        : opt.id === selectedAnswer && !result.is_correct
                        ? "border-red-400 bg-red-50 text-red-800"
                        : "border-slate-100 text-slate-500"
                      : selectedAnswer === opt.id
                      ? "border-brand-500 bg-brand-50 text-brand-800"
                      : "border-slate-200 hover:border-brand-300"
                  }`}
                >
                  <span className="font-bold mr-3">{opt.id.toUpperCase()}.</span>
                  {opt.text}
                </button>
              ))}
            </div>
          )}

          {!result ? (
            <button
              onClick={submitAnswer}
              disabled={!selectedAnswer || loading}
              className="w-full bg-brand-600 hover:bg-brand-700 text-white font-bold py-3 rounded-xl transition disabled:opacity-50"
            >
              {loading ? "Enviando..." : "Confirmar resposta"}
            </button>
          ) : (
            <div>
              <div className={`flex items-center gap-3 p-4 rounded-xl mb-4 ${result.is_correct ? "bg-green-50 text-green-800" : "bg-red-50 text-red-800"}`}>
                {result.is_correct ? <CheckCircle size={20} /> : <XCircle size={20} />}
                <span className="font-bold">
                  {result.is_correct ? `Correto! +${result.xp_earned} XP` : "Resposta incorreta"}
                </span>
              </div>
              {result.explanation && (
                <p className="text-slate-600 text-sm mb-4 bg-slate-50 p-4 rounded-xl">{result.explanation}</p>
              )}
              <button
                onClick={() => setCurrent(null)}
                className="w-full border border-brand-500 text-brand-600 font-bold py-3 rounded-xl hover:bg-brand-50 transition"
              >
                Próximo exercício
              </button>
            </div>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto">
      <h1 className="text-3xl font-bold text-slate-800 mb-2">Exercícios</h1>
      <p className="text-slate-500 mb-8">Pratique por tópico e dificuldade</p>

      <div className="flex gap-4 mb-8 flex-wrap">
        <select
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          className="border border-slate-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        >
          {TOPICS.map((t) => <option key={t.value} value={t.value}>{t.label}</option>)}
        </select>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className="border border-slate-200 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-brand-500"
        >
          {DIFFICULTIES.map((d) => <option key={d.value} value={d.value}>{d.label}</option>)}
        </select>
      </div>

      {exercises.length === 0 ? (
        <div className="text-center py-20 text-slate-400">
          <BookOpen size={48} className="mx-auto mb-4 opacity-40" />
          <p>Nenhum exercício encontrado com esses filtros.</p>
        </div>
      ) : (
        <div className="grid md:grid-cols-2 gap-4">
          {exercises.map((ex) => (
            <button
              key={ex.id}
              onClick={() => startExercise(ex)}
              className="bg-white rounded-2xl border border-slate-100 p-6 text-left hover:border-brand-300 hover:shadow-sm transition"
            >
              <div className="flex items-center gap-2 mb-3">
                <span className={`text-xs px-2 py-1 rounded-full font-medium ${DIFFICULTY_COLORS[ex.difficulty]}`}>
                  {ex.difficulty.replace(/_/g, " ")}
                </span>
                <span className="text-xs text-slate-400">{ex.exam_source}</span>
              </div>
              <p className="text-slate-700 line-clamp-3 text-sm">{ex.statement}</p>
            </button>
          ))}
        </div>
      )}
    </div>
  );
}

function BookOpen({ size, className }: { size: number; className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className={className}>
      <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
    </svg>
  );
}

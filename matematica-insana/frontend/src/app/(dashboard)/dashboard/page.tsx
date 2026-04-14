"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import { api } from "@/lib/api";
import { getStoredUser } from "@/lib/auth";
import type { Gamification, DiagnosticResult } from "@/types";
import { BookOpen, BarChart2, Flame, Star, Trophy, ArrowRight } from "lucide-react";

export default function DashboardPage() {
  const user = getStoredUser();
  const [gamification, setGamification] = useState<Gamification | null>(null);
  const [latestDiagnostic, setLatestDiagnostic] = useState<DiagnosticResult | null>(null);

  useEffect(() => {
    api.get("/gamification/me").then((r) => setGamification(r.data)).catch(() => {});
    api.get("/diagnostics/").then((r) => {
      const diagnostics: DiagnosticResult[] = r.data;
      const completed = diagnostics.filter((d) => d.status === "concluido");
      if (completed.length > 0) setLatestDiagnostic(completed[completed.length - 1]);
    }).catch(() => {});
  }, []);

  const levelProgress = gamification ? (gamification.xp % 100) : 0;

  return (
    <div className="max-w-5xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-slate-800">
          Olá, {user?.name?.split(" ")[0]}! 👋
        </h1>
        <p className="text-slate-500 mt-1">Continue de onde parou.</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          {
            label: "Nível",
            value: gamification?.level ?? 1,
            icon: Star,
            color: "text-yellow-500",
            bg: "bg-yellow-50",
          },
          {
            label: "XP Total",
            value: gamification?.xp ?? 0,
            icon: Trophy,
            color: "text-brand-600",
            bg: "bg-brand-50",
          },
          {
            label: "Sequência",
            value: `${gamification?.streak_days ?? 0} dias`,
            icon: Flame,
            color: "text-orange-500",
            bg: "bg-orange-50",
          },
          {
            label: "Precisão",
            value: `${gamification?.accuracy ?? 0}%`,
            icon: BarChart2,
            color: "text-green-600",
            bg: "bg-green-50",
          },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-2xl border border-slate-100 p-5 flex items-center gap-4"
          >
            <div className={`${stat.bg} p-3 rounded-xl`}>
              <stat.icon size={20} className={stat.color} />
            </div>
            <div>
              <p className="text-2xl font-bold text-slate-800">{stat.value}</p>
              <p className="text-sm text-slate-400">{stat.label}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Level progress */}
      {gamification && (
        <div className="bg-white rounded-2xl border border-slate-100 p-6 mb-6">
          <div className="flex justify-between text-sm mb-2">
            <span className="font-medium text-slate-700">Progresso — Nível {gamification.level}</span>
            <span className="text-slate-400">{levelProgress}/100 XP</span>
          </div>
          <div className="w-full bg-slate-100 rounded-full h-3">
            <div
              className="bg-brand-500 h-3 rounded-full transition-all"
              style={{ width: `${levelProgress}%` }}
            />
          </div>
        </div>
      )}

      {/* Quick actions */}
      <div className="grid md:grid-cols-2 gap-4 mb-8">
        <Link
          href="/exercises"
          className="bg-brand-600 hover:bg-brand-700 text-white rounded-2xl p-6 flex items-center justify-between transition"
        >
          <div>
            <BookOpen size={24} className="mb-3" />
            <h3 className="text-xl font-bold">Praticar exercícios</h3>
            <p className="text-white/70 text-sm mt-1">
              {gamification?.total_exercises ?? 0} exercícios feitos
            </p>
          </div>
          <ArrowRight size={20} />
        </Link>

        <Link
          href="/diagnostic"
          className="bg-white hover:bg-slate-50 text-slate-800 rounded-2xl border border-slate-100 p-6 flex items-center justify-between transition"
        >
          <div>
            <BarChart2 size={24} className="mb-3 text-brand-600" />
            <h3 className="text-xl font-bold">
              {latestDiagnostic ? "Ver diagnóstico" : "Fazer diagnóstico"}
            </h3>
            <p className="text-slate-500 text-sm mt-1">
              {latestDiagnostic
                ? `Nota geral: ${latestDiagnostic.overall_score}%`
                : "Descubra suas defasagens"}
            </p>
          </div>
          <ArrowRight size={20} className="text-slate-400" />
        </Link>
      </div>

      {/* Latest diagnostic gaps */}
      {latestDiagnostic && latestDiagnostic.gaps.length > 0 && (
        <div className="bg-white rounded-2xl border border-slate-100 p-6">
          <h2 className="text-lg font-bold text-slate-800 mb-4">Suas principais defasagens</h2>
          <div className="space-y-3">
            {latestDiagnostic.gaps.slice(0, 3).map((gap) => (
              <div key={gap.topic} className="flex items-center justify-between">
                <span className="text-slate-700 capitalize">
                  {gap.topic.replace(/_/g, " ")}
                </span>
                <div className="flex items-center gap-3">
                  <div className="w-32 bg-slate-100 rounded-full h-2">
                    <div
                      className="bg-red-400 h-2 rounded-full"
                      style={{ width: `${gap.score}%` }}
                    />
                  </div>
                  <span className="text-sm text-slate-500 w-12 text-right">
                    {gap.score.toFixed(0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

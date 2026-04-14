import Link from "next/link";

export default function LandingPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-brand-900 via-brand-700 to-brand-500 text-white">
      {/* Navbar */}
      <nav className="flex items-center justify-between px-8 py-5">
        <span className="text-2xl font-extrabold tracking-tight">
          Matemática <span className="text-accent-400">Insana</span>
        </span>
        <div className="flex gap-4">
          <Link
            href="/login"
            className="px-4 py-2 rounded-lg border border-white/30 hover:bg-white/10 transition text-sm font-medium"
          >
            Entrar
          </Link>
          <Link
            href="/register"
            className="px-4 py-2 rounded-lg bg-accent-500 hover:bg-accent-600 transition text-sm font-bold"
          >
            Começar grátis
          </Link>
        </div>
      </nav>

      {/* Hero */}
      <section className="flex flex-col items-center text-center px-4 py-24 gap-8">
        <div className="inline-flex items-center gap-2 bg-white/10 rounded-full px-4 py-1 text-sm border border-white/20">
          🧠 Diagnóstico personalizado por IA
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold leading-tight max-w-4xl">
          Matemática que faz{" "}
          <span className="text-accent-400">sentido</span>
        </h1>
        <p className="text-xl text-white/80 max-w-2xl">
          Descubra exatamente onde estão suas dificuldades e receba um plano de estudos
          personalizado. Do 6º ano ao vestibular, do básico ao avançado.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 mt-4">
          <Link
            href="/register"
            className="px-8 py-4 rounded-xl bg-accent-500 hover:bg-accent-600 font-bold text-lg shadow-lg transition"
          >
            Fazer diagnóstico grátis
          </Link>
          <Link
            href="#como-funciona"
            className="px-8 py-4 rounded-xl border border-white/30 hover:bg-white/10 font-medium text-lg transition"
          >
            Como funciona
          </Link>
        </div>
      </section>

      {/* Features */}
      <section id="como-funciona" className="bg-white text-slate-900 py-24 px-4">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">Como funciona</h2>
          <p className="text-center text-slate-500 mb-16 text-lg">
            Três passos para transformar sua relação com a matemática
          </p>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              {
                icon: "🎯",
                title: "Diagnóstico Inteligente",
                desc: "Responda exercícios calibrados pela Taxonomia de Bloom. O sistema identifica suas defasagens com precisão cirúrgica.",
              },
              {
                icon: "🗺️",
                title: "Plano Personalizado",
                desc: "Receba um caminho de aprendizado único, ordenado por prioridade, focado exatamente no que você precisa superar.",
              },
              {
                icon: "🏆",
                title: "Pratique & Suba de Nível",
                desc: "Exercícios adaptativos, pontos de XP, conquistas e rankings para manter sua motivação sempre alta.",
              },
            ].map((f) => (
              <div
                key={f.title}
                className="flex flex-col items-center text-center p-8 rounded-2xl bg-slate-50 border border-slate-100 shadow-sm hover:shadow-md transition"
              >
                <span className="text-5xl mb-4">{f.icon}</span>
                <h3 className="text-xl font-bold mb-2">{f.title}</h3>
                <p className="text-slate-600">{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-brand-900 py-20 px-4 text-center">
        <h2 className="text-4xl font-bold mb-4">Pronto para começar?</h2>
        <p className="text-white/70 text-lg mb-8">
          Faça seu diagnóstico gratuito e descubra seu ponto de partida.
        </p>
        <Link
          href="/register"
          className="inline-block px-10 py-4 rounded-xl bg-accent-500 hover:bg-accent-600 font-bold text-lg transition"
        >
          Começar agora — é grátis
        </Link>
      </section>
    </main>
  );
}

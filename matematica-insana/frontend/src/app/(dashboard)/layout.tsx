"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { isAuthenticated, logout, getStoredUser } from "@/lib/auth";
import { BookOpen, BarChart2, Trophy, Home, LogOut } from "lucide-react";

const navItems = [
  { href: "/dashboard", label: "Início", icon: Home },
  { href: "/exercises", label: "Exercícios", icon: BookOpen },
  { href: "/diagnostic", label: "Diagnóstico", icon: BarChart2 },
  { href: "/ranking", label: "Ranking", icon: Trophy },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) router.push("/login");
  }, [router]);

  const user = getStoredUser();

  return (
    <div className="min-h-screen flex bg-slate-50">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-slate-100 flex flex-col py-6 px-4 fixed h-full">
        <Link href="/dashboard" className="text-xl font-extrabold text-brand-700 mb-8 px-2">
          Matemática <span className="text-accent-500">Insana</span>
        </Link>

        <nav className="flex flex-col gap-1 flex-1">
          {navItems.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className="flex items-center gap-3 px-4 py-3 rounded-xl text-slate-600 hover:bg-brand-50 hover:text-brand-700 font-medium transition"
            >
              <Icon size={18} />
              {label}
            </Link>
          ))}
        </nav>

        <div className="border-t border-slate-100 pt-4 mt-4">
          <div className="px-4 py-2 mb-2">
            <p className="text-sm font-medium text-slate-800">{user?.name}</p>
            <p className="text-xs text-slate-400">{user?.email}</p>
          </div>
          <button
            onClick={logout}
            className="flex items-center gap-3 px-4 py-2 w-full rounded-xl text-slate-500 hover:bg-red-50 hover:text-red-600 transition text-sm"
          >
            <LogOut size={16} />
            Sair
          </button>
        </div>
      </aside>

      {/* Main */}
      <main className="ml-64 flex-1 p-8">{children}</main>
    </div>
  );
}

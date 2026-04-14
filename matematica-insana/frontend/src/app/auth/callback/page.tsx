"use client";
import { useEffect } from "react";
import { useRouter, useSearchParams } from "next/navigation";

export default function AuthCallbackPage() {
  const router = useRouter();
  const params = useSearchParams();

  useEffect(() => {
    const access_token = params.get("access_token");
    const refresh_token = params.get("refresh_token");
    if (access_token && refresh_token) {
      localStorage.setItem("access_token", access_token);
      localStorage.setItem("refresh_token", refresh_token);
      router.push("/dashboard");
    } else {
      router.push("/login");
    }
  }, [params, router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <p className="text-slate-500">Autenticando...</p>
    </div>
  );
}

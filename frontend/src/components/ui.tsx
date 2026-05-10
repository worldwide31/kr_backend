import type { ReactNode } from "react";

export function PageTitle({ title, subtitle }: { title: string; subtitle: string }) {
  return (
    <div className="mb-6">
      <h1 className="text-2xl font-semibold tracking-tight text-ink">{title}</h1>
      <p className="mt-2 max-w-3xl text-sm leading-6 text-muted">{subtitle}</p>
    </div>
  );
}

export function Panel({ children, className = "" }: { children: ReactNode; className?: string }) {
  return <section className={`rounded-lg border border-line/80 bg-[#fffaf1]/95 shadow-soft ${className}`}>{children}</section>;
}

export function Notice({
  title,
  children,
  tone = "info"
}: {
  title: string;
  children: ReactNode;
  tone?: "info" | "success" | "warning" | "error";
}) {
  const tones = {
    info: "border-brand/20 bg-[#eef5f2] text-[#315861]",
    success: "border-emerald-200 bg-emerald-50 text-emerald-800",
    warning: "border-[#dccda8] bg-[#fff6df] text-[#725f2d]",
    error: "border-rose-200 bg-rose-50 text-rose-800"
  };
  return (
    <div className={`mb-4 rounded-lg border px-4 py-3 text-sm shadow-soft ${tones[tone]}`}>
      <div className="font-semibold">{title}</div>
      <div className="mt-1 leading-6">{children}</div>
    </div>
  );
}

export function FieldHint({ children, tone = "neutral" }: { children: ReactNode; tone?: "neutral" | "warning" | "error" }) {
  const tones = {
    neutral: "text-slate-500",
    warning: "text-amber-700",
    error: "text-rose-700"
  };
  return <p className={`mt-2 text-xs leading-5 ${tones[tone]}`}>{children}</p>;
}

export function Stat({ label, value, tone = "brand" }: { label: string; value: ReactNode; tone?: "brand" | "accent" | "ink" }) {
  const tones = {
    brand: "text-[#254b54] bg-[#dfece8]",
    accent: "text-[#315d52] bg-[#e8f2ef]",
    ink: "text-cream bg-ink"
  };
  return (
    <Panel className="p-5">
      <div className={`mb-4 inline-flex rounded-full px-3 py-1 text-xs font-semibold ${tones[tone]}`}>{label}</div>
      <div className="text-3xl font-semibold tracking-tight text-ink">{value}</div>
    </Panel>
  );
}

export function StatusBadge({ children, tone }: { children: ReactNode; tone: "ok" | "wait" | "stop" | "neutral" }) {
  const tones = {
    ok: "bg-emerald-50 text-emerald-700",
    wait: "bg-[#fff1cb] text-[#725f2d]",
    stop: "bg-rose-50 text-rose-700",
    neutral: "bg-[#ebe3d4] text-muted"
  };
  return <span className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold ${tones[tone]}`}>{children}</span>;
}

export function Table({ children }: { children: ReactNode }) {
  return <div className="overflow-x-auto rounded-lg border border-line/80 bg-[#fffaf1] shadow-panel">{children}</div>;
}

export function PrimaryButton(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return (
    <button
      {...props}
      className={`focus-ring rounded-md bg-brand px-4 py-2 text-sm font-semibold text-white shadow-soft transition hover:bg-[#3b626d] disabled:cursor-not-allowed disabled:opacity-50 ${props.className ?? ""}`}
    />
  );
}

export function TextInput(props: React.InputHTMLAttributes<HTMLInputElement>) {
  return <input {...props} className={`focus-ring w-full rounded-md border border-line bg-white/80 px-3 py-2 text-sm text-ink placeholder:text-muted/70 ${props.className ?? ""}`} />;
}

export function Select(props: React.SelectHTMLAttributes<HTMLSelectElement>) {
  return <select {...props} className={`focus-ring w-full rounded-md border border-line bg-white/80 px-3 py-2 text-sm text-ink ${props.className ?? ""}`} />;
}

import { Boxes } from "lucide-react";
import { FormEvent, useState } from "react";
import { Navigate } from "react-router-dom";

import { Notice, PrimaryButton, TextInput } from "../components/ui";
import { useAuth } from "../services/auth";

export function LoginPage() {
  const { login, user } = useAuth();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  if (user) {
    return <Navigate to="/" replace />;
  }

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await login(username, password);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Не удалось войти.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="grid min-h-screen place-items-center px-4 py-10">
      <section className="w-full max-w-md rounded-xl border border-line/80 bg-[#fffaf1] p-7 shadow-panel">
        <div className="mb-7 flex items-center gap-3">
          <div className="grid h-12 w-12 place-items-center rounded-lg bg-accent text-ink">
            <Boxes size={24} />
          </div>
          <div>
            <h1 className="text-2xl font-semibold text-ink">MuzFlow</h1>
            <p className="text-sm text-muted">Вход в операторскую панель</p>
          </div>
        </div>

        <Notice title="Доступы для проверки">
          Админ: admin / admin123. Оператор: operator / operator123.
        </Notice>

        {error && <Notice title="Ошибка входа" tone="error">{error}</Notice>}

        <form className="space-y-4" onSubmit={submit}>
          <label className="block text-sm font-semibold text-ink">
            Логин
            <TextInput className="mt-2" value={username} onChange={(event) => setUsername(event.target.value)} />
          </label>
          <label className="block text-sm font-semibold text-ink">
            Пароль
            <TextInput className="mt-2" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
          </label>
          <PrimaryButton className="w-full" disabled={loading}>
            {loading ? "Вход..." : "Войти"}
          </PrimaryButton>
        </form>
      </section>
    </div>
  );
}

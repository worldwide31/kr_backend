import { Plus } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import { FieldHint, Notice, PageTitle, Panel, PrimaryButton, Select, Table, TextInput } from "../components/ui";
import { api } from "../services/api";
import { useAuth } from "../services/auth";
import type { Company, CompanyRole } from "../types/domain";

export function CompaniesPage() {
  const { isAdmin } = useAuth();
  const [companies, setCompanies] = useState<Company[]>([]);
  const [message, setMessage] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  const [form, setForm] = useState({ name: "", inn: "", role: "customer" as CompanyRole, email: "", phone: "" });

  const load = () => api.companies().then(setCompanies);
  useEffect(() => {
    load();
  }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage(null);
    if (!/^\d{10,12}$/.test(form.inn)) {
      setMessage({ tone: "warning", text: "ИНН должен содержать от 10 до 12 цифр без пробелов и дефисов." });
      return;
    }
    try {
      await api.createCompany({ ...form, email: form.email || null, phone: form.phone || null });
      setMessage({ tone: "success", text: "Контрагент добавлен в справочник." });
      setForm({ name: "", inn: "", role: "customer", email: "", phone: "" });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось создать контрагента." });
    }
  };

  return (
    <>
      <PageTitle title="Контрагенты" subtitle="Клиенты, поставщики и универсальные партнеры оптовой компании." />
      <Notice title="Подсказка оператору">
        Роль влияет на процессы: клиент доступен при создании заказа, поставщик доступен при создании поставки, роль «Клиент и поставщик» подходит для обеих операций.
      </Notice>
      {message && <Notice title={message.tone === "success" ? "Готово" : "Проверьте справочник"} tone={message.tone}>{message.text}</Notice>}
      {isAdmin ? (
        <Panel className="mb-5 p-4">
          <form className="grid gap-3 md:grid-cols-6" onSubmit={submit}>
            <TextInput required placeholder="Название" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
            <TextInput required placeholder="ИНН" value={form.inn} onChange={(e) => setForm({ ...form, inn: e.target.value })} />
            <Select value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value as CompanyRole })}>
              <option value="customer">Клиент</option>
              <option value="supplier">Поставщик</option>
              <option value="both">Клиент и поставщик</option>
            </Select>
            <TextInput placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <TextInput placeholder="Телефон" value={form.phone} onChange={(e) => setForm({ ...form, phone: e.target.value })} />
            <PrimaryButton className="inline-flex items-center justify-center gap-2"><Plus size={16} /> Добавить</PrimaryButton>
          </form>
          <FieldHint>
            Название и ИНН должны быть уникальными, иначе система не позволит создать дубль.
          </FieldHint>
        </Panel>
      ) : (
        <Notice title="Режим оператора">Вы можете просматривать контрагентов и использовать их в заказах и поставках. Добавление доступно администратору.</Notice>
      )}
      <Table>
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-4 py-3">Название</th><th className="px-4 py-3">ИНН</th><th className="px-4 py-3">Роль</th><th className="px-4 py-3">Контакты</th></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {companies.map((company) => (
              <tr key={company.id}>
                <td className="px-4 py-3 font-medium text-ink">{company.name}</td>
                <td className="px-4 py-3 text-slate-600">{company.inn}</td>
                <td className="px-4 py-3 text-slate-600">{company.role}</td>
                <td className="px-4 py-3 text-slate-600">{company.email || company.phone || "-"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Table>
    </>
  );
}

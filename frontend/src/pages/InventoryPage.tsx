import { Plus } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import { FieldHint, Notice, PageTitle, Panel, PrimaryButton, StatusBadge, Table, TextInput } from "../components/ui";
import { api } from "../services/api";
import type { InventoryItem, Warehouse } from "../types/domain";

export function InventoryPage() {
  const [items, setItems] = useState<InventoryItem[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [message, setMessage] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  const [form, setForm] = useState({ name: "", city: "", address: "", manager: "" });
  const load = async () => {
    const [nextWarehouses, nextItems] = await Promise.all([api.warehouses(), api.inventory()]);
    setWarehouses(nextWarehouses);
    setItems(nextItems);
  };
  useEffect(() => { load(); }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage(null);
    try {
      await api.createWarehouse({ ...form, manager: form.manager || null });
      setMessage({ tone: "success", text: "Склад создан. Теперь его можно выбирать в заказах и поставках." });
      setForm({ name: "", city: "", address: "", manager: "" });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось создать склад." });
    }
  };

  return (
    <>
      <PageTitle title="Склад и остатки" subtitle="Остатки по товарам и складам с контролем резерва и минимального уровня." />
      <Notice title="Подсказка оператору">
        «Всего» показывает физический остаток, «Резерв» уже закреплен за заказами, «Доступно» можно продавать новым клиентам.
      </Notice>
      {message && <Notice title={message.tone === "success" ? "Готово" : "Проверьте склад"} tone={message.tone}>{message.text}</Notice>}
      <Panel className="mb-5 p-4">
        <form className="grid gap-3 md:grid-cols-5" onSubmit={submit}>
          <TextInput required placeholder="Склад" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <TextInput required placeholder="Город" value={form.city} onChange={(e) => setForm({ ...form, city: e.target.value })} />
          <TextInput required placeholder="Адрес" value={form.address} onChange={(e) => setForm({ ...form, address: e.target.value })} />
          <TextInput placeholder="Ответственный" value={form.manager} onChange={(e) => setForm({ ...form, manager: e.target.value })} />
          <PrimaryButton className="inline-flex items-center justify-center gap-2"><Plus size={16} /> Склад</PrimaryButton>
        </form>
        <FieldHint>
          Если доступный остаток меньше или равен минимальному уровню товара, система покажет статус «Пополнить».
        </FieldHint>
      </Panel>
      <div className="mb-4 grid gap-3 md:grid-cols-3">
        {warehouses.map((warehouse) => (
          <Panel key={warehouse.id} className="p-4">
            <div className="font-semibold text-ink">{warehouse.name}</div>
            <div className="mt-1 text-sm text-slate-600">{warehouse.city}, {warehouse.address}</div>
            <div className="mt-3 text-xs text-slate-500">{warehouse.manager || "Ответственный не назначен"}</div>
          </Panel>
        ))}
      </div>
      <Table>
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-4 py-3">Товар</th><th className="px-4 py-3">Склад</th><th className="px-4 py-3">Всего</th><th className="px-4 py-3">Резерв</th><th className="px-4 py-3">Доступно</th><th className="px-4 py-3">Статус</th></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {items.map((item) => (
              <tr key={item.id}>
                <td className="px-4 py-3"><div className="font-medium text-ink">{item.product_name}</div><div className="font-mono text-xs text-slate-500">{item.sku}</div></td>
                <td className="px-4 py-3 text-slate-600">{item.warehouse_name}</td>
                <td className="px-4 py-3 text-slate-600">{item.quantity}</td>
                <td className="px-4 py-3 text-slate-600">{item.reserved}</td>
                <td className="px-4 py-3 font-medium text-ink">{item.available}</td>
                <td className="px-4 py-3">
                  <StatusBadge tone={item.available <= item.min_stock ? "wait" : "ok"}>{item.available <= item.min_stock ? "Пополнить" : "Норма"}</StatusBadge>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Table>
    </>
  );
}

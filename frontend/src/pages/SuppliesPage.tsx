import { CheckCircle2 } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import { FieldHint, Notice, PageTitle, Panel, PrimaryButton, Select, StatusBadge, Table, TextInput } from "../components/ui";
import { api } from "../services/api";
import type { Company, Product, Supply, Warehouse } from "../types/domain";

const status = {
  planned: ["Планируется", "wait"],
  received: ["Принята", "ok"],
  cancelled: ["Отменена", "stop"]
} as const;

export function SuppliesPage() {
  const [supplies, setSupplies] = useState<Supply[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [message, setMessage] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  const [form, setForm] = useState({ supplier_id: "", product_id: "", warehouse_id: "", quantity: "1", purchase_price: "0" });
  const load = async () => {
    const [nextSupplies, nextCompanies, nextProducts, nextWarehouses] = await Promise.all([
      api.supplies(),
      api.companies(),
      api.products(),
      api.warehouses()
    ]);
    setSupplies(nextSupplies);
    setCompanies(nextCompanies.filter((company) => company.role !== "customer"));
    setProducts(nextProducts);
    setWarehouses(nextWarehouses);
    setForm((current) => ({
      ...current,
      supplier_id: current.supplier_id || String(nextCompanies.find((company) => company.role !== "customer")?.id ?? ""),
      product_id: current.product_id || String(nextProducts[0]?.id ?? ""),
      warehouse_id: current.warehouse_id || String(nextWarehouses[0]?.id ?? ""),
      purchase_price: current.purchase_price === "0" ? String(nextProducts[0]?.purchase_price ?? "0") : current.purchase_price
    }));
  };
  useEffect(() => { load(); }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage(null);
    if (!form.supplier_id || !form.product_id || !form.warehouse_id || Number(form.quantity) <= 0) {
      setMessage({ tone: "warning", text: "Выберите поставщика, товар, склад и положительное количество." });
      return;
    }
    try {
      await api.createSupply({
        supplier_id: Number(form.supplier_id),
        items: [
          {
            product_id: Number(form.product_id),
            warehouse_id: Number(form.warehouse_id),
            quantity: Number(form.quantity),
            purchase_price: form.purchase_price
          }
        ]
      });
      setMessage({ tone: "success", text: "Поставка создана в статусе планирования. Остаток увеличится после приемки." });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось создать поставку." });
    }
  };

  const receive = async (id: number) => {
    setMessage(null);
    try {
      await api.receiveSupply(id);
      setMessage({ tone: "success", text: "Поставка принята, складские остатки увеличены." });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось принять поставку." });
    }
  };

  return (
    <>
      <PageTitle title="Поставки поставщиков" subtitle="Плановые поставки пополняют складские остатки после приемки." />
      <Notice title="Подсказка оператору">
        Создание поставки не меняет остатки сразу. Нажмите «Принять» только когда товар фактически поступил на склад.
      </Notice>
      {message && <Notice title={message.tone === "success" ? "Готово" : "Проверьте действие"} tone={message.tone}>{message.text}</Notice>}
      <Panel className="mb-5 p-4">
        <form className="grid gap-3 md:grid-cols-5" onSubmit={submit}>
          <Select value={form.supplier_id} onChange={(e) => setForm({ ...form, supplier_id: e.target.value })} required>
            {companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}
          </Select>
          <Select value={form.product_id} onChange={(e) => {
            const product = products.find((item) => item.id === Number(e.target.value));
            setForm({ ...form, product_id: e.target.value, purchase_price: String(product?.purchase_price ?? form.purchase_price) });
          }} required>
            {products.map((product) => <option key={product.id} value={product.id}>{product.name}</option>)}
          </Select>
          <Select value={form.warehouse_id} onChange={(e) => setForm({ ...form, warehouse_id: e.target.value })} required>
            {warehouses.map((warehouse) => <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>)}
          </Select>
          <TextInput type="number" min="1" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
          <PrimaryButton disabled={!form.supplier_id || !form.product_id || !form.warehouse_id}>Создать поставку</PrimaryButton>
        </form>
        <FieldHint>
          После приемки каждая позиция поставки добавляется к свободному складскому остатку выбранного склада.
        </FieldHint>
      </Panel>
      <Table>
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-4 py-3">Номер</th><th className="px-4 py-3">Поставщик</th><th className="px-4 py-3">ETA</th><th className="px-4 py-3">Сумма</th><th className="px-4 py-3">Статус</th><th className="px-4 py-3"></th></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {supplies.map((supply) => {
              const [label, tone] = status[supply.status];
              return (
                <tr key={supply.id}>
                  <td className="px-4 py-3 font-medium text-ink">{supply.number}</td>
                  <td className="px-4 py-3 text-slate-600">{supply.supplier_name}</td>
                  <td className="px-4 py-3 text-slate-600">{supply.eta ? new Date(supply.eta).toLocaleDateString("ru-RU") : "-"}</td>
                  <td className="px-4 py-3 text-slate-600">{supply.total} ₽</td>
                  <td className="px-4 py-3"><StatusBadge tone={tone}>{label}</StatusBadge></td>
                  <td className="px-4 py-3 text-right">
                    <PrimaryButton disabled={supply.status !== "planned"} onClick={() => receive(supply.id)} className="inline-flex items-center gap-2">
                      <CheckCircle2 size={16} /> Принять
                    </PrimaryButton>
                  </td>
                </tr>
              );
            })}
            {!supplies.length && <tr><td className="px-4 py-6 text-slate-500" colSpan={6}>Создайте поставку через API или используйте Swagger.</td></tr>}
          </tbody>
        </table>
      </Table>
    </>
  );
}

import { Plus } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import { FieldHint, Notice, PageTitle, Panel, PrimaryButton, Table, TextInput } from "../components/ui";
import { api } from "../services/api";
import type { Product } from "../types/domain";

export function CatalogPage() {
  const [products, setProducts] = useState<Product[]>([]);
  const [message, setMessage] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  const [form, setForm] = useState({ sku: "", name: "", category: "", unit: "шт", purchase_price: "0", sale_price: "0", min_stock: "0" });
  const load = () => api.products().then(setProducts);
  useEffect(() => { load(); }, []);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage(null);
    if (Number(form.sale_price) < Number(form.purchase_price)) {
      setMessage({ tone: "warning", text: "Цена продажи ниже закупочной. Проверьте маржу перед добавлением товара." });
      return;
    }
    try {
      await api.createProduct({ ...form, min_stock: Number(form.min_stock) });
      setMessage({ tone: "success", text: "Товар добавлен в каталог. Остаток появится после приемки поставки." });
      setForm({ sku: "", name: "", category: "", unit: "шт", purchase_price: "0", sale_price: "0", min_stock: "0" });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось добавить товар." });
    }
  };

  return (
    <>
      <PageTitle title="Каталог товаров" subtitle="Номенклатура, закупочные и отпускные цены, минимальные складские остатки." />
      <Notice title="Подсказка оператору">
        SKU используется как уникальный артикул. Новый товар не появляется на складе автоматически: пополните остаток через поставку.
      </Notice>
      {message && <Notice title={message.tone === "success" ? "Готово" : "Проверьте товар"} tone={message.tone}>{message.text}</Notice>}
      <Panel className="mb-5 p-4">
        <form className="grid gap-3 md:grid-cols-7" onSubmit={submit}>
          <TextInput required placeholder="SKU" value={form.sku} onChange={(e) => setForm({ ...form, sku: e.target.value })} />
          <TextInput required placeholder="Название" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          <TextInput required placeholder="Категория" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
          <TextInput required placeholder="Ед." value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} />
          <TextInput type="number" min="0" placeholder="Закупка" value={form.purchase_price} onChange={(e) => setForm({ ...form, purchase_price: e.target.value })} />
          <TextInput type="number" min="0" placeholder="Продажа" value={form.sale_price} onChange={(e) => setForm({ ...form, sale_price: e.target.value })} />
          <PrimaryButton className="inline-flex items-center justify-center gap-2"><Plus size={16} /> Добавить</PrimaryButton>
        </form>
        <FieldHint>
          Минимальный остаток используется на странице склада: позиции ниже этого уровня помечаются как требующие пополнения.
        </FieldHint>
      </Panel>
      <Table>
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-4 py-3">SKU</th><th className="px-4 py-3">Товар</th><th className="px-4 py-3">Категория</th><th className="px-4 py-3">Цена продажи</th><th className="px-4 py-3">Мин. остаток</th></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {products.map((product) => (
              <tr key={product.id}>
                <td className="px-4 py-3 font-mono text-xs text-slate-600">{product.sku}</td>
                <td className="px-4 py-3 font-medium text-ink">{product.name}</td>
                <td className="px-4 py-3 text-slate-600">{product.category}</td>
                <td className="px-4 py-3 text-slate-600">{product.sale_price} ₽/{product.unit}</td>
                <td className="px-4 py-3 text-slate-600">{product.min_stock}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Table>
    </>
  );
}

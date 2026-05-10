import { Send } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";

import { FieldHint, Notice, PageTitle, Panel, PrimaryButton, Select, StatusBadge, Table, TextInput } from "../components/ui";
import { api } from "../services/api";
import type { Company, InventoryItem, Order, Product, Warehouse } from "../types/domain";

const status = {
  draft: ["Черновик", "neutral"],
  confirmed: ["Подтвержден", "wait"],
  shipped: ["Отгружен", "ok"],
  cancelled: ["Отменен", "stop"]
} as const;

export function OrdersPage() {
  const [orders, setOrders] = useState<Order[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [warehouses, setWarehouses] = useState<Warehouse[]>([]);
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [message, setMessage] = useState<{ tone: "success" | "error" | "warning"; text: string } | null>(null);
  const [form, setForm] = useState({ customer_id: "", product_id: "", warehouse_id: "", quantity: "1", unit_price: "0", delivery_city: "Москва" });
  const load = async () => {
    const [nextOrders, nextCompanies, nextProducts, nextWarehouses, nextInventory] = await Promise.all([
      api.orders(),
      api.companies(),
      api.products(),
      api.warehouses(),
      api.inventory()
    ]);
    setOrders(nextOrders);
    setCompanies(nextCompanies.filter((company) => company.role !== "supplier"));
    setProducts(nextProducts);
    setWarehouses(nextWarehouses);
    setInventory(nextInventory);
    setForm((current) => ({
      ...current,
      customer_id: current.customer_id || String(nextCompanies.find((company) => company.role !== "supplier")?.id ?? ""),
      product_id: current.product_id || String(nextProducts[0]?.id ?? ""),
      warehouse_id: current.warehouse_id || String(nextWarehouses[0]?.id ?? ""),
      unit_price: current.unit_price === "0" ? String(nextProducts[0]?.sale_price ?? "0") : current.unit_price
    }));
  };
  useEffect(() => { load(); }, []);

  const selectedStock = inventory.find(
    (item) => item.product_id === Number(form.product_id) && item.warehouse_id === Number(form.warehouse_id)
  );
  const requestedQuantity = Number(form.quantity);
  const available = selectedStock?.available ?? 0;
  const canCreateOrder = Boolean(form.customer_id && form.product_id && form.warehouse_id && requestedQuantity > 0 && available >= requestedQuantity);

  const submit = async (event: FormEvent) => {
    event.preventDefault();
    setMessage(null);
    if (!canCreateOrder) {
      setMessage({
        tone: "warning",
        text: available <= 0
          ? "На выбранном складе нет доступного остатка по этому товару. Сначала примите поставку или выберите другой склад."
          : `Нельзя создать заказ на ${requestedQuantity} ед.: доступно только ${available} ед. Уменьшите количество или оформите поставку.`
      });
      return;
    }
    try {
      await api.createOrder({
        customer_id: Number(form.customer_id),
        delivery_city: form.delivery_city,
        items: [
          {
            product_id: Number(form.product_id),
            warehouse_id: Number(form.warehouse_id),
            quantity: requestedQuantity,
            unit_price: form.unit_price
          }
        ]
      });
      setMessage({ tone: "success", text: "Заказ создан и товар зарезервирован на складе." });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось создать заказ." });
    }
  };

  const ship = async (id: number) => {
    setMessage(null);
    try {
      await api.shipOrder(id);
      setMessage({ tone: "success", text: "Заказ отгружен, резерв списан с остатка." });
      await load();
    } catch (error) {
      setMessage({ tone: "error", text: error instanceof Error ? error.message : "Не удалось отгрузить заказ." });
    }
  };

  return (
    <>
      <PageTitle title="Заказы клиентов" subtitle="Заказы резервируют остатки, после отгрузки резерв списывается со склада." />
      <Notice title="Подсказка оператору">
        Заказ можно создать только при наличии свободного остатка на выбранном складе. Зарезервированные товары уже обещаны другим клиентам и не считаются доступными.
      </Notice>
      {message && <Notice title={message.tone === "success" ? "Готово" : "Проверьте действие"} tone={message.tone}>{message.text}</Notice>}
      <Panel className="mb-5 p-4">
        <form className="grid gap-3 md:grid-cols-6" onSubmit={submit}>
          <Select value={form.customer_id} onChange={(e) => setForm({ ...form, customer_id: e.target.value })} required>
            {companies.map((company) => <option key={company.id} value={company.id}>{company.name}</option>)}
          </Select>
          <Select value={form.product_id} onChange={(e) => {
            const product = products.find((item) => item.id === Number(e.target.value));
            setForm({ ...form, product_id: e.target.value, unit_price: String(product?.sale_price ?? form.unit_price) });
          }} required>
            {products.map((product) => <option key={product.id} value={product.id}>{product.name}</option>)}
          </Select>
          <Select value={form.warehouse_id} onChange={(e) => setForm({ ...form, warehouse_id: e.target.value })} required>
            {warehouses.map((warehouse) => <option key={warehouse.id} value={warehouse.id}>{warehouse.name}</option>)}
          </Select>
          <TextInput type="number" min="1" value={form.quantity} onChange={(e) => setForm({ ...form, quantity: e.target.value })} required />
          <TextInput value={form.delivery_city} onChange={(e) => setForm({ ...form, delivery_city: e.target.value })} required />
          <PrimaryButton disabled={!canCreateOrder}>Создать заказ</PrimaryButton>
        </form>
        <FieldHint tone={canCreateOrder ? "neutral" : "warning"}>
          Доступно на выбранном складе: {available} ед. Запрошено: {Number.isFinite(requestedQuantity) ? requestedQuantity : 0} ед.
        </FieldHint>
      </Panel>
      <Table>
        <table className="min-w-full divide-y divide-line text-sm">
          <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
            <tr><th className="px-4 py-3">Номер</th><th className="px-4 py-3">Клиент</th><th className="px-4 py-3">Город</th><th className="px-4 py-3">Сумма</th><th className="px-4 py-3">Статус</th><th className="px-4 py-3"></th></tr>
          </thead>
          <tbody className="divide-y divide-line">
            {orders.map((order) => {
              const [label, tone] = status[order.status];
              return (
                <tr key={order.id}>
                  <td className="px-4 py-3 font-medium text-ink">{order.number}</td>
                  <td className="px-4 py-3 text-slate-600">{order.customer_name}</td>
                  <td className="px-4 py-3 text-slate-600">{order.delivery_city}</td>
                  <td className="px-4 py-3 text-slate-600">{order.total} ₽</td>
                  <td className="px-4 py-3"><StatusBadge tone={tone}>{label}</StatusBadge></td>
                  <td className="px-4 py-3 text-right">
                    <PrimaryButton disabled={order.status !== "confirmed"} onClick={() => ship(order.id)} className="inline-flex items-center gap-2">
                      <Send size={16} /> Отгрузить
                    </PrimaryButton>
                  </td>
                </tr>
              );
            })}
            {!orders.length && <tr><td className="px-4 py-6 text-slate-500" colSpan={6}>Создайте заказ через API или используйте демо-данные как основу.</td></tr>}
          </tbody>
        </table>
      </Table>
    </>
  );
}

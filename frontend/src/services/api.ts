import type {
  ActivityEvent,
  Company,
  DashboardKpi,
  InventoryItem,
  Order,
  Product,
  Supply,
  Warehouse
} from "../types/domain";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json", ...init?.headers },
    ...init
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({ detail: response.statusText }));
    const detail = payload.detail;
    const message = Array.isArray(detail)
      ? detail.map((item) => item.msg ?? JSON.stringify(item)).join("; ")
      : detail;
    throw new Error(message ?? "Ошибка запроса. Проверьте данные и повторите действие.");
  }
  return response.json() as Promise<T>;
}

export const api = {
  seed: () => request<{ status: string }>("/seed", { method: "POST" }),
  kpi: () => request<DashboardKpi>("/dashboard/kpi"),
  events: () => request<ActivityEvent[]>("/events"),
  companies: () => request<Company[]>("/companies"),
  products: () => request<Product[]>("/products"),
  warehouses: () => request<Warehouse[]>("/warehouses"),
  inventory: () => request<InventoryItem[]>("/warehouses/inventory"),
  orders: () => request<Order[]>("/orders"),
  supplies: () => request<Supply[]>("/supplies"),
  shipOrder: (id: number) => request<Order>(`/orders/${id}/ship`, { method: "POST" }),
  receiveSupply: (id: number) => request<Supply>(`/supplies/${id}/receive`, { method: "POST" }),
  createCompany: (body: unknown) => request<Company>("/companies", { method: "POST", body: JSON.stringify(body) }),
  createProduct: (body: unknown) => request<Product>("/products", { method: "POST", body: JSON.stringify(body) }),
  createWarehouse: (body: unknown) => request<Warehouse>("/warehouses", { method: "POST", body: JSON.stringify(body) }),
  createOrder: (body: unknown) => request<Order>("/orders", { method: "POST", body: JSON.stringify(body) }),
  createSupply: (body: unknown) => request<Supply>("/supplies", { method: "POST", body: JSON.stringify(body) })
};

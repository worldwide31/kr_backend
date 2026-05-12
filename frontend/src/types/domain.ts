export type CompanyRole = "customer" | "supplier" | "both";
export type OrderStatus = "draft" | "confirmed" | "shipped" | "cancelled";
export type SupplyStatus = "planned" | "received" | "cancelled";

export interface Company {
  id: number;
  name: string;
  inn: string;
  role: CompanyRole;
  contact_name?: string | null;
  email?: string | null;
  phone?: string | null;
  address?: string | null;
  created_at: string;
}

export interface Product {
  id: number;
  sku: string;
  name: string;
  category: string;
  unit: string;
  purchase_price: string;
  sale_price: string;
  min_stock: number;
}

export interface Warehouse {
  id: number;
  name: string;
  city: string;
  address: string;
  manager?: string | null;
}

export interface InventoryItem {
  id: number;
  product_id: number;
  warehouse_id: number;
  product_name: string;
  sku: string;
  warehouse_name: string;
  quantity: number;
  reserved: number;
  available: number;
  min_stock: number;
}

export interface OrderItem {
  id: number;
  product_id: number;
  warehouse_id: number;
  product_name: string;
  warehouse_name: string;
  quantity: number;
  unit_price: string;
  total: string;
}

export interface Order {
  id: number;
  number: string;
  customer_id: number;
  customer_name: string;
  status: OrderStatus;
  delivery_city: string;
  comment?: string | null;
  created_at: string;
  total: string;
  items: OrderItem[];
}

export interface SupplyItem {
  id: number;
  product_id: number;
  warehouse_id: number;
  product_name: string;
  warehouse_name: string;
  quantity: number;
  purchase_price: string;
  total: string;
}

export interface Supply {
  id: number;
  number: string;
  supplier_id: number;
  supplier_name: string;
  status: SupplyStatus;
  eta?: string | null;
  created_at: string;
  total: string;
  items: SupplyItem[];
}

export interface DashboardKpi {
  companies: number;
  products: number;
  warehouses: number;
  active_orders: number;
  planned_supplies: number;
  inventory_units: number;
  reserved_units: number;
  low_stock_items: number;
  order_revenue: string;
}

export interface ActivityEvent {
  id: string;
  action: string;
  entity_type: string;
  entity_id: string;
  message: string;
  created_at: string;
}

export type UserRole = "admin" | "operator";

export interface AuthUser {
  username: string;
  role: UserRole;
}

export interface TokenResponse extends AuthUser {
  access_token: string;
  token_type: string;
}

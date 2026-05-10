import { Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { CatalogPage } from "./pages/CatalogPage";
import { CompaniesPage } from "./pages/CompaniesPage";
import { DashboardPage } from "./pages/DashboardPage";
import { InventoryPage } from "./pages/InventoryPage";
import { OrdersPage } from "./pages/OrdersPage";
import { SuppliesPage } from "./pages/SuppliesPage";

export function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<DashboardPage />} />
        <Route path="orders" element={<OrdersPage />} />
        <Route path="supplies" element={<SuppliesPage />} />
        <Route path="inventory" element={<InventoryPage />} />
        <Route path="catalog" element={<CatalogPage />} />
        <Route path="companies" element={<CompaniesPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}


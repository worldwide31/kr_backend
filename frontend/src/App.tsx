import { Navigate, Route, Routes } from "react-router-dom";

import { Layout } from "./components/Layout";
import { CatalogPage } from "./pages/CatalogPage";
import { CompaniesPage } from "./pages/CompaniesPage";
import { DashboardPage } from "./pages/DashboardPage";
import { InventoryPage } from "./pages/InventoryPage";
import { LoginPage } from "./pages/LoginPage";
import { OrdersPage } from "./pages/OrdersPage";
import { SuppliesPage } from "./pages/SuppliesPage";
import { useAuth } from "./services/auth";

function ProtectedLayout() {
  const { loading, user } = useAuth();
  if (loading) {
    return <div className="grid min-h-screen place-items-center text-ink">Загрузка сессии...</div>;
  }
  if (!user) {
    return <Navigate to="/login" replace />;
  }
  return <Layout />;
}

export function App() {
  return (
    <Routes>
      <Route path="login" element={<LoginPage />} />
      <Route element={<ProtectedLayout />}>
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

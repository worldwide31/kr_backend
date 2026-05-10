import { Boxes, Building2, ClipboardList, LayoutDashboard, Package, Truck, Warehouse } from "lucide-react";
import { NavLink, Outlet } from "react-router-dom";

const links = [
  { to: "/", label: "Обзор", icon: LayoutDashboard },
  { to: "/orders", label: "Заказы", icon: ClipboardList },
  { to: "/supplies", label: "Поставки", icon: Truck },
  { to: "/inventory", label: "Склад", icon: Warehouse },
  { to: "/catalog", label: "Каталог", icon: Package },
  { to: "/companies", label: "Контрагенты", icon: Building2 }
];

export function Layout() {
  return (
    <div className="min-h-screen">
      <aside className="fixed inset-y-0 left-0 z-20 hidden w-64 border-r border-white/10 bg-ink lg:block">
        <div className="flex h-20 items-center gap-3 border-b border-white/10 px-6">
          <div className="grid h-11 w-11 place-items-center rounded-lg bg-accent text-ink shadow-soft">
            <Boxes size={22} />
          </div>
          <div>
            <div className="text-lg font-semibold text-cream">MuzFlow</div>
            <div className="text-xs text-cream/60">Операторская панель</div>
          </div>
        </div>
        <nav className="space-y-1 p-4">
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                [
                  "flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition",
                  isActive ? "bg-cream text-ink" : "text-[#F5E9D4] hover:bg-white/10 hover:text-white"
                ].join(" ")
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>
        <div className="absolute bottom-0 left-0 right-0 border-t border-white/10 p-5">
          <div className="rounded-lg border border-white/10 bg-white/5 p-4 text-xs leading-5 text-cream/70">
            Оптовый учет музыкальных инструментов, студийного оборудования и концертного звука.
          </div>
        </div>
      </aside>

      <div className="lg:pl-64">
        <header className="sticky top-0 z-10 border-b border-line/70 bg-[#fffaf1]/82 backdrop-blur-xl">
          <div className="flex min-h-20 flex-wrap items-center justify-between gap-3 px-4 py-3 sm:px-6 lg:px-8">
            <div>
              <div className="text-sm font-semibold text-ink">Веб-сервис управления поставками и заказами</div>
              <div className="mt-1 text-xs text-muted">Музыкальный магазин · склады · поставки · заказы</div>
            </div>
            <nav className="flex gap-1 overflow-x-auto lg:hidden">
              {links.map(({ to, icon: Icon }) => (
                <NavLink
                  key={to}
                  to={to}
                  className={({ isActive }) =>
                    `grid h-10 w-10 shrink-0 place-items-center rounded-md ${isActive ? "bg-ink text-cream" : "bg-cream text-muted"}`
                  }
                >
                  <Icon size={18} />
                </NavLink>
              ))}
            </nav>
          </div>
        </header>
        <main className="px-4 py-6 sm:px-6 lg:px-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

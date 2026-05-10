import { Database, RefreshCw } from "lucide-react";
import { useEffect, useState } from "react";

import { PrimaryButton, Stat, Table, PageTitle } from "../components/ui";
import { api } from "../services/api";
import type { ActivityEvent, DashboardKpi } from "../types/domain";

export function DashboardPage() {
  const [kpi, setKpi] = useState<DashboardKpi | null>(null);
  const [events, setEvents] = useState<ActivityEvent[]>([]);
  const [loading, setLoading] = useState(false);

  const load = async () => {
    setLoading(true);
    try {
      const [nextKpi, nextEvents] = await Promise.all([api.kpi(), api.events()]);
      setKpi(nextKpi);
      setEvents(nextEvents);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const seed = async () => {
    await api.seed();
    await load();
  };

  return (
    <>
      <div className="flex flex-wrap items-start justify-between gap-3">
        <PageTitle title="Операционный обзор" subtitle="Ключевые показатели склада, заказов и поставок в одном рабочем экране." />
        <div className="flex gap-2">
          <PrimaryButton onClick={seed} className="inline-flex items-center gap-2 bg-ink text-cream hover:bg-[#172231]">
            <Database size={16} /> Демо-данные
          </PrimaryButton>
          <PrimaryButton onClick={load} disabled={loading} className="inline-flex items-center gap-2">
            <RefreshCw size={16} /> Обновить
          </PrimaryButton>
        </div>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Stat label="Активные заказы" value={kpi?.active_orders ?? "-"} />
        <Stat label="Плановые поставки" value={kpi?.planned_supplies ?? "-"} tone="accent" />
        <Stat label="Остаток, ед." value={kpi?.inventory_units ?? "-"} tone="ink" />
        <Stat label="Выручка заказов" value={`${kpi?.order_revenue ?? "0"} ₽`} />
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
        <Stat label="Контрагенты" value={kpi?.companies ?? "-"} tone="ink" />
        <Stat label="Товары" value={kpi?.products ?? "-"} tone="ink" />
        <Stat label="Резерв" value={kpi?.reserved_units ?? "-"} tone="accent" />
        <Stat label="Низкий остаток" value={kpi?.low_stock_items ?? "-"} tone="accent" />
      </div>

      <div className="mt-6">
        <h2 className="mb-3 text-lg font-semibold text-ink">Журнал операций MongoDB</h2>
        <Table>
          <table className="min-w-full divide-y divide-line text-sm">
            <thead className="bg-slate-50 text-left text-xs uppercase text-slate-500">
              <tr>
                <th className="px-4 py-3">Событие</th>
                <th className="px-4 py-3">Сущность</th>
                <th className="px-4 py-3">Описание</th>
                <th className="px-4 py-3">Дата</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-line">
              {events.map((event) => (
                <tr key={event.id}>
                  <td className="px-4 py-3 font-medium text-ink">{event.action}</td>
                  <td className="px-4 py-3 text-slate-600">{event.entity_type} #{event.entity_id}</td>
                  <td className="px-4 py-3 text-slate-700">{event.message}</td>
                  <td className="px-4 py-3 text-slate-500">{new Date(event.created_at).toLocaleString("ru-RU")}</td>
                </tr>
              ))}
              {!events.length && (
                <tr>
                  <td className="px-4 py-6 text-slate-500" colSpan={4}>Операции появятся после создания заказов, поставок или справочников.</td>
                </tr>
              )}
            </tbody>
          </table>
        </Table>
      </div>
    </>
  );
}

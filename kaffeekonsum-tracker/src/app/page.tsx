"use client";
import { Bar, Pie } from "react-chartjs-2";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import { Chart, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from "chart.js";
import { useMemo, useEffect, useState } from "react";

Chart.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const fakeBarData = {
  labels: ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"],
  datasets: [
    {
      label: "Tassen",
      data: [2, 3, 1, 4, 2, 5, 3],
      backgroundColor: "#6366f1",
    },
  ],
};

const fakePieData = {
  labels: ["Arabica", "Robusta", "Blend"],
  datasets: [
    {
      data: [10, 5, 7],
      backgroundColor: ["#6366f1", "#f59e42", "#10b981"],
    },
  ],
};

export default function Home() {
  const today = new Date();
  const [heatmapValues, setHeatmapValues] = useState<{date: string; count?: number}[]>([]);
  useEffect(() => {
    const data = Array.from({ length: 120 }, (_, i) => {
      const d = new Date(today);
      d.setDate(today.getDate() - i);
      return { date: d.toISOString().slice(0, 10), count: Math.floor(Math.random() * 5) };
    });
    setHeatmapValues(data);
  }, []);
  return (
    <main className="max-w-4xl mx-auto py-12 flex flex-col gap-12">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-2">Kaffeekonsum-Tracker</h1>
        <p className="text-lg text-muted-foreground mb-4">Tracke deinen Kaffeekonsum, analysiere Statistiken und entdecke Trends. Demo-Daten unten!</p>
      </section>
      <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-card rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-4">Täglicher Verbrauch</h2>
          <Bar data={fakeBarData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
        </div>
        <div className="bg-card rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-4">Sorten-Verteilung</h2>
          <Pie data={fakePieData} options={{ responsive: true, plugins: { legend: { position: "bottom" } } }} />
        </div>
      </section>
      <section className="bg-card rounded-lg p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">Kalender-Heatmap</h2>
        <CalendarHeatmap
          startDate={new Date(today.getFullYear(), today.getMonth(), today.getDate() - 119)}
          endDate={today}
          values={heatmapValues}
          classForValue={(v: { date: string; count?: number } | undefined) => v && v.count ? "react-calendar-heatmap-color-scale-" + v.count : "react-calendar-heatmap-empty"}
          showWeekdayLabels
        />
      </section>
    </main>
  );
}

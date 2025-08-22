"use client";
import { useEffect, useState } from "react";
import { account, getVarieties, addVariety, deleteVariety, getConsumption, addConsumption, deleteConsumption, updateConsumption, getAllVarieties } from "@/lib/appwrite";
import { Button } from "@/components/ui/button";
import { Bar, Pie } from "react-chartjs-2";
import CalendarHeatmap from "react-calendar-heatmap";
import "react-calendar-heatmap/dist/styles.css";
import { Chart, CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend } from "chart.js";
import { useRouter } from "next/navigation";
Chart.register(CategoryScale, LinearScale, BarElement, ArcElement, Tooltip, Legend);

const DEFAULT_VARIANTS = [
  "Arabica",
  "Robusta",
  "Espresso",
  "Filterkaffee",
  "Cappuccino"
];

export default function Dashboard() {
  const [user, setUser] = useState<any>(null);
  const [varieties, setVarieties] = useState<any[]>([]);
  const [consumptions, setConsumptions] = useState<any[]>([]);
  const [newVariety, setNewVariety] = useState("");
  const [newEntry, setNewEntry] = useState({ date: "", cups: 1, varietyId: "" });
  const [loading, setLoading] = useState(true);
  const [showVarieties, setShowVarieties] = useState(false);
  const [showStats, setShowStats] = useState(true);
  const [showPie, setShowPie] = useState(true);
  const [showHeatmap, setShowHeatmap] = useState(true);
  const router = useRouter();
  // Fetch user and data
  useEffect(() => {
    account.get().then(async u => {
      setUser(u);
      const userVarieties = (await getVarieties(u.$id)).documents;
      if (userVarieties.length === 0) {
        // Default-Varianten für neuen User anlegen
        await Promise.all(
          DEFAULT_VARIANTS.map(name => addVariety(name, u.$id))
        );
        setVarieties((await getVarieties(u.$id)).documents);
      } else {
        setVarieties(userVarieties);
      }
      setConsumptions((await getConsumption(u.$id)).documents);
      setLoading(false);
    }).catch(() => {
      setLoading(false);
      setUser(null);
    });
  }, []);
  // Redirect if not logged in
  useEffect(() => {
    if (!loading && !user) {
      router.push("/");
    }
  }, [loading, user, router]);
  // Add variety
  const handleAddVariety = async () => {
    if (!newVariety.trim() || !user) return;
    await addVariety(newVariety, 'admin');
    setVarieties((await getVarieties('admin')).documents);
    setNewVariety("");
  };
  // Delete variety
  const handleDeleteVariety = async (id: string) => {
    await deleteVariety(id);
    setVarieties((await getVarieties('admin')).documents);
  };
  // Add consumption
  const handleAddEntry = async () => {
    if (!newEntry.date || !newEntry.cups || !newEntry.varietyId || !user) return;
    await addConsumption(newEntry.date, newEntry.cups, newEntry.varietyId, user.$id);
    setConsumptions((await getConsumption(user.$id)).documents);
    setNewEntry({ date: "", cups: 1, varietyId: "" });
  };
  // Delete consumption
  const handleDeleteEntry = async (id: string) => {
    await deleteConsumption(id);
    setConsumptions((await getConsumption(user.$id)).documents);
  };
  // Update consumption
  const handleUpdateEntry = async (id: string, data: any) => {
    await updateConsumption(id, data);
    setConsumptions((await getConsumption(user.$id)).documents);
  };
  // Stats
  const barData = {
    labels: Array.from(new Set(consumptions.map(e => e.date))).sort(),
    datasets: [{
      label: "Tassen",
      data: Array.from(new Set(consumptions.map(e => e.date))).sort().map(d => consumptions.filter(e => e.date === d).reduce((a, b) => a + b.cups, 0)),
      backgroundColor: "#6366f1"
    }]
  };
  const pieData = {
    labels: varieties.map(v => v.name),
    datasets: [{
      data: varieties.map(v => consumptions.filter(e => e.varietyId === v.$id).reduce((a, b) => a + b.cups, 0)),
      backgroundColor: ["#6366f1", "#f59e42", "#10b981", "#ef4444", "#a21caf", "#eab308"]
    }]
  };
  const today = new Date();
  const heatmapValues = consumptions.map(e => ({ date: e.date, count: e.cups }));
  if (loading) return <div className="flex justify-center items-center h-64"><span className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary"></span></div>;
  if (!user) return <div className="p-8 text-center">Nicht eingeloggt.</div>;
  return (
    <main className="max-w-4xl mx-auto py-12 flex flex-col gap-12">
      <section className="text-center">
        <h1 className="text-4xl font-bold mb-2">Dein Kaffeekonsum</h1>
        <p className="text-lg text-muted-foreground mb-4">Hier siehst du deine echten Daten, kannst Einträge hinzufügen, bearbeiten und Statistiken einsehen.</p>
      </section>
      <section className="bg-card rounded-lg p-6 shadow">
        <div className="flex gap-4 mb-4">
          <Button variant={showStats ? "default" : "outline"} onClick={() => setShowStats(v => !v)}>Statistiken</Button>
          <Button variant={showPie ? "default" : "outline"} onClick={() => setShowPie(v => !v)}>Sorten-Verteilung</Button>
          <Button variant={showHeatmap ? "default" : "outline"} onClick={() => setShowHeatmap(v => !v)}>Kalender-Heatmap</Button>
          <Button variant="outline" onClick={() => router.push("/manage")}>Manage</Button>
        </div>
        <h2 className="text-xl font-semibold mb-4">Neuer Eintrag</h2>
        <form className="flex flex-wrap gap-2 items-end" onSubmit={e => { e.preventDefault(); handleAddEntry(); }}>
          <input type="date" className="border rounded px-2 py-1" value={newEntry.date} onChange={e => setNewEntry({ ...newEntry, date: e.target.value })} max={today.toISOString().slice(0, 10)} required />
          <input type="number" className="border rounded px-2 py-1 w-20" min={1} value={newEntry.cups} onChange={e => setNewEntry({ ...newEntry, cups: +e.target.value })} required />
          <select className="border rounded px-2 py-1" value={newEntry.varietyId} onChange={e => setNewEntry({ ...newEntry, varietyId: e.target.value })} required>
            <option value="">Sorte wählen</option>
            {varieties.map(v => <option key={v.$id} value={v.$id}>{v.name}</option>)}
          </select>
          <Button type="submit">Eintrag speichern</Button>
        </form>
      </section>
      <section className="bg-card rounded-lg p-6 shadow">
        <h2 className="text-xl font-semibold mb-4">Deine Einträge</h2>
        <table className="w-full text-left mb-2">
          <thead>
            <tr>
              <th>Datum</th><th>Tassen</th><th>Sorte</th><th></th>
            </tr>
          </thead>
          <tbody>
            {consumptions.map(e => (
              <tr key={e.$id}>
                <td>{e.date ? e.date : <span className="text-muted-foreground italic">Kein Datum</span>}</td>
                <td><input type="number" className="border rounded px-1 py-0.5 w-16" min={1} value={e.cups} onChange={ev => handleUpdateEntry(e.$id, { cups: +ev.target.value })} /></td>
                <td>
                  <select className="border rounded px-1 py-0.5" value={e.varietyId} onChange={ev => handleUpdateEntry(e.$id, { varietyId: ev.target.value })}>
                    {varieties.map(v => <option key={v.$id} value={v.$id}>{v.name}</option>)}
                  </select>
                </td>
                <td><Button size="sm" variant="destructive" onClick={() => handleDeleteEntry(e.$id)}>Löschen</Button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
      {showStats && (
        <section className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="bg-card rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Täglicher Verbrauch</h2>
            <Bar data={barData} options={{ responsive: true, plugins: { legend: { display: false } } }} />
          </div>
          {showPie && <div className="bg-card rounded-lg p-6 shadow">
            <h2 className="text-xl font-semibold mb-4">Sorten-Verteilung</h2>
            <Pie data={pieData} options={{ responsive: true, plugins: { legend: { position: "bottom" } } }} />
          </div>}
        </section>
      )}
      {showHeatmap && (
        <section className="bg-card rounded-lg p-6 shadow">
          <h2 className="text-xl font-semibold mb-4">Kalender-Heatmap</h2>
          <CalendarHeatmap
            startDate={new Date(today.getFullYear(), today.getMonth(), today.getDate() - 119)}
            endDate={today}
            values={heatmapValues}
            classForValue={v => v && v.count ? "react-calendar-heatmap-color-scale-" + Math.min(v.count, 4) : "react-calendar-heatmap-empty"}
            showWeekdayLabels
          />
        </section>
      )}
    </main>
  );
} 
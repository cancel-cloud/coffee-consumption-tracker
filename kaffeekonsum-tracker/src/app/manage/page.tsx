"use client";
import { useEffect, useState } from "react";
import { account, getAllVarieties, addVariety, deleteVariety, getConsumption, deleteConsumption } from "@/lib/appwrite";
import { Button } from "@/components/ui/button";
import FileUpload from "@/components/ui/FileUpload";
import { useRouter } from "next/navigation";

export default function ManagePage() {
  const [user, setUser] = useState<any>(null);
  const [varieties, setVarieties] = useState<any[]>([]);
  const [newVariety, setNewVariety] = useState("");
  const [loading, setLoading] = useState(true);
  const [csv, setCsv] = useState<string>("");
  const [csvFile, setCsvFile] = useState<File | null>(null);
  const [deleteConfirm, setDeleteConfirm] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);
  const router = useRouter();

  useEffect(() => {
    account.get().then(async u => {
      setUser(u);
      // Check admin by ID or by permission (simple: ID match)
      setIsAdmin(u.$id === process.env.NEXT_PUBLIC_ADMIN_ID);
      setVarieties((await getAllVarieties()).documents);
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

  // Admin: Add variety
  const handleAdd = async () => {
    await addVariety(newVariety, "admin");
    setVarieties((await getAllVarieties()).documents);
    setNewVariety("");
  };
  // Admin: Delete variety
  const handleDelete = async (id: string) => {
    await deleteVariety(id);
    setVarieties((await getAllVarieties()).documents);
  };

  // CSV Download
  const handleDownload = () => {
    const csvContent = ["name"].concat(varieties.map(v => v.name)).join("\n");
    const blob = new Blob([csvContent], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "varieties.csv";
    a.click();
    URL.revokeObjectURL(url);
  };
  // CSV Upload
  const handleUpload = async () => {
    if (!csvFile) return;
    const text = await csvFile.text();
    const lines = text.split("\n").filter(Boolean);
    const names = lines.slice(1); // skip header
    for (const name of names) {
      await addVariety(name, "admin");
    }
    setVarieties((await getAllVarieties()).documents);
    setCsvFile(null);
  };

  // Delete all user data
  const handleDeleteData = async () => {
    if (deleteConfirm !== "DELETE" || !user) return;
    const entries = (await getConsumption(user.$id)).documents;
    for (const entry of entries) {
      await deleteConsumption(entry.$id);
    }
    setDeleteConfirm("");
    alert("Alle deine Einträge wurden gelöscht.");
  };

  if (loading) return <div>Lädt...</div>;
  return (
    <main className="max-w-2xl mx-auto py-12 flex flex-col gap-8">
      <h1 className="text-3xl font-bold mb-4">Sorten verwalten</h1>
      {isAdmin ? (
        <>
          <div className="flex gap-2 mb-2">
            <input className="border rounded px-2 py-1" value={newVariety} onChange={e => setNewVariety(e.target.value)} placeholder="Neue Sorte" />
            <Button onClick={handleAdd}>Hinzufügen</Button>
          </div>
          <ul className="mb-4">
            {varieties.map(v => (
              <li key={v.$id} className="flex items-center gap-2 mb-1">
                <span>{v.name}</span>
                <Button size="sm" variant="destructive" onClick={() => handleDelete(v.$id)}>Löschen</Button>
              </li>
            ))}
          </ul>
        </>
      ) : null}
      <div className="flex gap-4 mb-4">
        <Button onClick={handleDownload}>CSV herunterladen</Button>
        <FileUpload accept=".csv" onFileChange={setCsvFile} label="CSV auswählen" />
        <Button onClick={handleUpload} disabled={!csvFile}>CSV hochladen</Button>
      </div>
      <div className="mt-8">
        <h2 className="text-xl font-semibold mb-2">Alle eigenen Einträge löschen</h2>
        <p>Zum Bestätigen <b>DELETE</b> eingeben:</p>
        <input className="border rounded px-2 py-1 mr-2" value={deleteConfirm} onChange={e => setDeleteConfirm(e.target.value)} />
        <Button variant="destructive" onClick={handleDeleteData} disabled={deleteConfirm !== "DELETE"}>Alle Daten löschen</Button>
      </div>
    </main>
  );
} 
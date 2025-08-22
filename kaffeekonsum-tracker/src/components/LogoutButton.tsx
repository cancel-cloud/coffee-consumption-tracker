"use client";
import { Button } from "@/components/ui/button";
import { account } from "@/lib/appwrite";
import { useRouter } from "next/navigation";

export default function LogoutButton({ onLogout }: { onLogout?: () => void }) {
  const router = useRouter();
  const handleLogout = async () => {
    await account.deleteSession("current");
    router.push("/");
    if (onLogout) onLogout();
  };
  return (
    <Button variant="outline" size="sm" className="ml-auto" onClick={handleLogout}>
      Logout
    </Button>
  );
} 
"use client";
import { useEffect, useState } from "react";
import { account } from "@/lib/appwrite";
import LoginButton from "@/components/LoginButton";
import LogoutButton from "@/components/LogoutButton";
import { useRouter, usePathname } from "next/navigation";

export default function SessionButton() {
  const [loggedIn, setLoggedIn] = useState<boolean | null>(null);
  const router = useRouter();
  const pathname = usePathname();
  useEffect(() => {
    account.get().then(
      () => setLoggedIn(true),
      () => setLoggedIn(false)
    );
  }, []);
  const handleLogout = () => {
    setLoggedIn(false);
  };
  if (loggedIn === null) return null;
  if (loggedIn) {
    return (
      <div className="flex gap-2 items-center">
        {(pathname !== "/dashboard") && (pathname === "/manage") && (
          <button className="border rounded px-3 py-1" onClick={() => router.push("/dashboard")}>Dashboard</button>
        )}
        <LogoutButton onLogout={handleLogout} />
      </div>
    );
  }
  return <LoginButton />;
} 
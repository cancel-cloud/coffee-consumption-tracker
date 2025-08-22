"use client";
import { Button } from "@/components/ui/button";
import { account } from "@/lib/appwrite";
import { OAuthProvider } from "appwrite";

export default function LoginButton() {
  const handleLogin = () => {
    account.createOAuth2Session(
      OAuthProvider.Google,
      "http://localhost:3000/dashboard",
      "http://localhost:3000/"
    );
  };
  return (
    <Button variant="outline" size="sm" className="ml-auto" onClick={handleLogin}>
      Login
    </Button>
  );
} 
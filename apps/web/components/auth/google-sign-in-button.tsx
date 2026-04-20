"use client";

import { signIn } from "next-auth/react";
import { useSearchParams } from "next/navigation";
import { useState } from "react";

import { Button } from "@/components/ui/button";

type GoogleSignInButtonProps = {
  className?: string;
};

export function GoogleSignInButton({ className }: GoogleSignInButtonProps) {
  const searchParams = useSearchParams();
  const callbackUrl = searchParams.get("callbackUrl") ?? "/app/dashboard";
  const [pending, setPending] = useState(false);

  return (
    <Button
      type="button"
      className={className}
      disabled={pending}
      onClick={() => {
        setPending(true);
        void signIn("google", { callbackUrl });
      }}
    >
      {pending ? "Redirecting…" : "Continue with Google"}
    </Button>
  );
}

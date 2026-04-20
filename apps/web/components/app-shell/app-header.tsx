import type { Session } from "next-auth";

import { SignOutButton } from "@/components/app-shell/sign-out-button";

type AppHeaderProps = {
  session: Session;
};

export function AppHeader({ session }: AppHeaderProps) {
  const email = session.user?.email ?? "Signed in";
  const name = session.user?.name;

  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b bg-background/80 px-6 backdrop-blur">
      <div className="min-w-0">
        <p className="truncate text-sm font-medium text-foreground">{name ?? email}</p>
        {name ? <p className="truncate text-xs text-muted-foreground">{email}</p> : null}
      </div>
      <SignOutButton />
    </header>
  );
}

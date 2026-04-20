import { auth } from "@/auth";
import { Button } from "@/components/ui/button";
import Link from "next/link";

export default async function HomePage() {
  const session = await auth();

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-8 bg-gradient-to-b from-background to-muted/30 px-6 py-16">
      <div className="max-w-md text-center">
        <p className="text-sm font-medium uppercase tracking-widest text-muted-foreground">Chronos</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-tight text-foreground sm:text-4xl">
          Time and focus, without the noise
        </h1>
        <p className="mt-4 text-muted-foreground">
          Sign in to set your working preferences and open the app. Calendar sync and scheduling arrive in upcoming
          steps.
        </p>
      </div>
      <div className="flex flex-wrap items-center justify-center gap-3">
        {session?.user ? (
          <>
            <Button asChild>
              <Link href="/app/dashboard">Open app</Link>
            </Button>
            {!session.user.onboardingComplete ? (
              <Button variant="outline" asChild>
                <Link href="/onboarding">Complete onboarding</Link>
              </Button>
            ) : null}
          </>
        ) : (
          <Button asChild>
            <Link href="/login">Sign in with Google</Link>
          </Button>
        )}
      </div>
    </main>
  );
}

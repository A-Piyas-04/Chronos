import { auth } from "@/auth";
import { OnboardingForm } from "@/components/onboarding/onboarding-form";
import Link from "next/link";
import { redirect } from "next/navigation";

import { Button } from "@/components/ui/button";

export default async function OnboardingPage() {
  const session = await auth();
  if (!session?.user) {
    redirect("/login?callbackUrl=/onboarding");
  }

  const displayName = session.user.name ?? session.user.email ?? "there";

  return (
    <div className="min-h-screen bg-muted/30 px-4 py-12">
      <div className="mx-auto flex max-w-lg flex-col items-center gap-8">
        <div className="flex w-full max-w-lg justify-end">
          <Button variant="ghost" size="sm" asChild>
            <Link href="/">Home</Link>
          </Button>
        </div>
        <OnboardingForm userName={displayName} />
      </div>
    </div>
  );
}

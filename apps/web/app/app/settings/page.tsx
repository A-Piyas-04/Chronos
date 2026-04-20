import { auth } from "@/auth";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { redirect } from "next/navigation";

export default async function SettingsPage() {
  const session = await auth();
  if (!session?.user) {
    redirect("/login");
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">Account and scheduling preferences.</p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Account</CardTitle>
          <CardDescription>Signed in with Google via Auth.js.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-1 text-sm">
          <p>
            <span className="font-medium text-foreground">Email:</span>{" "}
            <span className="text-muted-foreground">{session.user.email ?? "—"}</span>
          </p>
          <p>
            <span className="font-medium text-foreground">Name:</span>{" "}
            <span className="text-muted-foreground">{session.user.name ?? "—"}</span>
          </p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Scheduling preferences</CardTitle>
          <CardDescription>
            Editing timezone and working hours from this screen will be wired to the Chronos API in a follow-up. Values
            you saved during onboarding are stored on the server once PATCH /users/me exists.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Placeholder — preference form and read-back from the API will land with the settings feature.
          </p>
        </CardContent>
      </Card>
    </div>
  );
}

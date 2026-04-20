import { GoogleSignInButton } from "@/components/auth/google-sign-in-button";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";
import { Suspense } from "react";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-muted/30 px-4 py-12">
      <Card className="w-full max-w-md border-border/80 shadow-sm">
        <CardHeader className="text-center">
          <CardTitle className="text-2xl">Sign in</CardTitle>
          <CardDescription>Use your Google account to continue to Chronos.</CardDescription>
        </CardHeader>
        <CardContent className="flex flex-col gap-4">
          <Suspense
            fallback={
              <Button type="button" className="w-full" disabled>
                Loading…
              </Button>
            }
          >
            <GoogleSignInButton className="w-full" />
          </Suspense>
          <Button variant="ghost" asChild className="w-full text-muted-foreground">
            <Link href="/">Back to home</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}

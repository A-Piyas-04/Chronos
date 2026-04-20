import { NextResponse } from "next/server";

import { auth } from "@/auth";

export default auth((req) => {
  const { nextUrl } = req;
  const isLoggedIn = Boolean(req.auth);
  const onboardingComplete = req.auth?.user?.onboardingComplete ?? false;

  const isApp = nextUrl.pathname.startsWith("/app");
  const isOnboarding = nextUrl.pathname.startsWith("/onboarding");
  const isLogin = nextUrl.pathname.startsWith("/login");
  const isApiAuth = nextUrl.pathname.startsWith("/api/auth");

  if (isApiAuth) {
    return NextResponse.next();
  }

  if (isApp && !isLoggedIn) {
    const url = new URL("/login", nextUrl.origin);
    url.searchParams.set("callbackUrl", `${nextUrl.pathname}${nextUrl.search}`);
    return NextResponse.redirect(url);
  }

  if (isApp && isLoggedIn && !onboardingComplete) {
    return NextResponse.redirect(new URL("/onboarding", nextUrl.origin));
  }

  if (isOnboarding && !isLoggedIn) {
    const url = new URL("/login", nextUrl.origin);
    url.searchParams.set("callbackUrl", "/onboarding");
    return NextResponse.redirect(url);
  }

  if (isOnboarding && isLoggedIn && onboardingComplete) {
    return NextResponse.redirect(new URL("/app/dashboard", nextUrl.origin));
  }

  if (isLogin && isLoggedIn) {
    const dest = onboardingComplete ? "/app/dashboard" : "/onboarding";
    return NextResponse.redirect(new URL(dest, nextUrl.origin));
  }

  return NextResponse.next();
});

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)"],
};

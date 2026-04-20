import type { DefaultSession } from "next-auth";

declare module "next-auth" {
  interface Session {
    user: {
      onboardingComplete: boolean;
    } & DefaultSession["user"];
  }
}

declare module "next-auth/jwt" {
  interface JWT {
    onboardingComplete: boolean;
  }
}

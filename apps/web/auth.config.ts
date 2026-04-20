import type { NextAuthConfig } from "next-auth";
import Google from "next-auth/providers/google";

export default {
  trustHost: true,
  providers: [Google],
  pages: {
    signIn: "/login",
  },
  session: {
    strategy: "jwt",
  },
  callbacks: {
    jwt({ token, user, trigger, session }) {
      if (user) {
        token.onboardingComplete = false;
      }
      if (trigger === "update" && session && typeof session === "object") {
        const s = session as { onboardingComplete?: unknown };
        if (typeof s.onboardingComplete === "boolean") {
          token.onboardingComplete = s.onboardingComplete;
        }
      }
      return token;
    },
    session({ session, token }) {
      if (session.user) {
        session.user.onboardingComplete = Boolean(token.onboardingComplete);
      }
      return session;
    },
  },
} satisfies NextAuthConfig;

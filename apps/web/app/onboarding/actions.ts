"use server";

import { saveUserPreferences } from "@/lib/api/preferences";
import { ApiConfigurationError, ApiError } from "@/lib/api/errors";
import { onboardingFormSchema } from "@/lib/validation/onboarding";
import type { UserPreferencesPayload } from "@/types/preferences";

export type SaveOnboardingResult =
  | { ok: true }
  | { ok: false; error: string; fieldErrors?: Record<string, string[] | undefined> };

export async function saveOnboardingAction(input: unknown): Promise<SaveOnboardingResult> {
  const parsed = onboardingFormSchema.safeParse(input);
  if (!parsed.success) {
    const flat = parsed.error.flatten().fieldErrors;
    return {
      ok: false,
      error: "Please fix the highlighted fields.",
      fieldErrors: flat as Record<string, string[] | undefined>,
    };
  }

  const payload: UserPreferencesPayload = {
    timezone: parsed.data.timezone,
    workday_start_time: `${parsed.data.workday_start_time}:00`,
    workday_end_time: `${parsed.data.workday_end_time}:00`,
    deep_work_start_time: `${parsed.data.deep_work_start_time}:00`,
    deep_work_end_time: `${parsed.data.deep_work_end_time}:00`,
  };

  try {
    await saveUserPreferences(payload);
    return { ok: true };
  } catch (e) {
    if (e instanceof ApiConfigurationError) {
      return { ok: false, error: e.message };
    }
    if (e instanceof ApiError) {
      return {
        ok: false,
        error:
          e.status === 404 || e.status === 405
            ? "The Chronos API does not expose PATCH /users/me yet. Preferences were not saved."
            : `Could not save preferences (${e.status}).`,
      };
    }
    return { ok: false, error: "Something went wrong while saving. Try again." };
  }
}

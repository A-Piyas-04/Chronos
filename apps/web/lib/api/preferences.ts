import { apiPatchJson } from "@/lib/api/client";
import type { UserPreferencesPayload } from "@/types/preferences";

/**
 * Persist scheduling preferences for the current user.
 * Backend route is not implemented yet; this targets PATCH /users/me as planned in Phase 1.
 */
export async function saveUserPreferences(payload: UserPreferencesPayload): Promise<void> {
  await apiPatchJson("/users/me", payload);
}

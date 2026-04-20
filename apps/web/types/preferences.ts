/**
 * Payload sent to the Chronos API when saving scheduling preferences
 * (aligns with `UserPreference` / PATCH user profile on the backend).
 */
export type UserPreferencesPayload = {
  timezone: string;
  workday_start_time: string;
  workday_end_time: string;
  deep_work_start_time: string;
  deep_work_end_time: string;
};

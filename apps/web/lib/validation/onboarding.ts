import { z } from "zod";

const timeString = z
  .string()
  .regex(/^\d{2}:\d{2}$/, "Use a valid time (HH:MM)")
  .refine((v) => {
    const [h, m] = v.split(":").map(Number);
    return h >= 0 && h <= 23 && m >= 0 && m <= 59;
  }, "Invalid time");

const ianaTimezone = z.string().min(1, "Choose a timezone").refine((tz) => {
  try {
    Intl.DateTimeFormat(undefined, { timeZone: tz });
    return true;
  } catch {
    return false;
  }
}, "Invalid IANA timezone");

export const onboardingFormSchema = z
  .object({
    timezone: ianaTimezone,
    workday_start_time: timeString,
    workday_end_time: timeString,
    deep_work_start_time: timeString,
    deep_work_end_time: timeString,
  })
  .refine((data) => data.workday_start_time < data.workday_end_time, {
    message: "Workday end must be after workday start",
    path: ["workday_end_time"],
  })
  .refine((data) => data.deep_work_start_time < data.deep_work_end_time, {
    message: "Deep work end must be after deep work start",
    path: ["deep_work_end_time"],
  });

export type OnboardingFormValues = z.infer<typeof onboardingFormSchema>;

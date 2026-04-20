"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useSession } from "next-auth/react";
import { useRouter } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { Controller, useForm } from "react-hook-form";

import { saveOnboardingAction } from "@/app/onboarding/actions";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select } from "@/components/ui/select";
import { getSortedTimeZones } from "@/lib/timezones";
import { onboardingFormSchema, type OnboardingFormValues } from "@/lib/validation/onboarding";

type OnboardingFormProps = {
  userName: string;
};

export function OnboardingForm({ userName }: OnboardingFormProps) {
  const router = useRouter();
  const { update } = useSession();
  const timezones = useMemo(() => getSortedTimeZones(), []);
  const [formError, setFormError] = useState<string | null>(null);

  const form = useForm<OnboardingFormValues>({
    resolver: zodResolver(onboardingFormSchema),
    defaultValues: {
      timezone: "UTC",
      workday_start_time: "09:00",
      workday_end_time: "17:00",
      deep_work_start_time: "08:00",
      deep_work_end_time: "12:00",
    },
  });

  const {
    control,
    handleSubmit,
    register,
    setValue,
    formState: { errors, isSubmitting },
  } = form;

  useEffect(() => {
    const tz = Intl.DateTimeFormat().resolvedOptions().timeZone;
    setValue("timezone", tz, { shouldValidate: true });
  }, [setValue]);

  async function onSubmit(values: OnboardingFormValues) {
    setFormError(null);
    const result = await saveOnboardingAction(values);
    if (!result.ok) {
      setFormError(result.error);
      return;
    }
    await update({ onboardingComplete: true });
    router.push("/app/dashboard");
    router.refresh();
  }

  return (
    <Card className="w-full max-w-lg border-border/80 shadow-sm">
      <CardHeader>
        <CardTitle>Welcome, {userName}</CardTitle>
        <CardDescription>
          Set your timezone and working hours so Chronos can schedule work blocks accurately. You can change these
          later in settings.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form className="space-y-6" onSubmit={handleSubmit(onSubmit)} noValidate>
          {formError ? (
            <p className="rounded-md border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive">
              {formError}
            </p>
          ) : null}

          <div className="space-y-2">
            <Label htmlFor="timezone">Timezone</Label>
            <Controller
              name="timezone"
              control={control}
              render={({ field }) => (
                <Select
                  id="timezone"
                  value={field.value}
                  onChange={(e) => field.onChange(e.target.value)}
                  onBlur={field.onBlur}
                  ref={field.ref}
                  aria-invalid={Boolean(errors.timezone)}
                  aria-describedby="tz-hint"
                >
                  {timezones.map((tz) => (
                    <option key={tz} value={tz}>
                      {tz}
                    </option>
                  ))}
                </Select>
              )}
            />
            <p id="tz-hint" className="text-xs text-muted-foreground">
              Used to interpret your working hours in your local day.
            </p>
            {errors.timezone ? (
              <p className="text-sm text-destructive" role="alert">
                {errors.timezone.message}
              </p>
            ) : null}
          </div>

          <fieldset className="space-y-3 rounded-md border p-4">
            <legend className="px-1 text-sm font-medium">Workday</legend>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="workday_start_time">Start</Label>
                <Input
                  id="workday_start_time"
                  type="time"
                  step={60}
                  aria-invalid={Boolean(errors.workday_start_time)}
                  {...register("workday_start_time")}
                />
                {errors.workday_start_time ? (
                  <p className="text-sm text-destructive" role="alert">
                    {errors.workday_start_time.message}
                  </p>
                ) : null}
              </div>
              <div className="space-y-2">
                <Label htmlFor="workday_end_time">End</Label>
                <Input
                  id="workday_end_time"
                  type="time"
                  step={60}
                  aria-invalid={Boolean(errors.workday_end_time)}
                  {...register("workday_end_time")}
                />
                {errors.workday_end_time ? (
                  <p className="text-sm text-destructive" role="alert">
                    {errors.workday_end_time.message}
                  </p>
                ) : null}
              </div>
            </div>
          </fieldset>

          <fieldset className="space-y-3 rounded-md border p-4">
            <legend className="px-1 text-sm font-medium">Preferred deep work window</legend>
            <p className="text-xs text-muted-foreground">
              When you prefer longer focus blocks scheduled (subject to your calendar in later phases).
            </p>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <div className="space-y-2">
                <Label htmlFor="deep_work_start_time">Start</Label>
                <Input
                  id="deep_work_start_time"
                  type="time"
                  step={60}
                  aria-invalid={Boolean(errors.deep_work_start_time)}
                  {...register("deep_work_start_time")}
                />
                {errors.deep_work_start_time ? (
                  <p className="text-sm text-destructive" role="alert">
                    {errors.deep_work_start_time.message}
                  </p>
                ) : null}
              </div>
              <div className="space-y-2">
                <Label htmlFor="deep_work_end_time">End</Label>
                <Input
                  id="deep_work_end_time"
                  type="time"
                  step={60}
                  aria-invalid={Boolean(errors.deep_work_end_time)}
                  {...register("deep_work_end_time")}
                />
                {errors.deep_work_end_time ? (
                  <p className="text-sm text-destructive" role="alert">
                    {errors.deep_work_end_time.message}
                  </p>
                ) : null}
              </div>
            </div>
          </fieldset>

          <Button type="submit" className="w-full" disabled={isSubmitting}>
            {isSubmitting ? "Saving…" : "Save and continue"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}

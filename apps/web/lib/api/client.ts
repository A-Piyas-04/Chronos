import { ApiConfigurationError, ApiError } from "@/lib/api/errors";

function resolveBaseUrl(): string {
  const raw = process.env.NEXT_PUBLIC_API_URL?.trim();
  if (!raw) {
    throw new ApiConfigurationError(
      "Set NEXT_PUBLIC_API_URL in the environment (e.g. http://localhost:8000).",
    );
  }
  return raw.replace(/\/$/, "");
}

export async function apiFetch(path: string, init: RequestInit = {}): Promise<Response> {
  const base = resolveBaseUrl();
  const url = `${base}${path.startsWith("/") ? path : `/${path}`}`;
  const headers = new Headers(init.headers);
  if (init.body !== undefined && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const response = await fetch(url, {
    ...init,
    headers,
    cache: "no-store",
  });

  if (!response.ok) {
    const text = await response.text();
    throw new ApiError(`Request failed (${response.status})`, response.status, text);
  }

  return response;
}

export async function apiPatchJson<TBody extends object>(path: string, body: TBody): Promise<void> {
  await apiFetch(path, { method: "PATCH", body: JSON.stringify(body) });
}

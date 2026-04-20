export class ApiError extends Error {
  constructor(
    message: string,
    public readonly status: number,
    public readonly body?: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class ApiConfigurationError extends Error {
  constructor(message = "Chronos API base URL is not configured") {
    super(message);
    this.name = "ApiConfigurationError";
  }
}

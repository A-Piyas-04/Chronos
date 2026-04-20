export default function TasksPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-2">
      <h1 className="text-2xl font-semibold tracking-tight">Tasks</h1>
      <p className="text-muted-foreground">
        The task inbox will be implemented in a later phase. This page confirms navigation and layout only.
      </p>
      <div className="mt-8 rounded-lg border border-dashed border-muted-foreground/30 bg-muted/20 p-8 text-center text-sm text-muted-foreground">
        No tasks yet.
      </div>
    </div>
  );
}

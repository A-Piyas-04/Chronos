export default function DashboardPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-2">
      <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
      <p className="text-muted-foreground">
        Weekly calendar and imported events will appear here in a later phase. For now, use the sidebar to explore the
        app shell.
      </p>
      <div className="mt-8 rounded-lg border border-dashed border-muted-foreground/30 bg-muted/20 p-8 text-center text-sm text-muted-foreground">
        Empty state — nothing scheduled yet.
      </div>
    </div>
  );
}

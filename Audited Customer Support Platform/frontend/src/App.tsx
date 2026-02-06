import AppLayout from "./layout/AppLayout";
import Dashboard from "./pages/Dashboard";
import AgentDetail from "./pages/AgentDetail";

function App() {
  const path = window.location.pathname;

  let page = <Dashboard />;

  if (path.startsWith("/agents/")) {
    page = <AgentDetail />;
  }

  return <AppLayout>{page}</AppLayout>;
}

export default App;

import GovernanceSummary from "../components/GovernanceSummary";
import AgentLeaderboard from "../components/AgentLeaderboarder";
import styles from "./Dashboard.module.css";

export default function Dashboard() {
  return (
    <div>
      <h1 className={styles.heading}>Governance Overview</h1>
      <p className={styles.subtext}>
        System-wide quality and risk intelligence.
      </p>

      <GovernanceSummary />
      <AgentLeaderboard />
    </div>
  );
}



import { useEffect, useState } from "react";
import { fetchAgentLeaderboard } from "../lib/api";
import styles from "./AgentLeaderboard.module.css";

export default function AgentLeaderboard() {
    const [agents, setAgents] = useState<any[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchAgentLeaderboard()
            .then(setAgents)
            .catch(() => setError("Failed to load agent leaderboard"));
    }, []);

    if (error) return <div>{error}</div>;

    return (
        <div className={styles.wrapper}>
            <h2 className={styles.heading}>Agent Leaderboard</h2>

            <table className={styles.table}>
                <thead>
                    <tr>
                        <th>Agent</th>
                        <th>Score</th>
                        <th>Success</th>
                        <th>CCS</th>
                        <th>False Conf.</th>
                        <th>Catastrophic</th>
                        <th>Recovery</th>
                    </tr>
                </thead>

                <tbody>
                    {agents.map((agent) => (
                        <tr
                            key={agent.agent_id}
                            onClick={() => window.location.href = `/agents/${agent.agent_id}`}
                            style={{ cursor: "pointer" }}
                        >
                            <td>{agent.agent_id}</td>
                            <td>{agent.score}</td>
                            <td>{agent.successes}</td>
                            <td>{agent.ccs}</td>
                            <td>{agent.false_confidence}</td>
                            <td
                                className={
                                    agent.catastrophic_failures > 0 ? styles.danger : ""
                                }
                            >
                                {agent.catastrophic_failures}
                            </td>
                            <td className={agent.recovery > 0 ? styles.success : ""}>
                                {agent.recovery}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

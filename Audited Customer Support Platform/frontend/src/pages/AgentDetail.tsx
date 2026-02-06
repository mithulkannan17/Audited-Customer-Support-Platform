import { useEffect, useState } from "react";

export default function AgentDetail() {
    const agentId = window.location.pathname.split("/").pop();
    const [failures, setFailures] = useState<any[]>([]);
    const [error, setError] = useState("");

    useEffect(() => {
        fetch(
            `http://127.0.0.1:8000/api/v1/analytics/agents/${agentId}/failures`
        )
            .then((res) => res.json())
            .then(setFailures)
            .catch(() => setError("Failed to load agent details"));
    }, [agentId]);

    return (
        <div>
            <h1 style={{ fontSize: "22px", marginBottom: "8px" }}>
                Agent: {agentId}
            </h1>

            <p style={{ color: "#94a3b8", marginBottom: "24px" }}>
                Failure and risk breakdown
            </p>

            {error && <div>{error}</div>}

            <table
                style={{
                    width: "100%",
                    background: "#020617",
                    border: "1px solid #1e293b",
                    borderRadius: "8px",
                }}
            >
                <thead>
                    <tr>
                        <th style={{ padding: "12px" }}>Event Type</th>
                        <th style={{ padding: "12px" }}>Count</th>
                    </tr>
                </thead>
                <tbody>
                    {failures.map((f) => (
                        <tr key={f.event_type}>
                            <td style={{ padding: "12px" }}>{f.event_type}</td>
                            <td style={{ padding: "12px" }}>{f.count}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

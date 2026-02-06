import { useEffect, useState } from "react";
import { fetchGovernanceSummary } from "../lib/api";
import MetricCard from "./MetricCard";
import styles from "./GovernanceSummary.module.css";

export default function GovernanceSummary() {
    const [data, setData] = useState<any>(null);
    const [error, setError] = useState("");

    useEffect(() => {
        fetchGovernanceSummary()
            .then(setData)
            .catch(() => setError("Failed to load governance summary"));
    }, []);

    if (error) return <div>{error}</div>;
    if (!data) return <div>Loading summary…</div>;

    return (
        <div className={styles.grid}>
            <MetricCard
                title="CATASTROPHIC FAILURES"
                value={data.catastrophic_failures}
                tone="danger"
            />
            <MetricCard
                title="TRAINING EXCLUSIONS"
                value={data.training_exclusions}
            />
            <MetricCard
                title="RECOVERIES"
                value={data.recoveries}
                tone="success"
            />
            <MetricCard
                title="ACTIVE AGENTS"
                value={data.active_agents ?? 1}
            />
        </div>
    );
}

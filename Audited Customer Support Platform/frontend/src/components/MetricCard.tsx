import styles from "./MetricCard.module.css";

interface MetricCardProps {
    title: string;
    value: number;
    tone?: "neutral" | "danger" | "success";
}

export default function MetricCard({
    title,
    value,
    tone = "neutral",
}: MetricCardProps) {
    return (
        <div className={`${styles.card} ${styles[tone]}`}>
            <div className={styles.title}>{title}</div>
            <div className={styles.value}>{value}</div>
        </div>
    );
}

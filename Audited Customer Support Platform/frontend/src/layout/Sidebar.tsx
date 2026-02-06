import styles from "./Sidebar.module.css";

export default function Sidebar() {
    return (
        <aside className={styles.sidebar}>
            <div className={styles.title}>AI Governance</div>

            <nav className={styles.nav}>
                <div className={styles.item}>Dashboard</div>
                <div className={styles.item}>Agents</div>
                <div className={styles.item}>Governance</div>
            </nav>
        </aside>
    );
}

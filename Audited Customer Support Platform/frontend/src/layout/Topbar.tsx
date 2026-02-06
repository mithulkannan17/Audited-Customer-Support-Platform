import styles from "./Topbar.module.css";

export default function Topbar() {
  return (
    <header className={styles.topbar}>
      <span>Agent Quality Intelligence</span>
      <span className={styles.env}>Production · v1</span>
    </header>
  );
}

const BASE_URL = "http://127.0.0.1:8000/api/v1";

export async function fetchGovernanceSummary() {
    const res = await fetch(`${BASE_URL}/analytics/governance-summary`);
    if (!res.ok) {
        throw new Error("Failed to fetch governance summary");
    }
    return res.json();
}

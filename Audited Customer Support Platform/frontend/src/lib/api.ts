const BASE_URL = "http://127.0.0.1:8000/api/v1";
const ROLE = "admin";

export async function fetchGovernanceSummary() {
    return apiFetch(`${BASE_URL}/analytics/governance-summary`);
}

export async function fetchAgentLeaderboard() {
    return apiFetch(`${BASE_URL}/analytics/leaderboard`);
}

export async function apiFetch(url: string) {
    const res = await fetch(url, {
        headers: {
            "x-role": ROLE,
        },
    });

    if (!res.ok) {
        throw new Error("API error");
    }

    return res.json();
}
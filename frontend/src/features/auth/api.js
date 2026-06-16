const BASE_URL = import.meta.env.VITE_API_URL;

export const login = async (email, password) => {
    const res = await fetch(`${BASE_URL}/users/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "ログイン失敗");
    }

    return data;
};



export const register = async (email, password, role) => {
    const res = await fetch(`${BASE_URL}/users/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password, role }),
    });

    const data = await res.json();

    if (!res.ok) {
        throw new Error(data.detail || "登録失敗");
    }

    return data;
};
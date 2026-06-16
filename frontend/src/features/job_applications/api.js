import axios from "axios";

const API = import.meta.env.VITE_API_URL;

// 共通ヘッダー
const authHeader = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
});

// =========================
// 応募作成
// =========================
export const createJobApplication = async (jobPostingId, message = "") => {
    const res = await axios.post(
        `${API}/job-applications`,
        {
            job_posting_id: jobPostingId,
            message,
        },
        authHeader()
    );

    return res.data;
};

// =========================
// 自分の応募一覧
// =========================
export const getMyApplications = async () => {
    const res = await axios.get(
        `${API}/job-applications/me`,
        authHeader()
    );

    return res.data;
};

// =========================
// 応募詳細
// =========================
export const getApplication = async (id) => {
    const res = await axios.get(
        `${API}/job-applications/${id}`,
        authHeader()
    );

    return res.data;
};

// =========================
// 応募削除
// =========================
export const deleteApplication = async (id) => {
    const res = await axios.delete(
        `${API}/job-applications/${id}`,
        authHeader()
    );

    return res.data;
};
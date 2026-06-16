import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const authHeader = () => ({
    headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
});

// 一覧
export const getJobPostings = async () => {
    const res = await axios.get(`${API}/job-postings`, authHeader());
    return res.data;
};

// 単体
export const getJobPosting = async (id) => {
    const res = await axios.get(`${API}/job-postings/${id}`, authHeader());
    return res.data;
};

// 作成
export const createJobPosting = async (data) => {
    const res = await axios.post(`${API}/job-postings`, data, authHeader());
    return res.data;
};

// 企業別
export const getJobPostingsByOrg = async (organizationId) => {
    const res = await axios.get(
        `${API}/job-postings/organization/${organizationId}`,
        authHeader()
    );
    return res.data;
};
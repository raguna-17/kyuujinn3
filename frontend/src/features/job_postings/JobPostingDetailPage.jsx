import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getJobPosting } from "./api";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const JobPostingDetailPage = () => {
    const { id } = useParams();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchJob = async () => {
        try {
            const data = await getJobPosting(id);
            setJob(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchJob();
    }, [id]);

    const applyJob = async () => {
        try {
            await axios.post(
                `${API}/job-applications`,
                {
                    job_posting_id: Number(id),
                    message: "応募します"
                },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem("token")}`,
                    },
                }
            );

            alert("応募しました");
        } catch (e) {
            alert("応募失敗");
        }
    };

    if (loading) return <p>読み込み中...</p>;
    if (!job) return <p>求人が見つかりません</p>;

    return (
        <div>
            <h1>求人詳細</h1>

            <p>{job.description}</p>
            <p>{job.salary}円</p>

            <button onClick={applyJob}>
                応募する
            </button>
        </div>
    );
};

export default JobPostingDetailPage;
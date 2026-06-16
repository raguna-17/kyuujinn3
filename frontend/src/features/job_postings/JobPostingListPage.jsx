import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { getJobPostings } from "./api";

const JobPostingListPage = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        try {
            const data = await getJobPostings();
            setJobs(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    if (loading) return <p>読み込み中...</p>;

    return (
        <div>
            <h1>求人一覧</h1>

            <ul>
                {jobs.map((job) => (
                    <li key={job.id}>
                        <Link to={`/jobs/${job.id}`}>
                            {job.description} / {job.salary}円
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default JobPostingListPage;
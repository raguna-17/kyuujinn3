import { useEffect, useState } from "react";
import axios from "axios";

const API = import.meta.env.VITE_API_URL;

const ApplicationListPage = () => {
    const [apps, setApps] = useState([]);

    const fetchApps = async () => {
        const res = await axios.get(
            `${API}/job-applications/me`,
            {
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("token")}`,
                },
            }
        );

        setApps(res.data);
    };

    useEffect(() => {
        fetchApps();
    }, []);

    return (
        <div>
            <h1>応募履歴</h1>

            <ul>
                {apps.map((a) => (
                    <li key={a.id}>
                        求人ID: {a.job_posting_id} / 状態: {a.status}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default ApplicationListPage;
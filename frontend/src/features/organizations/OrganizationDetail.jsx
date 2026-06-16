import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { getOrganization } from "./api";

const OrganizationDetail = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    const [org, setOrg] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchData = async () => {
        try {
            const data = await getOrganization(id);
            setOrg(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, [id]);

    if (loading) return <p>読み込み中...</p>;
    if (!org) return <p>データなし</p>;

    return (
        <div>
            <h1>企業詳細</h1>

            <h2>{org.name}</h2>

            <p>資本金: {org.capital}</p>
            <p>所在地: {org.location}</p>
            <p>従業員数: {org.employee_count}</p>
            <p>設立年: {org.founded_year}</p>
            <p>代表者: {org.ceo_name}</p>

            {/* 求人作成導線 */}
            <button
                onClick={() => navigate("/jobs/new", { state: { organizationId: org.id } })}
            >
                求人票作成
            </button>

            <br />

            <Link to="/organizations">
                ← 一覧へ戻る
            </Link>
        </div>
    );
};

export default OrganizationDetail;
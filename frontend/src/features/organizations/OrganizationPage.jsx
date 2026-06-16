import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { getOrganizations, createOrganization } from "./api";

const OrganizationPage = () => {
    const navigate = useNavigate();

    const [orgs, setOrgs] = useState([]);
    const [loading, setLoading] = useState(true);

    const [form, setForm] = useState({
        name: "",
        capital: "",
        location: "",
        employee_count: "",
        founded_year: "",
        ceo_name: "",
    });

    const fetchData = async () => {
        try {
            const data = await getOrganizations();
            setOrgs(data);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchData();
    }, []);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        const payload = {
            ...form,
            capital: Number(form.capital),
            employee_count: Number(form.employee_count),
            founded_year: Number(form.founded_year),
        };

        await createOrganization(payload);

        setForm({
            name: "",
            capital: "",
            location: "",
            employee_count: "",
            founded_year: "",
            ceo_name: "",
        });

        fetchData();
    };

    if (loading) return <p>読み込み中...</p>;

    return (
        <div>
            <h1>企業作成</h1>

            {/* 作成フォーム */}
            <form onSubmit={handleSubmit}>
                <input name="name" placeholder="企業名" onChange={handleChange} value={form.name} />
                <input name="capital" placeholder="資本金" onChange={handleChange} value={form.capital} />
                <input name="location" placeholder="所在地" onChange={handleChange} value={form.location} />
                <input name="employee_count" placeholder="従業員数" onChange={handleChange} value={form.employee_count} />
                <input name="founded_year" placeholder="設立年" onChange={handleChange} value={form.founded_year} />
                <input name="ceo_name" placeholder="代表者名" onChange={handleChange} value={form.ceo_name} />

                <button type="submit">作成</button>
            </form>

            <h2>企業一覧</h2>

            <ul>
                {orgs.map((org) => (
                    <li key={org.id}>
                        <Link to={`/organizations/${org.id}`}>
                            {org.name}
                        </Link>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default OrganizationPage;
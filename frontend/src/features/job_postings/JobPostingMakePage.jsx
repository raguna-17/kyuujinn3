import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { createJobPosting } from "./api";

const JobPostingMakePage = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const organizationId = location.state?.organizationId;

    const [form, setForm] = useState({
        description: "",
        salary: "",
        employment_type: "full_time",
    });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!organizationId) {
            alert("企業情報がありません");
            return;
        }

        try {
            await createJobPosting({
                organization_id: organizationId,
                description: form.description,
                salary: Number(form.salary),
                employment_type: form.employment_type,
            });

            alert("求人票を作成しました");

            navigate("/jobs");
        } catch (err) {
            console.error(err);
            alert("作成に失敗しました");
        }
    };

    return (
        <div>
            <h1>求人作成</h1>

            <form onSubmit={handleSubmit}>
                <input
                    name="description"
                    placeholder="仕事内容"
                    value={form.description}
                    onChange={handleChange}
                />

                <input
                    name="salary"
                    placeholder="給与"
                    value={form.salary}
                    onChange={handleChange}
                />

                <select
                    name="employment_type"
                    value={form.employment_type}
                    onChange={handleChange}
                >
                    <option value="full_time">正社員</option>
                    <option value="part_time">アルバイト</option>
                    <option value="contract">契約社員</option>
                    <option value="intern">インターン</option>
                </select>

                <button type="submit">作成</button>
            </form>
        </div>
    );
};

export default JobPostingMakePage;
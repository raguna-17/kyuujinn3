import { Link } from "react-router-dom";

const Sidebar = ({ role }) => {
    return (
        <div style={{ width: "220px", padding: "16px", borderRight: "1px solid #ddd" }}>

            <h3>Menu</h3>

            {/* USER */}
            {role === "USER" && (
                <>
                    <Link to="/jobs">求人一覧</Link><br />
                    <Link to="/applications">応募一覧</Link>
                </>
            )}

            {/* COMPANY */}
            {role === "COMPANY" && (
                <>
                    <Link to="/organizations">企業管理</Link><br />
                    <Link to="/jobs/new">求人作成</Link><br />
                </>
            )}

            {/* ADMIN */}
            {role === "ADMIN" && (
                <>
                    <Link to="/jobs">求人管理</Link><br />
                    <Link to="/organizations">企業管理</Link><br />
                    <Link to="/applications">応募管理</Link><br />
                </>
            )}

        </div>
    );
};

export default Sidebar;
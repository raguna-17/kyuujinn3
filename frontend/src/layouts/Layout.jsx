import { Outlet, useNavigate } from "react-router-dom";
import { useEffect } from "react";
import Sidebar from "./Sidebar";
import Header from "./Header";

const Layout = () => {
    const navigate = useNavigate();

    const token = localStorage.getItem("token");
    const role = localStorage.getItem("role");

    useEffect(() => {
        if (!token) {
            navigate("/login");
        }
    }, [token, navigate]);

    if (!token) return null;

    return (
        <div style={{ display: "flex", minHeight: "100vh" }}>
            <Sidebar role={role} />

            <div style={{ flex: 1, display: "flex", flexDirection: "column" }}>
                <Header role={role} onLogout={() => {
                    localStorage.removeItem("token");
                    localStorage.removeItem("role");
                    navigate("/login");
                }} />

                <main style={{ flex: 1, padding: "16px" }}>
                    <Outlet />
                </main>
            </div>
        </div>
    );
};

export default Layout;
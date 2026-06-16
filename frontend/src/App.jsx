import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Layout from "./layouts/Layout";

import LoginPage from "./features/auth/LoginPage";
import RegisterPage from "./features/auth/RegisterPage";

import JobPostingListPage from "./features/job_postings/JobPostingListPage";
import JobPostingDetailPage from "./features/job_postings/JobPostingDetailPage";
import JobPostingMakePage from "./features/job_postings/JobPostingMakePage";

import ApplicationListPage from "./features/job_applications/ApplicationListPage";

import OrganizationPage from "./features/organizations/OrganizationPage";
import OrganizationDetail from "./features/organizations/OrganizationDetail";

const isAuthenticated = () => !!localStorage.getItem("token");
const getRole = () => localStorage.getItem("role");

// 認証ガード
const PrivateRoute = ({ children }) => {
  return isAuthenticated() ? children : <Navigate to="/login" />;
};

// 権限制御（ADMINは全通過）
const RoleRoute = ({ roles, children }) => {
  const role = getRole();
  const token = localStorage.getItem("token");

  console.log("role:", role);
  console.log("token:", token);

  if (!token) return <Navigate to="/login" />;
  if (!role) return <Navigate to="/login" />;

  if (role === "ADMIN") return children;

  return roles.includes(role) ? children : <Navigate to="/" />;
};

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* 認証前 */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        {/* 共通レイアウト */}
        <Route
          path="/"
          element={
            <PrivateRoute>
              <Layout />
            </PrivateRoute>
          }
        >

          {/* ===================== */}
          {/* JOBS（USER + COMPANY + ADMIN） */}
          {/* ===================== */}
          <Route
            path="jobs"
            element={
              <RoleRoute roles={["USER"]}>
                <JobPostingListPage />
              </RoleRoute>
            }
          />

          <Route
            path="jobs/:id"
            element={
              <RoleRoute roles={["USER"]}>
                <JobPostingDetailPage />
              </RoleRoute>
            }
          />

          <Route
            path="jobs/new"
            element={
              <RoleRoute roles={["COMPANY"]}>
                <JobPostingMakePage />
              </RoleRoute>
            }
          />

          {/* ===================== */}
          {/* APPLICATIONS（USER + ADMIN） */}
          {/* ===================== */}
          <Route
            path="applications"
            element={
              <RoleRoute roles={["USER"]}>
                <ApplicationListPage />
              </RoleRoute>
            }
          />

          {/* ===================== */}
          {/* ORGANIZATIONS（COMPANY + ADMIN） */}
          {/* ===================== */}
          <Route
            path="organizations"
            element={
              <RoleRoute roles={["COMPANY"]}>
                <OrganizationPage />
              </RoleRoute>
            }
          />

          <Route
            path="organizations/:id"
            element={
              <RoleRoute roles={["COMPANY"]}>
                <OrganizationDetail />
              </RoleRoute>
            }
          />

        </Route>

        {/* fallback */}
        <Route path="*" element={<Navigate to="/login" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
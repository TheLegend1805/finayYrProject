import React from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "../AuthContext/AuthContext.jsx";

const PrivateRoutes = () => {
  const { authToken } = useAuth();

  return authToken ? <Outlet /> : <Navigate to="/patient-login" />;
};

export default PrivateRoutes;

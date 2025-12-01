import { createContext, useContext, useState, useEffect } from "react";
import apiClient from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [access, setAccess] = useState(localStorage.getItem("access"));
  const [refresh, setRefresh] = useState(localStorage.getItem("refresh"));

  useEffect(() => {
    if (access) {
      localStorage.setItem("access", access);
    } else {
      localStorage.removeItem("access");
    }
    if (refresh) {
      localStorage.setItem("refresh", refresh);
    } else {
      localStorage.removeItem("refresh");
    }
  }, [access, refresh]);

  const login = async (email, password) => {
    const res = await apiClient.post("/auth/login/", { email, password });
    setAccess(res.data.access);
    setRefresh(res.data.refresh);
    // 유저 정보까지 필요하면 여기서 /auth/login/<nickname>/ 같은 프로필 API 한 번 더 호출해도 됨
  };

  const logout = async () => {
    try {
      if (refresh) {
        await apiClient.post("/auth/logout/", { refresh });
      }
    } catch (err) {
      console.error(err);
    } finally {
      setAccess(null);
      setRefresh(null);
      setUser(null);
    }
  };

  const value = {
    user,
    setUser,
    access,
    refresh,
    login,
    logout,
    isAuthenticated: !!access,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}

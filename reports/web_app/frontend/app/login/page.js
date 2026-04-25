"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Login() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState("patient"); // default role selection
  const [error, setError] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      // Send login request to backend endpoint (/auth/login)
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/login",
        new URLSearchParams({ username, password, role })
      );
      // For simplicity, both roles are directed to the chatbot page; you can adjust based on your logic.
      router.push("/chatbot");
    } catch (err) {
      setError(err.response?.data.detail || "Login failed");
    }
  };

  return (
    <main style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Login</h1>
      <form
        onSubmit={handleLogin}
        style={{ display: "flex", flexDirection: "column", alignItems: "center" }}
      >
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          style={{ padding: "10px", margin: "10px", width: "80%" }}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={{ padding: "10px", margin: "10px", width: "80%" }}
        />

        <div style={{ margin: "10px", textAlign: "left", width: "80%" }}>
          <p>Select your role:</p>
          <label style={{ marginRight: "10px" }}>
            <input
              type="radio"
              name="role"
              value="patient"
              checked={role === "patient"}
              onChange={() => setRole("patient")}
            />{" "}
            Patient
          </label>
          <label>
            <input
              type="radio"
              name="role"
              value="doctor"
              checked={role === "doctor"}
              onChange={() => setRole("doctor")}
            />{" "}
            Doctor
          </label>
        </div>

        {error && <p style={{ color: "red" }}>{error}</p>}
        <button type="submit" style={{ padding: "10px 20px", marginTop: "10px", cursor: "pointer" }}>
          Login
        </button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        Don't have an account? <a href="/signup">Sign up here</a>.
      </p>
    </main>
  );
}

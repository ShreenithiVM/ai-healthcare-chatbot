"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";

export default function Signup() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [role, setRole] = useState("patient"); // default selection
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (password !== confirm) {
      setError("Passwords do not match.");
      return;
    }
    try {
      // Send signup request to backend endpoint (/auth/signup)
      const response = await axios.post(
        "http://127.0.0.1:8000/auth/signup",
        new URLSearchParams({ username, password, role })
      );
      setSuccess(response.data.message || "Signup successful!");
      // Redirect after a short delay
      setTimeout(() => router.push("/login"), 2000);
    } catch (err) {
      setError(err.response?.data.detail || "Signup failed");
    }
  };

  return (
    <main style={{ padding: "2rem", textAlign: "center" }}>
      <h1>Sign Up</h1>
      <form
        onSubmit={handleSignup}
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
        <input
          type="password"
          placeholder="Confirm Password"
          value={confirm}
          onChange={(e) => setConfirm(e.target.value)}
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
        {success && <p style={{ color: "green" }}>{success}</p>}
        <button
          type="submit"
          style={{ padding: "10px 20px", marginTop: "10px", cursor: "pointer" }}
        >
          Sign Up
        </button>
      </form>
      <p style={{ marginTop: "1rem" }}>
        Already have an account? <a href="/login">Login here</a>.
      </p>
    </main>
  );
}

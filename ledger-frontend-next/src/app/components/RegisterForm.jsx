import { useState } from "react";
import { useRouter } from "next/router";

export default function RegisterForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [fullName, setFullName] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      const res = await fetch("http://127.0.0.1:8000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, full_name: fullName, password }),
      });

      if (!res.ok) {
        const errorData = await res.json();
        alert(errorData.detail || "Registration failed");
        return;
      }

      alert("Registration successful! Please login.");
      router.push("/");
    } catch (error) {
      alert("Error occurred during registration");
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: "auto" }}>
      <h2>Register</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
        required
        style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
      />
      <input
        type="text"
        placeholder="Full Name"
        value={fullName}
        onChange={e => setFullName(e.target.value)}
        required
        style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        required
        style={{ display: "block", width: "100%", marginBottom: 10, padding: 8 }}
      />
      <button type="submit" style={{ padding: 10, width: "100%" }}>Register</button>
    </form>
  );
}

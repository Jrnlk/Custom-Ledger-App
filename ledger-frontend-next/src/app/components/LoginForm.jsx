import { useState } from "react";
import { useRouter } from "next/router";

export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    try {
      const res = await fetch("http://127.0.0.1:8000/token", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: formData,
      });

      if (!res.ok) {
        const errorData = await res.json();
        alert(errorData.detail || "Login failed");
        return;
      }

      const data = await res.json();
      localStorage.setItem("token", data.access_token);
      router.push("/dashboard");
    } catch (error) {
      alert("Error occurred when logging in");
    }
  }

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: "auto" }}>
      <h2>Login</h2>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={e => setEmail(e.target.value)}
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
      <button type="submit" style={{ padding: 10, width: "100%" }}>Login</button>
    </form>
  );
}

import { useRouter } from "next/router";

export default function Navbar() {
  const router = useRouter();

  function logout() {
    localStorage.removeItem("token");
    router.push("/");
  }

  return (
    <nav style={{ padding: 20, borderBottom: "1px solid #ccc", marginBottom: 20 }}>
      <button onClick={() => router.push("/dashboard")} style={{ marginRight: 15 }}>
        Dashboard
      </button>
      <button onClick={() => router.push("/register")} style={{ marginRight: 15 }}>
        Register
      </button>
      <button onClick={logout} style={{ float: "right" }}>
        Logout
      </button>
    </nav>
  );
}

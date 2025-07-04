import { useEffect, useState } from "react";
import { useRouter } from "next/router";
import { api } from "../utils/apiClient";
import DepositForm from "./DepositForm";
import WithdrawForm from "./WithdrawForm";
import TransferForm from "./TransferForm";
import Navbar from "./NavBar";

export default function Dashboard() {
  const router = useRouter();
  const [user, setUser] = useState(null);
  const [accountId, setAccountId] = useState("");
  const [balance, setBalance] = useState(null);
  const [transactions, setTransactions] = useState([]);

  useEffect(() => {
    if (!localStorage.getItem("token")) {
      router.push("/");
      return;
    }

    async function loadData() {
      try {
        const userData = await api("/me");
        setUser(userData);

        // For demo, let's assume you have an endpoint that returns accounts for user
        const accounts = await api("/user/accounts");
        const acctId = accounts[0]?.id;
        setAccountId(acctId);

        if (acctId) {
          const bal = await api(`/balance/${acctId}`);
          setBalance(bal.balance);

          const txs = await api(`/transactions/${acctId}`);
          setTransactions(txs);
        }
      } catch {
        alert("Unauthorized or API error");
        localStorage.removeItem("token");
        router.push("/");
      }
    }

    loadData();
  }, [router]);

  if (!user) return <p>Loading dashboard...</p>;

  return (
    <>
      <Navbar />
      <div style={{ maxWidth: 800, margin: "auto" }}>
        <h2>Welcome, {user.email}</h2>
        <h3>Account ID: {accountId}</h3>
        <h3>Balance: ${balance?.toFixed(2)}</h3>

        <DepositForm accountId={accountId} onSuccess={() => router.reload()} />
        <WithdrawForm accountId={accountId} onSuccess={() => router.reload()} />
        <TransferForm fromAccountId={accountId} onSuccess={() => router.reload()} />

        <h3>Transactions</h3>
        <ul>
          {transactions.map(tx => (
            <li key={tx.id}>
              {new Date(tx.timestamp).toLocaleString()} — {tx.type.toUpperCase()} ${tx.amount} — {tx.description}
            </li>
          ))}
        </ul>
      </div>
    </>
  );
}

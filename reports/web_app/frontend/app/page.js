// pages/index.js
import Link from "next/link";

export default function Home() {
  return (
    <div className="container">
      <h1>Welcome to MedBot</h1>
      <p>Your AI-powered healthcare assistant.</p>
      <div style={{ margin: "1rem" }}>
        <Link href="/login">
          <button className="button">Login</button>
        </Link>
      </div>
      <div style={{ margin: "1rem" }}>
        <Link href="/signup">
          <button className="button">Sign Up</button>
        </Link>
      </div>
      <div style={{ margin: "1rem" }}>
        <Link href="/chatbot">
          <button className="button">Chat with MedBot</button>
        </Link>
      </div>
    </div>
  );
}

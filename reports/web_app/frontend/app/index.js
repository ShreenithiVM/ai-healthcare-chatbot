import Link from "next/link";

export default function Home() {
  return (
    <div>
      <h1>Welcome to MedBot</h1>
      <p>Your AI-powered healthcare assistant.</p>
      <Link href="/chatbot">
        <button>Chat with MedBot</button>
      </Link>
    </div>
  );
}

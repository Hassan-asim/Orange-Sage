import { Metadata } from "next"
import { LoginContent } from "./login-content"

export const metadata: Metadata = {
  title: "Login | Orange Sage",
  description: "Sign in to your Orange Sage account.",
}

export default function LoginPage() {
  return <LoginContent />
}

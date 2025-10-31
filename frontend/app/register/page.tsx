import { Metadata } from "next"
import { RegisterContent } from "./register-content"

export const metadata: Metadata = {
  title: "Register | Orange Sage",
  description: "Create your Orange Sage account to start securing your code.",
}

export default function RegisterPage() {
  return <RegisterContent />
}

import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { FindingsContent } from "./findings-content"

export const metadata: Metadata = {
  title: "Findings | Orange Sage",
  description: "View and manage detected vulnerabilities across scans.",
}

export default function FindingsPage() {
  return (
    <PublicLayout>
      <FindingsContent />
    </PublicLayout>
  )
}

import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { ReportsContent } from "./reports-content"

export const metadata: Metadata = {
  title: "Reports | Orange Sage",
  description: "View, download, and generate scan reports from your completed security scans.",
}

export default function ReportsPage() {
  return (
    <PublicLayout>
      <ReportsContent />
    </PublicLayout>
  )
}
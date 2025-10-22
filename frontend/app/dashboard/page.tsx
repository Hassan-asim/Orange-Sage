import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { DashboardContent } from "./dashboard-content"

export const metadata: Metadata = {
  title: "Dashboard | Orange Sage",
  description: "Overview of your scans, findings, and reports.",
}

export default function DashboardPage() {
  return (
    <PublicLayout>
      <DashboardContent />
    </PublicLayout>
  )
}

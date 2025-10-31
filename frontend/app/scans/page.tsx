import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { ScansContent } from "./scans-content"

export const metadata: Metadata = {
  title: "Scans | Orange Sage",
  description: "Monitor, manage, and launch project scans.",
}

export default function ScansPage() {
  return (
    <PublicLayout>
      <ScansContent />
    </PublicLayout>
  )
}

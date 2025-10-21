import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { SettingsContent } from "@/components/ui/settings-content"

export const metadata: Metadata = {
  title: "Settings | Orange Sage",
  description: "Manage your profile, security, notifications and preferences.",
}

export default function SettingsPage() {
  return (
    <PublicLayout>
      <SettingsContent />
    </PublicLayout>
  )
}

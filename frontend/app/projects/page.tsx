import { Metadata } from "next"
import { PublicLayout } from "@/components/layout/public-layout"
import { ProjectsContent } from "./projects-content"

export const metadata: Metadata = {
  title: "Projects | Orange Sage",
  description: "Manage and organize your cybersecurity projects.",
}

export default function ProjectsPage() {
  return (
    <PublicLayout>
      <ProjectsContent />
    </PublicLayout>
  )
}

"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { Label } from "@/components/ui/label"
import { 
  Plus,
  Search,
  Eye,
  Trash2,
  Calendar,
  Shield,
  AlertTriangle,
  CheckCircle,
  Clock
} from "lucide-react"

// TypeScript interfaces
interface Project {
  id: string
  name: string
  description: string
  status: "Active" | "Scanning" | "Archived"
  lastScan: string
  findings: number
  createdOn: string
  tags: string[]
}

interface NewProjectForm {
  name: string
  description: string
  tags: string
}

// Mock data
const mockProjects: Project[] = [
  {
    id: "1",
    name: "E-commerce API Security",
    description: "Comprehensive security assessment of the main e-commerce platform API endpoints",
    status: "Active",
    lastScan: "2025-10-21",
    findings: 12,
    createdOn: "2025-10-15",
    tags: ["API", "E-commerce", "Critical"]
  },
  {
    id: "2", 
    name: "Mobile App Backend",
    description: "Security testing for mobile application backend services and authentication",
    status: "Scanning",
    lastScan: "2025-10-20",
    findings: 8,
    createdOn: "2025-10-10",
    tags: ["Mobile", "Backend", "Auth"]
  },
  {
    id: "3",
    name: "Payment Gateway Integration",
    description: "PCI DSS compliance testing and security validation for payment processing",
    status: "Active",
    lastScan: "2025-10-19",
    findings: 3,
    createdOn: "2025-10-01",
    tags: ["Payment", "PCI-DSS", "Compliance"]
  },
  {
    id: "4",
    name: "User Authentication System",
    description: "Security review of user login, registration, and session management",
    status: "Archived",
    lastScan: "2025-10-15",
    findings: 5,
    createdOn: "2025-09-20",
    tags: ["Auth", "Security", "Users"]
  },
  {
    id: "5",
    name: "Admin Dashboard Security",
    description: "Comprehensive security testing of administrative interface and permissions",
    status: "Active",
    lastScan: "2025-10-18",
    findings: 15,
    createdOn: "2025-09-25",
    tags: ["Admin", "Dashboard", "Permissions"]
  },
  {
    id: "6",
    name: "Third-party Integrations",
    description: "Security assessment of external service integrations and data flow",
    status: "Scanning",
    lastScan: "2025-10-17",
    findings: 7,
    createdOn: "2025-09-30",
    tags: ["Integration", "External", "Data"]
  }
]

function getStatusBadge(status: Project["status"]) {
  switch (status) {
    case "Active":
      return <Badge className="bg-green-500/10 text-green-500 border-green-500/20">Active</Badge>
    case "Scanning":
      return <Badge className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">Scanning</Badge>
    case "Archived":
      return <Badge className="bg-gray-500/10 text-gray-500 border-gray-500/20">Archived</Badge>
    default:
      return <Badge variant="secondary">{status}</Badge>
  }
}

function getStatusIcon(status: Project["status"]) {
  switch (status) {
    case "Active":
      return <CheckCircle className="h-4 w-4 text-green-500" />
    case "Scanning":
      return <Clock className="h-4 w-4 text-yellow-500" />
    case "Archived":
      return <Shield className="h-4 w-4 text-gray-500" />
    default:
      return null
  }
}

function ProjectCard({ project }: { project: Project }) {
  return (
    <Card className="bg-card border-border hover:border-primary/20 transition-colors">
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <CardTitle className="text-lg font-semibold text-foreground truncate pr-2">
            {project.name}
          </CardTitle>
          {getStatusBadge(project.status)}
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground line-clamp-2">
          {project.description}
        </p>
        
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <div className="flex items-center gap-1">
            <Calendar className="h-3 w-3" />
            <span>{new Date(project.createdOn).toLocaleDateString()}</span>
          </div>
          <div className="flex items-center gap-1">
            <AlertTriangle className="h-3 w-3" />
            <span>{project.findings} findings</span>
          </div>
        </div>

        <div className="flex flex-wrap gap-1">
          {project.tags.slice(0, 3).map((tag, index) => (
            <Badge key={index} variant="secondary" className="text-xs">
              {tag}
            </Badge>
          ))}
          {project.tags.length > 3 && (
            <Badge variant="secondary" className="text-xs">
              +{project.tags.length - 3}
            </Badge>
          )}
        </div>

        <Button className="w-full bg-primary text-primary-foreground hover:bg-primary/90">
          <Eye className="h-4 w-4 mr-2" />
          View Details
        </Button>
      </CardContent>
    </Card>
  )
}

function ProjectTableRow({ project }: { project: Project }) {
  return (
    <TableRow className="border-border">
      <TableCell className="font-medium text-foreground">
        <div className="flex items-center gap-2">
          {getStatusIcon(project.status)}
          {project.name}
        </div>
      </TableCell>
      <TableCell className="text-muted-foreground">
        {new Date(project.lastScan).toLocaleDateString()}
      </TableCell>
      <TableCell>
        {getStatusBadge(project.status)}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {project.findings}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {new Date(project.createdOn).toLocaleDateString()}
      </TableCell>
      <TableCell>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Eye className="h-4 w-4" />
          </Button>
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-red-500 hover:text-red-600">
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </TableCell>
    </TableRow>
  )
}

function NewProjectDialog() {
  const [form, setForm] = useState<NewProjectForm>({
    name: "",
    description: "",
    tags: ""
  })
  const [open, setOpen] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    console.log("New project data:", {
      ...form,
      tags: form.tags.split(",").map(tag => tag.trim()).filter(Boolean)
    })
    setForm({ name: "", description: "", tags: "" })
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-6 py-2 rounded-full font-medium shadow-sm">
          <Plus className="h-4 w-4 mr-2" />
          New Project
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-card border-border">
        <DialogHeader>
          <DialogTitle className="text-foreground">Create New Project</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name" className="text-foreground">Project Name</Label>
            <Input
              id="name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Enter project name"
              required
              className="bg-background border-border text-foreground"
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="description" className="text-foreground">Description</Label>
            <Textarea
              id="description"
              value={form.description}
              onChange={(e) => setForm({ ...form, description: e.target.value })}
              placeholder="Describe your project"
              className="bg-background border-border text-foreground"
              rows={3}
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="tags" className="text-foreground">Tags</Label>
            <Input
              id="tags"
              value={form.tags}
              onChange={(e) => setForm({ ...form, tags: e.target.value })}
              placeholder="API, Security, Compliance (comma-separated)"
              className="bg-background border-border text-foreground"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button type="submit" className="bg-primary text-primary-foreground hover:bg-primary/90">
              Create Project
            </Button>
          </div>
        </form>
      </DialogContent>
    </Dialog>
  )
}

function EmptyState() {
  return (
    <Card className="bg-card border-border">
      <CardContent className="flex flex-col items-center justify-center py-12">
        <Shield className="h-16 w-16 text-muted-foreground mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No projects found</h3>
        <p className="text-muted-foreground text-center mb-6">
          Create your first project to get started with security scanning.
        </p>
        <NewProjectDialog />
      </CardContent>
    </Card>
  )
}

export function ProjectsContent() {
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [projects, setProjects] = useState<Project[]>([])

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setProjects(mockProjects)
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  const filteredProjects = projects.filter(project =>
    project.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.description.toLowerCase().includes(searchQuery.toLowerCase()) ||
    project.tags.some(tag => tag.toLowerCase().includes(searchQuery.toLowerCase()))
  )

  const useTableLayout = filteredProjects.length > 6

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-semibold text-foreground mb-2">
              Projects
            </h1>
            <p className="text-muted-foreground text-sm md:text-base">
              Manage your security projects and track their latest scan results.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search projects..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-background border-border text-foreground w-full sm:w-64"
              />
            </div>
            <NewProjectDialog />
          </div>
        </div>

        {/* Projects Content */}
        {isLoading ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="bg-card border-border">
                <CardHeader>
                  <div className="flex items-start justify-between">
                    <Skeleton className="h-6 w-48" />
                    <Skeleton className="h-6 w-16" />
                  </div>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Skeleton className="h-4 w-full" />
                  <Skeleton className="h-4 w-3/4" />
                  <div className="flex justify-between">
                    <Skeleton className="h-4 w-24" />
                    <Skeleton className="h-4 w-20" />
                  </div>
                  <div className="flex gap-2">
                    <Skeleton className="h-5 w-12" />
                    <Skeleton className="h-5 w-16" />
                    <Skeleton className="h-5 w-14" />
                  </div>
                  <Skeleton className="h-10 w-full" />
                </CardContent>
              </Card>
            ))}
          </div>
        ) : filteredProjects.length === 0 ? (
          projects.length === 0 ? <EmptyState /> : (
            <Card className="bg-card border-border">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Search className="h-16 w-16 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold text-foreground mb-2">No projects match your search</h3>
                <p className="text-muted-foreground text-center">
                  Try adjusting your search terms or create a new project.
                </p>
              </CardContent>
            </Card>
          )
        ) : useTableLayout ? (
          /* Table Layout for many projects */
          <Card className="bg-card border-border">
            <CardContent className="p-0">
              <Table>
                <TableHeader>
                  <TableRow className="border-border">
                    <TableHead className="text-muted-foreground">Project Name</TableHead>
                    <TableHead className="text-muted-foreground">Last Scan</TableHead>
                    <TableHead className="text-muted-foreground">Status</TableHead>
                    <TableHead className="text-muted-foreground">Findings</TableHead>
                    <TableHead className="text-muted-foreground">Created On</TableHead>
                    <TableHead className="text-muted-foreground">Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredProjects.map((project) => (
                    <ProjectTableRow key={project.id} project={project} />
                  ))}
                </TableBody>
              </Table>
            </CardContent>
          </Card>
        ) : (
          /* Card Layout for fewer projects */
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
            {filteredProjects.map((project) => (
              <ProjectCard key={project.id} project={project} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

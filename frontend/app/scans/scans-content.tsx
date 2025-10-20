"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { Label } from "@/components/ui/label"
import { Progress } from "@/components/ui/progress"
import { 
  Play,
  Filter,
  Eye,
  RotateCcw,
  Trash2,
  Activity,
  CheckCircle,
  AlertCircle,
  Clock,
  Zap,
  Shield
} from "lucide-react"

// TypeScript interfaces
interface Scan {
  id: string
  projectName: string
  scanType: "Full Scan" | "Quick Scan" | "Custom Scan"
  status: "Completed" | "Running" | "Failed"
  startedAt: string
  duration: string
  progress?: number
  findings?: number
  notes?: string
}

interface NewScanForm {
  projectId: string
  scanType: string
  notes: string
}

type ScanFilter = "All" | "Running" | "Completed" | "Failed"

// Mock data
const mockProjects = [
  { id: "1", name: "E-commerce API Security" },
  { id: "2", name: "Mobile App Backend" },
  { id: "3", name: "Payment Gateway Integration" },
  { id: "4", name: "User Authentication System" },
  { id: "5", name: "Admin Dashboard Security" }
]

const mockScans: Scan[] = [
  {
    id: "1",
    projectName: "E-commerce API Security",
    scanType: "Full Scan",
    status: "Running",
    startedAt: "2025-10-21T10:30:00",
    duration: "45m 12s",
    progress: 75,
    notes: "Comprehensive API security assessment"
  },
  {
    id: "2",
    projectName: "Mobile App Backend",
    scanType: "Quick Scan",
    status: "Completed",
    startedAt: "2025-10-21T09:15:00",
    duration: "12m 34s",
    findings: 8
  },
  {
    id: "3",
    projectName: "Payment Gateway Integration",
    scanType: "Full Scan",
    status: "Completed",
    startedAt: "2025-10-20T14:20:00",
    duration: "1h 23m",
    findings: 3
  },
  {
    id: "4",
    projectName: "User Authentication System",
    scanType: "Custom Scan",
    status: "Failed",
    startedAt: "2025-10-20T11:45:00",
    duration: "5m 18s",
    notes: "Network timeout during scan"
  },
  {
    id: "5",
    projectName: "Admin Dashboard Security",
    scanType: "Quick Scan",
    status: "Running",
    startedAt: "2025-10-21T11:00:00",
    duration: "18m 45s",
    progress: 42
  },
  {
    id: "6",
    projectName: "E-commerce API Security",
    scanType: "Quick Scan",
    status: "Completed",
    startedAt: "2025-10-19T16:30:00",
    duration: "8m 12s",
    findings: 12
  },
  {
    id: "7",
    projectName: "Mobile App Backend",
    scanType: "Full Scan",
    status: "Completed",
    startedAt: "2025-10-19T13:15:00",
    duration: "2h 8m",
    findings: 15
  },
  {
    id: "8",
    projectName: "Payment Gateway Integration",
    scanType: "Custom Scan",
    status: "Failed",
    startedAt: "2025-10-18T10:00:00",
    duration: "1m 45s",
    notes: "Configuration error"
  }
]

function getStatusBadge(status: Scan["status"]) {
  switch (status) {
    case "Completed":
      return <Badge className="bg-green-500/10 text-green-500 border-green-500/20">Completed</Badge>
    case "Running":
      return <Badge className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">Running</Badge>
    case "Failed":
      return <Badge className="bg-red-500/10 text-red-500 border-red-500/20">Failed</Badge>
    default:
      return <Badge variant="secondary">{status}</Badge>
  }
}

function getStatusIcon(status: Scan["status"]) {
  switch (status) {
    case "Completed":
      return <CheckCircle className="h-4 w-4 text-green-500" />
    case "Running":
      return <Activity className="h-4 w-4 text-yellow-500" />
    case "Failed":
      return <AlertCircle className="h-4 w-4 text-red-500" />
    default:
      return null
  }
}

function getScanTypeIcon(scanType: Scan["scanType"]) {
  switch (scanType) {
    case "Full Scan":
      return <Shield className="h-4 w-4 text-primary" />
    case "Quick Scan":
      return <Zap className="h-4 w-4 text-yellow-500" />
    case "Custom Scan":
      return <Activity className="h-4 w-4 text-blue-500" />
    default:
      return null
  }
}

function formatDateTime(dateString: string) {
  return new Date(dateString).toLocaleString()
}

function getElapsedTime(startedAt: string) {
  const start = new Date(startedAt)
  const now = new Date()
  const diff = Math.floor((now.getTime() - start.getTime()) / 1000)
  
  const hours = Math.floor(diff / 3600)
  const minutes = Math.floor((diff % 3600) / 60)
  const seconds = diff % 60
  
  if (hours > 0) {
    return `${hours}h ${minutes}m ${seconds}s`
  } else if (minutes > 0) {
    return `${minutes}m ${seconds}s`
  } else {
    return `${seconds}s`
  }
}

function ScanTableRow({ scan }: { scan: Scan }) {
  return (
    <TableRow className="border-border">
      <TableCell className="font-medium text-foreground">
        <div className="flex items-center gap-2">
          {getStatusIcon(scan.status)}
          {scan.projectName}
        </div>
      </TableCell>
      <TableCell className="text-muted-foreground">
        <div className="flex items-center gap-2">
          {getScanTypeIcon(scan.scanType)}
          {scan.scanType}
        </div>
      </TableCell>
      <TableCell>
        {getStatusBadge(scan.status)}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {formatDateTime(scan.startedAt)}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {scan.status === "Running" ? getElapsedTime(scan.startedAt) : scan.duration}
      </TableCell>
      <TableCell>
        <div className="flex items-center gap-2">
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
            <Eye className="h-4 w-4" />
          </Button>
          {scan.status === "Failed" && (
            <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-blue-500 hover:text-blue-600">
              <RotateCcw className="h-4 w-4" />
            </Button>
          )}
          <Button variant="ghost" size="sm" className="h-8 w-8 p-0 text-red-500 hover:text-red-600">
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </TableCell>
    </TableRow>
  )
}

function RunningScanCard({ scan }: { scan: Scan }) {
  return (
    <Card className="bg-card border-border">
      <CardContent className="p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Activity className="h-4 w-4 text-yellow-500" />
            <span className="font-medium text-foreground">{scan.projectName}</span>
          </div>
          {getStatusBadge(scan.status)}
        </div>
        
        <div className="space-y-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-muted-foreground">{scan.scanType}</span>
            <span className="text-muted-foreground">{scan.progress}%</span>
          </div>
          
          <Progress value={scan.progress} className="h-2" />
          
          <div className="flex items-center justify-between text-xs text-muted-foreground">
            <span>Elapsed: {getElapsedTime(scan.startedAt)}</span>
            <span>Est. remaining: {Math.floor((scan.progress || 1) / 100 * 5)}m</span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}

function NewScanDialog() {
  const [form, setForm] = useState<NewScanForm>({
    projectId: "",
    scanType: "",
    notes: ""
  })
  const [open, setOpen] = useState(false)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    const selectedProject = mockProjects.find(p => p.id === form.projectId)
    console.log("New scan data:", {
      ...form,
      projectName: selectedProject?.name
    })
    setForm({ projectId: "", scanType: "", notes: "" })
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-6 py-2 rounded-full font-medium shadow-sm">
          <Play className="h-4 w-4 mr-2" />
          New Scan
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-card border-border">
        <DialogHeader>
          <DialogTitle className="text-foreground">Start New Scan</DialogTitle>
        </DialogHeader>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="project" className="text-foreground">Select Project</Label>
            <Select value={form.projectId} onValueChange={(value) => setForm({ ...form, projectId: value })}>
              <SelectTrigger className="bg-background border-border text-foreground">
                <SelectValue placeholder="Choose a project" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                {mockProjects.map((project) => (
                  <SelectItem key={project.id} value={project.id} className="text-foreground">
                    {project.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="scanType" className="text-foreground">Scan Type</Label>
            <Select value={form.scanType} onValueChange={(value) => setForm({ ...form, scanType: value })}>
              <SelectTrigger className="bg-background border-border text-foreground">
                <SelectValue placeholder="Choose scan type" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="Full Scan" className="text-foreground">Full Scan</SelectItem>
                <SelectItem value="Quick Scan" className="text-foreground">Quick Scan</SelectItem>
                <SelectItem value="Custom Scan" className="text-foreground">Custom Scan</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="notes" className="text-foreground">Notes (Optional)</Label>
            <Textarea
              id="notes"
              value={form.notes}
              onChange={(e) => setForm({ ...form, notes: e.target.value })}
              placeholder="Add any specific notes or requirements"
              className="bg-background border-border text-foreground"
              rows={3}
            />
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <Button type="button" variant="ghost" onClick={() => setOpen(false)}>
              Cancel
            </Button>
            <Button 
              type="submit" 
              className="bg-primary text-primary-foreground hover:bg-primary/90"
              disabled={!form.projectId || !form.scanType}
            >
              <Play className="h-4 w-4 mr-2" />
              Start Scan
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
        <Activity className="h-16 w-16 text-muted-foreground mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No scans found</h3>
        <p className="text-muted-foreground text-center mb-6">
          Start a new scan to analyze your projects for security vulnerabilities.
        </p>
        <NewScanDialog />
      </CardContent>
    </Card>
  )
}

export function ScansContent() {
  const [isLoading, setIsLoading] = useState(true)
  const [filter, setFilter] = useState<ScanFilter>("All")
  const [scans, setScans] = useState<Scan[]>([])

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setScans(mockScans)
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  const filteredScans = scans.filter(scan => 
    filter === "All" || scan.status === filter
  )

  const runningScans = scans.filter(scan => scan.status === "Running")

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-semibold text-foreground mb-2">
              Scans
            </h1>
            <p className="text-muted-foreground text-sm md:text-base">
              View ongoing and completed scans across your projects.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <Select value={filter} onValueChange={(value: ScanFilter) => setFilter(value)}>
              <SelectTrigger className="bg-background border-border text-foreground w-full sm:w-40">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="All" className="text-foreground">All Scans</SelectItem>
                <SelectItem value="Running" className="text-foreground">Running</SelectItem>
                <SelectItem value="Completed" className="text-foreground">Completed</SelectItem>
                <SelectItem value="Failed" className="text-foreground">Failed</SelectItem>
              </SelectContent>
            </Select>
            <NewScanDialog />
          </div>
        </div>

        {/* Running Scans Section */}
        {!isLoading && runningScans.length > 0 && (
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-foreground mb-4 flex items-center gap-2">
              <Clock className="h-5 w-5" />
              Running Scans ({runningScans.length})
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {runningScans.map((scan) => (
                <RunningScanCard key={scan.id} scan={scan} />
              ))}
            </div>
          </div>
        )}

        {/* Scans Table */}
        {isLoading ? (
          <Card className="bg-card border-border">
            <CardContent className="p-0">
              <div className="p-6 space-y-4">
                {[...Array(6)].map((_, i) => (
                  <div key={i} className="flex items-center space-x-4">
                    <Skeleton className="h-4 w-[200px]" />
                    <Skeleton className="h-4 w-[120px]" />
                    <Skeleton className="h-6 w-[80px]" />
                    <Skeleton className="h-4 w-[150px]" />
                    <Skeleton className="h-4 w-[80px]" />
                    <Skeleton className="h-8 w-[100px]" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ) : filteredScans.length === 0 ? (
          scans.length === 0 ? <EmptyState /> : (
            <Card className="bg-card border-border">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Filter className="h-16 w-16 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold text-foreground mb-2">No scans match your filter</h3>
                <p className="text-muted-foreground text-center">
                  Try adjusting your filter or start a new scan.
                </p>
              </CardContent>
            </Card>
          )
        ) : (
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground">
                All Scans ({filteredScans.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow className="border-border">
                      <TableHead className="text-muted-foreground">Project Name</TableHead>
                      <TableHead className="text-muted-foreground">Scan Type</TableHead>
                      <TableHead className="text-muted-foreground">Status</TableHead>
                      <TableHead className="text-muted-foreground">Started At</TableHead>
                      <TableHead className="text-muted-foreground">Duration</TableHead>
                      <TableHead className="text-muted-foreground">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredScans.map((scan) => (
                      <ScanTableRow key={scan.id} scan={scan} />
                    ))}
                  </TableBody>
                </Table>
              </div>
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}

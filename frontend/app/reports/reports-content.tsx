"use client"

import { useState } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { toast } from "@/components/ui/use-toast"
import {
  FileText,
  Plus,
  Search,
  Eye,
  Download,
  Trash2,
  AlertTriangle,
  CheckCircle,
  Clock,
  Filter,
  Calendar,
  BarChart3
} from "lucide-react"

interface Report {
  id: string
  title: string
  projectName: string
  scanDate: string
  findingsCount: number
  generatedOn: string
  status: 'ready' | 'pending' | 'failed'
}

const mockReports: Report[] = [
  {
    id: "RPT-001",
    title: "Security Audit Report",
    projectName: "E-commerce Platform",
    scanDate: "2025-10-20",
    findingsCount: 23,
    generatedOn: "2025-10-21",
    status: "ready"
  },
  {
    id: "RPT-002",
    title: "Vulnerability Assessment",
    projectName: "Payment Gateway",
    scanDate: "2025-10-19",
    findingsCount: 7,
    generatedOn: "2025-10-20",
    status: "ready"
  },
  {
    id: "RPT-003",
    title: "Code Security Review",
    projectName: "User Authentication",
    scanDate: "2025-10-18",
    findingsCount: 15,
    generatedOn: "2025-10-19",
    status: "pending"
  },
  {
    id: "RPT-004",
    title: "Compliance Report",
    projectName: "Data Analytics",
    scanDate: "2025-10-17",
    findingsCount: 0,
    generatedOn: "2025-10-18",
    status: "failed"
  }
]

const mockProjects = [
  "E-commerce Platform",
  "Payment Gateway",
  "User Authentication",
  "Data Analytics",
  "Mobile App Backend"
]

export function ReportsContent() {
  const [reports, setReports] = useState<Report[]>(mockReports)
  const [searchQuery, setSearchQuery] = useState("")
  const [dateFilter, setDateFilter] = useState("all")
  const [isLoading, setIsLoading] = useState(false)
  const [previewReport, setPreviewReport] = useState<Report | null>(null)
  const [generateDialog, setGenerateDialog] = useState(false)
  const [selectedProject, setSelectedProject] = useState("")
  const [scanRange, setScanRange] = useState("")
  const [reportNotes, setReportNotes] = useState("")

  const filteredReports = reports.filter(report => {
    const matchesSearch = report.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         report.projectName.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesSearch
  })

  const stats = {
    total: reports.length,
    ready: reports.filter(r => r.status === 'ready').length,
    pending: reports.filter(r => r.status === 'pending').length,
    failed: reports.filter(r => r.status === 'failed').length
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'ready':
        return <Badge className="bg-green-500/20 text-green-400 border-green-500/30">Ready</Badge>
      case 'pending':
        return <Badge className="bg-yellow-500/20 text-yellow-400 border-yellow-500/30">Pending</Badge>
      case 'failed':
        return <Badge className="bg-red-500/20 text-red-400 border-red-500/30">Failed</Badge>
      default:
        return <Badge variant="secondary">{status}</Badge>
    }
  }

  const handlePreview = (report: Report) => {
    setPreviewReport(report)
  }

  const handleDownload = (report: Report) => {
    toast({
      title: "Download Started",
      description: `Downloading ${report.title} report...`,
    })
  }

  const handleDelete = (reportId: string) => {
    setReports(prev => prev.filter(r => r.id !== reportId))
    toast({
      title: "Report Deleted",
      description: "The report has been permanently deleted.",
    })
  }

  const handleGenerateReport = () => {
    if (!selectedProject || !scanRange) {
      toast({
        title: "Missing Information",
        description: "Please select a project and scan range.",
        variant: "destructive"
      })
      return
    }

    const newReport: Report = {
      id: `RPT-${String(reports.length + 1).padStart(3, '0')}`,
      title: "Generated Security Report",
      projectName: selectedProject,
      scanDate: new Date().toISOString().split('T')[0],
      findingsCount: Math.floor(Math.random() * 25),
      generatedOn: new Date().toISOString().split('T')[0],
      status: "pending"
    }

    setReports(prev => [newReport, ...prev])
    setGenerateDialog(false)
    setSelectedProject("")
    setScanRange("")
    setReportNotes("")

    toast({
      title: "Report Generation Started",
      description: "Your report is being generated and will be ready shortly.",
    })

    // Simulate report completion after 3 seconds
    setTimeout(() => {
      setReports(prev =>
        prev.map(r =>
          r.id === newReport.id
            ? { ...r, status: 'ready' as const }
            : r
        )
      )
      toast({
        title: "Report Ready",
        description: `${newReport.title} is now available for download.`,
      })
    }, 3000)
  }

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-foreground mb-2">Reports</h1>
            <p className="text-muted-foreground">
              Access and download reports generated from your completed scans.
            </p>
          </div>

          {/* Stats Cards */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <Card className="bg-card border-border">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-blue-500/20 rounded-lg">
                    <FileText className="h-4 w-4 text-blue-400" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Total Reports</p>
                    <p className="text-2xl font-bold text-foreground">{stats.total}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-green-500/20 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-green-400" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Ready</p>
                    <p className="text-2xl font-bold text-foreground">{stats.ready}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-yellow-500/20 rounded-lg">
                    <Clock className="h-4 w-4 text-yellow-400" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Pending</p>
                    <p className="text-2xl font-bold text-foreground">{stats.pending}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <Card className="bg-card border-border">
              <CardContent className="p-4">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-red-500/20 rounded-lg">
                    <AlertTriangle className="h-4 w-4 text-red-400" />
                  </div>
                  <div>
                    <p className="text-sm text-muted-foreground">Failed</p>
                    <p className="text-2xl font-bold text-foreground">{stats.failed}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Controls */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex-1 relative">
              <Search className="h-4 w-4 absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="Search reports by name or project..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-background border-border text-foreground"
              />
            </div>
            <Select value={dateFilter} onValueChange={setDateFilter}>
              <SelectTrigger className="w-full md:w-48 bg-background border-border">
                <Calendar className="h-4 w-4 mr-2" />
                <SelectValue placeholder="Filter by date" />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="all">All Time</SelectItem>
                <SelectItem value="7days">Last 7 days</SelectItem>
                <SelectItem value="30days">Last 30 days</SelectItem>
              </SelectContent>
            </Select>
            <Dialog open={generateDialog} onOpenChange={setGenerateDialog}>
              <DialogTrigger asChild>
                <Button className="bg-primary text-black hover:bg-primary/90">
                  <Plus className="h-4 w-4 mr-2" />
                  Generate Report
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-card border-border">
                <DialogHeader>
                  <DialogTitle className="text-foreground">Generate New Report</DialogTitle>
                </DialogHeader>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label className="text-foreground">Select Project</Label>
                    <Select value={selectedProject} onValueChange={setSelectedProject}>
                      <SelectTrigger className="bg-background border-border">
                        <SelectValue placeholder="Choose a project" />
                      </SelectTrigger>
                      <SelectContent className="bg-card border-border">
                        {mockProjects.map(project => (
                          <SelectItem key={project} value={project}>{project}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-foreground">Scan Range</Label>
                    <Select value={scanRange} onValueChange={setScanRange}>
                      <SelectTrigger className="bg-background border-border">
                        <SelectValue placeholder="Select scan range" />
                      </SelectTrigger>
                      <SelectContent className="bg-card border-border">
                        <SelectItem value="last">Last Scan</SelectItem>
                        <SelectItem value="all">All Scans</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div className="space-y-2">
                    <Label className="text-foreground">Optional Notes</Label>
                    <Textarea
                      value={reportNotes}
                      onChange={(e) => setReportNotes(e.target.value)}
                      placeholder="Add any additional notes for this report..."
                      className="bg-background border-border text-foreground"
                    />
                  </div>
                  <div className="flex justify-end gap-3">
                    <Button variant="ghost" onClick={() => setGenerateDialog(false)}>
                      Cancel
                    </Button>
                    <Button onClick={handleGenerateReport} className="bg-[#ea580c] text-white hover:bg-[#ea580c]/90">
                      Generate Report
                    </Button>
                  </div>
                </div>
              </DialogContent>
            </Dialog>
          </div>

          {/* Reports Table */}
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Generated Reports
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-4">
                  {[...Array(4)].map((_, i) => (
                    <div key={i} className="flex items-center space-x-4">
                      <Skeleton className="h-4 w-20" />
                      <Skeleton className="h-4 w-32" />
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-16" />
                      <Skeleton className="h-4 w-24" />
                      <Skeleton className="h-4 w-20" />
                      <Skeleton className="h-4 w-32" />
                    </div>
                  ))}
                </div>
              ) : filteredReports.length === 0 ? (
                <div className="text-center py-12">
                  <FileText className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-foreground mb-2">No reports yet</h3>
                  <p className="text-muted-foreground mb-4">
                    Generate one after your next scan to get started.
                  </p>
                  <Button
                    onClick={() => setGenerateDialog(true)}
                    className="bg-[#ea580c] text-white hover:bg-[#ea580c]/90"
                  >
                    Generate Report
                  </Button>
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <Table>
                    <TableHeader>
                      <TableRow className="border-border">
                        <TableHead className="text-muted-foreground">Report ID</TableHead>
                        <TableHead className="text-muted-foreground">Title</TableHead>
                        <TableHead className="text-muted-foreground">Project</TableHead>
                        <TableHead className="text-muted-foreground">Scan Date</TableHead>
                        <TableHead className="text-muted-foreground">Findings</TableHead>
                        <TableHead className="text-muted-foreground">Generated</TableHead>
                        <TableHead className="text-muted-foreground">Status</TableHead>
                        <TableHead className="text-muted-foreground">Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {filteredReports.map((report) => (
                        <TableRow key={report.id} className="border-border">
                          <TableCell className="font-mono text-sm text-foreground">
                            {report.id}
                          </TableCell>
                          <TableCell className="font-medium text-foreground">
                            {report.title}
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {report.projectName}
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {new Date(report.scanDate).toLocaleDateString()}
                          </TableCell>
                          <TableCell className="text-foreground">
                            <Badge variant="secondary" className="bg-muted text-foreground">
                              {report.findingsCount}
                            </Badge>
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {new Date(report.generatedOn).toLocaleDateString()}
                          </TableCell>
                          <TableCell>
                            {getStatusBadge(report.status)}
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handlePreview(report)}
                                disabled={report.status !== 'ready'}
                              >
                                <Eye className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDownload(report)}
                                disabled={report.status !== 'ready'}
                              >
                                <Download className="h-4 w-4" />
                              </Button>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => handleDelete(report.id)}
                                className="text-red-500 hover:text-red-600"
                              >
                                <Trash2 className="h-4 w-4" />
                              </Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Report Preview Dialog */}
          <Dialog open={!!previewReport} onOpenChange={() => setPreviewReport(null)}>
            <DialogContent className="bg-card border-border max-w-2xl">
              <DialogHeader>
                <DialogTitle className="text-foreground">Report Preview</DialogTitle>
              </DialogHeader>
              {previewReport && (
                <div className="space-y-6">
                  <div className="space-y-2">
                    <h3 className="text-lg font-medium text-foreground">{previewReport.title}</h3>
                    <p className="text-muted-foreground">
                      Project: {previewReport.projectName} • Generated: {new Date(previewReport.generatedOn).toLocaleDateString()}
                    </p>
                  </div>

                  <div className="grid grid-cols-4 gap-4">
                    <Card className="bg-background border-border">
                      <CardContent className="p-3">
                        <div className="text-center">
                          <p className="text-sm text-muted-foreground">Critical</p>
                          <p className="text-xl font-bold text-red-400">2</p>
                        </div>
                      </CardContent>
                    </Card>
                    <Card className="bg-background border-border">
                      <CardContent className="p-3">
                        <div className="text-center">
                          <p className="text-sm text-muted-foreground">High</p>
                          <p className="text-xl font-bold text-orange-400">5</p>
                        </div>
                      </CardContent>
                    </Card>
                    <Card className="bg-background border-border">
                      <CardContent className="p-3">
                        <div className="text-center">
                          <p className="text-sm text-muted-foreground">Medium</p>
                          <p className="text-xl font-bold text-yellow-400">8</p>
                        </div>
                      </CardContent>
                    </Card>
                    <Card className="bg-background border-border">
                      <CardContent className="p-3">
                        <div className="text-center">
                          <p className="text-sm text-muted-foreground">Low</p>
                          <p className="text-xl font-bold text-blue-400">8</p>
                        </div>
                      </CardContent>
                    </Card>
                  </div>

                  <div className="p-4 bg-background rounded-lg border border-border">
                    <h4 className="font-medium text-foreground mb-2">Key Insights</h4>
                    <p className="text-sm text-muted-foreground">
                      This security assessment identified {previewReport.findingsCount} potential vulnerabilities across your codebase.
                      The most critical issues include SQL injection vulnerabilities in the authentication module and
                      cross-site scripting (XSS) risks in user input handling. Immediate attention is recommended for
                      high-severity findings to maintain security compliance.
                    </p>
                  </div>

                  <div className="flex justify-end gap-3">
                    <Button variant="ghost" onClick={() => setPreviewReport(null)}>
                      Close
                    </Button>
                    <Button
                      onClick={() => handleDownload(previewReport)}
                      className="bg-[#ea580c] text-white hover:bg-[#ea580c]/90"
                    >
                      <Download className="h-4 w-4 mr-2" />
                      Download PDF
                    </Button>
                  </div>
                </div>
              )}
            </DialogContent>
          </Dialog>
        </div>
      </div>
    </div>
  )
}
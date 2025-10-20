"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Input } from "@/components/ui/input"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import {
  Search,
  Filter,
  FileText,
  Eye,
  CheckCircle,
  AlertTriangle,
  Shield,
  Bug,
  Download,
  AlertCircle,
  Info
} from "lucide-react"

// TypeScript interfaces
interface Finding {
  id: string
  projectName: string
  scanId: string
  scanType: string
  title: string
  severity: "Critical" | "High" | "Medium" | "Low"
  status: "Resolved" | "Unresolved" | "Ignored"
  detectedOn: string
  description: string
  stepsToReproduce: string
  recommendedFix: string
}

type SeverityFilter = "All" | "Critical" | "High" | "Medium" | "Low"

// Mock data
const mockFindings: Finding[] = [
  {
    id: "1",
    projectName: "E-commerce API Security",
    scanId: "scan_001",
    scanType: "Full Scan",
    title: "SQL Injection vulnerability in user authentication",
    severity: "Critical",
    status: "Unresolved",
    detectedOn: "2025-10-21",
    description: "SQL injection vulnerability found in the user login endpoint that allows attackers to bypass authentication and access sensitive data.",
    stepsToReproduce: "1. Navigate to /api/login\n2. Input malicious SQL payload: admin' OR '1'='1' --\n3. Observe authentication bypass",
    recommendedFix: "Use parameterized queries and input validation. Implement prepared statements to prevent SQL injection attacks."
  },
  {
    id: "2",
    projectName: "Mobile App Backend",
    scanId: "scan_002",
    scanType: "Quick Scan",
    title: "Cross-Site Scripting (XSS) in comment system",
    severity: "High",
    status: "Unresolved",
    detectedOn: "2025-10-21",
    description: "Reflected XSS vulnerability in the comment submission form allows execution of malicious scripts.",
    stepsToReproduce: "1. Submit comment with script tag\n2. View comment page\n3. Script executes in browser",
    recommendedFix: "Implement proper input sanitization and output encoding. Use Content Security Policy headers."
  },
  {
    id: "3",
    projectName: "Payment Gateway Integration",
    scanId: "scan_003",
    scanType: "Full Scan",
    title: "Insecure direct object reference in payment API",
    severity: "High",
    status: "Resolved",
    detectedOn: "2025-10-20",
    description: "Users can access other users' payment information by manipulating the payment ID parameter.",
    stepsToReproduce: "1. Make payment request\n2. Change payment_id parameter\n3. Access other user's payment data",
    recommendedFix: "Implement proper authorization checks and use indirect object references."
  },
  {
    id: "4",
    projectName: "User Authentication System",
    scanId: "scan_004",
    scanType: "Custom Scan",
    title: "Weak password policy implementation",
    severity: "Medium",
    status: "Unresolved",
    detectedOn: "2025-10-20",
    description: "Password policy allows weak passwords that can be easily compromised through brute force attacks.",
    stepsToReproduce: "1. Try to register with password '123'\n2. System accepts weak password\n3. Account vulnerable to brute force",
    recommendedFix: "Implement strong password requirements including minimum length, complexity, and character variety."
  },
  {
    id: "5",
    projectName: "Admin Dashboard Security",
    scanId: "scan_005",
    scanType: "Full Scan",
    title: "Missing authentication on admin endpoints",
    severity: "Critical",
    status: "Unresolved",
    detectedOn: "2025-10-19",
    description: "Critical admin endpoints lack proper authentication, allowing unauthorized access to sensitive functionality.",
    stepsToReproduce: "1. Access /admin/users directly\n2. No authentication required\n3. Full admin access granted",
    recommendedFix: "Implement proper authentication middleware for all admin routes. Use role-based access control."
  },
  {
    id: "6",
    projectName: "E-commerce API Security",
    scanId: "scan_006",
    scanType: "Quick Scan",
    title: "Information disclosure in error messages",
    severity: "Low",
    status: "Ignored",
    detectedOn: "2025-10-19",
    description: "Error messages reveal sensitive information about the database structure and application internals.",
    stepsToReproduce: "1. Send malformed request to API\n2. Observe detailed error message\n3. Information about DB structure exposed",
    recommendedFix: "Implement generic error messages for production. Log detailed errors server-side only."
  },
  {
    id: "7",
    projectName: "Mobile App Backend",
    scanId: "scan_007",
    scanType: "Full Scan",
    title: "Insufficient rate limiting on API endpoints",
    severity: "Medium",
    status: "Resolved",
    detectedOn: "2025-10-18",
    description: "API endpoints lack proper rate limiting, making them vulnerable to abuse and DDoS attacks.",
    stepsToReproduce: "1. Send rapid API requests\n2. No rate limiting enforced\n3. Server resources consumed",
    recommendedFix: "Implement rate limiting middleware with appropriate thresholds for different endpoint types."
  },
  {
    id: "8",
    projectName: "Payment Gateway Integration",
    scanId: "scan_008",
    scanType: "Custom Scan",
    title: "Sensitive data in HTTP logs",
    severity: "Medium",
    status: "Unresolved",
    detectedOn: "2025-10-18",
    description: "Payment card data is being logged in plain text in application logs, violating PCI DSS compliance.",
    stepsToReproduce: "1. Process payment transaction\n2. Check application logs\n3. Credit card data visible in logs",
    recommendedFix: "Remove sensitive data from logs. Implement log sanitization and use tokenization for payment data."
  },
  {
    id: "9",
    projectName: "User Authentication System",
    scanId: "scan_009",
    scanType: "Quick Scan",
    title: "Session fixation vulnerability",
    severity: "High",
    status: "Unresolved",
    detectedOn: "2025-10-17",
    description: "Application doesn't regenerate session IDs after successful authentication, allowing session fixation attacks.",
    stepsToReproduce: "1. Obtain session ID before login\n2. Login with valid credentials\n3. Session ID remains the same",
    recommendedFix: "Regenerate session IDs after successful authentication and implement proper session management."
  },
  {
    id: "10",
    projectName: "Admin Dashboard Security",
    scanId: "scan_010",
    scanType: "Full Scan",
    title: "Cross-Site Request Forgery (CSRF) protection missing",
    severity: "High",
    status: "Resolved",
    detectedOn: "2025-10-17",
    description: "Admin actions lack CSRF protection, allowing attackers to perform unauthorized actions on behalf of authenticated users.",
    stepsToReproduce: "1. Create malicious form targeting admin action\n2. Trick admin into submitting form\n3. Unauthorized action performed",
    recommendedFix: "Implement CSRF tokens for all state-changing operations. Use SameSite cookie attributes."
  },
  {
    id: "11",
    projectName: "E-commerce API Security",
    scanId: "scan_011",
    scanType: "Custom Scan",
    title: "Insecure cryptographic storage",
    severity: "Critical",
    status: "Unresolved",
    detectedOn: "2025-10-16",
    description: "User passwords are stored using weak hashing algorithms that can be easily cracked.",
    stepsToReproduce: "1. Check password storage mechanism\n2. MD5 hashing detected\n3. Passwords vulnerable to rainbow table attacks",
    recommendedFix: "Implement strong password hashing using bcrypt, scrypt, or Argon2 with appropriate work factors."
  },
  {
    id: "12",
    projectName: "Mobile App Backend",
    scanId: "scan_012",
    scanType: "Quick Scan",
    title: "Unnecessary HTTP methods enabled",
    severity: "Low",
    status: "Resolved",
    detectedOn: "2025-10-16",
    description: "Unnecessary HTTP methods like TRACE and OPTIONS are enabled, potentially exposing sensitive information.",
    stepsToReproduce: "1. Send TRACE request to server\n2. Server responds with request details\n3. Potential information disclosure",
    recommendedFix: "Disable unnecessary HTTP methods on the web server. Only allow required methods for each endpoint."
  }
]

// Summary stats calculations
const getSummaryStats = (findings: Finding[]) => {
  const total = findings.length
  const critical = findings.filter(f => f.severity === "Critical").length
  const high = findings.filter(f => f.severity === "High").length
  const resolved = findings.filter(f => f.status === "Resolved").length

  return { total, critical, high, resolved }
}

function getSeverityBadge(severity: Finding["severity"]) {
  switch (severity) {
    case "Critical":
      return <Badge className="bg-red-500/10 text-red-500 border-red-500/20">Critical</Badge>
    case "High":
      return <Badge className="bg-orange-500/10 text-orange-500 border-orange-500/20">High</Badge>
    case "Medium":
      return <Badge className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">Medium</Badge>
    case "Low":
      return <Badge className="bg-green-500/10 text-green-500 border-green-500/20">Low</Badge>
    default:
      return <Badge variant="secondary">{severity}</Badge>
  }
}

function getStatusBadge(status: Finding["status"]) {
  switch (status) {
    case "Resolved":
      return <Badge className="bg-green-500/10 text-green-500 border-green-500/20">Resolved</Badge>
    case "Unresolved":
      return <Badge className="bg-red-500/10 text-red-500 border-red-500/20">Unresolved</Badge>
    case "Ignored":
      return <Badge className="bg-gray-500/10 text-gray-500 border-gray-500/20">Ignored</Badge>
    default:
      return <Badge variant="secondary">{status}</Badge>
  }
}

function getSeverityIcon(severity: Finding["severity"]) {
  switch (severity) {
    case "Critical":
      return <AlertTriangle className="h-4 w-4 text-red-500" />
    case "High":
      return <AlertCircle className="h-4 w-4 text-orange-500" />
    case "Medium":
      return <Info className="h-4 w-4 text-yellow-500" />
    case "Low":
      return <CheckCircle className="h-4 w-4 text-green-500" />
    default:
      return null
  }
}

function SummaryCard({ title, value, icon: Icon, description }: {
  title: string
  value: number
  icon: any
  description: string
}) {
  return (
    <Card className="bg-card border-border">
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
        <Icon className="h-4 w-4 text-muted-foreground" />
      </CardHeader>
      <CardContent>
        <div className="text-2xl font-bold text-foreground">{value}</div>
        <p className="text-xs text-muted-foreground">{description}</p>
      </CardContent>
    </Card>
  )
}

function FindingDetailsDialog({ finding, onMarkResolved }: {
  finding: Finding
  onMarkResolved: (id: string) => void
}) {
  const [open, setOpen] = useState(false)

  const handleMarkResolved = () => {
    onMarkResolved(finding.id)
    setOpen(false)
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="ghost" size="sm" className="h-8 w-8 p-0">
          <Eye className="h-4 w-4" />
        </Button>
      </DialogTrigger>
      <DialogContent className="bg-card border-border max-w-2xl max-h-[80vh] overflow-y-auto">
        <DialogHeader>
          <div className="flex items-start justify-between gap-4">
            <DialogTitle className="text-foreground text-left flex-1">
              {finding.title}
            </DialogTitle>
            {getSeverityBadge(finding.severity)}
          </div>
        </DialogHeader>

        <div className="space-y-6">
          <div className="flex items-center justify-between text-sm">
            <div className="flex items-center gap-2 text-muted-foreground">
              <Shield className="h-4 w-4" />
              <span>{finding.projectName}</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground">
              <FileText className="h-4 w-4" />
              <span>{finding.scanType}</span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Description</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {finding.description}
              </p>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Steps to Reproduce</h4>
              <pre className="text-sm text-muted-foreground bg-background p-3 rounded-md border border-border whitespace-pre-wrap">
                {finding.stepsToReproduce}
              </pre>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Recommended Fix</h4>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {finding.recommendedFix}
              </p>
            </div>
          </div>

          <div className="flex items-center justify-between pt-4 border-t border-border">
            <div className="flex items-center gap-4">
              <span className="text-sm text-muted-foreground">Status:</span>
              {getStatusBadge(finding.status)}
            </div>
            {finding.status !== "Resolved" && (
              <Button
                onClick={handleMarkResolved}
                className="bg-green-500 text-white hover:bg-green-600"
              >
                <CheckCircle className="h-4 w-4 mr-2" />
                Mark as Resolved
              </Button>
            )}
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}

function FindingsTableRow({ finding, onMarkResolved }: {
  finding: Finding
  onMarkResolved: (id: string) => void
}) {
  return (
    <TableRow className="border-border">
      <TableCell className="font-medium text-foreground">
        {finding.projectName}
      </TableCell>
      <TableCell className="text-muted-foreground">
        <div className="flex flex-col">
          <span className="font-mono text-xs">{finding.scanId}</span>
          <span className="text-xs">{finding.scanType}</span>
        </div>
      </TableCell>
      <TableCell className="font-medium text-foreground">
        <div className="flex items-start gap-2 max-w-md">
          {getSeverityIcon(finding.severity)}
          <span className="line-clamp-2">{finding.title}</span>
        </div>
      </TableCell>
      <TableCell>
        {getSeverityBadge(finding.severity)}
      </TableCell>
      <TableCell>
        {getStatusBadge(finding.status)}
      </TableCell>
      <TableCell className="text-muted-foreground">
        {new Date(finding.detectedOn).toLocaleDateString()}
      </TableCell>
      <TableCell>
        <div className="flex items-center gap-2">
          <FindingDetailsDialog finding={finding} onMarkResolved={onMarkResolved} />
          {finding.status !== "Resolved" && (
            <Button
              variant="ghost"
              size="sm"
              className="h-8 w-8 p-0 text-green-500 hover:text-green-600"
              onClick={() => onMarkResolved(finding.id)}
            >
              <CheckCircle className="h-4 w-4" />
            </Button>
          )}
        </div>
      </TableCell>
    </TableRow>
  )
}

function EmptyState() {
  return (
    <Card className="bg-card border-border">
      <CardContent className="flex flex-col items-center justify-center py-12">
        <Bug className="h-16 w-16 text-muted-foreground mb-4" />
        <h3 className="text-lg font-semibold text-foreground mb-2">No findings yet</h3>
        <p className="text-muted-foreground text-center mb-6">
          Run a scan to discover vulnerabilities and security issues in your projects.
        </p>
        <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
          Start a Scan
        </Button>
      </CardContent>
    </Card>
  )
}

export function FindingsContent() {
  const [isLoading, setIsLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState("")
  const [severityFilter, setSeverityFilter] = useState<SeverityFilter>("All")
  const [findings, setFindings] = useState<Finding[]>([])

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setFindings(mockFindings)
      setIsLoading(false)
    }, 1000)

    return () => clearTimeout(timer)
  }, [])

  const handleMarkResolved = (id: string) => {
    setFindings(prev => prev.map(finding =>
      finding.id === id ? { ...finding, status: "Resolved" as const } : finding
    ))
  }

  const filteredFindings = findings.filter(finding => {
    const matchesSearch = finding.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         finding.projectName.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         finding.description.toLowerCase().includes(searchQuery.toLowerCase())

    const matchesSeverity = severityFilter === "All" || finding.severity === severityFilter

    return matchesSearch && matchesSeverity
  })

  const summaryStats = getSummaryStats(findings)

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 mb-8">
          <div className="flex-1">
            <h1 className="text-3xl md:text-4xl font-semibold text-foreground mb-2">
              Findings
            </h1>
            <p className="text-muted-foreground text-sm md:text-base">
              Review vulnerabilities and issues detected across your scans.
            </p>
          </div>
          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search findings..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10 bg-background border-border text-foreground w-full sm:w-64"
              />
            </div>
            <Select value={severityFilter} onValueChange={(value: SeverityFilter) => setSeverityFilter(value)}>
              <SelectTrigger className="bg-background border-border text-foreground w-full sm:w-40">
                <Filter className="h-4 w-4 mr-2" />
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-card border-border">
                <SelectItem value="All" className="text-foreground">All Severity</SelectItem>
                <SelectItem value="Critical" className="text-foreground">Critical</SelectItem>
                <SelectItem value="High" className="text-foreground">High</SelectItem>
                <SelectItem value="Medium" className="text-foreground">Medium</SelectItem>
                <SelectItem value="Low" className="text-foreground">Low</SelectItem>
              </SelectContent>
            </Select>
            <Button variant="secondary" className="bg-secondary text-secondary-foreground hover:bg-secondary/90">
              <Download className="h-4 w-4 mr-2" />
              Export Report
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        {!isLoading && findings.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
            <SummaryCard
              title="Total Findings"
              value={summaryStats.total}
              icon={Bug}
              description="All discovered issues"
            />
            <SummaryCard
              title="Critical Issues"
              value={summaryStats.critical}
              icon={AlertTriangle}
              description="Require immediate attention"
            />
            <SummaryCard
              title="High Severity"
              value={summaryStats.high}
              icon={AlertCircle}
              description="Important security issues"
            />
            <SummaryCard
              title="Resolved Findings"
              value={summaryStats.resolved}
              icon={CheckCircle}
              description="Successfully fixed"
            />
          </div>
        )}

        {/* Findings Table */}
        {isLoading ? (
          <Card className="bg-card border-border">
            <CardContent className="p-0">
              <div className="p-6 space-y-4">
                {[...Array(8)].map((_, i) => (
                  <div key={i} className="flex items-center space-x-4">
                    <Skeleton className="h-4 w-[150px]" />
                    <Skeleton className="h-4 w-[100px]" />
                    <Skeleton className="h-4 w-[250px]" />
                    <Skeleton className="h-6 w-[80px]" />
                    <Skeleton className="h-6 w-[90px]" />
                    <Skeleton className="h-4 w-[100px]" />
                    <Skeleton className="h-8 w-[80px]" />
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        ) : filteredFindings.length === 0 ? (
          findings.length === 0 ? <EmptyState /> : (
            <Card className="bg-card border-border">
              <CardContent className="flex flex-col items-center justify-center py-12">
                <Search className="h-16 w-16 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold text-foreground mb-2">No findings match your criteria</h3>
                <p className="text-muted-foreground text-center">
                  Try adjusting your search terms or filters.
                </p>
              </CardContent>
            </Card>
          )
        ) : (
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle className="text-foreground">
                Security Findings ({filteredFindings.length})
              </CardTitle>
            </CardHeader>
            <CardContent className="p-0">
              <div className="overflow-x-auto">
                <Table>
                  <TableHeader>
                    <TableRow className="border-border">
                      <TableHead className="text-muted-foreground">Project Name</TableHead>
                      <TableHead className="text-muted-foreground">Scan ID/Type</TableHead>
                      <TableHead className="text-muted-foreground">Finding Title</TableHead>
                      <TableHead className="text-muted-foreground">Severity</TableHead>
                      <TableHead className="text-muted-foreground">Status</TableHead>
                      <TableHead className="text-muted-foreground">Detected On</TableHead>
                      <TableHead className="text-muted-foreground">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {filteredFindings.map((finding) => (
                      <FindingsTableRow
                        key={finding.id}
                        finding={finding}
                        onMarkResolved={handleMarkResolved}
                      />
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

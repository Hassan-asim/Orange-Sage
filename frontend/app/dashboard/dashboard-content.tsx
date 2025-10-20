"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Skeleton } from "@/components/ui/skeleton"
import { 
  FolderOpen, 
  Activity, 
  AlertTriangle, 
  FileText, 
  Play, 
  Server, 
  Clock, 
  Database,
  Wifi
} from "lucide-react"
import { useState, useEffect } from "react"

// Mock data
const statsData = [
  {
    title: "Total Projects",
    value: "12",
    icon: FolderOpen,
    description: "Active projects"
  },
  {
    title: "Active Scans",
    value: "3",
    icon: Activity,
    description: "Currently running"
  },
  {
    title: "Critical Findings",
    value: "8",
    icon: AlertTriangle,
    description: "Require attention"
  },
  {
    title: "Reports Generated",
    value: "47",
    icon: FileText,
    description: "This month"
  }
]

const recentActivityData = [
  {
    id: 1,
    projectName: "E-commerce API",
    scanType: "Full Security Scan",
    status: "Completed",
    date: "2025-10-21"
  },
  {
    id: 2,
    projectName: "Mobile App Backend",
    scanType: "Vulnerability Assessment",
    status: "Running",
    date: "2025-10-21"
  },
  {
    id: 3,
    projectName: "Payment Gateway",
    scanType: "Penetration Test",
    status: "Failed",
    date: "2025-10-20"
  },
  {
    id: 4,
    projectName: "User Portal",
    scanType: "Code Review",
    status: "Completed",
    date: "2025-10-20"
  },
  {
    id: 5,
    projectName: "Admin Dashboard",
    scanType: "Security Audit",
    status: "Running",
    date: "2025-10-19"
  }
]

const systemHealthData = [
  {
    label: "Server Uptime",
    value: "99.98%",
    icon: Server,
    status: "healthy"
  },
  {
    label: "API Latency",
    value: "120ms",
    icon: Clock,
    status: "healthy"
  },
  {
    label: "Database Status",
    value: "Connected",
    icon: Database,
    status: "healthy"
  }
]

function getStatusBadge(status: string) {
  switch (status.toLowerCase()) {
    case "completed":
      return <Badge className="bg-green-500/10 text-green-500 border-green-500/20">Completed</Badge>
    case "running":
      return <Badge className="bg-yellow-500/10 text-yellow-500 border-yellow-500/20">Running</Badge>
    case "failed":
      return <Badge className="bg-red-500/10 text-red-500 border-red-500/20">Failed</Badge>
    default:
      return <Badge variant="secondary">{status}</Badge>
  }
}

function StatCard({ title, value, icon: Icon, description, isLoading }: {
  title: string
  value: string
  icon: any
  description: string
  isLoading: boolean
}) {
  if (isLoading) {
    return (
      <Card className="bg-card border-border">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <Skeleton className="h-4 w-[100px]" />
          <Skeleton className="h-4 w-4" />
        </CardHeader>
        <CardContent>
          <Skeleton className="h-8 w-[60px] mb-1" />
          <Skeleton className="h-3 w-[80px]" />
        </CardContent>
      </Card>
    )
  }

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

export function DashboardContent() {
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Simulate loading
    const timer = setTimeout(() => {
      setIsLoading(false)
    }, 1500)

    return () => clearTimeout(timer)
  }, [])

  return (
    <div className="min-h-screen bg-background">
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl md:text-4xl font-semibold text-foreground mb-2">
              Dashboard Overview
            </h1>
            <p className="text-muted-foreground text-sm md:text-base">
              Quick insight into your recent activity and system health.
            </p>
          </div>
          <Button className="bg-primary text-primary-foreground hover:bg-primary/90 px-6 py-2 rounded-full font-medium shadow-sm">
            <Play className="h-4 w-4 mr-2" />
            Start Scan
          </Button>
        </div>

        {/* Stats Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-8">
          {statsData.map((stat, index) => (
            <StatCard
              key={index}
              title={stat.title}
              value={stat.value}
              icon={stat.icon}
              description={stat.description}
              isLoading={isLoading}
            />
          ))}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Recent Activity Table */}
          <div className="lg:col-span-2">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="text-foreground">Recent Activity</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="space-y-3">
                    {[...Array(5)].map((_, i) => (
                      <div key={i} className="flex items-center space-x-4">
                        <Skeleton className="h-4 w-[150px]" />
                        <Skeleton className="h-4 w-[120px]" />
                        <Skeleton className="h-6 w-[80px]" />
                        <Skeleton className="h-4 w-[100px]" />
                      </div>
                    ))}
                  </div>
                ) : (
                  <Table>
                    <TableHeader>
                      <TableRow className="border-border">
                        <TableHead className="text-muted-foreground">Project Name</TableHead>
                        <TableHead className="text-muted-foreground">Scan Type</TableHead>
                        <TableHead className="text-muted-foreground">Status</TableHead>
                        <TableHead className="text-muted-foreground">Date</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {recentActivityData.map((activity) => (
                        <TableRow key={activity.id} className="border-border">
                          <TableCell className="font-medium text-foreground">
                            {activity.projectName}
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {activity.scanType}
                          </TableCell>
                          <TableCell>
                            {getStatusBadge(activity.status)}
                          </TableCell>
                          <TableCell className="text-muted-foreground">
                            {new Date(activity.date).toLocaleDateString()}
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                )}
              </CardContent>
            </Card>
          </div>

          {/* System Health Panel */}
          <div className="lg:col-span-1">
            <Card className="bg-card border-border">
              <CardHeader>
                <CardTitle className="text-foreground">System Health</CardTitle>
              </CardHeader>
              <CardContent>
                {isLoading ? (
                  <div className="space-y-4">
                    {[...Array(3)].map((_, i) => (
                      <div key={i} className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <Skeleton className="h-4 w-4" />
                          <Skeleton className="h-4 w-[80px]" />
                        </div>
                        <Skeleton className="h-4 w-[60px]" />
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="space-y-4">
                    {systemHealthData.map((item, index) => (
                      <div key={index} className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <item.icon className="h-4 w-4 text-muted-foreground" />
                          <span className="text-sm text-foreground">{item.label}</span>
                        </div>
                        <div className="flex items-center space-x-2">
                          <div className="h-2 w-2 bg-green-500 rounded-full"></div>
                          <span className="text-sm font-medium text-foreground">{item.value}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  )
}

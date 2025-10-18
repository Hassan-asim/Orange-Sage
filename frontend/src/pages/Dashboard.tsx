import React from 'react'
import { useQuery } from 'react-query'
import { Shield, Search, AlertTriangle, FileText, Plus, Activity } from 'lucide-react'
import { apiService } from '../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Progress } from '../components/ui/progress'

const Dashboard: React.FC = () => {
  const { data: scans, isLoading: scansLoading } = useQuery('scans', () => apiService.getScans())
  const { data: findings, isLoading: findingsLoading } = useQuery('findings', () => apiService.getFindings())

  const recentScans = scans?.scans?.slice(0, 5) || []
  const recentFindings = findings?.findings?.slice(0, 5) || []

  const getSeverityCount = (severity: string) => {
    return findings?.findings?.filter((finding: any) => finding.severity === severity).length || 0
  }

  const getStatusCount = (status: string) => {
    return scans?.scans?.filter((scan: any) => scan.status === status).length || 0
  }

  const getSeverityBadgeVariant = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'destructive'
      case 'high':
        return 'destructive'
      case 'medium':
        return 'secondary'
      case 'low':
        return 'outline'
      default:
        return 'outline'
    }
  }

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'completed':
        return 'default'
      case 'running':
        return 'secondary'
      case 'failed':
        return 'destructive'
      case 'pending':
        return 'outline'
      default:
        return 'outline'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Welcome to Orange Sage - AI-powered cybersecurity assessment platform
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          New Scan
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Scans</CardTitle>
            <Search className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{scans?.scans?.length || 0}</div>
            <p className="text-xs text-muted-foreground">
              {getStatusCount('running')} currently running
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Findings</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{findings?.findings?.length || 0}</div>
            <p className="text-xs text-muted-foreground">
              {getSeverityCount('critical')} critical issues
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Scans</CardTitle>
            <Activity className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{getStatusCount('running')}</div>
            <p className="text-xs text-muted-foreground">
              {getStatusCount('pending')} pending
            </p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Reports Generated</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">0</div>
            <p className="text-xs text-muted-foreground">
              PDF, DOCX, and HTML formats
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Recent Scans */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Scans</CardTitle>
            <CardDescription>
              Your latest security assessments
            </CardDescription>
          </CardHeader>
          <CardContent>
            {scansLoading ? (
              <div className="space-y-2">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-16 bg-muted animate-pulse rounded" />
                ))}
              </div>
            ) : recentScans.length > 0 ? (
              <div className="space-y-4">
                {recentScans.map((scan: any) => (
                  <div key={scan.id} className="flex items-center justify-between">
                    <div className="space-y-1">
                      <p className="text-sm font-medium">{scan.name}</p>
                      <p className="text-xs text-muted-foreground">
                        {new Date(scan.created_at).toLocaleDateString()}
                      </p>
                    </div>
                    <Badge variant={getStatusBadgeVariant(scan.status)}>
                      {scan.status}
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <Search className="mx-auto h-12 w-12 text-muted-foreground" />
                <h3 className="mt-2 text-sm font-semibold text-gray-900">No scans yet</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Get started by creating your first security scan.
                </p>
                <div className="mt-6">
                  <Button>
                    <Plus className="mr-2 h-4 w-4" />
                    New Scan
                  </Button>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* Recent Findings */}
        <Card>
          <CardHeader>
            <CardTitle>Recent Findings</CardTitle>
            <CardDescription>
              Latest security vulnerabilities discovered
            </CardDescription>
          </CardHeader>
          <CardContent>
            {findingsLoading ? (
              <div className="space-y-2">
                {[...Array(3)].map((_, i) => (
                  <div key={i} className="h-16 bg-muted animate-pulse rounded" />
                ))}
              </div>
            ) : recentFindings.length > 0 ? (
              <div className="space-y-4">
                {recentFindings.map((finding: any) => (
                  <div key={finding.id} className="flex items-center justify-between">
                    <div className="space-y-1">
                      <p className="text-sm font-medium">{finding.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {finding.endpoint || 'N/A'}
                      </p>
                    </div>
                    <Badge variant={getSeverityBadgeVariant(finding.severity)}>
                      {finding.severity}
                    </Badge>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-6">
                <AlertTriangle className="mx-auto h-12 w-12 text-muted-foreground" />
                <h3 className="mt-2 text-sm font-semibold text-gray-900">No findings yet</h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  Run a scan to discover security vulnerabilities.
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Security Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Security Overview</CardTitle>
          <CardDescription>
            Summary of your security posture
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Critical</span>
                <span className="text-sm text-muted-foreground">{getSeverityCount('critical')}</span>
              </div>
              <Progress value={(getSeverityCount('critical') / Math.max(findings?.findings?.length || 1, 1)) * 100} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">High</span>
                <span className="text-sm text-muted-foreground">{getSeverityCount('high')}</span>
              </div>
              <Progress value={(getSeverityCount('high') / Math.max(findings?.findings?.length || 1, 1)) * 100} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Medium</span>
                <span className="text-sm text-muted-foreground">{getSeverityCount('medium')}</span>
              </div>
              <Progress value={(getSeverityCount('medium') / Math.max(findings?.findings?.length || 1, 1)) * 100} className="h-2" />
            </div>
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm font-medium">Low</span>
                <span className="text-sm text-muted-foreground">{getSeverityCount('low')}</span>
              </div>
              <Progress value={(getSeverityCount('low') / Math.max(findings?.findings?.length || 1, 1)) * 100} className="h-2" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}

export default Dashboard

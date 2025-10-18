import React from 'react'
import { useQuery } from 'react-query'
import { useNavigate } from 'react-router-dom'
import { Plus, Search, Clock, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { apiService } from '../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Progress } from '../components/ui/progress'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table'

const Scans: React.FC = () => {
  const navigate = useNavigate()
  const { data: scans, isLoading } = useQuery('scans', () => apiService.getScans())

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />
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

  const formatDuration = (startTime: string, endTime?: string) => {
    if (!startTime) return 'N/A'
    const start = new Date(startTime)
    const end = endTime ? new Date(endTime) : new Date()
    const diff = end.getTime() - start.getTime()
    const minutes = Math.floor(diff / 60000)
    const seconds = Math.floor((diff % 60000) / 1000)
    return `${minutes}m ${seconds}s`
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Security Scans</h1>
          <p className="text-muted-foreground">
            Monitor and manage your security assessments
          </p>
        </div>
        <Button onClick={() => navigate('/scans/new')}>
          <Plus className="mr-2 h-4 w-4" />
          New Scan
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Scans</CardTitle>
            <Search className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{scans?.scans?.length || 0}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Running</CardTitle>
            <Clock className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {scans?.scans?.filter((scan: any) => scan.status === 'running').length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {scans?.scans?.filter((scan: any) => scan.status === 'completed').length || 0}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Failed</CardTitle>
            <XCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">
              {scans?.scans?.filter((scan: any) => scan.status === 'failed').length || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Scans Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Scans</CardTitle>
          <CardDescription>
            View and manage all your security scans
          </CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="space-y-2">
              {[...Array(5)].map((_, i) => (
                <div key={i} className="h-16 bg-muted animate-pulse rounded" />
              ))}
            </div>
          ) : scans?.scans?.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Target</TableHead>
                  <TableHead>Duration</TableHead>
                  <TableHead>Findings</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {scans.scans.map((scan: any) => (
                  <TableRow key={scan.id} className="cursor-pointer hover:bg-muted/50">
                    <TableCell className="font-medium">{scan.name}</TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(scan.status)}
                        <Badge variant={getStatusBadgeVariant(scan.status)}>
                          {scan.status}
                        </Badge>
                      </div>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {scan.target || 'N/A'}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {formatDuration(scan.started_at, scan.finished_at)}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {scan.findings_count || 0}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {new Date(scan.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => navigate(`/scans/${scan.id}`)}
                      >
                        View Details
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="text-center py-12">
              <Search className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No scans yet</h3>
              <p className="text-muted-foreground mb-6">
                Create your first security scan to start assessing your applications.
              </p>
              <Button onClick={() => navigate('/scans/new')}>
                <Plus className="mr-2 h-4 w-4" />
                Create Scan
              </Button>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}

export default Scans

import React from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { useQuery } from 'react-query'
import { ArrowLeft, Play, Square, Download, FileText, AlertTriangle, Clock, CheckCircle, XCircle } from 'lucide-react'
import { apiService } from '../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Progress } from '../components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table'

const ScanDetail: React.FC = () => {
  const { scanId } = useParams<{ scanId: string }>()
  const navigate = useNavigate()
  
  const { data: scan, isLoading: scanLoading } = useQuery(
    ['scan', scanId],
    () => apiService.getScan(Number(scanId)),
    { enabled: !!scanId }
  )
  
  const { data: agents, isLoading: agentsLoading } = useQuery(
    ['scan-agents', scanId],
    () => apiService.getScanAgents(Number(scanId)),
    { enabled: !!scanId }
  )

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'running':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      case 'pending':
        return <Clock className="h-4 w-4 text-yellow-500" />
      default:
        return <Clock className="h-4 w-4 text-gray-500" />
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

  const handleCancelScan = async () => {
    if (scanId) {
      try {
        await apiService.cancelScan(Number(scanId))
        // Refresh scan data
        window.location.reload()
      } catch (error) {
        console.error('Failed to cancel scan:', error)
      }
    }
  }

  const handleGenerateReport = async () => {
    if (scanId) {
      try {
        const result = await apiService.generateReport(Number(scanId), {
          format: 'pdf',
          include_charts: true,
          include_pocs: true,
          branding: 'Orange Sage'
        })
        console.log('Report generation started:', result)
      } catch (error) {
        console.error('Failed to generate report:', error)
      }
    }
  }

  if (scanLoading) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-muted animate-pulse rounded w-1/4"></div>
        <div className="grid gap-4 md:grid-cols-2">
          <div className="h-64 bg-muted animate-pulse rounded"></div>
          <div className="h-64 bg-muted animate-pulse rounded"></div>
        </div>
      </div>
    )
  }

  if (!scan) {
    return (
      <div className="text-center py-12">
        <h3 className="text-lg font-semibold mb-2">Scan not found</h3>
        <p className="text-muted-foreground mb-6">
          The scan you're looking for doesn't exist or you don't have access to it.
        </p>
        <Button onClick={() => navigate('/scans')}>
          <ArrowLeft className="mr-2 h-4 w-4" />
          Back to Scans
        </Button>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button variant="outline" size="icon" onClick={() => navigate('/scans')}>
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">{scan.name}</h1>
            <p className="text-muted-foreground">
              {scan.description || 'Security assessment scan'}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          {scan.status === 'running' && (
            <Button variant="destructive" onClick={handleCancelScan}>
              <Square className="mr-2 h-4 w-4" />
              Cancel Scan
            </Button>
          )}
          {scan.status === 'completed' && (
            <Button onClick={handleGenerateReport}>
              <Download className="mr-2 h-4 w-4" />
              Generate Report
            </Button>
          )}
        </div>
      </div>

      {/* Status Card */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            {getStatusIcon(scan.status)}
            <span>Scan Status</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-between">
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                <Badge variant={getStatusBadgeVariant(scan.status)}>
                  {scan.status}
                </Badge>
                <span className="text-sm text-muted-foreground">
                  {scan.agents_count} agents
                </span>
              </div>
              <div className="text-sm text-muted-foreground">
                Started: {scan.started_at ? new Date(scan.started_at).toLocaleString() : 'Not started'}
              </div>
              {scan.finished_at && (
                <div className="text-sm text-muted-foreground">
                  Finished: {new Date(scan.finished_at).toLocaleString()}
                </div>
              )}
            </div>
            {scan.status === 'running' && (
              <div className="w-32">
                <Progress value={50} className="h-2" />
                <p className="text-xs text-muted-foreground mt-1">In progress...</p>
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="agents">Agents</TabsTrigger>
          <TabsTrigger value="findings">Findings</TabsTrigger>
          <TabsTrigger value="logs">Logs</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-4">
          <div className="grid gap-4 md:grid-cols-2">
            <Card>
              <CardHeader>
                <CardTitle>Scan Information</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Target:</span>
                  <span className="text-sm">{scan.target || 'N/A'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Created:</span>
                  <span className="text-sm">{new Date(scan.created_at).toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Duration:</span>
                  <span className="text-sm">
                    {scan.started_at && scan.finished_at
                      ? `${Math.floor((new Date(scan.finished_at).getTime() - new Date(scan.started_at).getTime()) / 60000)}m`
                      : 'N/A'}
                  </span>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Summary</CardTitle>
              </CardHeader>
              <CardContent className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Total Findings:</span>
                  <span className="text-sm font-medium">{scan.findings_count || 0}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Critical:</span>
                  <span className="text-sm font-medium text-red-600">
                    {scan.summary?.critical_count || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">High:</span>
                  <span className="text-sm font-medium text-orange-600">
                    {scan.summary?.high_count || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Medium:</span>
                  <span className="text-sm font-medium text-yellow-600">
                    {scan.summary?.medium_count || 0}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-muted-foreground">Low:</span>
                  <span className="text-sm font-medium text-green-600">
                    {scan.summary?.low_count || 0}
                  </span>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="agents" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Active Agents</CardTitle>
              <CardDescription>
                AI agents performing the security assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              {agentsLoading ? (
                <div className="space-y-2">
                  {[...Array(3)].map((_, i) => (
                    <div key={i} className="h-16 bg-muted animate-pulse rounded" />
                  ))}
                </div>
              ) : agents?.agents?.length > 0 ? (
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Agent</TableHead>
                      <TableHead>Status</TableHead>
                      <TableHead>Progress</TableHead>
                      <TableHead>Iteration</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {agents.agents.map((agent: any) => (
                      <TableRow key={agent.id}>
                        <TableCell className="font-medium">{agent.name}</TableCell>
                        <TableCell>
                          <Badge variant={getStatusBadgeVariant(agent.status)}>
                            {agent.status}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          <div className="w-32">
                            <Progress value={agent.progress} className="h-2" />
                          </div>
                        </TableCell>
                        <TableCell>{agent.iteration}/{agent.max_iterations}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              ) : (
                <div className="text-center py-6">
                  <AlertTriangle className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                  <h3 className="text-lg font-semibold mb-2">No agents found</h3>
                  <p className="text-muted-foreground">
                    Agents will appear here when the scan starts.
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="findings" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Security Findings</CardTitle>
              <CardDescription>
                Vulnerabilities and security issues discovered during the scan
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="text-center py-6">
                <AlertTriangle className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">Findings will appear here</h3>
                <p className="text-muted-foreground">
                  Security findings will be displayed as they are discovered during the scan.
                </p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="logs" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle>Scan Logs</CardTitle>
              <CardDescription>
                Real-time logs from the security assessment
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="bg-muted p-4 rounded-lg font-mono text-sm">
                <div className="text-muted-foreground">
                  {scan.status === 'running' ? (
                    <div className="space-y-1">
                      <div>[INFO] Scan started successfully</div>
                      <div>[INFO] Initializing AI agents...</div>
                      <div>[INFO] Agents are now running security assessments</div>
                      <div className="text-primary">[LIVE] Scan in progress...</div>
                    </div>
                  ) : scan.status === 'completed' ? (
                    <div className="space-y-1">
                      <div>[INFO] Scan started successfully</div>
                      <div>[INFO] Initializing AI agents...</div>
                      <div>[INFO] Agents completed security assessments</div>
                      <div className="text-green-600">[SUCCESS] Scan completed successfully</div>
                    </div>
                  ) : (
                    <div className="text-muted-foreground">No logs available</div>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

export default ScanDetail

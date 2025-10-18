import React from 'react'
import { useQuery } from 'react-query'
import { FileText, Download, Eye, Calendar, User, Plus } from 'lucide-react'
import { apiService } from '../services/apiService'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Badge } from '../components/ui/badge'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '../components/ui/table'

const Reports: React.FC = () => {
  // Mock data for reports since we don't have a reports endpoint yet
  const reports = [
    {
      id: 1,
      name: 'Security Assessment Report - Web Application',
      format: 'PDF',
      status: 'completed',
      scan_id: 1,
      created_at: '2024-01-15T10:30:00Z',
      file_size: '2.4 MB',
      download_url: '/api/v1/reports/1/download'
    },
    {
      id: 2,
      name: 'Vulnerability Report - API Endpoints',
      format: 'DOCX',
      status: 'completed',
      scan_id: 2,
      created_at: '2024-01-14T15:45:00Z',
      file_size: '1.8 MB',
      download_url: '/api/v1/reports/2/download'
    },
    {
      id: 3,
      name: 'Security Assessment Report - Mobile App',
      format: 'HTML',
      status: 'generating',
      scan_id: 3,
      created_at: '2024-01-13T09:15:00Z',
      file_size: null,
      download_url: null
    }
  ]

  const getStatusBadgeVariant = (status: string) => {
    switch (status) {
      case 'completed':
        return 'default'
      case 'generating':
        return 'secondary'
      case 'failed':
        return 'destructive'
      case 'pending':
        return 'outline'
      default:
        return 'outline'
    }
  }

  const getFormatIcon = (format: string) => {
    switch (format.toLowerCase()) {
      case 'pdf':
        return <FileText className="h-4 w-4 text-red-500" />
      case 'docx':
        return <FileText className="h-4 w-4 text-blue-500" />
      case 'html':
        return <FileText className="h-4 w-4 text-green-500" />
      default:
        return <FileText className="h-4 w-4 text-gray-500" />
    }
  }

  const handleDownload = async (reportId: number) => {
    try {
      const blob = await apiService.downloadReport(reportId)
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `report-${reportId}.pdf`
      document.body.appendChild(a)
      a.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(a)
    } catch (error) {
      console.error('Failed to download report:', error)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
          <p className="text-muted-foreground">
            Generate and download security assessment reports
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" />
          Generate Report
        </Button>
      </div>

      {/* Stats Cards */}
      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Reports</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{reports.length}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Completed</CardTitle>
            <FileText className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {reports.filter(r => r.status === 'completed').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Generating</CardTitle>
            <FileText className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {reports.filter(r => r.status === 'generating').length}
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Size</CardTitle>
            <FileText className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">4.2 MB</div>
          </CardContent>
        </Card>
      </div>

      {/* Reports Table */}
      <Card>
        <CardHeader>
          <CardTitle>All Reports</CardTitle>
          <CardDescription>
            Security assessment reports in various formats
          </CardDescription>
        </CardHeader>
        <CardContent>
          {reports.length > 0 ? (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Format</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Size</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {reports.map((report) => (
                  <TableRow key={report.id} className="cursor-pointer hover:bg-muted/50">
                    <TableCell className="font-medium">{report.name}</TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {getFormatIcon(report.format)}
                        <span className="text-sm">{report.format}</span>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant={getStatusBadgeVariant(report.status)}>
                        {report.status}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {report.file_size || 'N/A'}
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {new Date(report.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center space-x-2">
                        {report.status === 'completed' && (
                          <Button
                            variant="outline"
                            size="sm"
                            onClick={() => handleDownload(report.id)}
                          >
                            <Download className="mr-2 h-4 w-4" />
                            Download
                          </Button>
                        )}
                        {report.status === 'generating' && (
                          <Button variant="outline" size="sm" disabled>
                            <Eye className="mr-2 h-4 w-4" />
                            Generating...
                          </Button>
                        )}
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          ) : (
            <div className="text-center py-12">
              <FileText className="mx-auto h-12 w-12 text-muted-foreground mb-4" />
              <h3 className="text-lg font-semibold mb-2">No reports yet</h3>
              <p className="text-muted-foreground mb-6">
                Generate your first security assessment report from a completed scan.
              </p>
              <Button>
                <Plus className="mr-2 h-4 w-4" />
                Generate Report
              </Button>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Report Formats Info */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="h-5 w-5 text-red-500" />
              <span>PDF Reports</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Professional PDF reports with charts, findings, and recommendations. 
              Perfect for executive summaries and compliance documentation.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="h-5 w-5 text-blue-500" />
              <span>DOCX Reports</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Editable Word documents that can be customized and shared with your team. 
              Ideal for collaborative review and editing.
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <FileText className="h-5 w-5 text-green-500" />
              <span>HTML Reports</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Interactive HTML reports that can be viewed in any web browser. 
              Great for online sharing and embedding in dashboards.
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default Reports

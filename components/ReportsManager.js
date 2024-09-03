import { useState, useEffect } from 'react'

export default function ReportsManager() {
  const [reports, setReports] = useState([])
  const [selectedReport, setSelectedReport] = useState(null)

  useEffect(() => {
    fetchReports()
  }, [])

  const fetchReports = async () => {
    try {
      const response = await fetch('/api/reports')
      if (response.ok) {
        const data = await response.json()
        setReports(data)
      } else {
        console.error('Failed to fetch reports')
      }
    } catch (error) {
      console.error('Error fetching reports:', error)
    }
  }

  const handleReportSelect = async (reportId) => {
    try {
      const response = await fetch(`/api/reports/${reportId}`)
      if (response.ok) {
        const data = await response.json()
        setSelectedReport(data)
      } else {
        console.error('Failed to fetch report')
      }
    } catch (error) {
      console.error('Error fetching report:', error)
    }
  }

  const handleDownloadReport = (reportId) => {
    window.open(`/api/reports/${reportId}/download`, '_blank')
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold mb-4">Reports Manager</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="col-span-1 bg-gray-100 p-4 rounded">
          <h3 className="font-bold mb-2">Saved Reports</h3>
          <ul className="space-y-2">
            {reports.map(report => (
              <li key={report.id} className="flex justify-between items-center">
                <button 
                  onClick={() => handleReportSelect(report.id)}
                  className="text-blue-500 hover:underline"
                >
                  {report.name}
                </button>
                <button 
                  onClick={() => handleDownloadReport(report.id)}
                  className="px-2 py-1 bg-green-500 text-white rounded text-sm"
                >
                  Download
                </button>
              </li>
            ))}
          </ul>
        </div>
        <div className="col-span-2 bg-gray-100 p-4 rounded">
          <h3 className="font-bold mb-2">Report Details</h3>
          {selectedReport ? (
            <div>
              <h4 className="font-bold">{selectedReport.name}</h4>
              <p>Date: {new Date(selectedReport.date).toLocaleString()}</p>
              <p>Targets: {selectedReport.targets.join(', ')}</p>
              <h5 className="font-bold mt-4">Summary:</h5>
              <ul className="list-disc pl-5">
                <li>Total vulnerabilities: {selectedReport.total_vulnerabilities}</li>
                <li>Risk score: {selectedReport.risk_score}</li>
                <li>Critical issues: {selectedReport.critical_issues}</li>
              </ul>
              <h5 className="font-bold mt-4">Vulnerabilities:</h5>
              <ul className="list-disc pl-5">
                {selectedReport.vulnerabilities.map((vuln, index) => (
                  <li key={index}>
                    {vuln.type} - Severity: {vuln.severity}
                  </li>
                ))}
              </ul>
            </div>
          ) : (
            <p>Select a report to view details</p>
          )}
        </div>
      </div>
    </div>
  )
}
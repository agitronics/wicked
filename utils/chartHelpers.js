export const generateVulnerabilityChart = (vulnerabilities) => {
  return {
    labels: vulnerabilities.map(v => v.type),
    datasets: [
      {
        label: 'Severity',
        data: vulnerabilities.map(v => ({
          'Critical': 4,
          'High': 3,
          'Medium': 2,
          'Low': 1
        }[v.severity])),
        backgroundColor: vulnerabilities.map(v => ({
          'Critical': 'rgba(255, 99, 132, 0.5)',
          'High': 'rgba(255, 159, 64, 0.5)',
          'Medium': 'rgba(255, 205, 86, 0.5)',
          'Low': 'rgba(75, 192, 192, 0.5)'
        }[v.severity])),
      }
    ]
  }
}

export const generateTargetDistributionChart = (targets) => {
  const categories = Object.keys(targets)
  const data = Object.values(targets).map(arr => arr.length)
  
  return {
    labels: categories,
    datasets: [
      {
        data: data,
        backgroundColor: [
          'rgba(255, 99, 132, 0.5)',
          'rgba(54, 162, 235, 0.5)',
          'rgba(255, 206, 86, 0.5)',
          'rgba(75, 192, 192, 0.5)',
          'rgba(153, 102, 255, 0.5)',
          'rgba(255, 159, 64, 0.5)'
        ]
      }
    ]
  }
}
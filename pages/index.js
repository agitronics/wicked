import { useState } from 'react'
import Head from 'next/head'
import AdvancedIntegratedScan from '../components/AdvancedIntegratedScan'
import ReportsManager from '../components/ReportsManager'

export default function Home() {
  const [activeTab, setActiveTab] = useState('advanced-integrated-scan')

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'advanced-integrated-scan':
        return <AdvancedIntegratedScan />
      case 'reports-manager':
        return <ReportsManager />
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Head>
        <title>Advanced Network Tools Interface</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="container mx-auto p-4">
        <h1 className="text-4xl font-bold mb-8">Advanced Network Tools Interface</h1>
        <div className="flex flex-wrap mb-4">
          {['Advanced Integrated Scan', 'Reports Manager'].map((tab) => (
            <button
              key={tab.toLowerCase().replace(' ', '-')}
              className={`mr-2 mb-2 px-4 py-2 rounded ${
                activeTab === tab.toLowerCase().replace(' ', '-')
                  ? 'bg-blue-500 text-white'
                  : 'bg-white text-blue-500'
              }`}
              onClick={() => setActiveTab(tab.toLowerCase().replace(' ', '-'))}
            >
              {tab}
            </button>
          ))}
        </div>
        <div className="bg-white p-6 rounded shadow">{renderActiveTab()}</div>
      </main>
    </div>
  )
}
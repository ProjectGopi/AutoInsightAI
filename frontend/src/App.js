import { Routes, Route, Link } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Datasets from "./pages/Datasets";
import Analytics from "./pages/Analytics";
import Settings from "./pages/Settings";
import { useEffect, useState } from "react";
import { getSettings } from "./services/api";


function App() {
  const [results, setResults] = useState(null);
  const [darkMode, setDarkMode] = useState(false);
  useEffect(() => {
      fetchSettings();
    }, []);

    const fetchSettings = async () => {
      try {
        const res = await getSettings();
        setDarkMode(res.data.dark_mode);
      } catch (error) {
        console.error("Error loading settings:", error);
      }
    };
  return (
    <div className={`${darkMode ? "dark" : ""} flex min-h-screen bg-gray-100 dark:bg-gray-900`}>

      {/* Sidebar */}
      <div className="hidden w-64 p-6 bg-white shadow-lg dark:bg-gray-800 md:block">
        <h2 className="mb-8 text-2xl font-bold text-blue-700 dark:text-blue-400">
          AutoInsight
        </h2>

        <ul className="space-y-4 text-gray-600 dark:text-gray-300">
          <li>
            <Link to="/" className="font-medium hover:text-blue-600">
              Dashboard
            </Link>
          </li>

          <li>
            <Link to="/datasets" className="hover:text-blue-600">
              Datasets
            </Link>
          </li>

          <li>
            <Link to="/settings" className="hover:text-blue-600">
              Settings
            </Link>
          </li>
        </ul>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-10">

        <Routes>
          <Route 
            path="/" 
            element={
              <Dashboard 
                results={results}
                setResults={setResults}
              />
            } 
          />
          <Route path="/datasets" element={<Datasets />} />
          <Route path="/analytics/:datasetId" element={<Analytics />} />
          <Route 
            path="/settings" 
            element={<Settings setDarkMode={setDarkMode} />} 
          />
        </Routes>

      </div>
    </div>
  );
}

export default App;
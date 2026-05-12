    import { useState } from "react";
    import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    CartesianGrid,
    } from "recharts";

    import {
    uploadDataset,
    analyzeDataset,
    getResults,
    getPowerBI,
    } from "../services/api";

    function Dashboard({ results, setResults }) {

    const [file, setFile] = useState(null);
    const [status, setStatus] = useState("");
    const [powerBI, setPowerBI] = useState(null);

    const isProcessing =
        status === "Processing..." ||
        status === "Starting Analysis..." ||
        status === "Uploading...";

    const handleUpload = async () => {
        if (!file) return alert("Select a file first");

        const formData = new FormData();
        formData.append("file", file);

        try {
        setStatus("Uploading...");
        const uploadRes = await uploadDataset(formData);

        const datasetId = uploadRes.data.dataset_id;

        setStatus("Starting Analysis...");
        await analyzeDataset(datasetId);

        pollResults(datasetId);

        } catch (error) {
        console.error(error);
        setStatus("Error occurred");
        }
    };

    const pollResults = (datasetId) => {
        const interval = setInterval(async () => {
        const res = await getResults(datasetId);

        if (res.data.status === "completed") {
            setResults(res.data.results);

            const powerRes = await getPowerBI(datasetId);
            setPowerBI(powerRes.data.powerbi_export);

            setStatus("Completed");
            clearInterval(interval);
        } else {
            setStatus("Processing...");
        }
        }, 3000);
    };

    return (
        <div>

        <h1 className="text-3xl font-bold text-blue-700 mb-6">
            AI Analytics Dashboard
        </h1>

        {/* Upload Section */}
        <div className="bg-white p-8 rounded-2xl shadow-lg border max-w-xl">
            <input
            type="file"
            className="mb-4"
            onChange={(e) => setFile(e.target.files[0])}
            />

            <button
            onClick={handleUpload}
            className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            >
            Upload & Analyze
            </button>

            {isProcessing && (
            <div className="flex items-center space-x-2 mt-4">
                <div className="w-4 h-4 border-2 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                <p className="font-semibold">{status}</p>
            </div>
            )}

            {status === "Completed" && (
            <p className="mt-4 font-semibold text-green-600">
                Analysis Completed
            </p>
            )}
        </div>

        {/* Results */}
        {results && (
            <div className="mt-10 space-y-6">

            {/* KPI Chart */}
            <div className="bg-white p-6 rounded-xl shadow">
                <h2 className="text-xl font-bold mb-4">
                KPI Influence Chart
                </h2>

                <div className="overflow-x-auto">
                <BarChart
                    width={700}
                    height={300}
                    data={results.kpi_insights.top_influencers}
                >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="feature" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="importance" fill="#2563eb" />
                </BarChart>
                </div>
            </div>

            {/* Power BI */}
            {powerBI && (
                <div className="bg-white p-6 rounded-xl shadow">
                <h2 className="text-xl font-bold mb-4">
                    Power BI Recommendations
                </h2>

                <p>
                    Clean Dataset Path:
                    <span className="text-blue-600 ml-2">
                    {powerBI.clean_dataset_path}
                    </span>
                </p>
                </div>
            )}

            </div>
        )}

        </div>
    );
    }

    export default Dashboard;
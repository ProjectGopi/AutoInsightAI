    import { useEffect, useState } from "react";
    import { useParams } from "react-router-dom";
    import { getResults } from "../services/api";

    function Analytics() {
    const { datasetId } = useParams();
    const [results, setResults] = useState(null);

    useEffect(() => {
        const fetchResults = async () => {
            try {
            const res = await getResults(datasetId);
            setResults(res.data);
            } catch (error) {
            console.error(error);
            }
        };

        fetchResults();
        }, [datasetId]);

    const fetchResults = async () => {
        try {
        const res = await getResults(datasetId);
        setResults(res.data);
        console.log(res.data);
        } catch (error) {
        console.error(error);
        }
        
    };

    if (!results) {
        return <div className="text-gray-800 dark:text-white">Loading analysis...</div>;
    }

    const analysis = results.results || {};

    const profile = analysis.profile_summary || {};
    const anomaly = analysis.anomaly_insights || {};
    const ranked = analysis.ranked_insights?.ranked_insights || [];

    return (
        <div className="space-y-8 text-gray-800 dark:text-white">

        <h1 className="text-3xl font-bold">Dataset Analytics</h1>

        {/* KPI CARDS */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-4">

            <Card title="Total Rows" value={profile.num_rows} />
            <Card title="Total Columns" value={profile.num_columns} />
            <Card title="Data Quality Score" value={profile.data_quality_score} />
            <Card title="Anomaly %" value={`${anomaly.anomaly_percentage || 0}%`} />

        </div>

        {/* ANOMALY SUMMARY */}
        <div className="p-6 bg-white shadow dark:bg-gray-800 rounded-xl">
            <h2 className="mb-4 text-xl font-bold">Anomaly Overview</h2>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-3">
            <MiniCard label="Total Anomalies" value={anomaly.total_anomalies} />
            <MiniCard label="Anomaly %" value={`${anomaly.anomaly_percentage}%`} />
            <MiniCard label="Confidence Score" value={anomaly.confidence_score} />
            </div>
        </div>

        {/* RANKED INSIGHTS */}
        <div className="p-6 bg-white shadow dark:bg-gray-800 rounded-xl">
            <h2 className="mb-4 text-xl font-bold">Top Ranked Insights</h2>

            <table className="w-full text-left">
            <thead>
                <tr className="border-b border-gray-200 dark:border-gray-700">
                <th className="py-2">Type</th>
                <th>Description</th>
                <th>Score</th>
                </tr>
            </thead>
            <tbody>
                {ranked.map((insight, index) => (
                <tr
                    key={index}
                    className="border-b border-gray-200 dark:border-gray-700"
                >
                    <td className="py-2 capitalize">{insight.type}</td>
                    <td>{insight.description}</td>
                    <td>{insight.score}</td>
                </tr>
                ))}
            </tbody>
            </table>

        </div>

        </div>
    );
    }

    function Card({ title, value }) {
    return (
        <div className="p-6 bg-white shadow dark:bg-gray-800 rounded-xl">
        <p className="text-sm text-gray-500 dark:text-gray-400">{title}</p>
        <p className="text-3xl font-bold">{value ?? "-"}</p>
        </div>
    );
    }

    function MiniCard({ label, value }) {
    return (
        <div className="p-4 bg-gray-100 rounded-lg dark:bg-gray-700">
        <p className="text-sm text-gray-500 dark:text-gray-300">{label}</p>
        <p className="text-xl font-bold">{value ?? "-"}</p>
        </div>
    );
    }

    export default Analytics;
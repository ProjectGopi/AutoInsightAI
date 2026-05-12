    import { useEffect, useState } from "react";
    import { useNavigate } from "react-router-dom";
    import { getDatasets, deleteDataset } from "../services/api";

    function Datasets() {
    const [datasets, setDatasets] = useState([]);

    useEffect(() => {
        fetchDatasets();

        const interval = setInterval(() => {
            fetchDatasets();
        }, 3000);

        return () => clearInterval(interval);
        }, []);
    const navigate = useNavigate();
    const fetchDatasets = async () => {
        try {
        const res = await getDatasets();
        setDatasets(res.data);
        } catch (error) {
        console.error("Error fetching datasets:", error);
        }
    };
    const handleDelete = async (id) => {
        try {
            await deleteDataset(id);
            fetchDatasets(); // refresh table
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
        <h1 className="mb-6 text-2xl font-bold">Uploaded Datasets</h1>

        {datasets.length === 0 ? (
            <p>No datasets found</p>
        ) : (
            <div className="p-6 bg-white shadow rounded-xl">
            <table className="w-full">
                <thead>
                <tr className="text-left border-b">
                    <th>ID</th>
                    <th>Filename</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
                </thead>
                <tbody>
                {datasets.map((ds) => (
                    <tr key={ds.id} className="border-b hover:bg-gray-50">
                        <td>{ds.id}</td>
                        <td>{ds.filename}</td>

                        <td>
                            <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                                ds.status === "completed"
                                    ? "bg-green-100 text-green-700"
                                    : ds.status === "processing"
                                    ? "bg-yellow-100 text-yellow-700 animate-pulse"
                                    : "bg-gray-100 text-gray-600"
                                }`}>
                                {ds.status.toUpperCase()}
                                </span>
                        </td>

                        <td className="space-x-2">

                            <button
                            onClick={() => navigate(`/analytics/${ds.id}`)}
                            className="text-sm text-blue-600 hover:underline"
                            >
                            View
                            </button>

                            <button
                            onClick={() => handleDelete(ds.id)}
                            className="text-sm text-red-600 hover:underline"
                            >
                            Delete
                            </button>

                        </td>
                        </tr>
                ))}
                </tbody>
            </table>
            </div>
        )}
        </div>
    );
    }

    export default Datasets;
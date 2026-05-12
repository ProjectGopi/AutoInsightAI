    import axios from "axios";

    const api = axios.create({
    baseURL: "http://localhost:8000",
    });

    export const uploadDataset = (formData) =>
    api.post("/upload", formData);

    export const analyzeDataset = (id) =>
    api.post(`/analyze/${id}`);

    export const getResults = (id) =>
    api.get(`/results/${id}`);

    export const getPowerBI = (id) =>
    api.get(`/powerbi/${id}`);

    export const getDatasets = () =>
    api.get("/datasets");

    export const deleteDataset = (id) =>
    api.delete(`/datasets/${id}`);

    export const getSettings = () => api.get("/settings");
    export const updateSettings = (data) =>
    api.put("/settings", data);
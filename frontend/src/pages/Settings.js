    import { useEffect, useState } from "react";
    import { getSettings, updateSettings } from "../services/api";

    function Settings({ setDarkMode }) {
    const [settings, setSettings] = useState(null);

    useEffect(() => {
        loadSettings();
    }, []);

    const loadSettings = async () => {
        const res = await getSettings();
        setSettings(res.data);
    };

    const handleSave = async () => {
        await updateSettings(settings);
        setDarkMode(settings.dark_mode);
        alert("Settings saved successfully");
    };

    if (!settings) return <p>Loading...</p>;

    return (
        <div className="space-y-8">

        <h1 className="text-3xl font-bold text-blue-700">
            System Settings
        </h1>

        <div className="p-6 space-y-4 bg-white shadow rounded-xl">

            <h2 className="text-xl font-semibold">
            Analysis Configuration
            </h2>

            <select
            value={settings.anomaly_level}
            onChange={(e) =>
                setSettings({ ...settings, anomaly_level: e.target.value })
            }
            className="w-full p-2 border rounded"
            >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            </select>

            <div className="flex justify-between">
            <span>Auto Analyze After Upload</span>
            <input
                type="checkbox"
                checked={settings.auto_analyze}
                onChange={() =>
                setSettings({
                    ...settings,
                    auto_analyze: !settings.auto_analyze
                })
                }
            />
            </div>

            <input
            type="text"
            placeholder="Default Target Column"
            value={settings.default_target || ""}
            onChange={(e) =>
                setSettings({
                ...settings,
                default_target: e.target.value
                })
            }
            className="w-full p-2 border rounded"
            />

        </div>

        <div className="p-6 space-y-4 bg-white shadow rounded-xl">

            <h2 className="text-xl font-semibold">
            Interface Settings
            </h2>

            <div className="flex justify-between">
            <span>Dark Mode</span>
            <input
                type="checkbox"
                checked={settings.dark_mode}
                onChange={() =>
                setSettings({
                    ...settings,
                    dark_mode: !settings.dark_mode
                })
                }
            />
            </div>

        </div>

        <button
            onClick={handleSave}
            className="px-6 py-2 text-white bg-blue-600 rounded-lg"
        >
            Save Settings
        </button>

        </div>
    );
    }

    export default Settings;
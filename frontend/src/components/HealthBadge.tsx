"use client";

import { useEffect, useState } from "react";
import { apiClient } from "@/lib/api";

type HealthState = "ok" | "warning" | "error" | "loading";

interface HealthData {
  apiStatus: HealthState;
  dbStatus: HealthState;
  latency?: number;
  errorMessage?: string;
}

export function HealthBadge() {
  const [health, setHealth] = useState<HealthData>({
    apiStatus: "loading",
    dbStatus: "loading",
  });

  const checkHealth = async () => {
    try {
      // Check API health
      const apiHealth = await apiClient.health();
      const apiStatus: HealthState = apiHealth.status === "ok" ? "ok" : "error";

      // Check DB health
      try {
        const dbHealth = await apiClient.dbHealth();
        const dbStatus: HealthState =
          dbHealth.status === "connected"
            ? "ok"
            : dbHealth.status === "error"
            ? "error"
            : "warning";

        setHealth({
          apiStatus,
          dbStatus,
          latency: dbHealth.latency_ms,
          errorMessage: dbHealth.details,
        });
      } catch (dbError) {
        setHealth({
          apiStatus,
          dbStatus: "error",
          errorMessage: dbError instanceof Error ? dbError.message : "DB check failed",
        });
      }
    } catch (apiError) {
      setHealth({
        apiStatus: "error",
        dbStatus: "error",
        errorMessage: apiError instanceof Error ? apiError.message : "API check failed",
      });
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // Check every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: HealthState) => {
    switch (status) {
      case "ok":
        return "bg-green-500";
      case "warning":
        return "bg-yellow-500";
      case "error":
        return "bg-red-500";
      case "loading":
        return "bg-gray-400 animate-pulse";
    }
  };

  const getStatusText = (apiStatus: HealthState, dbStatus: HealthState) => {
    if (apiStatus === "loading" || dbStatus === "loading") {
      return "Checking...";
    }
    if (apiStatus === "ok" && dbStatus === "ok") {
      return "All systems operational";
    }
    if (apiStatus === "error") {
      return "API offline";
    }
    if (dbStatus === "error") {
      return "Database issue";
    }
    return "System degraded";
  };

  const statusText = getStatusText(health.apiStatus, health.dbStatus);

  return (
    <div className="group relative inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white px-3 py-1.5 text-sm shadow-sm">
      {/* Status dots */}
      <div className="flex items-center gap-1.5">
        <div
          className={`h-2 w-2 rounded-full ${getStatusColor(health.apiStatus)}`}
          title="API Status"
        />
        <div
          className={`h-2 w-2 rounded-full ${getStatusColor(health.dbStatus)}`}
          title="Database Status"
        />
      </div>
      
      <span className="text-gray-600">{statusText}</span>

      {/* Tooltip */}
      <div className="pointer-events-none absolute bottom-full left-1/2 mb-2 hidden w-64 -translate-x-1/2 rounded-lg border border-gray-200 bg-white p-3 text-sm shadow-lg group-hover:block">
        <div className="space-y-2">
          <div className="flex items-center justify-between">
            <span className="font-medium">API Status:</span>
            <span
              className={`capitalize ${
                health.apiStatus === "ok"
                  ? "text-green-600"
                  : health.apiStatus === "error"
                  ? "text-red-600"
                  : "text-gray-500"
              }`}
            >
              {health.apiStatus}
            </span>
          </div>
          <div className="flex items-center justify-between">
            <span className="font-medium">Database Status:</span>
            <span
              className={`capitalize ${
                health.dbStatus === "ok"
                  ? "text-green-600"
                  : health.dbStatus === "error"
                  ? "text-red-600"
                  : "text-gray-500"
              }`}
            >
              {health.dbStatus}
            </span>
          </div>
          {health.latency !== undefined && (
            <div className="flex items-center justify-between">
              <span className="font-medium">DB Latency:</span>
              <span className="text-gray-700">{health.latency.toFixed(2)} ms</span>
            </div>
          )}
          {health.errorMessage && (
            <div className="mt-2 rounded bg-red-50 p-2 text-xs text-red-700">
              {health.errorMessage}
            </div>
          )}
        </div>
        <div className="mt-2 text-xs text-gray-400">
          Auto-refreshes every 30 seconds
        </div>
      </div>
    </div>
  );
}

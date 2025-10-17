/**
 * API client for ClassMind backend
 */

import { useAuth } from "@clerk/nextjs";

export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

/**
 * Generic API fetch wrapper with error handling
 */
export async function api<T>(
  path: string,
  init?: RequestInit
): Promise<T> {
  const url = `${API_URL}${path}`;
  
  const response = await fetch(url, {
    ...init,
    headers: {
      'Content-Type': 'application/json',
      ...(init?.headers || {}),
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    let errorMessage: string;
    
    try {
      const errorJson = JSON.parse(errorText);
      errorMessage = errorJson.detail || errorJson.message || errorText;
    } catch {
      errorMessage = errorText || response.statusText;
    }
    
    throw new Error(`API Error (${response.status}): ${errorMessage}`);
  }

  return response.json() as Promise<T>;
}

/**
 * Hook for authenticated API calls
 */
export function useAuthenticatedApi() {
  const { getToken } = useAuth();

  async function authFetch<T>(
    path: string,
    init?: RequestInit
  ): Promise<T> {
    const token = await getToken();
    const url = `${API_URL}${path}`;
    
    const response = await fetch(url, {
      ...init,
      headers: {
        'Content-Type': 'application/json',
        ...(init?.headers || {}),
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      let errorMessage: string;
      
      try {
        const errorJson = JSON.parse(errorText);
        errorMessage = errorJson.detail || errorJson.message || errorText;
      } catch {
        errorMessage = errorText || response.statusText;
      }
      
      throw new Error(`API Error (${response.status}): ${errorMessage}`);
    }

    return response.json() as Promise<T>;
  }

  return { authFetch };
}

/**
 * Type definitions for API responses
 */
export interface Routine {
  id: number;
  title: string;
  time: string | null;
  section_id: number | null;
  created_at: string | null;
}

export interface RoutineCreate {
  title: string;
  time?: string | null;
  section_id?: number | null;
}

export interface HealthStatus {
  status: 'ok';
}

export interface DbHealthStatus {
  status: 'connected' | 'error';
  database: string;
  latency_ms: number;
  rows_sampled?: number;
  details?: string;
}

/**
 * API client methods
 */
export const apiClient = {
  // Health endpoints
  health: () => api<HealthStatus>('/health'),
  dbHealth: () => api<DbHealthStatus>('/db-health'),

  // Routines endpoints
  routines: {
    list: (limit?: number) => {
      const query = limit ? `?limit=${limit}` : '';
      return api<Routine[]>(`/api/routines/${query}`);
    },
    
    get: (id: number) => api<Routine>(`/api/routines/${id}`),
    
    create: (data: RoutineCreate) =>
      api<Routine>('/api/routines/', {
        method: 'POST',
        body: JSON.stringify(data),
      }),
    
    update: (id: number, data: Partial<RoutineCreate>) =>
      api<Routine>(`/api/routines/${id}`, {
        method: 'PATCH',
        body: JSON.stringify(data),
      }),
    
    delete: (id: number) =>
      api<Routine>(`/api/routines/${id}`, {
        method: 'DELETE',
      }),
  },
};

"use client";

import { useEffect, useState } from "react";
import { SignedIn, SignedOut, SignInButton } from "@clerk/nextjs";
import { Routine, RoutineCreate } from "@/lib/api";
import { useAuthenticatedApi } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

function RoutinesContent() {
  const [routines, setRoutines] = useState<Routine[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAdding, setIsAdding] = useState(false);
  
  const { authFetch } = useAuthenticatedApi();
  
  // Form state
  const [newRoutine, setNewRoutine] = useState<RoutineCreate>({
    title: "",
    time: "",
  });

  // Fetch routines
  const fetchRoutines = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await authFetch<Routine[]>('/api/routines/');
      setRoutines(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch routines");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchRoutines();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Add routine
  const handleAddRoutine = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!newRoutine.title.trim()) {
      setError("Routine title is required");
      return;
    }

    try {
      setIsAdding(true);
      setError(null);
      const created = await authFetch<Routine>('/api/routines/', {
        method: 'POST',
        body: JSON.stringify(newRoutine),
      });
      setRoutines([created, ...routines]);
      setNewRoutine({ title: "", time: "" });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create routine");
    } finally {
      setIsAdding(false);
    }
  };

  // Delete routine
  const handleDeleteRoutine = async (id: number) => {
    if (!confirm("Are you sure you want to delete this routine?")) {
      return;
    }

    try {
      await authFetch(`/api/routines/${id}`, {
        method: 'DELETE',
      });
      setRoutines(routines.filter((r) => r.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete routine");
    }
  };

  return (
    <div className="container mx-auto max-w-4xl p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">Routines</h1>
        <p className="text-gray-600 mt-2">Manage your daily routines and schedules</p>
      </div>

      {/* Add Routine Form */}
      <Card className="mb-6">
        <CardHeader>
          <CardTitle>Add New Routine</CardTitle>
          <CardDescription>Create a new routine to track your activities</CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleAddRoutine} className="flex gap-3">
            <Input
              type="text"
              placeholder="Routine title (e.g., Morning Workout)"
              value={newRoutine.title}
              onChange={(e) => setNewRoutine({ ...newRoutine, title: e.target.value })}
              className="flex-1"
              disabled={isAdding}
            />
            <Input
              type="text"
              placeholder="Time (e.g., 09:00 AM)"
              value={newRoutine.time || ""}
              onChange={(e) => setNewRoutine({ ...newRoutine, time: e.target.value })}
              className="w-40"
              disabled={isAdding}
            />
            <Button type="submit" disabled={isAdding}>
              {isAdding ? "Adding..." : "Add Routine"}
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Error Message */}
      {error && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-12">
          <div className="text-gray-500">Loading routines...</div>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && routines.length === 0 && (
        <Card>
          <CardContent className="flex flex-col items-center justify-center py-12">
            <p className="text-gray-500 mb-2">No routines yet</p>
            <p className="text-sm text-gray-400">Add your first routine using the form above</p>
          </CardContent>
        </Card>
      )}

      {/* Routines List */}
      {!isLoading && routines.length > 0 && (
        <div className="space-y-3">
          {routines.map((routine) => (
            <Card key={routine.id}>
              <CardContent className="flex items-center justify-between p-4">
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{routine.title}</h3>
                  <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                    {routine.time && (
                      <span className="flex items-center gap-1">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        {routine.time}
                      </span>
                    )}
                    {routine.created_at && (
                      <span className="text-xs">
                        Added {new Date(routine.created_at).toLocaleDateString()}
                      </span>
                    )}
                  </div>
                </div>
                <Button
                  variant="destructive"
                  size="sm"
                  onClick={() => handleDeleteRoutine(routine.id)}
                >
                  Delete
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

export default function RoutinesPage() {
  return (
    <>
      {/* Signed Out State */}
      <SignedOut>
        <div className="container mx-auto max-w-4xl p-6">
          <Card className="mt-12">
            <CardContent className="flex flex-col items-center justify-center py-12">
              <h2 className="text-2xl font-bold mb-4">Sign in to manage your routines</h2>
              <p className="text-gray-600 mb-6">Create, track, and organize your daily routines</p>
              <SignInButton mode="modal">
                <Button size="lg">
                  Sign In to Get Started
                </Button>
              </SignInButton>
            </CardContent>
          </Card>
        </div>
      </SignedOut>

      {/* Signed In State */}
      <SignedIn>
        <RoutinesContent />
      </SignedIn>
    </>
  );
}

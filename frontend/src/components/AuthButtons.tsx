"use client";

import { SignInButton, SignOutButton, SignUpButton, UserButton, useUser } from "@clerk/nextjs";
import { Button } from "@/components/ui/button";

export function AuthButtons() {
  const { isSignedIn, isLoaded } = useUser();

  if (!isLoaded) {
    return (
      <div className="flex items-center gap-2">
        <div className="h-8 w-20 animate-pulse rounded bg-gray-200" />
      </div>
    );
  }

  if (isSignedIn) {
    return (
      <div className="flex items-center gap-3">
        <UserButton 
          afterSignOutUrl="/"
          appearance={{
            elements: {
              avatarBox: "h-9 w-9"
            }
          }}
        />
        <SignOutButton>
          <Button variant="outline" size="sm">
            Sign Out
          </Button>
        </SignOutButton>
      </div>
    );
  }

  return (
    <div className="flex items-center gap-2">
      <SignInButton mode="modal">
        <Button variant="outline" size="sm">
          Sign In
        </Button>
      </SignInButton>
      <SignUpButton mode="modal">
        <Button size="sm">
          Sign Up
        </Button>
      </SignUpButton>
    </div>
  );
}

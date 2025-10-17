-- ============================================
-- Clerk Authentication Migration
-- ============================================
-- This migration adds user_id column and Row Level Security (RLS)
-- to enable multi-user support with Clerk authentication
--
-- Run this in your Supabase SQL Editor

-- Step 1: Add user_id column to routines table
ALTER TABLE public.routines 
ADD COLUMN IF NOT EXISTS user_id TEXT;

-- Step 2: Enable Row Level Security on routines table
ALTER TABLE public.routines 
ENABLE ROW LEVEL SECURITY;

-- Step 3: Drop existing policies if any (safe to run even if they don't exist)
DROP POLICY IF EXISTS "Users can view their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can insert their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can update their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can delete their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users manage own routines" ON public.routines;

-- Step 4: Create RLS policy for user data isolation
-- This single policy handles all operations (SELECT, INSERT, UPDATE, DELETE)
-- Users can only access routines where user_id matches their JWT sub claim
CREATE POLICY "Users manage own routines" 
ON public.routines 
FOR ALL 
USING (auth.jwt() ->> 'sub' = user_id)
WITH CHECK (auth.jwt() ->> 'sub' = user_id);

-- Step 5: Create index for better query performance
CREATE INDEX IF NOT EXISTS idx_routines_user_id 
ON public.routines(user_id);

-- ============================================
-- Verification Queries
-- ============================================
-- Run these to verify the migration was successful:

-- Check if user_id column exists
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'public' 
  AND table_name = 'routines' 
  AND column_name = 'user_id';

-- Check if RLS is enabled
SELECT tablename, rowsecurity
FROM pg_tables
WHERE schemaname = 'public' 
  AND tablename = 'routines';

-- List all policies on routines table
SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual, with_check
FROM pg_policies
WHERE schemaname = 'public' 
  AND tablename = 'routines';

-- Check if index exists
SELECT indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public' 
  AND tablename = 'routines'
  AND indexname = 'idx_routines_user_id';

-- ============================================
-- Rollback (if needed)
-- ============================================
-- Uncomment and run these if you need to undo the migration:

-- DROP INDEX IF EXISTS idx_routines_user_id;
-- DROP POLICY IF EXISTS "Users manage own routines" ON public.routines;
-- ALTER TABLE public.routines DISABLE ROW LEVEL SECURITY;
-- ALTER TABLE public.routines DROP COLUMN IF EXISTS user_id;

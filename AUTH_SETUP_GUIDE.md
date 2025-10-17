# Clerk Authentication Setup Guide

## ✅ What's Already Done

### Backend
- ✅ JWT verification module (`app/core/jwt.py`) with JWKS caching
- ✅ Auth dependencies (`app/core/auth.py`) for FastAPI routes
- ✅ Protected API endpoints (POST/DELETE require authentication)
- ✅ User ID filtering in repository layer
- ✅ Dependencies installed (`python-jose`, `httpx`)
- ✅ Configuration extended for Clerk JWKS URL

### Frontend
- ✅ Clerk package installed (`@clerk/nextjs`)
- ✅ Auth components created (`AuthButtons.tsx`)
- ✅ Authenticated API client (`useAuthenticatedApi` hook)
- ✅ ClerkProvider wrapper in layout
- ✅ Protected routines page with sign-in CTA

## 🔧 Required Setup Steps

### Step 1: Create a Clerk Account and Application

1. Go to [https://clerk.com](https://clerk.com) and sign up
2. Create a new application in the Clerk Dashboard
3. Enable **Google** as an OAuth provider (Settings → Authentication → Social Connections)
4. Copy the following keys from the Clerk Dashboard:

   **From API Keys page:**
   - Publishable Key (starts with `pk_test_...` or `pk_live_...`)
   - Secret Key (starts with `sk_test_...` or `sk_live_...`)

   **For JWKS URL:**
   - Your application domain will be something like: `https://your-app-name.clerk.accounts.dev`
   - The JWKS URL will be: `https://your-app-name.clerk.accounts.dev/.well-known/jwks.json`

### Step 2: Configure Backend Environment

Create or update `backend/.env`:

```env
# Database
DATABASE_URL=your_supabase_database_url
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Clerk Authentication
CLERK_JWKS_URL=https://your-app-name.clerk.accounts.dev/.well-known/jwks.json

# CORS (comma-separated list of allowed origins)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

**Note:** Replace `your-app-name` with your actual Clerk application subdomain.

### Step 3: Configure Frontend Environment

Create or update `frontend/.env.local`:

```env
# API Configuration
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000

# Supabase
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxxxxxxxxxxxxxxxxxx
CLERK_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxx
```

### Step 4: Database Migration for User ID

Run this SQL in your Supabase SQL Editor:

```sql
-- Add user_id column to routines table
ALTER TABLE public.routines 
ADD COLUMN IF NOT EXISTS user_id TEXT;

-- Enable Row Level Security
ALTER TABLE public.routines 
ENABLE ROW LEVEL SECURITY;

-- Drop existing policies if any
DROP POLICY IF EXISTS "Users can view their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can insert their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can update their own routines" ON public.routines;
DROP POLICY IF EXISTS "Users can delete their own routines" ON public.routines;

-- Create RLS policies for user isolation
CREATE POLICY "Users can view their own routines" 
ON public.routines FOR SELECT 
USING (auth.jwt() ->> 'sub' = user_id);

CREATE POLICY "Users can insert their own routines" 
ON public.routines FOR INSERT 
WITH CHECK (auth.jwt() ->> 'sub' = user_id);

CREATE POLICY "Users can update their own routines" 
ON public.routines FOR UPDATE 
USING (auth.jwt() ->> 'sub' = user_id);

CREATE POLICY "Users can delete their own routines" 
ON public.routines FOR DELETE 
USING (auth.jwt() ->> 'sub' = user_id);

-- Optional: Add an index for better query performance
CREATE INDEX IF NOT EXISTS idx_routines_user_id 
ON public.routines(user_id);
```

**Important:** The RLS policies use `auth.jwt() ->> 'sub'` which extracts the user ID from the JWT token that will be passed to Supabase queries.

### Step 5: Update Supabase Client (Backend)

If you want the backend to pass JWTs to Supabase for RLS enforcement, update `app/core/supabase_client.py`:

```python
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()

def get_supabase_client(user_token: str | None = None) -> Client:
    """Get Supabase client, optionally with user JWT for RLS"""
    if user_token:
        # Use user's JWT token for RLS enforcement
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY,
            options={"headers": {"Authorization": f"Bearer {user_token}"}}
        )
    else:
        # Use service role key (bypasses RLS)
        return create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_SERVICE_ROLE_KEY
        )
```

Then update repository methods to accept and use the token.

## 🧪 Testing the Setup

### 1. Start Backend Server

```bash
cd backend
source venv/Scripts/activate  # On Windows: venv\Scripts\activate
uvicorn app.main:app --reload
```

Verify health endpoints:
- http://127.0.0.1:8000/health (should return `{"status":"healthy"}`)
- http://127.0.0.1:8000/db-health (should return database connection status)

### 2. Start Frontend Server

```bash
cd frontend
pnpm dev
```

Open http://localhost:3000

### 3. Test Authentication Flow

1. **Sign In**: Click "Sign In" in the header
2. **Google OAuth**: Choose Google sign-in in the Clerk modal
3. **Create Routine**: After signing in, add a new routine
4. **Verify Database**: Check Supabase to confirm the `user_id` is populated
5. **Sign Out**: Click your user avatar → Sign Out
6. **Verify Protection**: You should see the sign-in CTA on the routines page

### 4. Test API Protection

Try creating a routine without auth:

```bash
curl -X POST http://127.0.0.1:8000/api/routines/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","time":"10:00 AM"}'
```

**Expected:** 401 Unauthorized

Try with a valid token (get from browser DevTools → Application → Cookies → `__session`):

```bash
curl -X POST http://127.0.0.1:8000/api/routines/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title":"Test","time":"10:00 AM"}'
```

**Expected:** 200 OK with created routine

## 🚀 Deployment Checklist

### Frontend (Vercel)

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variables:
   - `NEXT_PUBLIC_API_URL` (your backend URL)
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`
   - `CLERK_SECRET_KEY`
4. Deploy

### Backend (Railway/Digital Ocean)

1. Create new project
2. Add environment variables (all from backend `.env`)
3. Deploy from GitHub
4. Update frontend `NEXT_PUBLIC_API_URL` to deployed backend URL
5. Update backend `ALLOWED_ORIGINS` to include frontend production URL

### Post-Deployment

1. Update Clerk Dashboard:
   - Add production domain to **Allowed Origins** (Settings → Domains)
   - Update **Redirect URLs** if needed
2. Test authentication flow in production
3. Verify database writes with `user_id`

## 📝 Key Files Reference

### Backend
- `app/core/config.py` - Configuration with Clerk JWKS URL
- `app/core/jwt.py` - JWT verification logic
- `app/core/auth.py` - FastAPI auth dependencies
- `app/api/routines.py` - Protected API endpoints
- `app/repos/routines_repo.py` - User ID filtering

### Frontend
- `src/app/layout.tsx` - ClerkProvider wrapper
- `src/components/AuthButtons.tsx` - Auth UI components
- `src/lib/api.ts` - Authenticated API client
- `src/app/routines/page.tsx` - Protected routines page

## 🔍 Troubleshooting

### "Invalid token" errors
- Verify JWKS URL in backend `.env`
- Check Clerk Dashboard → API Keys for correct keys
- Ensure frontend is sending tokens in Authorization header

### "Module not found: @clerk/nextjs"
- Run `pnpm install` in frontend directory
- Check that `@clerk/nextjs` is in `package.json`

### CORS errors
- Add frontend URL to `ALLOWED_ORIGINS` in backend `.env`
- Restart backend server after env changes

### Database RLS blocking queries
- Verify JWT token is being passed to Supabase
- Check RLS policies in Supabase Dashboard
- Use service role key in backend to bypass RLS (current implementation)

### Users can see each other's routines
- Ensure `user_id` column is populated
- Verify RLS policies are enabled
- Check that backend is filtering by `user_id` in repository

## 📚 Additional Resources

- [Clerk Documentation](https://clerk.com/docs)
- [Supabase RLS Guide](https://supabase.com/docs/guides/auth/row-level-security)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Next.js Authentication](https://nextjs.org/docs/authentication)

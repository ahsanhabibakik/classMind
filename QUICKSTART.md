# ClassMind - Quick Start Guide

## 🚀 Starting the Application

### Backend (FastAPI)

**Option 1: Using the startup script**

```bash
cd e:/1code/passionproject/classMind/backend
bash start.sh
```

**Option 2: Manual commands**

```bash
cd e:/1code/passionproject/classMind/backend
source venv/Scripts/activate
uvicorn app.main:app --reload
```

The backend will be available at:

- **API**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health
- **DB Health**: http://127.0.0.1:8000/db-health

### Frontend (Next.js)

```bash
cd e:/1code/passionproject/classMind/frontend
npm install  # First time only
npm run dev
```

The frontend will be available at:

- **App**: http://localhost:3000
- **Routines Page**: http://localhost:3000/routines

---

## ✅ Testing the Application

### 1. Test Backend Health

Open these URLs in your browser:

- http://127.0.0.1:8000/health → Should show `{"status":"ok"}`
- http://127.0.0.1:8000/db-health → Should show database connection status with latency

### 2. Test API Endpoints

Visit the interactive API docs:

- http://127.0.0.1:8000/docs

Try these operations:

1. **GET /api/routines/** - List all routines
2. **POST /api/routines/** - Create a new routine
3. **DELETE /api/routines/{id}** - Delete a routine

### 3. Test Frontend

1. Open http://localhost:3000/routines
2. Check that the health badge in the header shows green dots
3. Add a new routine using the form
4. Delete a routine
5. Hover over the health badge to see detailed status

---

## 🎯 What Was Implemented

### Backend Improvements ✅

- ✅ Centralized config with environment validation
- ✅ Repository layer for clean database operations
- ✅ Enhanced routines API with full CRUD
- ✅ CORS middleware for frontend communication
- ✅ Structured logging
- ✅ Enhanced health endpoints with latency measurement

### Frontend Features ✅

- ✅ Type-safe API client
- ✅ Health badge with real-time monitoring
- ✅ Routines page with full CRUD functionality
- ✅ Beautiful UI with shadcn/ui components
- ✅ Loading and error states
- ✅ Responsive design

---

## 🐛 Troubleshooting

### Backend Won't Start

```bash
# Make sure you're in the backend directory
cd e:/1code/passionproject/classMind/backend

# Activate virtual environment
source venv/Scripts/activate

# Check if uvicorn is installed
pip list | grep uvicorn

# If not, install it
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --reload
```

### Frontend Won't Start

```bash
# Make sure you're in the frontend directory
cd e:/1code/passionproject/classMind/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### CORS Errors

- Make sure backend is running on port 8000
- Make sure frontend is running on port 3000
- Check that CORS_ORIGINS in `backend/app/core/config.py` includes `http://localhost:3000`

### Database Connection Errors

- Verify your `.env` file in backend has correct SUPABASE_URL and SUPABASE_KEY
- Check that the `routines` table exists in your Supabase database
- Test the connection: http://127.0.0.1:8000/db-health

---

## 📚 API Documentation

Once the backend is running, visit:

- **Interactive Docs**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

All endpoints are documented with:

- Request/response schemas
- Validation rules
- Example values
- Error responses

---

## 🎨 UI Features

### Health Badge

- **Green dots**: All systems operational
- **Red dots**: System errors
- **Hover**: Shows detailed information including:
  - API status
  - Database status
  - Database latency in milliseconds
  - Error messages (if any)
- **Auto-refresh**: Updates every 30 seconds

### Routines Page

- **List view**: Shows all routines with time
- **Add form**: Create new routines with title and optional time
- **Delete button**: Remove routines with confirmation
- **Empty state**: Helpful message when no routines exist
- **Loading state**: Shows while fetching data
- **Error handling**: Displays error messages in red banner

---

## 🔄 Next Steps

See `IMPLEMENTATION_SUMMARY.md` for:

- Detailed technical documentation
- Future feature roadmap
- Testing recommendations
- Deployment guides

---

## 🆘 Need Help?

If you encounter any issues:

1. Check the terminal output for error messages
2. Verify all environment variables are set correctly
3. Make sure both backend and frontend are running
4. Check the browser console for frontend errors
5. Check the terminal logs for backend errors

**Common Issues:**

- Port already in use: Stop other services or change ports
- Module not found: Run `pip install -r requirements.txt` or `npm install`
- Database errors: Check Supabase credentials in `.env`
- CORS errors: Verify backend is running and CORS is configured

---

**Ready to start? Run the commands above!** 🚀

# 🎯 ClassMind - Command Reference

Quick reference for all common commands.

## 🖥️ Backend Commands

### Start Development Server

```bash
cd backend
source venv/Scripts/activate
uvicorn app.main:app --reload
```

### Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Add New Package

```bash
pip install package-name
pip freeze > requirements.txt
```

### Run Tests

```bash
pytest tests/ -v
pytest tests/ -v --cov=app
```

### Database Migrations

```bash
# Using Supabase CLI (if installed)
supabase migration new migration_name
supabase db push
```

## 🌐 Frontend Commands

### Start Development Server

```bash
cd frontend
npm run dev
```

### Install Dependencies

```bash
cd frontend
npm install
```

### Add New Package

```bash
npm install package-name
npm install -D package-name  # Dev dependency
```

### Build for Production

```bash
npm run build
npm start  # Run production build
```

### Lint & Format

```bash
npm run lint
npm run format
```

## 🧪 Testing Commands

### Backend Tests

```bash
cd backend
pytest                    # Run all tests
pytest tests/test_file.py # Run specific file
pytest -v                 # Verbose output
pytest --cov              # With coverage
pytest -k "test_name"     # Run specific test
```

### Frontend Tests

```bash
cd frontend
npm test                  # Run all tests
npm test -- --watch       # Watch mode
npm test -- --coverage    # With coverage
```

## 🔧 Utility Commands

### Check Backend Health

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/db-health
```

### View API Docs

```bash
# Open in browser
start http://127.0.0.1:8000/docs         # Windows
open http://127.0.0.1:8000/docs          # Mac
xdg-open http://127.0.0.1:8000/docs      # Linux
```

### Check Python Environment

```bash
cd backend
source venv/Scripts/activate
python --version
pip list
which python
```

### Check Node Environment

```bash
cd frontend
node --version
npm --version
npm list
```

## 🗄️ Database Commands

### Using Supabase Dashboard

- Go to https://app.supabase.com
- Select your project
- Navigate to Table Editor or SQL Editor

### Direct SQL (via Supabase)

```sql
-- View routines table
SELECT * FROM routines;

-- Count routines
SELECT COUNT(*) FROM routines;

-- Create test routine
INSERT INTO routines (title, time) VALUES ('Test Routine', '09:00 AM');

-- Delete all test routines
DELETE FROM routines WHERE title LIKE '%Test%';
```

## 🐳 Docker Commands (Future)

### Build Images

```bash
docker build -t classmind-backend ./backend
docker build -t classmind-frontend ./frontend
```

### Run Containers

```bash
docker run -p 8000:8000 classmind-backend
docker run -p 3000:3000 classmind-frontend
```

### Docker Compose

```bash
docker-compose up
docker-compose down
docker-compose logs -f
```

## 🚀 Deployment Commands

### Backend (Railway/Render)

```bash
# Using Railway CLI
railway up
railway logs

# Using Render
# Connect GitHub repo in Render dashboard
```

### Frontend (Vercel)

```bash
# Using Vercel CLI
cd frontend
vercel          # Deploy to preview
vercel --prod   # Deploy to production
vercel logs     # View logs
```

## 🔑 Environment Variables

### Backend (.env)

```bash
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
OPENAI_API_KEY=your_key
```

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## 📦 Package Management

### Backend (pip)

```bash
pip install package-name           # Install package
pip uninstall package-name         # Uninstall
pip list                           # List installed
pip freeze > requirements.txt      # Export deps
pip install -r requirements.txt    # Install from file
```

### Frontend (npm)

```bash
npm install package-name           # Install package
npm uninstall package-name         # Uninstall
npm list                           # List installed
npm outdated                       # Check updates
npm update                         # Update packages
```

## 🔍 Debugging Commands

### Backend Debug Mode

```bash
uvicorn app.main:app --reload --log-level debug
```

### Frontend Debug Mode

```bash
npm run dev -- --debug
```

### Check Ports

```bash
# Windows
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Mac/Linux
lsof -i :8000
lsof -i :3000
```

### Kill Process on Port

```bash
# Windows
taskkill /PID <PID> /F

# Mac/Linux
kill -9 <PID>
```

## 🎨 Code Quality

### Backend

```bash
# Format with black
black app/

# Lint with pylint
pylint app/

# Type check with mypy
mypy app/

# Sort imports
isort app/
```

### Frontend

```bash
# Format with prettier
npm run format

# Lint with ESLint
npm run lint

# Type check
npm run type-check
```

## 📊 Monitoring

### View Logs

```bash
# Backend logs (in terminal running uvicorn)
# Frontend logs (in terminal running npm run dev)
# Browser console (F12 in browser)
```

### Check System Resources

```bash
# CPU and Memory
top          # Mac/Linux
htop         # Mac/Linux (if installed)
# Task Manager on Windows (Ctrl+Shift+Esc)
```

## 🔐 Security Checks

### Check for Vulnerabilities

```bash
# Backend
pip-audit

# Frontend
npm audit
npm audit fix
```

### Update Dependencies

```bash
# Backend
pip list --outdated
pip install --upgrade package-name

# Frontend
npm outdated
npm update
```

---

## 💡 Pro Tips

1. **Use aliases** for common commands:

   ```bash
   # Add to .bashrc or .zshrc
   alias be="cd /path/to/backend && source venv/Scripts/activate"
   alias fe="cd /path/to/frontend"
   alias berun="be && uvicorn app.main:app --reload"
   alias ferun="fe && npm run dev"
   ```

2. **Use tmux or screen** to run backend and frontend in split terminals

3. **Use VS Code tasks** to start both servers with one command

4. **Keep a terminal** open for each: backend, frontend, and testing

---

**For more detailed information, see:**

- [Quick Start Guide](QUICKSTART.md)
- [Implementation Summary](IMPLEMENTATION_SUMMARY.md)
- [Main README](README.md)

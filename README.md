# 🎓 ClassMind - AI-Powered Routine Management

> Manage your daily routines with AI assistance

ClassMind is a full-stack web application that helps users manage their daily routines with AI-powered features. Built with FastAPI, Next.js, Supabase, and LangChain.

## ✨ Features

- ✅ **Full CRUD Operations** - Create, read, update, and delete routines
- ✅ **Real-time Health Monitoring** - Track API and database status with live updates
- ✅ **Type-Safe API** - Fully typed backend and frontend for reliability
- ✅ **Beautiful UI** - Modern, responsive design with Tailwind CSS and shadcn/ui
- ✅ **Repository Pattern** - Clean architecture with separated concerns
- ✅ **Automatic Validation** - Pydantic models ensure data integrity
- 🔄 **AI Suggestions** - Coming soon: LangChain-powered routine recommendations
- 🤖 **Telegram Bot** - Coming soon: Manage routines via Telegram

## 🏗️ Tech Stack

### Backend

- **FastAPI** - Modern, fast web framework
- **Supabase** - PostgreSQL database with real-time capabilities
- **Pydantic** - Data validation and settings management
- **LangChain** - AI/ML integration (planned)
- **Python 3.11+**

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety throughout
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful, accessible components
- **React Hooks** - Modern state management

## 📁 Project Structure

```
classMind/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   │   ├── auth.py
│   │   │   ├── routines.py    # Routines CRUD
│   │   │   └── notifications.py
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Settings & env config
│   │   │   ├── logging.py     # Logging setup
│   │   │   ├── supabase_client.py
│   │   │   ├── langchain_utils.py
│   │   │   └── rag_pipeline.py
│   │   ├── repos/             # Repository layer
│   │   │   └── routines_repo.py
│   │   ├── models.py          # Database models
│   │   └── main.py            # App entry point
│   ├── requirements.txt
│   ├── start.sh               # Startup script
│   └── .env                   # Environment variables
│
├── frontend/                  # Next.js frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx     # Root layout with health badge
│   │   │   ├── page.tsx       # Home page
│   │   │   └── routines/
│   │   │       └── page.tsx   # Routines CRUD page
│   │   ├── components/
│   │   │   ├── HealthBadge.tsx # Real-time health monitoring
│   │   │   └── ui/            # shadcn/ui components
│   │   └── lib/
│   │       ├── api.ts         # Type-safe API client
│   │       └── utils.ts       # Utilities
│   ├── package.json
│   ├── tsconfig.json
│   └── .env.local             # Frontend env vars
│
├── QUICKSTART.md              # Quick start guide
├── IMPLEMENTATION_SUMMARY.md   # Technical documentation
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI API key (for AI features)

### 1. Clone and Setup

```bash
git clone https://github.com/ahsanhabibakik/classMind.git
cd classMind
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/Scripts/activate  # On Windows Git Bash

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENAI_API_KEY=your_openai_key
EOF

# Start server
uvicorn app.main:app --reload
```

Backend will run at http://127.0.0.1:8000

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at http://localhost:3000

## 📖 Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running fast
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Technical deep dive
- **[API Docs](http://127.0.0.1:8000/docs)** - Interactive OpenAPI docs (when running)

## 🧪 Testing

### Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Frontend Tests

```bash
cd frontend
npm test
```

## 📊 API Endpoints

### Health

- `GET /health` - Basic health check
- `GET /db-health` - Database connectivity with latency

### Routines

- `GET /api/routines/` - List all routines
- `GET /api/routines/{id}` - Get single routine
- `POST /api/routines/` - Create routine
- `PATCH /api/routines/{id}` - Update routine
- `DELETE /api/routines/{id}` - Delete routine

### Authentication (Coming Soon)

- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user

## 🎯 Roadmap

### Phase 1: Core Features ✅

- [x] Backend API with FastAPI
- [x] Supabase integration
- [x] Routines CRUD
- [x] Health monitoring
- [x] Frontend with Next.js
- [x] Type-safe API client
- [x] Beautiful UI

### Phase 2: Authentication 🔄

- [ ] Supabase Auth integration
- [ ] Google OAuth
- [ ] Magic link login
- [ ] User profiles
- [ ] Protected routes

### Phase 3: AI Features 🔮

- [ ] LangChain integration
- [ ] AI routine suggestions
- [ ] Natural language processing
- [ ] Smart scheduling
- [ ] Routine templates

### Phase 4: Advanced Features 🚀

- [ ] Telegram bot
- [ ] Notifications & reminders
- [ ] Analytics dashboard
- [ ] Routine sharing
- [ ] Team collaboration
- [ ] Mobile app (React Native)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Ahsan Habib Akik**

- GitHub: [@ahsanhabibakik](https://github.com/ahsanhabibakik)

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Vercel for Next.js
- Supabase for the backend infrastructure
- shadcn for the beautiful UI components
- LangChain for AI capabilities

## 📧 Support

For support, email ahsanhabibakik@example.com or open an issue on GitHub.

---

**Made with ❤️ by Ahsan Habib Akik**

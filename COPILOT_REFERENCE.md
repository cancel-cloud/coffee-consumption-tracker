# COPILOT_REFERENCE.md

## Project Overview

The **Coffee Consumption Tracker** is a dual-application project designed to help users log, visualize, and analyze their coffee drinking habits. The repository contains two separate but complementary applications:

1. **Python Backend** (Streamlit-based) - Local/standalone application
2. **Next.js Frontend** (Web-based) - Cloud-connected application using Appwrite

## Project Goals

- **Data Collection**: Enable users to log daily coffee consumption with variety tracking
- **Visualization**: Provide charts, heatmaps, and statistics for consumption patterns
- **Analysis**: Support data export and detailed analytics
- **Accessibility**: Offer both local (Python) and web-based (Next.js) interfaces
- **Health Awareness**: Track caffeine intake with warnings and recommendations

## Tech Stack

### Python Backend Application
- **Framework**: Streamlit 1.48.1
- **Database**: SQLite with SQLAlchemy ORM
- **Visualization**: matplotlib, calplot (calendar heatmaps)
- **Data Processing**: pandas, numpy
- **Language**: German interface
- **Storage**: Local SQLite database (`coffee.db`)

### Next.js Frontend Application
- **Framework**: Next.js 15.3.2 with TypeScript
- **UI Library**: Shadcn/UI + TailwindCSS
- **Backend Service**: Appwrite (cloud database and auth)
- **Charts**: Chart.js with react-chartjs-2
- **Heatmaps**: react-calendar-heatmap
- **Authentication**: Appwrite account management
- **Language**: German/English interface

## Repository Structure

```
coffee-consumption-tracker/
├── app.py                          # Python Streamlit application
├── coffee.db                       # SQLite database (auto-generated)
├── requirements.txt                # Python dependencies
├── package.json                    # Root package.json (legacy)
├── README.md                       # Main project documentation
├── LICENSE                         # MIT License
└── kaffeekonsum-tracker/           # Next.js web application
    ├── src/
    │   ├── app/                    # Next.js App Router pages
    │   │   ├── dashboard/          # Main dashboard with analytics
    │   │   ├── manage/             # Data management interface
    │   │   ├── layout.tsx          # Root layout with navigation
    │   │   └── page.tsx            # Landing page with charts
    │   └── components/
    │       ├── ui/                 # Shadcn/UI components
    │       ├── LoginButton.tsx     # Appwrite authentication
    │       ├── LogoutButton.tsx    # Sign out functionality
    │       └── SessionButton.tsx   # Session management
    ├── env.example                 # Appwrite configuration template
    ├── package.json                # Frontend dependencies
    ├── eslint.config.mjs           # ESLint configuration
    ├── next.config.ts              # Next.js configuration
    ├── tailwind.config.js          # TailwindCSS setup
    └── tsconfig.json               # TypeScript configuration
```

## Key Files and Components

### Python Backend (`app.py`)
- **Database Tables**: 
  - `consumption` (id, date, cups, variety_id)
  - `varieties` (id, name, caffeine_mg)
- **Features**:
  - Coffee logging with date and quantity
  - Variety management with caffeine tracking
  - Statistics and visualizations
  - Calendar heatmap for consumption patterns
  - CSV import/export functionality
  - Health warnings for excessive caffeine

### Next.js Frontend
- **Pages**:
  - `/` - Landing page with sample charts
  - `/dashboard` - Main analytics dashboard (requires auth)
  - `/manage` - Data management interface (requires auth)
- **Authentication**: Appwrite-based user management
- **Data Storage**: Appwrite database collections
- **UI Components**: Modern React components with TypeScript

## Development Setup

### Python Backend
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

### Next.js Frontend
```bash
cd kaffeekonsum-tracker

# Install dependencies
npm install

# Set up environment variables
cp env.example .env.local
# Edit .env.local with your Appwrite configuration

# Run development server
npm run dev

# Build for production
npm run build
```

## Environment Configuration

### Appwrite Setup (Required for Next.js app)
Create `.env.local` in `kaffeekonsum-tracker/` directory:
```env
NEXT_PUBLIC_APPWRITE_PROJECT_ID=your_project_id
NEXT_PUBLIC_APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
NEXT_PUBLIC_APPWRITE_Database_ID=your_database_id
NEXT_PUBLIC_APPWRITE_CONSUMPTION_COLLECTION_ID=your_collection_id
NEXT_PUBLIC_APPWRITE_VARIETIES_COLLECTION_ID=your_varieties_id
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_ADMIN_ID=your_admin_user_id
```

## Coding Conventions

### Python Backend (PEP8)
- Use snake_case for variables and functions
- 4-space indentation
- German language for UI strings
- SQLAlchemy ORM patterns
- Streamlit component organization

### Next.js Frontend (ESLint/Prettier)
- ESLint configuration in `eslint.config.mjs`
- TypeScript strict mode enabled
- React functional components with hooks
- Tailwind utility classes for styling
- Component organization: UI components in `/components/ui/`

## Common Development Tasks

### Adding New Features
1. **Python Backend**: Add new Streamlit sections in `app.py`
2. **Frontend**: Create new pages in `src/app/` or components in `src/components/`

### Database Schema Changes
- **Python**: Modify SQLAlchemy table definitions and add migration logic
- **Frontend**: Update Appwrite collections and adjust TypeScript interfaces

### UI/UX Updates
- **Python**: Modify Streamlit components and CSS styling
- **Frontend**: Update React components and Tailwind classes

## Testing and Quality Assurance

### Python Backend
```bash
# Run the app to test functionality
streamlit run app.py

# Check for Python syntax/import issues
python -c "import app"
```

### Next.js Frontend
```bash
cd kaffeekonsum-tracker

# Lint code
npm run lint

# Build to check for errors
npm run build

# Run development server
npm run dev
```

## Data Models

### Python SQLite Schema
```sql
CREATE TABLE varieties (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    caffeine_mg INTEGER DEFAULT 0
);

CREATE TABLE consumption (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    cups INTEGER NOT NULL,
    variety_id INTEGER NOT NULL
);
```

### Appwrite Collections
- **Varieties**: Store coffee types with caffeine content
- **Consumption**: Track daily consumption records
- **Users**: Appwrite's built-in user management

## Common Issues and Solutions

### Python Backend
- **Database Lock**: Ensure only one Streamlit instance is running
- **Dependency Issues**: Use virtual environment for Python packages
- **German Characters**: Ensure UTF-8 encoding for proper display

### Next.js Frontend
- **Appwrite Connection**: Verify environment variables and network access
- **Build Errors**: Check for missing `@/lib/appwrite` configuration
- **Font Loading**: Google Fonts may be blocked in some environments

## Special Instructions for Copilot

### Before Starting Any Issue
1. Always reference this `COPILOT_REFERENCE.md` file
2. Understand which application (Python/Next.js) the issue affects
3. Check current build/lint status before making changes
4. Consider impact on both German and English language support

### Making Changes
- **Minimal Changes**: Preserve existing functionality
- **Database Changes**: Be careful with schema modifications
- **UI Updates**: Maintain consistency with existing design patterns
- **Dependencies**: Avoid unnecessary package additions

### Documentation Updates
- Update this reference file when adding major features
- Maintain README files for both applications
- Document new environment variables or setup requirements
- Keep coding conventions consistent

## Future Considerations

- **Internationalization**: Currently German-focused, consider i18n support
- **Data Synchronization**: Potential integration between Python and Next.js apps
- **Mobile Support**: Next.js app is responsive, Python app is desktop-focused
- **Advanced Analytics**: ML-based consumption pattern analysis
- **Health Integration**: Connect with fitness tracking APIs

---

*This reference file should be updated whenever major architectural changes are made to either application.*
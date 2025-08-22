# Coffee Consumption Tracker

Coffee Consumption Tracker is a dual-application project consisting of a Python/Streamlit data analysis tool and a Next.js web application with Appwrite backend integration. The project enables users to track, visualize, and analyze their coffee consumption patterns.

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

## Working Effectively

### Repository Structure
- **Root**: Python/Streamlit application (`app.py`) with SQLite database
- **`kaffeekonsum-tracker/`**: Next.js web application with Appwrite backend
- **`requirements.txt`**: Python dependencies for Streamlit app
- **`kaffeekonsum-tracker/package.json`**: Node.js dependencies for web app

### Environment Setup and Dependencies

**Bootstrap the repository:**
```bash
# Python environment
pip install -r requirements.txt
pip install sqlalchemy  # Missing from requirements.txt - CRITICAL dependency

# Next.js environment  
cd kaffeekonsum-tracker
npm install  # Takes ~50 seconds, expect 1 low severity vulnerability
```

**Create required missing files for Next.js app:**
```bash
# Create lib directory and required files
mkdir -p kaffeekonsum-tracker/src/lib

# Create kaffeekonsum-tracker/src/lib/utils.ts
cat > kaffeekonsum-tracker/src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
EOF

# Create kaffeekonsum-tracker/src/lib/appwrite.ts
cat > kaffeekonsum-tracker/src/lib/appwrite.ts << 'EOF'
import { Client, Account, Databases } from 'appwrite';

const client = new Client();

client
    .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT || '')
    .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID || '');

export const account = new Account(client);
export const databases = new Databases(client);

// Placeholder functions - these need to be implemented based on the actual usage
export const getVarieties = async () => {
    // TODO: Implement
    return { documents: [] };
};

export const addVariety = async (name: string, userId: string) => {
    // TODO: Implement
    return {};
};

export const deleteVariety = async (id: string) => {
    // TODO: Implement
    return {};
};

export const getConsumption = async () => {
    // TODO: Implement
    return { documents: [] };
};

export const addConsumption = async (data: any) => {
    // TODO: Implement
    return {};
};

export const deleteConsumption = async (id: string) => {
    // TODO: Implement
    return {};
};

export const updateConsumption = async (id: string, data: any) => {
    // TODO: Implement
    return {};
};

export const getAllVarieties = async () => {
    // TODO: Implement
    return { documents: [] };
};
EOF

# Create environment file for Next.js
cat > kaffeekonsum-tracker/.env.local << 'EOF'
NEXT_PUBLIC_APPWRITE_PROJECT_ID=test_project_id
NEXT_PUBLIC_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
NEXT_PUBLIC_APPWRITE_Database_ID=test_db_id
NEXT_PUBLIC_APPWRITE_CONSUMPTION_COLLECTION_ID=test_consumption_id
NEXT_PUBLIC_APPWRITE_VARIETIES_COLLECTION_ID=test_varieties_id
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_ADMIN_ID=test_admin_id
EOF
```

### Build and Development Commands

**Python/Streamlit Application:**
```bash
# Run development server
streamlit run app.py
# Accessible at: http://localhost:8501
# Startup time: ~3-5 seconds
```

**Next.js Web Application:**
```bash
cd kaffeekonsum-tracker

# Development server - NEVER CANCEL
npm run dev  # Takes ~5-10 seconds to start
# Accessible at: http://localhost:3000

# Production build - NEVER CANCEL - Set timeout to 60+ minutes
npm run build  # Takes ~16-20 seconds with environment setup
# Build will fail without .env.local file and lib files

# Production server
npm start  # Takes ~500ms to start after build
# Accessible at: http://localhost:3000

# Linting (has known issues)
npm run lint  # Takes ~2-3 seconds, expect TypeScript/ESLint errors
```

**CRITICAL BUILD REQUIREMENTS:**
- **NEVER CANCEL**: Build processes may appear to hang but are working. Set timeouts of 60+ minutes.
- Next.js build requires environment variables in `.env.local` or it will fail with Appwrite errors
- Missing `src/lib/` files will cause build failures - create them as shown above
- Linting errors do not prevent dev server or production builds when configured correctly

## Validation

**Always manually validate applications after making changes:**

**Streamlit App Validation:**
1. Start: `streamlit run app.py`
2. Navigate to http://localhost:8501
3. Test core functionality:
   - Add coffee entry (date, cups, variety selection)
   - Click "💾 Speichern" button
   - Verify metrics update (Today, This Week, etc.)
   - Check data appears in editing table
   - Test export functionality

**Next.js App Validation:**
1. Ensure environment file exists: `kaffeekonsum-tracker/.env.local`
2. Start: `cd kaffeekonsum-tracker && npm run dev`
3. Navigate to http://localhost:3000
4. Test core functionality:
   - Homepage loads with charts/visualizations
   - Navigation to /dashboard and /manage works
   - UI components render properly
   - No critical JavaScript errors in console

**Production Build Validation:**
```bash
cd kaffeekonsum-tracker
npm run build  # Must complete successfully
npm start       # Must start production server
```

## Common Issues and Solutions

**Missing SQLAlchemy Error:**
```bash
# Error: No module named 'sqlalchemy'
pip install sqlalchemy
```

**Next.js Build Failures:**
```bash
# Missing lib files - create as shown in setup section
# Missing environment variables - create .env.local as shown above
# Google Fonts network errors - already fixed by removing external font imports
```

**Linting Issues:**
- Build configured to ignore linting errors during production builds
- Linting errors are expected and do not prevent functionality
- Focus on runtime functionality over linting compliance

## Development Workflows

**Making Changes to Streamlit App:**
1. Edit `app.py` or related Python files
2. Streamlit auto-reloads on file changes
3. Test functionality in browser
4. No separate build step required

**Making Changes to Next.js App:**
1. Edit files in `kaffeekonsum-tracker/src/`
2. Development server auto-reloads
3. Test in browser at http://localhost:3000
4. For production testing: `npm run build && npm start`

**Environment Configuration:**
- Streamlit: No environment setup required for basic functionality
- Next.js: Requires `.env.local` with Appwrite configuration
- Database: SQLite database (`coffee.db`) created automatically by Streamlit app

## Key Locations

**Python/Streamlit App:**
- Main application: `app.py`
- Database: `coffee.db` (auto-created)
- Dependencies: `requirements.txt` (missing sqlalchemy - install separately)

**Next.js App:**
- Source code: `kaffeekonsum-tracker/src/`
- Components: `kaffeekonsum-tracker/src/components/`
- Pages: `kaffeekonsum-tracker/src/app/`
- API integration: `kaffeekonsum-tracker/src/lib/appwrite.ts`
- Utilities: `kaffeekonsum-tracker/src/lib/utils.ts`
- Configuration: `kaffeekonsum-tracker/next.config.ts`
- Environment: `kaffeekonsum-tracker/.env.local`

## Testing Strategy

**No formal test suite exists** - validation is manual:
1. Start both applications successfully
2. Test core user workflows in both apps
3. Verify data persistence and retrieval
4. Check responsive design and UI components
5. Validate build processes complete without errors

**Always test the complete user journey:**
- Add coffee consumption data
- View statistics and visualizations  
- Export/import functionality
- Cross-application data consistency

## Timing Expectations

- Python dependency installation: ~30 seconds
- Node.js dependency installation: ~50 seconds  
- Streamlit app startup: ~3-5 seconds
- Next.js dev server startup: ~5-10 seconds
- Next.js production build: ~16-20 seconds
- Next.js production server startup: ~500ms

**NEVER CANCEL long-running operations** - set timeouts appropriately and wait for completion.
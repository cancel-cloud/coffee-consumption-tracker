# Coffee Consumption Tracker

This project helps you log, visualize, and analyze your coffee drinking habits through two complementary applications. Choose the approach that best fits your needs:

- **🐍 Python Backend**: A Streamlit-based local application for offline tracking and analysis
- **🌐 Next.js Frontend**: A modern web application with cloud sync via Appwrite
- **📊 Rich Analytics**: Comprehensive visualizations, statistics, and health tracking

## Applications Overview

### Python Streamlit Application (`app.py`)
A feature-complete local application perfect for personal use:
- **Local SQLite database** - Your data stays on your machine
- **German interface** - Localized user experience
- **Comprehensive tracking** - Varieties, caffeine content, consumption patterns
- **Rich visualizations** - Charts, calendar heatmaps, statistics
- **Data management** - CSV import/export, editing capabilities
- **Health features** - Caffeine warnings and daily recommendations

### Next.js Web Application (`kaffeekonsum-tracker/`)
A modern web interface with cloud capabilities:
- **Cloud sync** - Data stored in Appwrite database
- **User authentication** - Secure account management
- **Responsive design** - Works on desktop and mobile
- **Real-time charts** - Interactive data visualization
- **Modern UI** - Built with Tailwind CSS and Shadcn/UI
- **TypeScript** - Type-safe development

## Features

- 📈 **Daily Consumption Logging**: Track cups consumed by date and variety
- 🌱 **Coffee Variety Management**: Catalog different coffee types with caffeine content
- 📊 **Visual Analytics**: Charts, graphs, and calendar heatmaps
- ⚡ **Caffeine Tracking**: Monitor daily caffeine intake with health warnings
- 📁 **Data Import/Export**: CSV support for data portability
- ✏️ **Data Editing**: Modify or delete historical entries
- 🎨 **Beautiful UI**: Intuitive interfaces in both applications

## Technologies Used

### Python Application
- **Streamlit** - Web application framework
- **SQLAlchemy** - Database ORM
- **pandas & matplotlib** - Data analysis and visualization
- **calplot** - Calendar heatmap visualization
- **SQLite** - Local database storage

### Next.js Application
- **Next.js 15** - React framework with App Router
- **TypeScript** - Type-safe JavaScript
- **Appwrite** - Backend-as-a-Service (database, auth)
- **Tailwind CSS** - Utility-first CSS framework
- **Shadcn/UI** - Modern React component library
- **Chart.js** - Interactive chart library

## Quick Start

### Option 1: Python Streamlit App (Recommended for local use)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/cancel-cloud/coffee-consumption-tracker.git
   cd coffee-consumption-tracker
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### Option 2: Next.js Web App (Cloud-connected)

1. **Navigate to the frontend directory:**
   ```bash
   cd kaffeekonsum-tracker
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Set up environment variables:**
   ```bash
   cp env.example .env.local
   # Edit .env.local with your Appwrite configuration
   ```

4. **Run the development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser** to `http://localhost:3000`

## Documentation

- **📖 [Copilot Reference](./COPILOT_REFERENCE.md)** - Comprehensive development guide
- **🚀 [Next.js App Setup](./kaffeekonsum-tracker/README.md)** - Frontend-specific documentation
- **🐍 Python App** - No additional setup required, just run with Streamlit

## Project Structure

```
coffee-consumption-tracker/
├── app.py                    # Python Streamlit application
├── requirements.txt          # Python dependencies
├── coffee.db                 # SQLite database (auto-generated)
├── COPILOT_REFERENCE.md     # Development documentation
└── kaffeekonsum-tracker/     # Next.js web application
    ├── src/app/             # App Router pages
    ├── src/components/       # React components
    ├── package.json         # Frontend dependencies
    └── env.example          # Environment configuration template
```

## License

MIT License

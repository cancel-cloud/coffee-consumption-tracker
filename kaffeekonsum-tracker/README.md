# Kaffeekonsum-Tracker - Next.js Web Application

A modern, cloud-connected coffee consumption tracking application built with Next.js and Appwrite. This web application provides a beautiful, responsive interface for logging and analyzing your coffee consumption patterns.

## Features

- 🔐 **User Authentication** - Secure login/logout with Appwrite
- 📊 **Interactive Dashboard** - Real-time charts and analytics
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile
- ⚡ **Caffeine Tracking** - Monitor daily caffeine intake
- 🌱 **Variety Management** - Catalog and manage coffee varieties
- 📈 **Data Visualization** - Bar charts, pie charts, and calendar heatmaps
- 🎨 **Modern UI** - Built with Tailwind CSS and Shadcn/UI components

## Tech Stack

- **Framework**: Next.js 15.3.2 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **UI Components**: Shadcn/UI
- **Charts**: Chart.js with react-chartjs-2
- **Backend**: Appwrite (Database, Authentication)
- **Deployment**: Vercel-ready

## Prerequisites

- Node.js 18+ and npm
- Appwrite account and project setup
- Modern web browser

## Getting Started

### 1. Installation

```bash
# Clone the repository (if not already done)
git clone https://github.com/cancel-cloud/coffee-consumption-tracker.git
cd coffee-consumption-tracker/kaffeekonsum-tracker

# Install dependencies
npm install
```

### 2. Environment Setup

Copy the environment template and configure your Appwrite settings:

```bash
cp env.example .env.local
```

Edit `.env.local` with your Appwrite configuration:

```env
NEXT_PUBLIC_APPWRITE_PROJECT_ID=your_project_id
NEXT_PUBLIC_APPWRITE_ENDPOINT=https://fra.cloud.appwrite.io/v1
NEXT_PUBLIC_APPWRITE_Database_ID=your_database_id
NEXT_PUBLIC_APPWRITE_CONSUMPTION_COLLECTION_ID=your_collection_id
NEXT_PUBLIC_APPWRITE_VARIETIES_COLLECTION_ID=your_varieties_id
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_ADMIN_ID=your_admin_user_id
```

### 3. Appwrite Setup

1. **Create an Appwrite account** at [appwrite.io](https://appwrite.io)
2. **Create a new project** and note the project ID
3. **Set up the database** with the following collections:

#### Varieties Collection
```json
{
  "name": "string",
  "caffeine_mg": "integer"
}
```

#### Consumption Collection
```json
{
  "date": "datetime",
  "cups": "integer",
  "variety_id": "string",
  "user_id": "string"
}
```

4. **Configure authentication** - Enable email/password authentication
5. **Set permissions** for collections based on your needs

### 4. Development

```bash
# Start the development server
npm run dev

# The app will be available at http://localhost:3000
```

### 5. Building for Production

```bash
# Build the application
npm run build

# Start the production server
npm start
```

## Project Structure

```
kaffeekonsum-tracker/
├── src/
│   ├── app/                    # App Router pages
│   │   ├── dashboard/          # Main dashboard page
│   │   │   └── page.tsx
│   │   ├── manage/             # Data management page
│   │   │   └── page.tsx
│   │   ├── layout.tsx          # Root layout with navigation
│   │   ├── page.tsx            # Landing page
│   │   └── globals.css         # Global styles
│   └── components/
│       ├── ui/                 # Shadcn/UI components
│       │   ├── button.tsx
│       │   └── ...
│       ├── LoginButton.tsx     # Authentication component
│       ├── LogoutButton.tsx    # Sign out component
│       └── SessionButton.tsx   # Session management
├── public/                     # Static assets
├── env.example                 # Environment template
├── package.json                # Dependencies and scripts
├── next.config.ts              # Next.js configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── tsconfig.json               # TypeScript configuration
└── eslint.config.mjs           # ESLint configuration
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Pages and Features

### Landing Page (`/`)
- Sample charts and visualizations
- Introduction to the application
- No authentication required

### Dashboard (`/dashboard`)
- **Authentication required**
- Interactive consumption charts
- Coffee variety statistics
- Calendar heatmap of consumption patterns
- Quick data entry forms

### Management (`/manage`)
- **Authentication required**
- Coffee variety management
- Data import/export functionality
- Administrative features

## Configuration

### ESLint
The project uses Next.js ESLint configuration with TypeScript support:
- Extends `next/core-web-vitals` and `next/typescript`
- Configured in `eslint.config.mjs`

### Tailwind CSS
Modern utility-first CSS framework with custom configuration:
- Responsive design utilities
- Custom color schemes
- Component-friendly classes

### TypeScript
Strict TypeScript configuration for type safety:
- Modern ES2022 target
- App Router support
- Path aliases (`@/` points to `src/`)

## Coding Conventions

- **Components**: Use functional components with hooks
- **Styling**: Tailwind utility classes preferred
- **Type Safety**: Explicit TypeScript types for all props and state
- **File Naming**: kebab-case for files, PascalCase for components
- **Imports**: Use path aliases (`@/components`, `@/lib`)

## Common Development Tasks

### Adding New Pages
1. Create new directory in `src/app/`
2. Add `page.tsx` file with default export
3. Follow App Router conventions

### Adding Components
1. Create component in `src/components/`
2. Use TypeScript for props interface
3. Apply Tailwind classes for styling

### Integrating with Appwrite
1. Use existing patterns from `@/lib/appwrite`
2. Handle authentication state properly
3. Implement proper error handling

## Troubleshooting

### Build Issues
- Ensure all environment variables are set
- Check Appwrite connectivity
- Verify Google Fonts access (may be blocked in some environments)

### Authentication Problems
- Verify Appwrite project configuration
- Check environment variables
- Ensure proper collection permissions

### Development Server Issues
- Clear `.next` cache: `rm -rf .next`
- Reinstall dependencies: `rm -rf node_modules package-lock.json && npm install`

## Deployment

### Vercel (Recommended)
1. Connect your GitHub repository to Vercel
2. Configure environment variables in Vercel dashboard
3. Deploy automatically on push to main branch

### Other Platforms
- Ensure Node.js 18+ support
- Configure environment variables
- Build with `npm run build`
- Serve with `npm start`

## Contributing

1. Follow the existing code style and conventions
2. Run `npm run lint` before committing
3. Test all functionality before submitting changes
4. Update documentation for new features

## License

This project is licensed under the MIT License - see the [LICENSE](../LICENSE) file for details.

---

For more information about the overall project structure and development guidelines, see the [COPILOT_REFERENCE.md](../COPILOT_REFERENCE.md) file.

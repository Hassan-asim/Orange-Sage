# Orange Sage Frontend

This is the frontend application for Orange Sage, built with React, TypeScript, and Tailwind CSS using shadcn/ui components.

## Features

- **Modern UI**: Built with shadcn/ui components and Tailwind CSS
- **Responsive Design**: Mobile-first approach with responsive layouts
- **Authentication**: User login and registration with JWT tokens
- **Dashboard**: Overview of scans, findings, and security metrics
- **Project Management**: Create and manage security assessment projects
- **Scan Management**: Monitor and control security scans
- **Findings**: Review discovered vulnerabilities and security issues
- **Reports**: Generate and download security assessment reports
- **Settings**: User preferences and account management

## Tech Stack

- **React 18**: Modern React with hooks and functional components
- **TypeScript**: Type-safe JavaScript
- **Vite**: Fast build tool and development server
- **Tailwind CSS**: Utility-first CSS framework
- **shadcn/ui**: High-quality, accessible UI components
- **React Router**: Client-side routing
- **React Query**: Data fetching and caching
- **React Hook Form**: Form handling and validation
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API requests

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running (see backend README)

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create environment file:
```bash
cp .env.example .env
```

3. Update environment variables in `.env`:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`.

### Building for Production

Build the application:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── ui/             # shadcn/ui components
│   └── Layout.tsx      # Main layout component
├── hooks/              # Custom React hooks
├── pages/              # Page components
├── services/           # API services
├── styles/             # Global styles
└── utils/              # Utility functions
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run lint:fix` - Fix ESLint issues

## Environment Variables

- `VITE_API_BASE_URL` - Backend API base URL (default: http://localhost:8000/api/v1)

## Deployment

The frontend can be deployed to any static hosting service:

- **Vercel**: Connect your GitHub repository
- **Netlify**: Drag and drop the `dist` folder
- **AWS S3**: Upload the `dist` folder to an S3 bucket
- **GitHub Pages**: Use GitHub Actions to deploy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License.

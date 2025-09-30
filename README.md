# FlavorGraph - Recipe Navigator

FlavorGraph is an intelligent recipe navigation platform built with Next.js, Supabase, and modern UI components. Discover, organize, and enjoy cooking with our comprehensive recipe management system.

## Features

- 🔐 **Authentication**: Secure user authentication with Supabase
- 🍳 **Recipe Management**: Browse, search, and organize recipes
- 🎨 **Modern UI**: Beautiful, responsive design with Tailwind CSS
- 🌙 **Dark Mode**: Built-in theme switching support
- 📱 **Mobile Responsive**: Optimized for all device sizes
- 🔍 **Smart Search**: Intelligent recipe discovery
- 👥 **Community**: Share and discover recipes from other users

## Tech Stack

- **Framework**: Next.js 14 with App Router
- **Authentication**: Supabase Auth
- **Database**: Supabase PostgreSQL
- **Styling**: Tailwind CSS
- **UI Components**: Radix UI + shadcn/ui
- **Icons**: Lucide React
- **Fonts**: Geist Sans & Mono
- **TypeScript**: Full type safety

## Getting Started

### Prerequisites

- Node.js 18+ 
- pnpm (recommended) or npm
- Supabase account

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd flavor-graph-auth
   ```

2. **Install dependencies**
   ```bash
   pnpm install
   # or
   npm install
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env.local
   ```
   
   Fill in your Supabase credentials:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_DEV_SUPABASE_REDIRECT_URL=http://localhost:3000/auth/callback
   ```

4. **Set up Supabase**
   - Create a new Supabase project
   - Enable authentication in your Supabase dashboard
   - Configure authentication providers as needed
   - Set up your database schema (if required)

5. **Run the development server**
   ```bash
   pnpm dev
   # or
   npm run dev
   ```

6. **Open your browser**
   Navigate to [http://localhost:3000](http://localhost:3000)

## Project Structure

```
├── app/                    # Next.js App Router
│   ├── auth/              # Authentication pages
│   ├── dashboard/         # Dashboard page
│   ├── about/             # About page
│   ├── protected/         # Protected routes
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # UI components (shadcn/ui)
│   ├── recipe-card.tsx   # Recipe card component
│   └── theme-provider.tsx # Theme provider
├── hooks/                # Custom React hooks
├── lib/                  # Utility functions
│   ├── supabase/        # Supabase configuration
│   └── utils.ts         # General utilities
├── public/              # Static assets
└── styles/              # Global styles
```

## Available Scripts

- `pnpm dev` - Start development server
- `pnpm build` - Build for production
- `pnpm start` - Start production server
- `pnpm lint` - Run ESLint

## Authentication Flow

1. **Sign Up**: Users create accounts with email/password
2. **Email Verification**: Supabase sends verification emails
3. **Sign In**: Authenticated users access protected routes
4. **Session Management**: Automatic session handling with middleware

## Key Pages

- **Home** (`/`) - Landing page with app overview
- **Dashboard** (`/dashboard`) - Main recipe browsing interface
- **About** (`/about`) - Information about FlavorGraph
- **Login** (`/auth/login`) - User authentication
- **Sign Up** (`/auth/sign-up`) - User registration
- **Protected** (`/protected`) - Example protected route

## Deployment

### Vercel (Recommended)

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Add environment variables in Vercel dashboard
4. Deploy automatically on push

### Other platforms

The app can be deployed on any platform that supports Next.js:
- Netlify
- Railway
- AWS Amplify
- DigitalOcean App Platform

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact the development team.

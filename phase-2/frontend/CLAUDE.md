# Frontend Development Guide - Phase II

## Overview

This is the Next.js frontend for the Phase II Todo application. It provides a modern web interface for user authentication and task management using Better Auth for JWT-based authentication.

## Technology Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (JWT)
- **HTTP Client**: fetch API
- **State Management**: React hooks + localStorage

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
```

Edit `.env.local` with your actual values:
- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000)
- `BETTER_AUTH_SECRET`: Must match backend secret (generate with `openssl rand -hex 32`)
- `BETTER_AUTH_URL`: Frontend URL (default: http://localhost:3000)

### 3. Run Development Server

```bash
npm run dev
```

Frontend runs at: **http://localhost:3000**

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx           # Root layout
│   ├── page.tsx             # Landing page
│   ├── globals.css          # Global styles
│   ├── login/
│   │   └── page.tsx         # Login page
│   ├── register/
│   │   └── page.tsx         # Register page
│   └── dashboard/
│       └── page.tsx         # Tasks dashboard (protected)
├── components/
│   ├── auth/
│   │   ├── LoginForm.tsx    # Login form component
│   │   └── RegisterForm.tsx # Register form component
│   └── tasks/
│       ├── TaskList.tsx     # Task list component
│       ├── TaskItem.tsx     # Individual task
│       ├── TaskForm.tsx     # Create/edit task form
│       └── TaskActions.tsx  # Task action buttons
├── lib/
│   ├── auth.ts              # Better Auth configuration
│   ├── api.ts               # API client utilities
│   └── types.ts             # TypeScript types
├── hooks/
│   ├── useAuth.ts           # Authentication hook
│   └── useTasks.ts          # Tasks data hook
└── middleware.ts            # Route protection
```

## Development Guidelines

### 1. Code Organization

- **Components**: Reusable UI components (stateless when possible)
- **Hooks**: Custom React hooks for data fetching and state
- **Lib**: Utility functions, API clients, type definitions
- **App**: Next.js App Router pages and layouts

### 2. Authentication Flow

**Better Auth Integration**:
- JWT tokens stored in httpOnly cookies (handled by Better Auth)
- Token automatically sent with API requests
- Protected routes check auth state via middleware

**Login Flow**:
1. User submits credentials
2. Better Auth validates and issues JWT
3. Token stored in httpOnly cookie
4. Redirect to dashboard

**Protected Routes**:
```typescript
// middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'

export function middleware(request: NextRequest) {
  const token = request.cookies.get('better-auth.session_token')

  if (!token) {
    return NextResponse.redirect(new URL('/login', request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: '/dashboard/:path*'
}
```

### 3. API Integration

**API Client Pattern**:

```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
) {
  const response = await fetch(`${API_BASE}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    credentials: 'include', // Send cookies
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Request failed')
  }

  return response.json()
}
```

**Usage in Components**:

```typescript
// hooks/useTasks.ts
import { useEffect, useState } from 'react'
import { apiRequest } from '@/lib/api'

export function useTasks(userId: string) {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function fetchTasks() {
      try {
        const data = await apiRequest(`/api/${userId}/tasks`)
        setTasks(data)
      } catch (error) {
        console.error('Failed to fetch tasks:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchTasks()
  }, [userId])

  return { tasks, loading }
}
```

### 4. Error Handling

**Display Errors to Users**:

```typescript
const [error, setError] = useState<string | null>(null)

async function handleSubmit(e: FormEvent) {
  e.preventDefault()
  setError(null)

  try {
    await apiRequest('/api/tasks', {
      method: 'POST',
      body: JSON.stringify(formData)
    })
  } catch (err) {
    setError(err instanceof Error ? err.message : 'Something went wrong')
  }
}

// In JSX
{error && (
  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}
```

### 5. TypeScript Types

**Define Shared Types**:

```typescript
// lib/types.ts
export interface User {
  id: string
  email: string
  name: string | null
}

export interface Task {
  id: number
  title: string
  description: string | null
  completed: boolean
  user_id: string
  created_at: string
  updated_at: string
}

export interface CreateTaskInput {
  title: string
  description?: string
}

export interface UpdateTaskInput {
  title?: string
  description?: string
}
```

## Styling with Tailwind

**Consistent Design Patterns**:

```typescript
// Button variants
const primaryButton = "px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
const secondaryButton = "px-6 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300"
const dangerButton = "px-6 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700"

// Form inputs
const inputClass = "w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"

// Cards
const cardClass = "bg-white rounded-lg shadow-md p-6"
```

## State Management

**Use React Hooks**:
- `useState` for local component state
- `useEffect` for data fetching
- Custom hooks for shared logic
- Context API for global state (auth, theme)

**Example Auth Context**:

```typescript
// contexts/AuthContext.tsx
import { createContext, useContext, useState, useEffect } from 'react'

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Implementation...

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth must be used within AuthProvider')
  return context
}
```

## Testing

```bash
# Run tests (when configured)
npm test

# Type checking
npm run type-check

# Linting
npm run lint
```

## Common Tasks

### Add New Page

1. Create file in `app/<route>/page.tsx`
2. Define TypeScript types for props
3. Implement component with Tailwind styling
4. Add to middleware config if protected

### Add New Component

1. Create file in `components/<category>/<Name>.tsx`
2. Define component props interface
3. Use Tailwind for styling
4. Export from component

### Add New API Integration

1. Define types in `lib/types.ts`
2. Create API function in `lib/api.ts`
3. Create custom hook in `hooks/` if stateful
4. Use in component

## Phase II Constraints

**Must NOT**:
- ❌ Add AI features
- ❌ Add MCP tools
- ❌ Add real-time features (WebSockets)
- ❌ Add advanced state management (Redux, Zustand)
- ❌ Add Docker/Kubernetes

**Must HAVE**:
- ✅ Better Auth JWT integration
- ✅ Protected routes with middleware
- ✅ Clean component architecture
- ✅ TypeScript type safety
- ✅ Responsive design (mobile-first)

## Troubleshooting

### API Requests Fail

- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend is running on correct port
- Check browser console for CORS errors
- Verify JWT token is being sent (check cookies)

### Better Auth Issues

- Ensure `BETTER_AUTH_SECRET` matches backend
- Check cookie settings in Better Auth config
- Verify `BETTER_AUTH_URL` is correct
- Clear cookies and try login again

### Build Errors

- Run `npm install` to ensure dependencies are up to date
- Check TypeScript errors with `npm run type-check`
- Clear `.next` folder: `rm -rf .next`
- Verify Node.js version: `node -v` (should be 18+)

### Styling Issues

- Verify Tailwind config includes all content paths
- Check `globals.css` imports Tailwind directives
- Run `npm run dev` to rebuild CSS
- Check browser DevTools for applied classes

## Resources

- Next.js Docs: https://nextjs.org/docs
- Better Auth Docs: https://better-auth.com/docs
- Tailwind CSS Docs: https://tailwindcss.com/docs
- TypeScript Handbook: https://www.typescriptlang.org/docs/
- Specification: `/specs/001-fullstack-web-app/spec.md`
- Plan: `/specs/001-fullstack-web-app/plan.md`

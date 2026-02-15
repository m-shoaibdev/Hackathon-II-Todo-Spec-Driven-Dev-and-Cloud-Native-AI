/**
 * User login page
 *
 * Public route for user authentication
 */

import LoginForm from '@/components/auth/LoginForm'

export default function LoginPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="w-full max-w-md">
        {/* Page header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Welcome Back</h1>
          <p className="text-gray-600">
            Login to access your todo list
          </p>
        </div>

        {/* Login form card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <LoginForm />
        </div>

        {/* Back to home link */}
        <div className="text-center mt-6">
          <a
            href="/"
            className="text-sm text-gray-600 hover:text-gray-800"
          >
            ← Back to home
          </a>
        </div>
      </div>
    </main>
  )
}

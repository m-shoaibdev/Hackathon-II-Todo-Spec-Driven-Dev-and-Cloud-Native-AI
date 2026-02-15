/**
 * User registration page
 *
 * Public route for new user account creation
 */

import RegisterForm from '@/components/auth/RegisterForm'

export default function RegisterPage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="w-full max-w-md">
        {/* Page header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold mb-2">Create Account</h1>
          <p className="text-gray-600">
            Get started with your personal todo list
          </p>
        </div>

        {/* Registration form card */}
        <div className="bg-white rounded-lg shadow-lg p-8">
          <RegisterForm />
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

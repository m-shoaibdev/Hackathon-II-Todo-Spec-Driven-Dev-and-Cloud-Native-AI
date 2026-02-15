export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-4">Todo App - Phase II</h1>
        <p className="text-xl mb-8">Multi-user task management with authentication</p>
        <div className="flex gap-4 justify-center">
          <a href="/login" className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Login
          </a>
          <a href="/register" className="px-6 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700">
            Register
          </a>
        </div>
      </div>
    </main>
  )
}

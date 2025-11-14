import React from 'react'

const Login = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="w-full max-w-md p-6 bg-white border-4 border-black rounded-lg shadow-md">
        <h1 className="text-2xl font-bold mb-4 text-center">Login</h1>
        <form>
          <input
            className="w-full p-2 mb-3 border rounded"
            placeholder="Email"
            type="email"
          />
          <input
            className="w-full p-2 mb-3 border rounded"
            placeholder="Password"
            type="password"
          />
          <button className="w-full bg-black text-white p-2 rounded">Sign In</button>
        </form>
      </div>
    </div>
  )
}

export default Login

import React from 'react'

const Navbar = () => {
  return (
    <nav className="bg-black p-4 flex justify-between items-center">
      <div className="flex items-center space-x-2">
        {/* <img
          src=""
          alt="Icon"
          className="h-6 w-6 text-purple-600"
        /> */}
        <span className="text-purple-600 font-semibold">SummarizeIT</span>
      </div>
    </nav>
  )
}

export default Navbar

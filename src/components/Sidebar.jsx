import React from 'react'

const Sidebar = ({props}) => {
  return (
    <>
        <aside className='h-screen'>
            <nav className='h-full flex flex-col bg-white border-r shadow-sm'>
                <div className='p-4 pb-2 flex justify-between items-center'></div>
            </nav>
        </aside>
    </>
  )
}

export default Sidebar

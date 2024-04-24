import React, { useState } from 'react';
import axios from 'axios';
import { baseUrl } from './components/baseUtrl';
import Navbar from './components/Navbar';

function App() {
  const [url, setUrl] = useState('');
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${baseUrl}/summarize`, { url });
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error fetching summary:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar />
      <div className='bg-black min-h-screen flex justify-center items-center'>
        <div className='max-w-xl w-full'>
          <form onSubmit={handleSubmit} className='flex items-center'>
            <label className='mr-2 flex-1'>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                className='border border-purple-500 px-3 py-2 focus:outline-none focus:border-purple-700 bg-transparent text-white rounded-xl w-full'
                placeholder='Enter the URL'
                required
              />
            </label>
            <button type="submit" disabled={loading} className='bg-purple-500 text-white px-4 py-2 rounded-lg focus:outline-none hover:bg-purple-700 rounded-xl'>
              {loading ? 'Loading...' : 'Summarize'}
            </button>
          </form>
          {loading && (
            <div className='mt-4 flex justify-center'>
              <div className='loader'></div>
            </div>
          )}
          {summary && (
            <div className='mt-8'>
              <h2 className='text-xl text-gray-300'>Summary:</h2>
              <p className='mt-2 text-purple-500'>{summary}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

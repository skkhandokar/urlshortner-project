import React, { useState } from 'react';

function UrlSite() {
    const [originalUrl, setOriginalUrl] = useState('');
    const [shortUrl, setShortUrl] = useState('');
  
    const handleSubmit = async (e) => {
      e.preventDefault();
      const response = await fetch('http://localhost:8000/api/shorten/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ original_url: originalUrl }),
      });
      const data = await response.json();
      setShortUrl(`http://localhost:8000/${data.short_url}`);
    };
  
    return (
      <div className="App">
        <h1>URL Shortener</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="url"
            placeholder="Enter original URL"
            value={originalUrl}
            onChange={(e) => setOriginalUrl(e.target.value)}
            required
          />
          <button type="submit">Shorten</button>
        </form>
        {shortUrl && (
          <div>
            <p>Shortened URL: <a href={shortUrl} target="_blank" rel="noopener noreferrer">{shortUrl}</a></p>
          </div>
        )}
      </div>
    );
  }


export default UrlSite

import './App.css';
import React from 'react';
import { HashRouter, Routes, Route } from 'react-router-dom';

import UrlSite from './Conponants/urlApp/UrlSite';
// eslint-disable-next-line no-unused-vars
 // Assuming Layout is a component and should start with an uppercase letter
                        
function App() {
  return (
    <HashRouter>
      <Routes>

        <Route path="/" exact element={<UrlSite />} />

      </Routes>
    </HashRouter>
  );
}

export default App;

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './components/Home';
import TaskPage from './components/Task';
import FeedbackPage from './components/Feedback';

const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/task" element={<TaskPage />} />
        <Route path="/feedback/:submissionId" element={<FeedbackPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
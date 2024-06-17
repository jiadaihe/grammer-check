import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

interface FeedbackData {
  score: number;
  feedback: string;
}

const FeedbackPage: React.FC = () => {
  const { submissionId } = useParams<{ submissionId: string }>();
  const [feedback, setFeedback] = useState<FeedbackData | null>(null);

  useEffect(() => {
    // Fetch the score and feedback from the backend
    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/feedback/${submissionId}`);
        const data = await response.json();
        setFeedback(data);
      } catch (error) {
        console.error('Error fetching feedback:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>Feedback</h1>
      {feedback ? (
        <>
          <h2>Score: {feedback.score}</h2>
          <p>{feedback.feedback}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
};

export default FeedbackPage;
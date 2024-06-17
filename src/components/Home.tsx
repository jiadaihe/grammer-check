import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface CandidateDetails {
  name: string;
  email: string;
  phone: string;
}

const HomePage: React.FC = () => {
  const [candidateDetails, setCandidateDetails] = useState<CandidateDetails>({
    name: '',
    email: '',
    phone: '',
  });
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    // Save the candidate details
    console.log('Name:', candidateDetails.name);
    console.log('Email:', candidateDetails.email);
    console.log('Phone:', candidateDetails.phone);
    // Navigate to the Task Page
    navigate('/task');
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCandidateDetails((prevDetails) => ({
      ...prevDetails,
      [name]: value,
    }));
  };

  return (
    <div>
      <h1>Take2 AI Simulation</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="name">Name:</label>
          <input
            type="text"
            id="name"
            name="name"
            value={candidateDetails.name}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email:</label>
          <input
            type="email"
            id="email"
            name="email"
            value={candidateDetails.email}
            onChange={handleInputChange}
            required
          />
        </div>
        <div>
          <label htmlFor="phone">Phone:</label>
          <input
            type="tel"
            id="phone"
            name="phone"
            value={candidateDetails.phone}
            onChange={handleInputChange}
            required
          />
        </div>
        <button type="submit">Start Simulation</button>
      </form>
    </div>
  );
};

export default HomePage;
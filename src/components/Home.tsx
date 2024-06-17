import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface User {
  id: number | null
  name: string
  email: string
  phone: string
}

const HomePage: React.FC = () => {
  const [user, setUser] = useState<User>({
    id: null,
    name: '',
    email: '',
    phone: '',
  });
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    try {
      e.preventDefault();
      const response = await fetch('http://localhost:8000/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          name: user.name,
          email: user.email,
          phone: user.phone,
        }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setUser((prevUser) => ({
        ...prevUser,
        id: data.userId,
      }));
      // Navigate to the Task Page
      navigate(`/task/${data.userId}`);
    } catch (error) {
      console.error('Error submitting user:', error);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setUser((prevDetails) => ({
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
            value={user.name}
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
            value={user.email}
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
            value={user.phone}
            onChange={handleInputChange}
          />
        </div>
        <button type="submit">Start Simulation</button>
      </form>
    </div>
  );
};

export default HomePage;
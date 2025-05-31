import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders CarbonScope app', () => {
  render(<App />);
  const linkElement = screen.getByText(/CarbonScope/i);
  expect(linkElement).toBeInTheDocument();
});

test('renders carbon footprint analyzer text', () => {
  render(<App />);
  const element = screen.getByText(/Carbon Footprint/i);
  expect(element).toBeInTheDocument();
});

import React from 'react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { AppProvider } from '../store/appStore';
import { HomePage } from '../pages/HomePage';
import { TrackerPage } from '../pages/TrackerPage';
import { AnalyzingPage } from '../pages/AnalyzingPage';
import { Navbar } from '../components/common/Navbar';

// Mock scrollTo
window.scrollTo = vi.fn();

describe('Core Page Components Render Tests', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
  });

  it('renders Navbar with logo and primary links', () => {
    render(
      <AppProvider>
        <MemoryRouter>
          <Navbar />
        </MemoryRouter>
      </AppProvider>
    );

    // Should render logo title
    expect(screen.getByText(/Navigator/i)).toBeInTheDocument();
  });

  it('renders HomePage hero section and explore CTA', () => {
    render(
      <AppProvider>
        <MemoryRouter>
          <HomePage />
        </MemoryRouter>
      </AppProvider>
    );

    // Hero headline should be visible
    const headings = screen.getAllByRole('heading');
    expect(headings.length).toBeGreaterThan(0);
  });

  it('renders AnalyzingPage with progress steps', () => {
    render(
      <AppProvider>
        <MemoryRouter>
          <AnalyzingPage />
        </MemoryRouter>
      </AppProvider>
    );

    expect(screen.getByText(/Understanding your profile signals/i)).toBeInTheDocument();
  });

  it('renders TrackerPage with header and action buttons', () => {
    render(
      <AppProvider>
        <MemoryRouter>
          <TrackerPage />
        </MemoryRouter>
      </AppProvider>
    );

    expect(screen.getByText(/Application Guidance Tracker/i)).toBeInTheDocument();
  });
});

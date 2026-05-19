import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';

import KpiCard from '../components/KpiCard';

describe('KpiCard', () => {
  it('renders title and value', () => {
    render(<KpiCard title="Total Employees" value={1000} subtitle="All regions" />);
    expect(screen.getByText('Total Employees')).toBeInTheDocument();
    expect(screen.getByText('1000')).toBeInTheDocument();
    expect(screen.getByText('All regions')).toBeInTheDocument();
  });
});

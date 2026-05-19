import axios from 'axios';
import type {
  Employee,
  EmployeeCreatePayload,
  EmployeeFilters,
  EmployeeUpdatePayload,
  FilterMetadata,
  PaginatedResponse,
} from '../types/employee';
import type { CountrySalaryStats, DashboardInsights, JobTitleSalaryStats } from '../types/insights';

const API_BASE = import.meta.env.VITE_API_URL || '/api/v1';

const client = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 60_000,
});

export const employeeApi = {
  list: (filters: EmployeeFilters = {}) =>
    client.get<PaginatedResponse<Employee>>('/employees', { params: filters }).then((r) => r.data),

  get: (id: number) => client.get<Employee>(`/employees/${id}`).then((r) => r.data),

  create: (payload: EmployeeCreatePayload) =>
    client.post<Employee>('/employees', payload).then((r) => r.data),

  update: (id: number, payload: EmployeeUpdatePayload) =>
    client.put<Employee>(`/employees/${id}`, payload).then((r) => r.data),

  delete: (id: number) => client.delete(`/employees/${id}`),

  metadata: () => client.get<FilterMetadata>('/employees/metadata/filters').then((r) => r.data),
};

export const insightsApi = {
  countryStats: (country?: string) =>
    client
      .get<CountrySalaryStats[]>('/insights/salary/country', { params: { country } })
      .then((r) => r.data),

  jobTitleStats: (country?: string, job_title?: string) =>
    client
      .get<JobTitleSalaryStats[]>('/insights/salary/job-title', { params: { country, job_title } })
      .then((r) => r.data),

  dashboard: (country?: string) =>
    client
      .get<DashboardInsights>('/insights/dashboard', { params: { country } })
      .then((r) => r.data),
};

export default client;

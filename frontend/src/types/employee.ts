export type EmploymentType = 'full_time' | 'part_time' | 'contract' | 'intern';
export type EmployeeStatus = 'active' | 'inactive';
export type Gender = 'male' | 'female' | 'other' | 'prefer_not_to_say';

export interface Employee {
  id: number;
  employee_id: string;
  full_name: string;
  email: string;
  phone_number: string;
  job_title: string;
  department: string;
  country: string;
  salary: number;
  currency: string;
  date_of_joining: string;
  employment_type: EmploymentType;
  manager_name: string;
  status: EmployeeStatus;
  gender?: Gender | null;
  city?: string | null;
  bonus?: number | null;
  last_appraisal_rating?: number | null;
  age_band?: string | null;
  experience_years?: number | null;
  created_at: string;
  updated_at: string;
}

export interface EmployeeCreatePayload {
  employee_id: string;
  full_name: string;
  email: string;
  phone_number: string;
  job_title: string;
  department: string;
  country: string;
  salary: number;
  currency: string;
  date_of_joining: string;
  employment_type: EmploymentType;
  manager_name: string;
  status: EmployeeStatus;
  gender?: Gender | null;
  city?: string | null;
  bonus?: number | null;
  last_appraisal_rating?: number | null;
  age_band?: string | null;
  experience_years?: number | null;
}

export type EmployeeUpdatePayload = Partial<EmployeeCreatePayload>;

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface EmployeeFilters {
  search?: string;
  country?: string;
  department?: string;
  job_title?: string;
  status?: EmployeeStatus;
  salary_min?: number;
  salary_max?: number;
  page?: number;
  page_size?: number;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}

export interface FilterMetadata {
  countries: string[];
  departments: string[];
  job_titles: string[];
}

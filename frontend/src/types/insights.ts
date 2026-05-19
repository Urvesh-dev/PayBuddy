export interface CountrySalaryStats {
  country: string;
  min_salary: number;
  max_salary: number;
  avg_salary: number;
  employee_count: number;
  currency?: string | null;
}

export interface JobTitleSalaryStats {
  country: string;
  job_title: string;
  avg_salary: number;
  employee_count: number;
  min_salary: number;
  max_salary: number;
}

export interface DepartmentPayroll {
  department: string;
  total_payroll: number;
  avg_salary: number;
  employee_count: number;
}

export interface TopEmployee {
  employee_id: string;
  full_name: string;
  job_title: string;
  department: string;
  country: string;
  salary: number;
  currency: string;
}

export interface DashboardInsights {
  total_employees: number;
  active_employees: number;
  inactive_employees: number;
  median_salary: number | null;
  country_stats: CountrySalaryStats[];
  department_payroll: DepartmentPayroll[];
  top_paid_employees: TopEmployee[];
  country_employee_counts: Record<string, number>;
  salary_percentiles: { percentile: number; salary: number }[];
  status_breakdown: { status: string; count: number }[];
  hiring_trend: { year: number; month: number; count: number }[];
  gender_pay_gap: { gender: string; avg_salary: number; employee_count: number }[];
}

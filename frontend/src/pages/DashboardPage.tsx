import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  FormControl,
  Grid,
  InputLabel,
  MenuItem,
  Select,
  Typography,
} from '@mui/material';
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import { toast } from 'react-toastify';

import EmptyState from '../components/EmptyState';
import KpiCard from '../components/KpiCard';
import LoadingState from '../components/LoadingState';
import { employeeApi, insightsApi } from '../services/api';
import type { DashboardInsights } from '../types/insights';
import { getApiErrorMessage } from '../utils/apiError';

const formatSalaryTooltip = (value: number | string | ReadonlyArray<number | string>): string => {
  const raw = Array.isArray(value) ? value[0] : value;
  return Number(raw).toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
};

export default function DashboardPage() {
  const [data, setData] = useState<DashboardInsights | null>(null);
  const [countries, setCountries] = useState<string[]>([]);
  const [country, setCountry] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadInsights = () => {
    setLoading(true);
    setError(null);
    insightsApi
      .dashboard(country || undefined)
      .then(setData)
      .catch((err) => {
        const message = getApiErrorMessage(err, 'Failed to load insights');
        setError(message);
        toast.error(message);
      })
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    employeeApi.metadata().then((m) => setCountries(m.countries)).catch(() => {});
  }, []);

  useEffect(() => {
    loadInsights();
  }, [country]);

  if (loading) return <LoadingState message="Loading salary insights..." />;

  if (error || !data) {
    return (
      <Box>
        <Typography variant="h5" fontWeight={700} mb={2}>
          Salary Insights
        </Typography>
        <EmptyState
          title="Could not load insights"
          description={error ?? 'No data returned from the server.'}
        />
        <Button variant="contained" onClick={loadInsights} sx={{ mt: 2 }}>
          Retry
        </Button>
      </Box>
    );
  }

  const deptChart = data.department_payroll.slice(0, 10).map((d) => ({
    name: d.department,
    payroll: Number(d.total_payroll),
    avg: Number(d.avg_salary),
  }));

  const countryChart = data.country_stats.map((c) => ({
    name: c.country,
    avg: Number(c.avg_salary),
    count: c.employee_count,
  }));

  const hiringChart = data.hiring_trend.slice(-24).map((h) => ({
    label: `${h.year}-${String(h.month).padStart(2, '0')}`,
    hires: h.count,
  }));

  const statusChart = data.status_breakdown;

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5" fontWeight={700}>
          Salary Insights
        </Typography>
        <FormControl size="small" sx={{ minWidth: 200 }}>
          <InputLabel>Filter by Country</InputLabel>
          <Select
            label="Filter by Country"
            value={country}
            onChange={(e) => setCountry(e.target.value)}
          >
            <MenuItem value="">All Countries</MenuItem>
            {countries.map((c) => (
              <MenuItem key={c} value={c}>
                {c}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Grid container spacing={2} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard title="Total Employees" value={data.total_employees.toLocaleString()} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard title="Active" value={data.active_employees.toLocaleString()} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard title="Inactive" value={data.inactive_employees.toLocaleString()} />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KpiCard
            title="Median Salary"
            value={
              data.median_salary
                ? Number(data.median_salary).toLocaleString(undefined, { maximumFractionDigits: 0 })
                : '—'
            }
          />
        </Grid>
      </Grid>

      <Grid container spacing={2}>
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Average Salary by Country
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={countryChart}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" tick={{ fontSize: 11 }} angle={-25} textAnchor="end" height={70} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="avg" fill="#1565C0" name="Avg Salary" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Department Payroll Cost
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={deptChart} layout="vertical">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" width={100} tick={{ fontSize: 11 }} />
                  <Tooltip />
                  <Bar dataKey="payroll" fill="#00897B" name="Total Payroll" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Hiring Trend
              </Typography>
              <ResponsiveContainer width="100%" height={280}>
                <LineChart data={hiringChart}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="label" tick={{ fontSize: 10 }} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="hires" stroke="#1565C0" strokeWidth={2} />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top 10 Highest Paid
              </Typography>
              <Box component="table" width="100%" sx={{ borderCollapse: 'collapse' }}>
                <thead>
                  <tr>
                    <th align="left">Name</th>
                    <th align="left">Title</th>
                    <th align="right">Salary</th>
                  </tr>
                </thead>
                <tbody>
                  {data.top_paid_employees.map((e) => (
                    <tr key={e.employee_id}>
                      <td>{e.full_name}</td>
                      <td>{e.job_title}</td>
                      <td align="right">
                        {e.currency} {Number(e.salary).toLocaleString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {data.gender_pay_gap.length > 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Gender Pay Gap (Avg Salary)
                </Typography>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart
                    data={data.gender_pay_gap.map((g) => ({
                      gender: g.gender,
                      avg: Number(g.avg_salary),
                    }))}
                  >
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="gender" />
                    <YAxis tickFormatter={formatSalaryTooltip} />
                    <Tooltip
                      formatter={(value) => [formatSalaryTooltip(value), 'Avg Salary'] as [string, string]}
                    />
                    <Bar dataKey="avg" fill="#7B1FA2" name="Avg Salary" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>

      <Box mt={2}>
        <Typography variant="body2" color="text.secondary">
          Status: {statusChart.map((s) => `${s.status}: ${s.count}`).join(' · ')}
        </Typography>
      </Box>
    </Box>
  );
}

import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
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
  TextField,
  Typography,
} from '@mui/material';
import { toast } from 'react-toastify';

import LoadingState from '../components/LoadingState';
import { employeeApi } from '../services/api';
import type {
  EmployeeCreatePayload,
  EmployeeUpdatePayload,
  EmploymentType,
  EmployeeStatus,
} from '../types/employee';
import { getApiErrorMessage } from '../utils/apiError';

const COUNTRIES = [
  'United States', 'United Kingdom', 'Canada', 'Germany', 'France',
  'India', 'Australia', 'Singapore', 'Japan', 'Brazil',
  'Netherlands', 'Spain', 'Italy', 'Mexico', 'South Africa',
];

const defaultForm: EmployeeCreatePayload = {
  employee_id: '',
  full_name: '',
  email: '',
  phone_number: '+14155552671',
  job_title: '',
  department: '',
  country: 'United States',
  salary: 0,
  currency: 'USD',
  date_of_joining: new Date().toISOString().slice(0, 10),
  employment_type: 'full_time',
  manager_name: '',
  status: 'active',
};

export default function EmployeeFormPage() {
  const { id } = useParams();
  const isEdit = Boolean(id);
  const navigate = useNavigate();
  const [form, setForm] = useState<EmployeeCreatePayload>(defaultForm);
  const [loading, setLoading] = useState(isEdit);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (!id) return;
    employeeApi
      .get(Number(id))
      .then((emp) => {
        setForm({
          employee_id: emp.employee_id,
          full_name: emp.full_name,
          email: emp.email,
          phone_number: emp.phone_number,
          job_title: emp.job_title,
          department: emp.department,
          country: emp.country,
          salary: Number(emp.salary),
          currency: emp.currency,
          date_of_joining: emp.date_of_joining,
          employment_type: emp.employment_type,
          manager_name: emp.manager_name,
          status: emp.status,
          gender: emp.gender,
          city: emp.city,
          bonus: emp.bonus ? Number(emp.bonus) : undefined,
          experience_years: emp.experience_years ?? undefined,
        });
      })
      .catch(() => toast.error('Failed to load employee'))
      .finally(() => setLoading(false));
  }, [id]);

  const update = (field: keyof EmployeeCreatePayload, value: unknown) => {
    setForm((f) => ({ ...f, [field]: value }));
  };

  const buildUpdatePayload = (): EmployeeUpdatePayload => {
    const payload: EmployeeUpdatePayload = { ...form };
    if (payload.city === '') {
      payload.city = null;
    }
    if (payload.bonus === undefined || Number.isNaN(payload.bonus)) {
      delete payload.bonus;
    }
    return payload;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (form.salary <= 0) {
      toast.error('Salary must be positive');
      return;
    }
    setSaving(true);
    try {
      if (isEdit && id) {
        await employeeApi.update(Number(id), buildUpdatePayload());
        toast.success('Employee updated');
      } else {
        await employeeApi.create(form);
        toast.success('Employee created');
      }
      navigate('/employees');
    } catch (err) {
      toast.error(getApiErrorMessage(err, 'Failed to save employee'));
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <LoadingState />;

  return (
    <Box maxWidth={900}>
      <Typography variant="h5" fontWeight={700} mb={3}>
        {isEdit ? 'Edit Employee' : 'Add Employee'}
      </Typography>
      <Card>
        <CardContent>
          <form onSubmit={handleSubmit}>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Employee ID" value={form.employee_id}
                  onChange={(e) => update('employee_id', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Full Name" value={form.full_name}
                  onChange={(e) => update('full_name', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required type="email" label="Email" value={form.email}
                  onChange={(e) => update('email', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Phone" value={form.phone_number}
                  onChange={(e) => update('phone_number', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Job Title" value={form.job_title}
                  onChange={(e) => update('job_title', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Department" value={form.department}
                  onChange={(e) => update('department', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={4}>
                <FormControl fullWidth>
                  <InputLabel>Country</InputLabel>
                  <Select label="Country" value={form.country}
                    onChange={(e) => update('country', e.target.value)}>
                    {COUNTRIES.map((c) => <MenuItem key={c} value={c}>{c}</MenuItem>)}
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6} md={4}>
                <TextField fullWidth required type="number" label="Salary" value={form.salary}
                  onChange={(e) => update('salary', Number(e.target.value))} />
              </Grid>
              <Grid item xs={6} md={4}>
                <TextField fullWidth required label="Currency" value={form.currency}
                  onChange={(e) => update('currency', e.target.value.toUpperCase())} />
              </Grid>
              <Grid item xs={12} md={4}>
                <TextField fullWidth required type="date" label="Date of Joining"
                  InputLabelProps={{ shrink: true }} value={form.date_of_joining}
                  onChange={(e) => update('date_of_joining', e.target.value)} />
              </Grid>
              <Grid item xs={6} md={4}>
                <FormControl fullWidth>
                  <InputLabel>Employment Type</InputLabel>
                  <Select label="Employment Type" value={form.employment_type}
                    onChange={(e) => update('employment_type', e.target.value as EmploymentType)}>
                    <MenuItem value="full_time">Full Time</MenuItem>
                    <MenuItem value="part_time">Part Time</MenuItem>
                    <MenuItem value="contract">Contract</MenuItem>
                    <MenuItem value="intern">Intern</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={6} md={4}>
                <FormControl fullWidth>
                  <InputLabel>Status</InputLabel>
                  <Select label="Status" value={form.status}
                    onChange={(e) => update('status', e.target.value as EmployeeStatus)}>
                    <MenuItem value="active">Active</MenuItem>
                    <MenuItem value="inactive">Inactive</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth required label="Manager Name" value={form.manager_name}
                  onChange={(e) => update('manager_name', e.target.value)} />
              </Grid>
              <Grid item xs={12} md={6}>
                <TextField fullWidth label="City" value={form.city || ''}
                  onChange={(e) => update('city', e.target.value)} />
              </Grid>
            </Grid>
            <Box mt={3} display="flex" gap={2}>
              <Button type="submit" variant="contained" disabled={saving}>
                {saving ? 'Saving...' : 'Save'}
              </Button>
              <Button variant="outlined" onClick={() => navigate('/employees')}>
                Cancel
              </Button>
            </Box>
          </form>
        </CardContent>
      </Card>
    </Box>
  );
}

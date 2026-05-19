import { useEffect, useState } from 'react';
import { Link as RouterLink, useNavigate, useParams } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Grid,
  Typography,
} from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import { toast } from 'react-toastify';

import LoadingState from '../components/LoadingState';
import { employeeApi } from '../services/api';
import type { Employee } from '../types/employee';

function DetailRow({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <Grid item xs={12} sm={6}>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
      <Typography variant="body1" fontWeight={500}>
        {value}
      </Typography>
    </Grid>
  );
}

export default function EmployeeDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    employeeApi
      .get(Number(id))
      .then(setEmployee)
      .catch(() => toast.error('Employee not found'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) return <LoadingState />;
  if (!employee) return null;

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/employees')}>
          Back
        </Button>
        <Button
          variant="contained"
          startIcon={<EditIcon />}
          component={RouterLink}
          to={`/employees/${employee.id}/edit`}
        >
          Edit
        </Button>
      </Box>

      <Typography variant="h5" fontWeight={700} gutterBottom>
        {employee.full_name}
      </Typography>
      <Chip
        label={employee.status}
        color={employee.status === 'active' ? 'success' : 'default'}
        size="small"
        sx={{ mb: 2 }}
      />

      <Card>
        <CardContent>
          <Grid container spacing={3}>
            <DetailRow label="Employee ID" value={employee.employee_id} />
            <DetailRow label="Email" value={employee.email} />
            <DetailRow label="Phone" value={employee.phone_number} />
            <DetailRow label="Job Title" value={employee.job_title} />
            <DetailRow label="Department" value={employee.department} />
            <DetailRow label="Country" value={employee.country} />
            <DetailRow label="City" value={employee.city || '—'} />
            <DetailRow
              label="Salary"
              value={`${employee.currency} ${Number(employee.salary).toLocaleString()}`}
            />
            <DetailRow
              label="Bonus"
              value={
                employee.bonus
                  ? `${employee.currency} ${Number(employee.bonus).toLocaleString()}`
                  : '—'
              }
            />
            <DetailRow label="Manager" value={employee.manager_name} />
            <DetailRow label="Employment Type" value={employee.employment_type} />
            <DetailRow label="Date of Joining" value={employee.date_of_joining} />
            <DetailRow label="Experience (years)" value={employee.experience_years ?? '—'} />
            <DetailRow label="Gender" value={employee.gender || '—'} />
          </Grid>
        </CardContent>
      </Card>
    </Box>
  );
}

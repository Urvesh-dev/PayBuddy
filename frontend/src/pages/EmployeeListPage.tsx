import { useCallback, useEffect, useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Chip,
  FormControl,
  Grid,
  IconButton,
  InputLabel,
  MenuItem,
  Select,
  TextField,
  Tooltip,
  Typography,
} from '@mui/material';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import AddIcon from '@mui/icons-material/Add';
import DeleteOutlineIcon from '@mui/icons-material/DeleteOutline';
import EditOutlinedIcon from '@mui/icons-material/EditOutlined';
import VisibilityOutlinedIcon from '@mui/icons-material/VisibilityOutlined';
import { toast } from 'react-toastify';

import EmptyState from '../components/EmptyState';
import LoadingState from '../components/LoadingState';
import { employeeApi } from '../services/api';
import type { Employee, EmployeeFilters, FilterMetadata } from '../types/employee';
import { getApiErrorMessage } from '../utils/apiError';

export default function EmployeeListPage() {
  const navigate = useNavigate();
  const [rows, setRows] = useState<Employee[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [metadata, setMetadata] = useState<FilterMetadata | null>(null);
  const [filters, setFilters] = useState<EmployeeFilters>({
    page: 1,
    page_size: 20,
    sort_by: 'created_at',
    sort_order: 'desc',
  });
  const [search, setSearch] = useState('');
  const [paginationModel, setPaginationModel] = useState<GridPaginationModel>({
    page: 0,
    pageSize: 20,
  });

  const fetchEmployees = useCallback(async () => {
    setLoading(true);
    try {
      const data = await employeeApi.list({
        ...filters,
        search: search || undefined,
        page: paginationModel.page + 1,
        page_size: paginationModel.pageSize,
      });
      setRows(data.items);
      setTotal(data.total);
    } catch (err) {
      toast.error(getApiErrorMessage(err, 'Failed to load employees'));
    } finally {
      setLoading(false);
    }
  }, [filters, search, paginationModel]);

  useEffect(() => {
    employeeApi.metadata().then(setMetadata).catch(() => {});
  }, []);

  useEffect(() => {
    fetchEmployees();
  }, [fetchEmployees]);

  const handleDelete = async (id: number) => {
    if (!window.confirm('Delete this employee?')) return;
    try {
      await employeeApi.delete(id);
      toast.success('Employee deleted');
      fetchEmployees();
    } catch {
      toast.error('Failed to delete employee');
    }
  };

  const columns: GridColDef[] = [
    { field: 'employee_id', headerName: 'ID', width: 110 },
    { field: 'full_name', headerName: 'Name', flex: 1, minWidth: 160 },
    { field: 'email', headerName: 'Email', flex: 1, minWidth: 180 },
    { field: 'job_title', headerName: 'Title', width: 160 },
    { field: 'department', headerName: 'Dept', width: 130 },
    { field: 'country', headerName: 'Country', width: 130 },
    {
      field: 'salary',
      headerName: 'Salary',
      width: 120,
      valueFormatter: (v, row) =>
        `${row.currency} ${Number(v).toLocaleString()}`,
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value}
          size="small"
          color={params.value === 'active' ? 'success' : 'default'}
        />
      ),
    },
    {
      field: 'actions',
      headerName: 'Actions',
      width: 140,
      minWidth: 140,
      maxWidth: 140,
      sortable: false,
      filterable: false,
      disableColumnMenu: true,
      align: 'center',
      headerAlign: 'center',
      renderCell: (params) => (
        <Box display="flex" alignItems="center" justifyContent="center" gap={0.5} width="100%">
          <Tooltip title="View">
            <IconButton
              size="small"
              aria-label="View employee"
              onClick={() => navigate(`/employees/${params.row.id}`)}
            >
              <VisibilityOutlinedIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Edit">
            <IconButton
              size="small"
              aria-label="Edit employee"
              onClick={() => navigate(`/employees/${params.row.id}/edit`)}
            >
              <EditOutlinedIcon fontSize="small" />
            </IconButton>
          </Tooltip>
          <Tooltip title="Delete">
            <IconButton
              size="small"
              color="error"
              aria-label="Delete employee"
              onClick={() => handleDelete(params.row.id)}
            >
              <DeleteOutlineIcon fontSize="small" />
            </IconButton>
          </Tooltip>
        </Box>
      ),
    },
  ];

  return (
    <Box>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h5" fontWeight={700}>
          Employees
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          component={RouterLink}
          to="/employees/new"
        >
          Add Employee
        </Button>
      </Box>

      <Grid container spacing={2} mb={2}>
        <Grid item xs={12} md={3}>
          <TextField
            fullWidth
            size="small"
            label="Search"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && fetchEmployees()}
          />
        </Grid>
        <Grid item xs={6} md={2}>
          <FormControl fullWidth size="small">
            <InputLabel>Country</InputLabel>
            <Select
              label="Country"
              value={filters.country || ''}
              onChange={(e) => setFilters((f) => ({ ...f, country: e.target.value || undefined }))}
            >
              <MenuItem value="">All</MenuItem>
              {metadata?.countries.map((c) => (
                <MenuItem key={c} value={c}>
                  {c}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6} md={2}>
          <FormControl fullWidth size="small">
            <InputLabel>Department</InputLabel>
            <Select
              label="Department"
              value={filters.department || ''}
              onChange={(e) =>
                setFilters((f) => ({ ...f, department: e.target.value || undefined }))
              }
            >
              <MenuItem value="">All</MenuItem>
              {metadata?.departments.map((d) => (
                <MenuItem key={d} value={d}>
                  {d}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6} md={2}>
          <FormControl fullWidth size="small">
            <InputLabel>Status</InputLabel>
            <Select
              label="Status"
              value={filters.status || ''}
              onChange={(e) =>
                setFilters((f) => ({
                  ...f,
                  status: (e.target.value as Employee['status']) || undefined,
                }))
              }
            >
              <MenuItem value="">All</MenuItem>
              <MenuItem value="active">Active</MenuItem>
              <MenuItem value="inactive">Inactive</MenuItem>
            </Select>
          </FormControl>
        </Grid>
        <Grid item xs={6} md={3}>
          <Button variant="outlined" onClick={fetchEmployees} sx={{ mr: 1 }}>
            Apply Filters
          </Button>
          <Button
            variant="text"
            onClick={() => {
              setFilters({ page: 1, page_size: 20 });
              setSearch('');
            }}
          >
            Reset
          </Button>
        </Grid>
      </Grid>

      {loading ? (
        <LoadingState message="Loading employees..." />
      ) : rows.length === 0 ? (
        <EmptyState title="No employees found" description="Try adjusting filters or add a new employee." />
      ) : (
        <DataGrid
          rows={rows}
          columns={columns}
          getRowId={(r) => r.id}
          rowCount={total}
          paginationMode="server"
          paginationModel={paginationModel}
          onPaginationModelChange={setPaginationModel}
          pageSizeOptions={[10, 20, 50]}
          autoHeight
          disableRowSelectionOnClick
          sx={{
            bgcolor: 'background.paper',
            border: 1,
            borderColor: 'divider',
            '& .MuiDataGrid-columnHeaders': { bgcolor: 'grey.50' },
            '& .actions-cell': { overflow: 'visible !important' },
          }}
          getCellClassName={(params) =>
            params.field === 'actions' ? 'actions-cell' : ''
          }
        />
      )}
    </Box>
  );
}

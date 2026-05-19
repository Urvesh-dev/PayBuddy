import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
} from '@mui/material';
import { toast } from 'react-toastify';

import { useAuthStore } from '../store/authStore';

export default function LoginPage() {
  const [email, setEmail] = useState('hr@paybuddy.com');
  const [password, setPassword] = useState('password');
  const login = useAuthStore((s) => s.login);
  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (login(email, password)) {
      toast.success('Welcome back!');
      navigate('/employees');
    } else {
      toast.error('Invalid credentials');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        background: 'linear-gradient(135deg, #1565C0 0%, #00897B 100%)',
      }}
    >
      <Container maxWidth="sm">
        <Card elevation={4}>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h4" fontWeight={700} gutterBottom color="primary">
              PayBuddy
            </Typography>
            <Typography variant="body1" color="text.secondary" mb={3}>
              HR Salary Management — sign in with any email (mock auth)
            </Typography>
            <form onSubmit={handleSubmit}>
              <TextField
                fullWidth
                label="Email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                margin="normal"
                required
              />
              <TextField
                fullWidth
                label="Password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                margin="normal"
                required
              />
              <Button type="submit" fullWidth variant="contained" size="large" sx={{ mt: 3 }}>
                Sign In
              </Button>
            </form>
          </CardContent>
        </Card>
      </Container>
    </Box>
  );
}

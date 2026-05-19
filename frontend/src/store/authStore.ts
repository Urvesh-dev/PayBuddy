import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface AuthState {
  isAuthenticated: boolean;
  userName: string;
  login: (email: string, password: string) => boolean;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      isAuthenticated: false,
      userName: '',
      login: (email: string, _password: string) => {
        if (email.trim()) {
          set({ isAuthenticated: true, userName: email.split('@')[0] || 'HR Manager' });
          return true;
        }
        return false;
      },
      logout: () => set({ isAuthenticated: false, userName: '' }),
    }),
    { name: 'paybuddy-auth' },
  ),
);

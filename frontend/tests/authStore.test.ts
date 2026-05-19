import { beforeEach, describe, expect, it } from 'vitest';

import { useAuthStore } from '../store/authStore';

describe('authStore', () => {
  beforeEach(() => {
    useAuthStore.setState({ isAuthenticated: false, userName: '' });
  });

  it('logs in with valid email', () => {
    const result = useAuthStore.getState().login('hr@paybuddy.com', 'secret');
    expect(result).toBe(true);
    expect(useAuthStore.getState().isAuthenticated).toBe(true);
    expect(useAuthStore.getState().userName).toBe('hr');
  });

  it('logs out', () => {
    useAuthStore.getState().login('hr@paybuddy.com', 'secret');
    useAuthStore.getState().logout();
    expect(useAuthStore.getState().isAuthenticated).toBe(false);
  });
});

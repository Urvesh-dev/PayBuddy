import axios from 'axios';

/** Extract a human-readable message from FastAPI / axios errors. */
export function getApiErrorMessage(err: unknown, fallback: string): string {
  if (!axios.isAxiosError(err)) {
    return fallback;
  }

  const detail = err.response?.data?.detail;
  if (typeof detail === 'string') {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === 'object' && item !== null && 'msg' in item) {
          const loc = 'loc' in item && Array.isArray(item.loc) ? item.loc.join('.') : 'field';
          return `${loc}: ${String(item.msg)}`;
        }
        return String(item);
      })
      .join('; ');
  }
  return fallback;
}

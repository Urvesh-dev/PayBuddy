import { Box, Typography } from '@mui/material';
import InboxIcon from '@mui/icons-material/Inbox';

interface Props {
  title: string;
  description?: string;
}

export default function EmptyState({ title, description }: Props) {
  return (
    <Box textAlign="center" py={8}>
      <InboxIcon sx={{ fontSize: 48, color: 'text.disabled', mb: 2 }} />
      <Typography variant="h6">{title}</Typography>
      {description && (
        <Typography variant="body2" color="text.secondary" mt={1}>
          {description}
        </Typography>
      )}
    </Box>
  );
}

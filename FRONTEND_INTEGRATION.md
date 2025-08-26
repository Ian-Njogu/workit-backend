# Frontend Integration Plan

This document outlines the step-by-step plan for migrating the frontend from MSW mocks to the real Django backend API.

## Overview

The integration will be done gradually, page by page, while keeping MSW as a fallback until each page is fully tested and verified. This approach ensures a smooth transition without breaking existing functionality.

## Environment Configuration

### Frontend Environment Variables

Add these to your frontend `.env` file:

```bash
# API Configuration
VITE_API_URL=http://localhost:8000
VITE_USE_REAL_API=true

# Fallback Configuration (optional)
VITE_MSW_FALLBACK=true
```

### Backend Environment Variables

Ensure your backend `.env` has:

```bash
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## API Client Setup

### Axios Configuration

Create or update your API client configuration:

```typescript
// src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add JWT token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${import.meta.env.VITE_API_URL}/api/auth/refresh`, {
          refresh: refreshToken,
        });

        const { access } = response.data;
        localStorage.setItem('access_token', access);

        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, redirect to login
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

## Migration Steps

### Phase 1: Authentication & User Management

**Files to modify:**
- `src/features/auth/` - Login, registration, user context
- `src/lib/api.ts` - API client setup

**Changes:**
1. Replace MSW auth endpoints with real API calls
2. Update user context to use real JWT tokens
3. Implement token refresh logic
4. Update login/logout flows

**MSW Fallback:** Keep MSW enabled for auth until fully tested

**Expected Response Shapes:**
```typescript
// Login Response
interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: number;
    email: string;
    name: string;
    role: 'client' | 'worker';
  };
}

// User Context
interface User {
  id: number;
  email: string;
  name: string;
  role: 'client' | 'worker';
}
```

### Phase 2: Workers List & Detail

**Files to modify:**
- `src/features/workers/` - Workers list, worker detail
- `src/pages/workers/` - Workers pages

**Changes:**
1. Replace MSW worker endpoints with real API calls
2. Update filtering and pagination to use real API
3. Handle real API response formats

**MSW Fallback:** Disable MSW for workers after testing

**API Endpoints:**
- `GET /api/workers/` - List workers with filtering
- `GET /api/workers/{id}/` - Worker details

**Expected Response Shapes:**
```typescript
// Workers List Response
interface WorkersResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<{
    id: number;
    user: {
      id: number;
      email: string;
      name: string;
      role: string;
    };
    category: string;
    location: string;
    hourly_rate: string;
    rating: string;
    review_count: number;
    available: boolean;
  }>;
}

// Worker Detail Response
interface WorkerDetailResponse {
  id: number;
  user: User;
  category: string;
  location: string;
  hourly_rate: string;
  rating: string;
  review_count: number;
  skills: string[];
  portfolio: string[];
  available: boolean;
}
```

### Phase 3: Job Creation & Management

**Files to modify:**
- `src/features/jobs/` - Job creation, job management
- `src/pages/jobs/` - Job pages

**Changes:**
1. Replace MSW job endpoints with real API calls
2. Update job creation form to use real API
3. Implement real job status updates
4. Handle real job filtering

**MSW Fallback:** Disable MSW for jobs after testing

**API Endpoints:**
- `POST /api/jobs/` - Create job
- `GET /api/jobs/?client_id={id}` - List client's jobs
- `PATCH /api/jobs/{id}/` - Update job status

**Expected Response Shapes:**
```typescript
// Job Creation Request
interface CreateJobRequest {
  title: string;
  category: string;
  description: string;
  location: string;
  budget: string;
  deadline?: string;
  invited_worker_id?: number;
}

// Job Response
interface JobResponse {
  id: number;
  client: User;
  worker: User | null;
  title: string;
  category: string;
  description: string;
  location: string;
  budget: string;
  deadline: string | null;
  status: 'pending' | 'accepted' | 'in_progress' | 'completed' | 'cancelled';
  created_at: string;
}
```

### Phase 4: Job Feed & Applications

**Files to modify:**
- `src/features/applications/` - Job applications
- `src/pages/feed/` - Job feed page

**Changes:**
1. Replace MSW feed endpoints with real API calls
2. Update application submission to use real API
3. Implement real job filtering in feed
4. Handle real application responses

**MSW Fallback:** Disable MSW for feed after testing

**API Endpoints:**
- `GET /api/jobs/feed/` - Job feed for workers
- `POST /api/jobs/{id}/applications/` - Apply to job

**Expected Response Shapes:**
```typescript
// Job Feed Response
interface JobFeedResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<{
    id: number;
    client: User;
    title: string;
    category: string;
    description: string;
    location: string;
    budget: string;
    deadline: string | null;
    status: string;
    created_at: string;
  }>;
}

// Application Creation Request
interface CreateApplicationRequest {
  message: string;
  quote: string;
}
```

### Phase 5: Client Dashboard & Application Management

**Files to modify:**
- `src/features/applications/` - Application management
- `src/pages/dashboard/` - Client dashboard

**Changes:**
1. Replace MSW application endpoints with real API calls
2. Update application listing to use real API
3. Implement real accept/reject functionality
4. Handle real application status updates

**MSW Fallback:** Disable MSW for applications after testing

**API Endpoints:**
- `GET /api/applications/?client_id={id}` - List applications to client's jobs
- `POST /api/applications/{id}/accept/` - Accept application
- `POST /api/applications/{id}/reject/` - Reject application

**Expected Response Shapes:**
```typescript
// Applications List Response
interface ApplicationsResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Array<{
    id: number;
    worker: User;
    job: {
      id: number;
      title: string;
      category: string;
      location: string;
    };
    message: string;
    quote: string;
    status: 'pending' | 'accepted' | 'rejected';
    created_at: string;
    worker_name: string;
    job_title: string;
    job_category: string;
    job_location: string;
  }>;
}
```

### Phase 6: Worker Dashboard & Job Management

**Files to modify:**
- `src/features/jobs/` - Worker job management
- `src/pages/dashboard/` - Worker dashboard

**Changes:**
1. Replace MSW worker job endpoints with real API calls
2. Update job status management to use real API
3. Implement real job filtering for workers
4. Handle real job assignment responses

**MSW Fallback:** Disable MSW for worker jobs after testing

**API Endpoints:**
- `GET /api/jobs/?worker_id={id}` - List worker's assigned jobs
- `PATCH /api/jobs/{id}/` - Update job status (worker)

## Testing Strategy

### For Each Phase:

1. **Enable real API** for the specific feature
2. **Test all functionality** with real backend
3. **Verify error handling** (network errors, validation errors)
4. **Test edge cases** (empty responses, pagination, filtering)
5. **Verify MSW fallback** still works if needed
6. **Disable MSW** for the feature once fully tested

### Testing Checklist:

- [ ] API calls work correctly
- [ ] Error handling works as expected
- [ ] Loading states work properly
- [ ] Pagination works correctly
- [ ] Filtering works correctly
- [ ] Real-time updates work
- [ ] JWT authentication works
- [ ] Token refresh works
- [ ] Logout works correctly

## Error Handling

### Network Errors
```typescript
try {
  const response = await api.get('/api/workers/');
  // Handle success
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.response?.status === 401) {
      // Handle unauthorized
    } else if (error.response?.status === 400) {
      // Handle validation errors
    } else if (error.code === 'NETWORK_ERROR') {
      // Handle network errors
    }
  }
}
```

### Validation Errors
```typescript
// Backend validation error response
interface ValidationError {
  field_name: string[];
}

// Frontend error handling
if (error.response?.status === 400) {
  const validationErrors = error.response.data;
  // Display validation errors to user
}
```

## Performance Considerations

### API Optimization
- Use `select_related` and `prefetch_related` in backend
- Implement proper pagination
- Use efficient filtering

### Frontend Optimization
- Implement proper loading states
- Use React Query or SWR for caching
- Implement optimistic updates where appropriate

## Rollback Plan

If issues arise during migration:

1. **Immediate rollback**: Set `VITE_USE_REAL_API=false`
2. **Investigate issues** with backend team
3. **Fix backend issues** and retest
4. **Gradually re-enable** real API

## Success Criteria

Migration is complete when:

- [ ] All pages work with real API
- [ ] MSW is completely disabled
- [ ] All functionality works as expected
- [ ] Performance is acceptable
- [ ] Error handling is robust
- [ ] Authentication flow is smooth
- [ ] All edge cases are handled

## Timeline

- **Phase 1**: 1-2 days (Authentication)
- **Phase 2**: 1-2 days (Workers)
- **Phase 3**: 2-3 days (Jobs)
- **Phase 4**: 2-3 days (Feed & Applications)
- **Phase 5**: 2-3 days (Client Dashboard)
- **Phase 6**: 2-3 days (Worker Dashboard)

**Total estimated time**: 10-16 days

## Notes

- Keep MSW enabled until each phase is fully tested
- Test thoroughly in development before moving to staging
- Coordinate with backend team for any API changes
- Document any deviations from expected response shapes
- Monitor performance and error rates during migration

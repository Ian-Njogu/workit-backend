import { http, HttpResponse } from 'msw'


// Categories of services workers can provide
const categories = [
  { id: 1, name: 'Plumbing', icon: '🔧' },
  { id: 2, name: 'Cleaning', icon: '🧹' },
  { id: 3, name: 'Electrical', icon: '⚡' },
  { id: 4, name: 'Carpentry', icon: '🔨' },
  { id: 5, name: 'Painting', icon: '🎨' },
  { id: 6, name: 'Gardening', icon: '🌱' },
  { id: 7, name: 'Moving', icon: '📦' },
  { id: 8, name: 'General Labor', icon: '👷' }
]

// Worker profiles with detailed info
const workers = [
  {
    id: 1,
    name: 'John Mwangi',
    category: 'Plumbing',
    categoryId: 1,
    location: 'Nairobi West',
    hourlyRate: 800,
    rating: 4.8,
    reviewCount: 24,
    skills: ['Pipe fitting', 'Drainage', 'Water heater installation'],
    experience: '5 years',
    available: true,
    // Example portfolio projects
    portfolio: [
      { id: 1, title: 'Kitchen Sink Installation', description: 'Complete kitchen sink and drainage system installation', image: 'https://via.placeholder.com/300x200' },
      { id: 2, title: 'Bathroom Renovation', description: 'Full bathroom plumbing renovation', image: 'https://via.placeholder.com/300x200' }
    ],
    // Client reviews
    reviews: [
      { id: 1, client: 'Sarah K.', rating: 5, comment: 'Excellent work, very professional and clean.', date: '2024-01-15' },
      { id: 2, client: 'Mike O.', rating: 4, comment: 'Good quality work, arrived on time.', date: '2024-01-10' }
    ]
  },
  {
    id: 2,
    name: 'Mary Wanjiku',
    category: 'Cleaning',
    categoryId: 2,
    location: 'Nairobi Central',
    hourlyRate: 500,
    rating: 4.9,
    reviewCount: 31,
    skills: ['Deep cleaning', 'Window cleaning', 'Carpet cleaning'],
    experience: '3 years',
    available: true,
    portfolio: [
      { id: 3, title: 'Office Deep Clean', description: 'Complete office cleaning and sanitization', image: 'https://via.placeholder.com/300x200' }
    ],
    reviews: [
      { id: 3, client: 'Jane D.', rating: 5, comment: 'Very thorough and professional cleaning service.', date: '2024-01-12' }
    ]
  },
  {
    id: 3,
    name: 'Peter Kamau',
    category: 'Electrical',
    categoryId: 3,
    location: 'Nairobi East',
    hourlyRate: 1000,
    rating: 4.7,
    reviewCount: 18,
    skills: ['Wiring', 'Lighting installation', 'Electrical repairs'],
    experience: '7 years',
    available: false,
    portfolio: [
      { id: 4, title: 'House Wiring', description: 'Complete electrical wiring for new house', image: 'https://via.placeholder.com/300x200' }
    ],
    reviews: [
      { id: 4, client: 'David M.', rating: 5, comment: 'Professional electrician, highly recommended.', date: '2024-01-08' }
    ]
  }
]

// Jobs posted by clients and assigned to workers
const jobs = [
  {
    id: 1,
    clientId: 1,
    workerId: 1,
    title: 'Fix leaking kitchen sink',
    description: 'Kitchen sink is leaking from the base, need urgent repair',
    category: 'Plumbing',
    location: 'Nairobi West',
    budget: 2000,
    deadline: '2024-02-01T16:00:00Z',
    status: 'in_progress',
    createdAt: '2024-01-15T10:00:00Z',
    scheduledDate: '2024-01-16T14:00:00Z'
  },
  {
    id: 2,
    clientId: 1,
    workerId: 2,
    title: 'Deep clean apartment',
    description: 'Need deep cleaning for 2-bedroom apartment before moving out',
    category: 'Cleaning',
    location: 'Nairobi Central',
    budget: 3000,
    deadline: '2024-01-12T12:00:00Z',
    status: 'completed',
    createdAt: '2024-01-10T09:00:00Z',
    completedDate: '2024-01-12T16:00:00Z'
  }
]

// Applications to jobs by workers
const applications = [
]

// Reviews left after job completion
const reviews = [
]


// These are mock API endpoints used with MSW (Mock Service Worker)

export const handlers = [
  // Get all categories
  http.get('/api/v1/categories', () => {
    return HttpResponse.json(categories)
  }),

  // Get all workers with optional filtering and pagination
  http.get('/api/v1/workers', ({ request }) => {
    const url = new URL(request.url)
    const category = url.searchParams.get('category')  // filter by category
    const location = url.searchParams.get('location')  // filter by location
    const page = parseInt(url.searchParams.get('page') || '1') // pagination
    const limit = parseInt(url.searchParams.get('limit') || '10')
    
    let filteredWorkers = [...workers]
    
    // Apply category filter
    if (category) {
      filteredWorkers = filteredWorkers.filter(w => w.category === category)
    }
    
    // Apply location filter
    if (location) {
      filteredWorkers = filteredWorkers.filter(w => w.location.includes(location))
    }
    
    // Paginate workers
    const start = (page - 1) * limit
    const end = start + limit
    const paginatedWorkers = filteredWorkers.slice(start, end)
    
    return HttpResponse.json({
      workers: paginatedWorkers,
      pagination: {
        page,
        limit,
        total: filteredWorkers.length,
        totalPages: Math.ceil(filteredWorkers.length / limit)
      }
    })
  }),

  // Get a single worker by ID
  http.get('/api/v1/workers/:id', ({ params }) => {
    const worker = workers.find(w => w.id === parseInt(params.id))
    if (!worker) {
      return new HttpResponse(null, { status: 404 })
    }
    return HttpResponse.json(worker)
  }),

  // Mock authentication endpoint (login)
  http.post('/api/v1/auth/login', async ({ request }) => {
    const { email, password, role } = await request.json()
    
    // Accept any email/password for testing
    if (email && password) {
      return HttpResponse.json({
        accessToken: 'mock-jwt-token-' + Date.now(),
        user: {
          id: 1,
          email,
          name: 'Test User',
          role: role === 'worker' ? 'worker' : 'client'
        }
      })
    }
    
    // If missing credentials → unauthorized
    return new HttpResponse(null, { status: 401 })
  }),

  // Create a new job
  http.post('/api/v1/jobs', async ({ request }) => {
    const jobData = await request.json()
    const newJob = {
      id: jobs.length + 1,
      ...jobData,
      status: 'pending',
      createdAt: new Date().toISOString()
    }
    jobs.push(newJob)
    return HttpResponse.json(newJob, { status: 201 })
  }),

  // Get all jobs (or jobs by client ID, or worker feed)
  http.get('/api/v1/jobs', ({ request }) => {
    const url = new URL(request.url)
    const clientId = url.searchParams.get('client_id')
    const feedForWorkerId = url.searchParams.get('feed_for_worker_id')

    if (clientId) {
      const clientJobs = jobs.filter(job => job.clientId === parseInt(clientId))
      return HttpResponse.json(clientJobs)
    }

    if (feedForWorkerId) {
      const workerId = parseInt(feedForWorkerId)
      const worker = workers.find(w => w.id === workerId)
      if (!worker) {
        return HttpResponse.json([])
      }
      const feed = jobs.filter(j => 
        j.status === 'pending' &&
        j.category === worker.category &&
        j.location.includes(worker.location.split(' ')[0])
      )
      return HttpResponse.json(feed)
    }
    
    return HttpResponse.json(jobs)
  }),

  // Update a job (PATCH request)
  http.patch('/api/v1/jobs/:id', async ({ params, request }) => {
    const jobId = parseInt(params.id)
    const job = jobs.find(j => j.id === jobId)
    
    if (!job) {
      return new HttpResponse(null, { status: 404 })
    }
    
    // Merge updates into job object
    const updates = await request.json()
    Object.assign(job, updates)
    
    return HttpResponse.json(job)
  }),

  // List applications (optionally by client_id or job_id)
  http.get('/api/v1/applications', ({ request }) => {
    const url = new URL(request.url)
    const clientId = url.searchParams.get('client_id')
    const jobId = url.searchParams.get('job_id')

    let result = [...applications]
    if (jobId) {
      result = result.filter(a => a.jobId === parseInt(jobId))
    }
    if (clientId) {
      const clientJobIds = jobs.filter(j => j.clientId === parseInt(clientId)).map(j => j.id)
      result = result.filter(a => clientJobIds.includes(a.jobId))
    }
    // hydrate simple job fields for convenience
    const hydrated = result.map(a => {
      const job = jobs.find(j => j.id === a.jobId)
      const worker = workers.find(w => w.id === a.workerId)
      return { ...a, jobTitle: job?.title, jobCategory: job?.category, jobLocation: job?.location, workerName: worker?.name }
    })
    return HttpResponse.json(hydrated)
  }),

  // Worker applies to a job
  http.post('/api/v1/jobs/:id/applications', async ({ params, request }) => {
    const jobId = parseInt(params.id)
    const job = jobs.find(j => j.id === jobId)
    if (!job) {
      return new HttpResponse(null, { status: 404 })
    }
    const body = await request.json()
    const app = {
      id: applications.length + 1,
      jobId,
      workerId: body.workerId,
      message: body.message,
      quote: body.quote,
      status: 'pending',
      createdAt: new Date().toISOString()
    }
    applications.push(app)
    return HttpResponse.json(app, { status: 201 })
  }),

  // Client invites a worker to a job
  http.post('/api/v1/jobs/:id/invitations', async ({ params, request }) => {
    const jobId = parseInt(params.id)
    const job = jobs.find(j => j.id === jobId)
    if (!job) {
      return new HttpResponse(null, { status: 404 })
    }
    const { workerId } = await request.json()
    job.invitedWorkerId = workerId
    return HttpResponse.json(job)
  }),

  // Client accepts an application (assign worker and move to accepted)
  http.post('/api/v1/applications/:id/accept', ({ params }) => {
    const appId = parseInt(params.id)
    const app = applications.find(a => a.id === appId)
    if (!app) {
      return new HttpResponse(null, { status: 404 })
    }
    app.status = 'accepted'
    const job = jobs.find(j => j.id === app.jobId)
    if (job) {
      job.workerId = app.workerId
      job.status = 'accepted'
    }
    return HttpResponse.json(app)
  }),

  // Client rejects an application
  http.post('/api/v1/applications/:id/reject', ({ params }) => {
    const appId = parseInt(params.id)
    const app = applications.find(a => a.id === appId)
    if (!app) {
      return new HttpResponse(null, { status: 404 })
    }
    app.status = 'rejected'
    return HttpResponse.json(app)
  }),

  // List jobs assigned to a worker
  http.get('/api/v1/worker/:id/jobs', ({ params }) => {
    const workerId = parseInt(params.id)
    const assigned = jobs.filter(j => j.workerId === workerId)
    return HttpResponse.json(assigned)
  }),

  // Post a review
  http.post('/api/v1/reviews', async ({ request }) => {
    const body = await request.json()
    const review = { id: reviews.length + 1, ...body, createdAt: new Date().toISOString() }
    reviews.push(review)
    return HttpResponse.json(review, { status: 201 })
  })
]

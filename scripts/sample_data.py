#!/usr/bin/env python
"""
Sample data script for JobBoard backend.
Run this after migrations to populate the database with test data.
"""

import os
import sys
import django
from decimal import Decimal

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jobboard_backend.settings')
django.setup()

from apps.users.models import User
from apps.workers.models import WorkerProfile
from apps.jobs.models import Job
from apps.applications.models import Application

def create_sample_data():
    """Create sample users, workers, jobs, and applications."""
    
    print("Creating sample data...")
    
    # Create sample users
    print("Creating users...")
    
    # Clients
    client1 = User.objects.create_user(
        email='john.client@example.com',
        password='password123',
        name='John Client',
        role='client'
    )
    
    client2 = User.objects.create_user(
        email='sarah.client@example.com',
        password='password123',
        name='Sarah Client',
        role='client'
    )
    
    # Workers
    worker1 = User.objects.create_user(
        email='jane.worker@example.com',
        password='password123',
        name='Jane Worker',
        role='worker'
    )
    
    worker2 = User.objects.create_user(
        email='mike.worker@example.com',
        password='password123',
        name='Mike Worker',
        role='worker'
    )
    
    worker3 = User.objects.create_user(
        email='alice.worker@example.com',
        password='password123',
        name='Alice Worker',
        role='worker'
    )
    
    print(f"Created {User.objects.count()} users")
    
    # Create worker profiles
    print("Creating worker profiles...")
    
    WorkerProfile.objects.create(
        user=worker1,
        category='Web Development',
        location='Remote',
        hourly_rate=Decimal('50.00'),
        rating=Decimal('4.8'),
        review_count=12,
        skills=['React', 'Node.js', 'Python', 'Django'],
        portfolio=['https://portfolio1.com', 'https://project2.com'],
        available=True
    )
    
    WorkerProfile.objects.create(
        user=worker2,
        category='Graphic Design',
        location='New York',
        hourly_rate=Decimal('45.00'),
        rating=Decimal('4.6'),
        review_count=8,
        skills=['Photoshop', 'Illustrator', 'InDesign', 'UI/UX'],
        portfolio=['https://design1.com', 'https://design2.com'],
        available=True
    )
    
    WorkerProfile.objects.create(
        user=worker3,
        category='Mobile Development',
        location='San Francisco',
        hourly_rate=Decimal('60.00'),
        rating=Decimal('4.9'),
        review_count=15,
        skills=['React Native', 'iOS', 'Android', 'Flutter'],
        portfolio=['https://mobile1.com', 'https://mobile2.com'],
        available=True
    )
    
    print(f"Created {WorkerProfile.objects.count()} worker profiles")
    
    # Create sample jobs
    print("Creating jobs...")
    
    job1 = Job.objects.create(
        client=client1,
        title='Website Development for E-commerce',
        category='Web Development',
        description='Need a modern e-commerce website built with React and Node.js. Should include user authentication, product catalog, shopping cart, and payment integration.',
        location='Remote',
        budget=Decimal('8000.00'),
        deadline='2024-03-01',
        status='pending'
    )
    
    job2 = Job.objects.create(
        client=client2,
        title='Logo and Brand Identity Design',
        category='Graphic Design',
        description='Looking for a professional logo design and complete brand identity package including business cards, letterhead, and social media templates.',
        location='Remote',
        budget=Decimal('2000.00'),
        deadline='2024-02-15',
        status='pending'
    )
    
    job3 = Job.objects.create(
        client=client1,
        title='Mobile App for Food Delivery',
        category='Mobile Development',
        description='Need a mobile app for food delivery service with features like user registration, restaurant listings, order placement, and real-time tracking.',
        location='Remote',
        budget=Decimal('15000.00'),
        deadline='2024-04-01',
        status='pending'
    )
    
    print(f"Created {Job.objects.count()} jobs")
    
    # Create sample applications
    print("Creating applications...")
    
    Application.objects.create(
        job=job1,
        worker=worker1,
        message='I have extensive experience building e-commerce websites. I can deliver a modern, responsive design with all the features you need. My portfolio includes several successful e-commerce projects.',
        quote=Decimal('7500.00'),
        status='pending'
    )
    
    Application.objects.create(
        job=job1,
        worker=worker3,
        message='While I specialize in mobile development, I also have strong web development skills. I can build a fast, scalable e-commerce platform using modern technologies.',
        quote=Decimal('7800.00'),
        status='pending'
    )
    
    Application.objects.create(
        job=job2,
        worker=worker2,
        message='I specialize in brand identity design and have created logos for many successful businesses. I can deliver a professional, memorable brand that represents your company well.',
        quote=Decimal('1800.00'),
        status='pending'
    )
    
    Application.objects.create(
        job=job3,
        worker=worker3,
        message='I have built several food delivery apps and understand the unique challenges of this industry. I can deliver a user-friendly app with all the features you need.',
        quote=Decimal('14000.00'),
        status='pending'
    )
    
    print(f"Created {Application.objects.count()} applications")
    
    print("\nSample data created successfully!")
    print("\nSample users:")
    print(f"  Client: {client1.email} (password: password123)")
    print(f"  Client: {client2.email} (password: password123)")
    print(f"  Worker: {worker1.email} (password: password123)")
    print(f"  Worker: {worker2.email} (password: password123)")
    print(f"  Worker: {worker3.email} (password: password123)")

def clear_sample_data():
    """Clear all sample data from the database."""
    print("Clearing sample data...")
    
    Application.objects.all().delete()
    Job.objects.all().delete()
    WorkerProfile.objects.all().delete()
    User.objects.filter(role__in=['client', 'worker']).delete()
    
    print("Sample data cleared!")

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage sample data for JobBoard backend')
    parser.add_argument('action', choices=['create', 'clear'], help='Action to perform')
    
    args = parser.parse_args()
    
    if args.action == 'create':
        create_sample_data()
    elif args.action == 'clear':
        clear_sample_data()

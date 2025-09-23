from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from .models import Category, Project, ProjectImage, ProjectStat, ProjectTimeline


class PortfolioModelsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.category = Category.objects.create(name='Test Category')
        self.project = Project.objects.create(
            title='Test Project',
            description='Test description',
            category=self.category,
            year=2024,
            location='Test Location',
            size='100 m²',
            duration='6 Months',
            completion_date=date(2024, 12, 31),
            lead_architect='Test Architect',
            status='planned',
            featured=True
        )

    def test_category_creation(self):
        """Test category model creation"""
        self.assertEqual(self.category.name, 'Test Category')
        self.assertEqual(self.category.slug, 'test-category')

    def test_project_creation(self):
        """Test project model creation"""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.category, self.category)
        self.assertTrue(self.project.featured)
        self.assertEqual(str(self.project), 'Test Project (2024)')

    def test_project_absolute_url(self):
        """Test project get_absolute_url method"""
        expected_url = f'/portfolio/{self.project.id}/'
        self.assertEqual(self.project.get_absolute_url(), expected_url)

    def test_project_stats(self):
        """Test project stats relationship"""
        stat = ProjectStat.objects.create(
            project=self.project,
            label='Test Stat',
            value='Test Value',
            order=1
        )
        self.assertEqual(self.project.stats.count(), 1)
        self.assertEqual(stat.project, self.project)

    def test_project_timeline(self):
        """Test project timeline relationship"""
        timeline = ProjectTimeline.objects.create(
            project=self.project,
            title='Test Milestone',
            date=date(2024, 6, 1),
            description='Test milestone description',
            completed=True,
            order=1
        )
        self.assertEqual(self.project.timeline.count(), 1)
        self.assertEqual(timeline.project, self.project)


class PortfolioViewsTest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.project = Project.objects.create(
            title='Test Project',
            description='Test description',
            category=self.category,
            year=2024,
            location='Test Location',
            size='100 m²',
            duration='6 Months',
            completion_date=date(2024, 12, 31),
            lead_architect='Test Architect',
            status='completed',
            featured=True
        )

    def test_project_list_view(self):
        """Test project list view"""
        url = reverse('portfolio:project_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Our Projects')

    def test_project_detail_view(self):
        """Test project detail view"""
        url = reverse('portfolio:project_detail', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'Test description')

    def test_project_detail_not_found(self):
        """Test project detail view with non-existent project"""
        url = reverse('portfolio:project_detail', kwargs={'project_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_project_list_filtering(self):
        """Test project list filtering"""
        # Test year filter
        url = reverse('portfolio:project_list')
        response = self.client.get(url, {'year': '2024'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

        # Test category filter
        response = self.client.get(url, {'category': 'test-category'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

        # Test featured filter
        response = self.client.get(url, {'category': 'featured'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

        # Test search
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')

    def test_project_list_empty_results(self):
        """Test project list with no matching results"""
        url = reverse('portfolio:project_list')
        response = self.client.get(url, {'search': 'NonExistentProject'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No Projects Found')


class PortfolioAPITest(TestCase):
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.project = Project.objects.create(
            title='Test Project',
            description='Test description',
            category=self.category,
            year=2024,
            location='Test Location',
            size='100 m²',
            duration='6 Months',
            completion_date=date(2024, 12, 31),
            lead_architect='Test Architect',
            status='completed',
            featured=True
        )

    def test_project_list_api(self):
        """Test project list API endpoint"""
        url = reverse('portfolio:project_list_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['projects']), 1)
        self.assertEqual(data['projects'][0]['title'], 'Test Project')

    def test_project_detail_api(self):
        """Test project detail API endpoint"""
        url = reverse('portfolio:project_detail_api', kwargs={'project_id': self.project.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['project']['title'], 'Test Project')

    def test_project_detail_api_not_found(self):
        """Test project detail API with non-existent project"""
        url = reverse('portfolio:project_detail_api', kwargs={'project_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
        data = response.json()
        self.assertFalse(data['success'])

    def test_categories_api(self):
        """Test categories API endpoint"""
        url = reverse('portfolio:categories_api')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(len(data['categories']), 1)
        self.assertEqual(data['categories'][0]['name'], 'Test Category')

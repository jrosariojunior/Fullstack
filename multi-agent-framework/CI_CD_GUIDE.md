# 🚀 CI/CD Pipeline Implementation Guide

Complete guide for setting up and using the CI/CD pipeline for the Multi-Agent Framework.

---

## 📋 Overview

The CI/CD pipeline automatically:
1. **Lint & Format** - Code quality checks (black, isort, flake8, mypy)
2. **Unit Tests** - Run test suite with coverage tracking
3. **Security Scan** - Check for vulnerabilities (bandit, safety)
4. **Build Docker** - Create containerized application
5. **Deploy Staging** - Deploy to staging environment
6. **Deploy Production** - Deploy to production environment

---

## 🔧 Setup Instructions

### Step 1: Enable GitHub Actions

1. Go to your GitHub repository
2. Click **Settings** → **Actions**
3. Enable **Actions** if not already enabled

### Step 2: Configure Secrets

Add the following secrets in **Settings → Secrets and variables → Actions**:

```
GITHUB_TOKEN          (automatically available)
REGISTRY_URL          (your container registry URL)
REGISTRY_USERNAME     (Docker Hub or registry username)
REGISTRY_PASSWORD     (Docker Hub or registry password)
SLACK_WEBHOOK_URL     (optional, for notifications)
STAGING_API_URL       (staging environment API URL)
PRODUCTION_API_URL    (production environment API URL)
DEPLOY_KEY            (SSH key for deployment server)
```

### Step 3: Configure Branch Protection (Optional but Recommended)

1. Go to **Settings → Branches**
2. Add branch protection rules for `main` and `develop`
3. Require status checks to pass:
   - **lint**
   - **test**
   - **security**
   - **build**

---

## 📊 Pipeline Workflow

### 1. On Push to `main` or `develop`

```
Push → [Lint] → [Test] → [Security] → [Build] → [Deploy]
       ↓        ↓         ↓            ↓         ↓
       ✓        ✓         ✓            ✓    (staging/prod)
```

### 2. On Pull Request

Runs **lint**, **test**, and **security** checks only (no deployment).

---

## 🧪 Running Tests Locally

### Prerequisites
```bash
pip install pytest pytest-cov pytest-asyncio
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=backend --cov-report=html
# View coverage: open htmlcov/index.html
```

### Run Specific Test File
```bash
pytest tests/test_api.py -v
```

### Run Tests by Marker
```bash
pytest -m "not slow" tests/  # Skip slow tests
pytest -m "asyncio" tests/   # Only async tests
```

### Run with Output
```bash
pytest tests/ -v -s  # -s shows print statements
```

---

## 🐳 Building Docker Image Locally

### Build Image
```bash
docker build -t multi-agent-framework:latest .
```

### Run Container
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@db:5432/dbname" \
  -e REDIS_URL="redis://redis:6379/0" \
  -e CLAUDE_API_KEY="your-key" \
  multi-agent-framework:latest
```

### Test Container Health
```bash
curl http://localhost:8000/health
```

---

## 📝 Code Quality Standards

### Black (Code Formatting)
```bash
black backend/          # Format code
black --check backend/  # Check without formatting
```

### isort (Import Sorting)
```bash
isort backend/          # Sort imports
isort --check backend/  # Check without sorting
```

### Flake8 (Linting)
```bash
flake8 backend/ --max-line-length=100
```

### MyPy (Type Checking)
```bash
mypy backend/ --ignore-missing-imports
```

---

## 🔒 Security Checks

### Bandit (Security Scanning)
```bash
bandit -r backend/ -ll  # Low severity and above
```

### Safety (Dependency Vulnerabilities)
```bash
safety check  # Check requirements.txt
```

---

## 🎯 Deployment Configuration

### Staging Deployment

Edit `.github/workflows/ci-cd.yml` and add:

```yaml
deploy-staging:
  needs: build
  if: github.ref == 'refs/heads/develop'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to Heroku (example)
      run: |
        echo "Deploying to Heroku..."
        git remote add heroku https://git.heroku.com/app-staging.git
        git push heroku develop:main
```

### Production Deployment

```yaml
deploy-production:
  needs: build
  if: github.ref == 'refs/heads/main'
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    
    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Your deployment command here
```

---

## 📈 Monitoring Pipeline

### View Pipeline Status

1. Go to **Actions** tab in GitHub
2. Click on the workflow run
3. View job status and logs

### Job Logs

Click on each job to see detailed logs:
- **lint** - Code quality issues
- **test** - Test failures and coverage
- **security** - Vulnerability findings
- **build** - Docker build output
- **deploy** - Deployment status

---

## 🐛 Debugging Failed Tests

### View Test Output
```bash
pytest tests/test_api.py -v -s
```

### Run Single Test
```bash
pytest tests/test_api.py::TestHealthCheck::test_health_check_success -v
```

### Run with Pytest Plugins
```bash
pytest --pdb           # Drop into debugger on failure
pytest -x              # Stop on first failure
pytest --lf            # Run last failed
```

---

## 📊 Coverage Requirements

The pipeline requires **70%+ code coverage**.

### Check Coverage Locally
```bash
pytest --cov=backend --cov-report=term-missing tests/
```

### Improve Coverage
1. Identify uncovered lines (shown in red)
2. Add tests for those code paths
3. Re-run coverage check

---

## 🔄 Workflow for Contributors

### 1. Create Feature Branch
```bash
git checkout -b feature/my-feature
```

### 2. Make Changes
```bash
# Edit code
git add .
git commit -m "Add feature"
```

### 3. Push and Create PR
```bash
git push origin feature/my-feature
# Go to GitHub and create pull request
```

### 4. Check Pipeline Status
- Wait for all checks to pass
- If any fail, check logs and fix
- Push fixes to same branch

### 5. Merge When Ready
```bash
# After approval and all checks pass
git merge feature/my-feature
git push origin main
```

---

## 📋 GitHub Actions Best Practices

### 1. Use Caching
The workflow already includes Python package caching:
```yaml
uses: actions/setup-python@v4
with:
  cache: 'pip'
```

### 2. Use Secrets for Sensitive Data
Never commit API keys or passwords:
```yaml
- name: Deploy
  env:
    API_KEY: ${{ secrets.API_KEY }}
  run: ./deploy.sh
```

### 3. Use Artifacts for Reports
Save test results and coverage:
```yaml
- uses: actions/upload-artifact@v3
  with:
    name: test-results
    path: htmlcov/
```

---

## 🚨 Common Issues & Solutions

### Issue: Tests Fail Locally But Pass in CI

**Solution:** Check Python version and dependencies
```bash
python --version  # Should be 3.11+
pip install -r requirements.txt
pytest tests/
```

### Issue: Docker Build Fails

**Solution:** Check Dockerfile and dependencies
```bash
docker build -t test:latest .
docker run test:latest python -m pytest
```

### Issue: GitHub Actions Timeout

**Solution:** Increase timeout or optimize tests
```yaml
timeout-minutes: 30  # Add to job config
```

### Issue: Cannot Find Test Modules

**Solution:** Ensure `__init__.py` exists in test directories
```bash
touch tests/__init__.py
```

---

## 📞 Troubleshooting

### View Workflow File
```bash
cat .github/workflows/ci-cd.yml
```

### Debug GitHub Actions Locally
Use `act` tool to run workflows locally:
```bash
# Install act: https://github.com/nektos/act
act -j lint    # Run lint job
act -j test    # Run test job
```

### Check Syntax
```bash
# YAML syntax validation
yamllint .github/workflows/ci-cd.yml
```

---

## 📚 Additional Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Pytest Documentation**: https://docs.pytest.org/
- **Docker Documentation**: https://docs.docker.com/
- **Black Code Formatter**: https://black.readthedocs.io/

---

## ✨ Next Steps

1. **Push to GitHub** - Commit `.github/workflows/ci-cd.yml`
2. **Configure Secrets** - Add required secrets in GitHub Settings
3. **Create PR** - Make a test PR to verify pipeline works
4. **Monitor** - Check Actions tab for runs
5. **Iterate** - Fix any issues and refine workflow

---

## 🎉 Pipeline Complete!

Your CI/CD pipeline is now ready to:
- ✅ Automatically test all code
- ✅ Enforce code quality standards
- ✅ Scan for security vulnerabilities
- ✅ Build Docker images
- ✅ Deploy to staging and production

**Every commit is now automatically validated!** 🚀

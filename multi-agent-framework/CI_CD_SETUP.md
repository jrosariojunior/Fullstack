# 🔄 CI/CD Setup - Complete Guide

Complete setup guide for the GitHub Actions CI/CD pipeline.

---

## ✅ What's Included

### 1. **GitHub Actions Workflow** (`.github/workflows/ci-cd.yml`)
- Lint & Code Quality checks
- Unit Tests with coverage
- Security scanning
- Docker image building
- Staging & Production deployment

### 2. **Docker Support**
- `Dockerfile` - Production-ready container
- `.dockerignore` - Optimized image build

### 3. **Testing Infrastructure**
- `tests/conftest.py` - Shared pytest fixtures
- `tests/test_api.py` - API endpoint tests
- `tests/test_agents.py` - Agent tests
- `tests/test_llm_providers.py` - LLM provider tests
- `pytest.ini` - Pytest configuration

### 4. **Configuration Files**
- Updated `requirements.txt` with test/security tools
- `.github/workflows/ci-cd.yml` - Main CI/CD pipeline

---

## 🚀 Quick Start (10 minutes)

### Step 1: Push to GitHub

```bash
# If not already a git repo
git init
git remote add origin https://github.com/YOUR_USERNAME/multi-agent-framework.git

# Commit everything
git add .
git commit -m "Add CI/CD pipeline and test suite"
git branch -M main
git push -u origin main
```

### Step 2: Configure GitHub Secrets

1. Go to your repo on GitHub
2. **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret** and add:

```
REGISTRY_PASSWORD     = your-docker-hub-password
REGISTRY_USERNAME     = your-docker-hub-username
```

(GITHUB_TOKEN is automatic)

### Step 3: Watch Pipeline Run

1. Go to **Actions** tab
2. Click the latest workflow
3. Watch jobs run in sequence

**That's it!** Pipeline now runs on every push. ✅

---

## 📊 Pipeline Jobs Explained

### 1. **Lint** (5 min)
```
Check code formatting, imports, and quality
- Black code formatter
- isort import sorting
- flake8 linting
- mypy type checking
```

✅ **Pass Requirement:** Code must be properly formatted

### 2. **Test** (10 min)
```
Run unit tests with coverage tracking
- pytest runs all tests in tests/
- Coverage report generated (70% minimum)
- Results uploaded to Codecov
```

✅ **Pass Requirement:** 70%+ coverage, all tests pass

### 3. **Security** (3 min)
```
Scan for vulnerabilities
- bandit checks for security issues
- safety checks for vulnerable packages
```

✅ **Pass Requirement:** No critical security issues

### 4. **Build** (5 min)
```
Build Docker image and push to registry
- Docker image created
- Pushed to container registry (ghcr.io)
```

✅ **Pass Requirement:** Docker image builds successfully

### 5. **Deploy Staging** (5 min)
```
Deploy to staging environment
- Only runs on develop branch
- Smoke tests verify deployment
```

### 6. **Deploy Production** (5 min)
```
Deploy to production environment
- Only runs on main branch
- Health checks verify deployment
```

---

## 🧪 Running Tests Locally

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run All Tests
```bash
pytest tests/ -v
```

### Run with Coverage
```bash
pytest tests/ -v --cov=backend --cov-report=html
```

### Run Specific Tests
```bash
pytest tests/test_api.py -v
pytest tests/test_api.py::TestHealthCheck -v
pytest tests/test_api.py::TestHealthCheck::test_health_check_success -v
```

### Run with Debugging
```bash
pytest tests/ -v -s --pdb
```

---

## 🐳 Building Docker Locally

### Build Image
```bash
docker build -t multi-agent-framework:latest .
```

### Run Container
```bash
docker run -it -p 8000:8000 \
  -e DATABASE_URL="postgresql://user:pass@localhost/dbname" \
  -e REDIS_URL="redis://localhost:6379/0" \
  -e CLAUDE_API_KEY="your-api-key" \
  multi-agent-framework:latest
```

### Test Container
```bash
# In another terminal
curl http://localhost:8000/health
```

---

## 📋 Deployment Checklist

### Before Deploying to Staging

- [ ] All tests pass locally: `pytest tests/`
- [ ] Code is formatted: `black backend/`
- [ ] Imports are sorted: `isort backend/`
- [ ] No linting issues: `flake8 backend/`
- [ ] No type errors: `mypy backend/`
- [ ] Coverage is 70%+: `pytest --cov=backend tests/`

### Before Deploying to Production

- [ ] Staging deployment successful
- [ ] Smoke tests on staging passed
- [ ] PR reviewed and approved
- [ ] All GitHub checks passed
- [ ] Version number bumped (optional)

---

## 🔄 Typical Workflow

### 1. Start Feature Branch
```bash
git checkout -b feature/new-feature
```

### 2. Make Changes & Test
```bash
# Edit code
pytest tests/ -v  # Verify tests pass
black backend/    # Format code
isort backend/    # Sort imports
```

### 3. Commit & Push
```bash
git add .
git commit -m "Add new feature"
git push origin feature/new-feature
```

### 4. Create Pull Request
- Go to GitHub
- Create PR from `feature/new-feature` to `develop`
- Pipeline automatically runs checks

### 5. Fix Any Issues
```bash
# If tests fail
pytest tests/ -v  # Debug locally
# Make fixes
git add .
git commit -m "Fix tests"
git push origin feature/new-feature
```

### 6. Merge to Develop
- Wait for all checks to pass (green checkmarks)
- Approve PR
- Merge to develop
- Pipeline deploys to staging

### 7. Merge to Main (for Release)
```bash
git checkout main
git pull origin main
git merge develop
git push origin main
```
- Pipeline deploys to production

---

## 📈 Monitoring & Debugging

### View Pipeline Status
```
GitHub → Actions → Click workflow run → View job details
```

### Common Issues & Solutions

#### Issue: Tests fail in CI but pass locally
**Solution:** Check Python version and environment
```bash
python --version  # Should be 3.11+
pip install -r requirements.txt
pytest tests/
```

#### Issue: Docker build fails
**Solution:** Check Dockerfile and dependencies
```bash
docker build -t test:latest .
docker run test:latest python -m pytest
```

#### Issue: Lint fails
**Solution:** Run formatters locally
```bash
black backend/
isort backend/
flake8 backend/
```

#### Issue: Coverage below 70%
**Solution:** Add tests for uncovered code
```bash
pytest --cov=backend --cov-report=html tests/
# Open htmlcov/index.html and find red (uncovered) lines
```

---

## 🔒 Security Scanning

### Run Security Checks Locally
```bash
# Check for code vulnerabilities
bandit -r backend/ -ll

# Check for vulnerable dependencies
safety check
```

### Common Security Issues
- Hardcoded secrets → Use environment variables
- SQL injection → Use parameterized queries
- XSS attacks → Validate all inputs
- Unsafe serialization → Use safe JSON only

---

## 📊 Adding Status Badges

Add these to your `README.md` to show pipeline status:

```markdown
# Multi-Agent Framework

[![CI/CD Pipeline](https://github.com/YOUR_USERNAME/multi-agent-framework/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/YOUR_USERNAME/multi-agent-framework/actions)
[![Code Coverage](https://codecov.io/gh/YOUR_USERNAME/multi-agent-framework/branch/main/graph/badge.svg)](https://codecov.io/gh/YOUR_USERNAME/multi-agent-framework)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
```

---

## 🎯 Next Steps After Setup

### Immediate
- [ ] Push code to GitHub
- [ ] Configure secrets
- [ ] Verify first pipeline run
- [ ] Fix any failing checks

### Short Term (1-2 weeks)
- [ ] Expand test coverage to 90%+
- [ ] Add integration tests
- [ ] Setup Slack notifications
- [ ] Configure staging deployment

### Medium Term (1-2 months)
- [ ] Setup production deployment
- [ ] Add database migration automation
- [ ] Add performance benchmarks
- [ ] Setup monitoring & alerting

---

## 📚 Resources

- **GitHub Actions Docs**: https://docs.github.com/en/actions
- **Pytest Docs**: https://docs.pytest.org/
- **Docker Docs**: https://docs.docker.com/
- **Black Formatting**: https://black.readthedocs.io/

---

## ✨ Success Checklist

- [x] CI/CD workflow created
- [x] Test suite scaffolded
- [x] Docker configuration done
- [x] Requirements updated
- [x] Setup documentation written
- [x] Ready to push to GitHub

---

## 🎉 You're Done!

The CI/CD pipeline is now set up and ready to use.

Every time you:
- **Push code** → Automated testing & validation
- **Create PR** → Automatic quality checks
- **Merge to develop** → Deploy to staging
- **Merge to main** → Deploy to production

**CI/CD automation is now active!** 🚀

---

## 📞 Getting Help

If pipeline fails:
1. Check the GitHub Actions logs
2. Run tests locally: `pytest tests/ -v`
3. Check formatting: `black --check backend/`
4. Review error message in job log
5. Fix issue and push again

Happy automating! 🤖

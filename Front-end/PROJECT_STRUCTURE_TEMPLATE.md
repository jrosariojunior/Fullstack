# 🏗️ Project Structure Template

**Status:** ✅ Complete  
**Version:** 1.0  
**Last Updated:** April 2026

Standard folder organization for Next.js projects. Customize based on your project needs, but maintain consistent conventions across the team.

---

## 📁 Universal Project Structure

Use this as your baseline. Customize for your specific project type.

```
my-project/
├── .github/
│   ├── workflows/
│   │   └── ci-cd.yml                # GitHub Actions CI/CD
│   ├── CODEOWNERS
│   └── PULL_REQUEST_TEMPLATE.md
│
├── .vscode/                         # VS Code settings (shared)
│   ├── extensions.json              # Recommended extensions
│   ├── launch.json                  # Debug configuration
│   └── settings.json                # Editor settings
│
├── public/                          # Static assets
│   ├── images/
│   │   ├── logo.svg
│   │   ├── favicon.ico
│   │   └── og-image.png
│   ├── fonts/
│   ├── icons/
│   └── videos/
│
├── src/
│   ├── app/                         # Next.js App Router
│   │   ├── layout.tsx               # Root layout
│   │   ├── page.tsx                 # Homepage
│   │   ├── not-found.tsx            # 404 page
│   │   ├── error.tsx                # Error boundary
│   │   │
│   │   ├── (auth)/                  # Auth routes group
│   │   │   ├── login/
│   │   │   │   ├── page.tsx
│   │   │   │   └── layout.tsx
│   │   │   ├── signup/
│   │   │   ├── forgot-password/
│   │   │   └── reset-password/
│   │   │
│   │   ├── (dashboard)/             # Dashboard routes group
│   │   │   ├── layout.tsx           # Dashboard layout
│   │   │   ├── dashboard/           # Main dashboard
│   │   │   │   ├── page.tsx
│   │   │   │   └── layout.tsx
│   │   │   ├── settings/
│   │   │   │   ├── page.tsx
│   │   │   │   ├── profile/
│   │   │   │   ├── account/
│   │   │   │   └── notifications/
│   │   │   └── [resource]/          # Dynamic routes
│   │   │       └── page.tsx
│   │   │
│   │   ├── blog/                    # Blog section
│   │   │   ├── page.tsx             # Blog listing
│   │   │   ├── layout.tsx
│   │   │   ├── [slug]/              # Blog post
│   │   │   │   ├── page.tsx
│   │   │   │   └── layout.tsx
│   │   │   └── category/
│   │   │       └── [category]/
│   │   │
│   │   ├── api/                     # API routes
│   │   │   ├── auth/
│   │   │   │   ├── [...nextauth]/   # NextAuth
│   │   │   │   ├── login/
│   │   │   │   └── logout/
│   │   │   ├── users/
│   │   │   │   ├── route.ts         # GET /api/users
│   │   │   │   ├── [id]/
│   │   │   │   │   └── route.ts     # GET/PUT/DELETE /api/users/[id]
│   │   │   │   └── profile/
│   │   │   ├── products/
│   │   │   ├── orders/
│   │   │   └── webhooks/
│   │   │       └── stripe/
│   │   │
│   │   └── admin/                   # Admin section (if applicable)
│   │       ├── layout.tsx
│   │       ├── page.tsx
│   │       └── [resource]/
│   │
│   ├── components/                  # Reusable components
│   │   ├── ui/                      # Design system components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Dropdown.tsx
│   │   │   ├── Badge.tsx
│   │   │   └── [other design system]
│   │   │
│   │   ├── layout/                  # Layout components
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Navigation.tsx
│   │   │   └── Breadcrumbs.tsx
│   │   │
│   │   ├── sections/                # Page sections
│   │   │   ├── Hero.tsx
│   │   │   ├── Features.tsx
│   │   │   ├── Testimonials.tsx
│   │   │   ├── CTA.tsx
│   │   │   └── Pricing.tsx
│   │   │
│   │   ├── features/                # Feature-specific components
│   │   │   ├── auth/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── SignupForm.tsx
│   │   │   │   └── PasswordReset.tsx
│   │   │   ├── dashboard/
│   │   │   │   ├── StatsCard.tsx
│   │   │   │   ├── Chart.tsx
│   │   │   │   └── DataTable.tsx
│   │   │   ├── ecommerce/
│   │   │   │   ├── ProductCard.tsx
│   │   │   │   ├── Cart.tsx
│   │   │   │   └── Checkout.tsx
│   │   │   └── blog/
│   │   │       ├── PostCard.tsx
│   │   │       ├── PostList.tsx
│   │   │       └── SearchPosts.tsx
│   │   │
│   │   └── common/                  # Shared utility components
│   │       ├── Loading.tsx
│   │       ├── Error.tsx
│   │       ├── Empty.tsx
│   │       └── Skeleton.tsx
│   │
│   ├── hooks/                       # Custom React hooks
│   │   ├── useAuth.ts               # Auth context
│   │   ├── useFetch.ts              # Data fetching
│   │   ├── useLocalStorage.ts       # Local storage
│   │   ├── useDebounce.ts
│   │   ├── useIntersection.ts
│   │   └── [project-specific hooks]
│   │
│   ├── lib/                         # Utilities & services
│   │   ├── api.ts                   # API client setup
│   │   ├── auth.ts                  # Auth utilities
│   │   ├── db.ts                    # Database connection
│   │   ├── stripe.ts                # Stripe utilities
│   │   ├── validators.ts            # Data validation
│   │   ├── constants.ts             # App constants
│   │   └── [other utilities]
│   │
│   ├── stores/                      # State management (Zustand)
│   │   ├── authStore.ts
│   │   ├── userStore.ts
│   │   ├── appStore.ts
│   │   └── [feature-specific stores]
│   │
│   ├── services/                    # API services
│   │   ├── userService.ts
│   │   ├── authService.ts
│   │   ├── productService.ts
│   │   ├── orderService.ts
│   │   └── [feature-specific services]
│   │
│   ├── styles/                      # Global styles
│   │   ├── globals.css              # Global styles
│   │   ├── variables.css            # CSS variables
│   │   ├── animations.css           # Animations
│   │   └── [feature styles]
│   │
│   ├── types/                       # TypeScript types
│   │   ├── index.ts                 # Main types export
│   │   ├── user.ts
│   │   ├── product.ts
│   │   ├── order.ts
│   │   ├── api.ts                   # API response types
│   │   └── [feature-specific types]
│   │
│   ├── utils/                       # Utility functions
│   │   ├── cn.ts                    # Class name utility
│   │   ├── format.ts                # Formatting utilities
│   │   ├── parse.ts                 # Parsing utilities
│   │   ├── validate.ts              # Validation utilities
│   │   └── [feature-specific utils]
│   │
│   └── middleware.ts                # Next.js middleware
│
├── tests/                           # Test files
│   ├── unit/
│   │   ├── utils/
│   │   └── lib/
│   ├── integration/
│   │   ├── api/
│   │   └── features/
│   ├── e2e/
│   │   ├── auth.spec.ts
│   │   ├── checkout.spec.ts
│   │   └── user-flow.spec.ts
│   └── fixtures/                    # Test data & mocks
│
├── docs/                            # Project documentation
│   ├── README.md                    # Project overview
│   ├── SETUP.md                     # Setup instructions
│   ├── ARCHITECTURE.md              # Architecture decisions
│   ├── API.md                       # API documentation
│   ├── CONTRIBUTING.md              # Contributing guidelines
│   ├── DEPLOYMENT.md                # Deployment guide
│   ├── TROUBLESHOOTING.md           # Common issues
│   └── [feature-specific docs]
│
├── scripts/                         # Build & utility scripts
│   ├── setup.sh                     # Setup script
│   ├── seed.ts                      # Database seed
│   └── generate-types.ts            # Type generation
│
├── .env.local                       # Local environment variables
├── .env.example                     # Example environment variables
├── .eslintrc.json                  # ESLint configuration
├── .prettierrc                      # Prettier configuration
├── .prettierignore
├── .gitignore
├── .gitattributes
│
├── next.config.js                  # Next.js configuration
├── tailwind.config.js              # Tailwind configuration
├── postcss.config.js               # PostCSS configuration
├── tsconfig.json                   # TypeScript configuration
│
├── vitest.config.ts                # Vitest configuration
├── playwright.config.ts            # Playwright configuration
├── jest.config.js                  # Jest configuration (if using)
│
├── package.json                    # Dependencies & scripts
├── package-lock.json
│
├── .github/                         # GitHub specific
│   └── workflows/
│       └── ci-cd.yml
│
├── vercel.json                      # Vercel deployment config
└── README.md                        # Project README
```

---

## 🎯 Naming Conventions

### Files & Folders
```
Components:      PascalCase         Button.tsx, UserProfile.tsx
Pages:           lowercase          page.tsx, layout.tsx
Hooks:           camelCase          useAuth.ts, useFetch.ts
Utils:           camelCase          format.ts, validate.ts
Types:           PascalCase         User.ts, Product.ts
Stores:          camelCase          authStore.ts, userStore.ts
Services:        camelCase          userService.ts, authService.ts
Tests:           *.test.ts or       Button.test.ts
                 *.spec.ts          Button.spec.ts
API routes:      lowercase          /api/users, /api/products
Dynamic routes:  brackets           [id], [slug], [...rest]
```

### TypeScript Types
```
Interface:       PascalCase         interface User { }
Type:            PascalCase         type Status = 'active' | 'inactive'
Enum:            PascalCase         enum Role { ADMIN, USER }
Constants:       UPPER_SNAKE_CASE   const MAX_ATTEMPTS = 3
Variables:       camelCase          let currentUser = null
Functions:       camelCase          function getUser() { }
```

---

## 📦 Component Organization

### Component File Structure
```
Button/
├── Button.tsx           # Component implementation
├── Button.test.ts       # Unit tests
├── Button.stories.tsx   # Storybook stories (if using)
└── index.ts             # Export

ProductCard/
├── ProductCard.tsx
├── ProductCard.test.ts
├── index.ts
└── types.ts             # Component-specific types

LoginForm/
├── LoginForm.tsx
├── LoginForm.test.ts
├── index.ts
├── types.ts
├── hooks.ts             # Component-specific hooks
└── validations.ts       # Component-specific validations
```

### Component Template
```typescript
// Button.tsx
import { ReactNode } from 'react';
import styles from './Button.module.css';

export interface ButtonProps {
  children: ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  onClick?: () => void;
  className?: string;
}

/**
 * Button component with multiple variants
 *
 * @example
 * <Button variant="primary" size="md">
 *   Click me
 * </Button>
 */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  onClick,
  className,
}: ButtonProps) {
  return (
    <button
      className={`button button--${variant} button--${size} ${className || ''}`}
      disabled={disabled}
      onClick={onClick}
    >
      {children}
    </button>
  );
}
```

---

## 📝 Route Organization Guide

### For SaaS/Dashboards
```
src/app/
├── page.tsx                        # Landing/Homepage
├── auth/
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   └── reset-password/page.tsx
├── dashboard/
│   ├── layout.tsx                 # Dashboard layout
│   ├── page.tsx                   # Main dashboard
│   ├── profile/page.tsx
│   └── settings/page.tsx
├── api/
│   ├── auth/[...nextauth]/route.ts
│   ├── users/route.ts
│   └── products/route.ts
└── admin/
    └── page.tsx
```

### For Marketing Sites
```
src/app/
├── page.tsx                        # Homepage
├── about/page.tsx
├── services/page.tsx
├── blog/
│   ├── page.tsx                   # Blog listing
│   └── [slug]/page.tsx            # Blog post
├── contact/page.tsx
├── api/
│   └── contact/route.ts
└── [other pages]/page.tsx
```

### For E-commerce
```
src/app/
├── page.tsx                        # Homepage
├── products/
│   ├── page.tsx                   # Products listing
│   └── [id]/page.tsx              # Product detail
├── cart/page.tsx
├── checkout/
│   ├── page.tsx
│   ├── shipping/page.tsx
│   └── payment/page.tsx
├── orders/page.tsx                # Order history
├── account/page.tsx
├── api/
│   ├── products/route.ts
│   ├── cart/route.ts
│   ├── orders/route.ts
│   └── checkout/route.ts
└── admin/page.tsx
```

---

## 🔧 Environment Variables

Create `.env.example` with all required variables:

```bash
# Authentication
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your_secret_here

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
REDIS_URL=redis://localhost:6379

# API Keys
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
GITHUB_ID=...
GITHUB_SECRET=...

# External Services
ANALYTICS_ID=G-XXXXXXXXXX
SENTRY_DSN=https://...
OPENAI_API_KEY=sk-...

# Feature Flags
FEATURE_NEW_CHECKOUT=false
FEATURE_ANALYTICS=true
```

---

## 📋 Configuration Files Checklist

Setup these files during project initialization:

```
TypeScript & Build
- [ ] tsconfig.json
- [ ] next.config.js
- [ ] .eslintrc.json
- [ ] .prettierrc

Styling
- [ ] tailwind.config.js
- [ ] postcss.config.js

Testing
- [ ] vitest.config.ts
- [ ] playwright.config.ts

Git
- [ ] .gitignore
- [ ] .gitattributes

Environment
- [ ] .env.example
- [ ] .env.local (not committed)

Deployment
- [ ] vercel.json (or deployment config)

GitHub
- [ ] .github/workflows/ci-cd.yml
- [ ] .github/CODEOWNERS
- [ ] .github/PULL_REQUEST_TEMPLATE.md
```

---

## 🚀 Quick Setup Command

```bash
# Create new Next.js project with this structure
npx create-next-app@latest my-project \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir

cd my-project

# Create folders
mkdir -p src/{components/{ui,layout,sections,features,common},hooks,lib,stores,services,styles,types,utils}
mkdir -p tests/{unit,integration,e2e,fixtures}
mkdir -p docs
mkdir -p scripts
mkdir -p public/{images,fonts,icons}

# Create necessary files
touch .env.local .env.example
cp .github/workflows/ci-cd.yml . # Copy from PROTOCOL

# Install dependencies
npm install -D vitest playwright @testing-library/react @testing-library/jest-dom
npm install zustand axios nextauth
```

---

## 📊 Folder Size Guidelines

Keep these in mind for maintainability:

```
components/        < 20 MB
lib/              < 5 MB
utils/            < 2 MB
hooks/            < 1 MB
stores/           < 500 KB
types/            < 500 KB
styles/           < 2 MB
```

If any folder exceeds these sizes, consider breaking it into subfolders.

---

## ✅ Project Structure Validation

Before starting Phase 3, verify:

- [ ] All folders created
- [ ] Naming conventions understood by team
- [ ] .env.example has all required variables
- [ ] Configuration files created and configured
- [ ] TypeScript strict mode enabled
- [ ] ESLint and Prettier configured
- [ ] Git hooks configured (pre-commit)
- [ ] README.md explains structure
- [ ] Team agrees on conventions

---

**Version:** 1.0 | **Status:** ✅ Complete | **Last Updated:** April 2026


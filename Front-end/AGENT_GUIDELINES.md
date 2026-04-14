# 👥 Agent Guidelines - Detailed Role Descriptions

**Status:** ✅ Complete  
**Version:** 1.0  
**Last Updated:** April 2026

Comprehensive guidelines for each of the 5 specialized agents, including decision frameworks, responsibilities, and integration points.

---

## 📋 Table of Contents

1. [Agente de Briefing](#agente-de-briefing--)
2. [Agente Front-end](#agente-front-end--)
3. [Agente SEO](#agente-seo--)
4. [Agente UX/UI](#agente-uxui--)
5. [Agente QA/Auditoria](#agente-qaauditoria--)

---

## 🧭 Agente de Briefing 🧭

### Core Responsibility
**Coordenador inicial que coleta, organiza e valida todas as informações do projeto**

The Briefing Agent acts as the project's gatekeeper, ensuring absolute clarity before any technical work begins. They are responsible for translating business needs into actionable requirements.

### Key Responsibilities

#### Phase-by-Phase

**Phase 1: Discovery (Days 1-3)**

1. **Initial Interview**
   - Schedule discovery call with stakeholder(s)
   - Prepare intake questionnaire (from TEMPLATES_BRIEFING.md)
   - Document all answers thoroughly
   - Ask follow-up questions until clarity is achieved
   - Record session (with permission) for team reference

2. **Competitive Analysis**
   - Research top 5 competitors
   - Document their features, design, SEO approach
   - Identify market gaps and opportunities
   - Create competitive analysis document

3. **Requirement Gathering**
   - Use MOSCOW prioritization method:
     - **Must have**: Core functionality (60% of features)
     - **Should have**: Important but not critical (25%)
     - **Could have**: Nice-to-have features (10%)
     - **Won't have**: Out of scope (5%)
   - Document constraints (technical, legal, budgetary)
   - Identify dependencies and risks

4. **Goal Definition**
   - Business goals (revenue, users, market share)
   - User goals (problems solved, outcomes desired)
   - Success metrics (concrete, measurable)
   - Success timeline (3-month, 6-month, 12-month)

5. **Create Project Brief**
   - Use PROJECT_BRIEF_COMPARTILHADO_TEMPLATE.md
   - Fill all sections completely
   - Get stakeholder sign-off
   - Distribute to entire team

### Decision Framework: When to Go Back to Client

| Situation | Action |
|-----------|--------|
| Requirement is vague | Ask specific clarifying questions |
| Two requirements conflict | Document both, let client choose priority |
| Scope seems too large | Break into phases, prioritize |
| Budget/timeline mismatch | Discuss trade-offs explicitly |
| Unclear success metrics | Define concrete, measurable KPIs |
| Unexpected technical constraint | Document, present options to client |

### Deliverables Checklist

- [ ] Completed intake questionnaire
- [ ] Competitive analysis document
- [ ] Personas (3-5 detailed personas)
- [ ] User journeys (3-5 key journeys mapped)
- [ ] Requirements list (MOSCOW prioritized)
- [ ] Business goals (quantified)
- [ ] Success metrics (specific and measurable)
- [ ] Constraints and risks documented
- [ ] Project timeline (phases with durations)
- [ ] Budget allocation (if applicable)
- [ ] Final project brief (signed off by client)
- [ ] Team kickoff presentation deck

### Tools & Templates
- TEMPLATES_BRIEFING.md (all interview guides)
- PROJECT_BRIEF_COMPARTILHADO_TEMPLATE.md
- Google Docs/Sheets for data collection
- Figma for competitive visual analysis

### Integration with Other Agents

| Agent | When | What Briefing Provides |
|-------|------|------------------------|
| **Front-end** | Phase 2 | Tech requirements, scale, performance needs |
| **SEO** | Phase 2 | Business goals, target audience, competitive landscape |
| **UX/UI** | Phase 2 | User personas, journeys, interaction requirements |
| **QA** | Phase 5 | Success criteria, acceptance tests, edge cases |

### Success Criteria

✅ **Stakeholder Satisfaction**: Client feels heard and understood  
✅ **100% Clarity**: No ambiguity in requirements  
✅ **Team Alignment**: All agents agree on project direction  
✅ **Completeness**: No missing information before proceeding  
✅ **Documentation**: Everything recorded for future reference  

---

## 💻 Agente Front-end 💻

### Core Responsibility
**Desenvolvedor técnico especializado que arquiteta e implementa a solução**

The Front-end Agent is the technical architect and implementation lead. They make technology decisions, establish project structure, and build the actual application with performance and scalability as core concerns.

### Key Responsibilities

#### Phase-by-Phase

**Phase 2: Planning (Days 4-5)**

1. **Tech Stack Decision**
   - Review TECH_STACK_DECISIONS.md for your project type
   - Analyze requirements (SaaS? Landing page? E-commerce?)
   - Consider:
     - Project scale and complexity
     - Team expertise
     - Performance requirements
     - SEO needs
     - Timeline and budget
   - Present recommendation to team with trade-offs
   - Get consensus before moving forward

2. **Architecture Design**
   - Create system architecture diagram
   - Define data flow (frontend ↔ backend)
   - Plan state management approach
   - Design API contracts (with backend team if exists)
   - Document deployment strategy

3. **Project Structure**
   - Use PROJECT_STRUCTURE_TEMPLATE.md as baseline
   - Customize for your tech stack
   - Create folder hierarchy
   - Define naming conventions
   - Document component organization

**Phase 3: Design Implementation (Days 6-8)**

1. **Component Architecture**
   - Break design into components
   - Define component hierarchy
   - Identify reusable patterns
   - Plan prop interfaces
   - Document component APIs

2. **Setup Development Environment**
   - Initialize project (Next.js, etc.)
   - Configure build tools
   - Setup testing framework
   - Configure linting and formatting
   - Create development documentation

**Phase 4: Development (Days 9-18)**

1. **Component Development**
   - Implement components following design spec
   - Use TypeScript for type safety
   - Follow naming conventions
   - Write unit tests (80% coverage target)
   - Document components (JSDoc)

2. **State Management**
   - Implement state solutions (Context, Zustand, etc.)
   - Connect API data fetching
   - Handle loading and error states
   - Implement caching strategies

3. **Performance Optimization**
   - Monitor Core Web Vitals:
     - Largest Contentful Paint (LCP) < 2.5s
     - First Input Delay (FID) < 100ms
     - Cumulative Layout Shift (CLS) < 0.1
   - Implement code splitting
   - Optimize images and assets
   - Implement lazy loading

4. **SEO Implementation** (with SEO Agent)
   - Implement meta tags (title, description)
   - Setup Open Graph tags
   - Implement structured data (JSON-LD)
   - Create sitemap
   - Setup robots.txt
   - Ensure semantic HTML

### Decision Framework: Tech Stack Selection

**Ask these questions:**
1. What is the project scale? (Solo site → Enterprise dashboard)
2. What's the team's expertise? (New to React → React veterans)
3. What's the content distribution? (Static → Dynamic → Real-time)
4. What's the performance budget? (Core Web Vitals requirements)
5. What's the timeline? (1 week → 6 months)

**Then choose from:**
- **Static Site**: Next.js (Static Export) + Tailwind
- **SaaS/Dashboard**: Next.js + React + TypeScript + Zustand + shadcn/ui
- **E-commerce**: Next.js + React + TypeScript + PostgreSQL + Stripe
- **Marketing Site**: Next.js (SSG) + Tailwind + Vercel
- **Real-time App**: Next.js + React + WebSockets + Zustand

### Deliverables Checklist

- [ ] Tech stack decision documented with trade-offs
- [ ] Architecture diagram (system design)
- [ ] Project structure created and documented
- [ ] Development environment setup instructions
- [ ] Component inventory (all planned components)
- [ ] API contracts defined
- [ ] State management design documented
- [ ] Performance budget defined
- [ ] SEO technical checklist completed
- [ ] Testing strategy documented
- [ ] Deployment checklist
- [ ] Developer documentation

### Tools & Templates
- TECH_STACK_DECISIONS.md (all decision matrices)
- PROJECT_STRUCTURE_TEMPLATE.md (folder structure)
- Masterclass files for technical deep dives
- Next.js/React documentation

### Code Quality Standards

```
TypeScript:
- No `any` types (use strict mode)
- Props interfaces documented
- Generic types for reusable components

Components:
- Named exports (not default)
- Single responsibility principle
- Comprehensive prop interfaces
- JSDoc comments

CSS:
- Tailwind utility classes
- Component-level styling
- CSS-in-JS only when necessary
- No hardcoded values (use design tokens)

Testing:
- Unit tests for logic
- Component tests with React Testing Library
- E2E tests for critical paths
- 80%+ coverage target
```

### Integration with Other Agents

| Agent | Phase | Collaboration |
|-------|-------|---------------|
| **Briefing** | 1 | Receive requirements, clarify tech needs |
| **SEO** | 2,4 | Align on SEO-friendly architecture |
| **UX/UI** | 3 | Receive designs, validate implementation feasibility |
| **QA** | 4,5 | Regular code reviews, performance testing |

### Success Criteria

✅ **Performance**: Core Web Vitals all green  
✅ **Code Quality**: Linting passes, 80%+ test coverage  
✅ **Type Safety**: Zero `any` types in strict mode  
✅ **Documentation**: Code is self-documenting + JSDoc  
✅ **Maintainability**: Clear structure, reusable components  
✅ **SEO Ready**: Technical SEO all implemented  

---

## 🔍 Agente SEO 🔍

### Core Responsibility
**Especialista em posicionamento Google que arquiteta site para crescimento orgânico**

The SEO Agent ensures the entire project is built with search engine visibility as a core concern, not an afterthought. They work throughout the project to maximize organic traffic potential.

### Key Responsibilities

#### Phase-by-Phase

**Phase 1: Discovery (Days 1-3)**

1. **Keyword Research**
   - Identify primary keywords (high volume, high intent)
   - Identify secondary keywords (long-tail, specific)
   - Analyze keyword difficulty
   - Target 50-100 keywords total
   - Document keyword families

2. **Competitive SEO Analysis**
   - Research top 10 ranking competitors
   - Analyze their keyword targeting
   - Review their backlink profile
   - Identify content gaps
   - Document opportunities

3. **Target Audience Analysis**
   - Understand search intent (informational, navigational, transactional)
   - Identify seasonal trends
   - Understand user pain points
   - Map keywords to user journey

**Phase 2: Planning (Days 4-5)**

1. **Site Architecture**
   - Design URL structure (SEO-friendly):
     - `/blog/category/keyword-title/` format
     - Use hyphens (not underscores)
     - Keep URLs short and descriptive
   - Plan internal linking strategy
   - Design navigation hierarchy
   - Plan breadcrumb structure

2. **Content Strategy**
   - Create 12-month content calendar
   - Plan 10-20 pillar articles (1500+ words each)
   - Plan 50+ supporting articles (800-1500 words)
   - Plan content for each stage of buyer journey
   - Define content goals and KPIs

3. **Technical SEO Foundation**
   - Plan meta tag strategy
   - Design structured data schema
   - Plan XML sitemap
   - Plan robots.txt
   - Identify mobile-first considerations
   - Plan Core Web Vitals targets

**Phase 3: Design (Days 6-8)**

1. **Design System SEO**
   - Ensure heading hierarchy (H1 → H2 → H3)
   - Plan readable typography (16px+ body text)
   - Design mobile-first layouts
   - Ensure adequate white space
   - Plan image alt-text strategy

**Phase 4: Development (Days 9-18)**

1. **Technical Implementation**
   - Implement meta tags dynamically
   - Setup Open Graph tags
   - Implement JSON-LD structured data
   - Create XML sitemap
   - Setup robots.txt
   - Configure canonical URLs
   - Ensure mobile responsiveness

2. **Content Optimization** (with Front-end)
   - Implement H1 tags (one per page)
   - Use descriptive H2/H3 tags
   - Optimize image alt texts
   - Internal linking strategy
   - Schema markup implementation

3. **Performance Monitoring**
   - Setup Google Analytics 4
   - Setup Google Search Console
   - Setup Ahrefs/SEMrush tracking
   - Monitor Core Web Vitals
   - Track keyword rankings

**Phase 5: Audit (Days 19-20)**

1. **SEO Technical Audit**
   - Mobile responsiveness check
   - Meta tags completeness
   - Structured data validation
   - Internal linking analysis
   - Page speed analysis
   - Core Web Vitals review
   - Indexation check

**Phase 6: Post-Launch (Ongoing)**

1. **Content Creation Pipeline**
   - Months 1-2: 10 pillar articles
   - Months 3-6: 20 supporting articles
   - Months 7-12: Continue strategy, 30+ articles
   - Monitor search rankings
   - Adjust strategy based on data

2. **Link Building**
   - Guest posting opportunities
   - Broken link building
   - Resource page placements
   - Industry partnerships
   - PR opportunities

3. **Monitoring & Optimization**
   - Weekly ranking tracking
   - Monthly traffic analysis
   - Quarterly strategy reviews
   - Continuous optimization

### Decision Framework: Keyword Selection

| Metric | Target | Action |
|--------|--------|--------|
| Search Volume | 1000+ searches/month | Priority keyword |
| Difficulty | Low-Medium (20-50) | Achievable ranking |
| Intent Match | Matches business goal | Include in strategy |
| Competition | Fewer than 10 big players | Good opportunity |

### SEO Checklist by Page Type

**Homepage**
- [ ] Unique meta description (160 chars)
- [ ] Primary keyword in title
- [ ] H1 matches title
- [ ] Company schema markup
- [ ] Internal links to key pages
- [ ] Mobile responsive
- [ ] Core Web Vitals green

**Blog Post**
- [ ] Unique title (target keyword included)
- [ ] Meta description (160 chars, compelling)
- [ ] H1 matches title
- [ ] H2/H3 hierarchy correct
- [ ] Images with alt text
- [ ] 3-5 internal links
- [ ] 5-10 external links
- [ ] Author schema
- [ ] Published date schema
- [ ] 1500+ words (pillar) or 800+ words (supporting)

**Landing Page**
- [ ] Unique title with keyword
- [ ] Meta description compelling CTA
- [ ] H1 clear value proposition
- [ ] H2 subheadings for sections
- [ ] Clear CTA above fold
- [ ] Lead schema markup
- [ ] Image optimization
- [ ] Mobile-optimized form
- [ ] Trust signals visible

### Deliverables Checklist

- [ ] Keyword research (50-100 keywords)
- [ ] Competitive analysis (top 10 competitors)
- [ ] Target audience keywords mapping
- [ ] Site architecture diagram (SEO-friendly)
- [ ] Content calendar (12 months)
- [ ] Pillar article outlines (10-20)
- [ ] Technical SEO checklist
- [ ] Meta tag strategy documented
- [ ] Structured data schema plan
- [ ] Internal linking strategy
- [ ] Google Analytics 4 setup
- [ ] Google Search Console setup
- [ ] Ahrefs/SEMrush tracking setup
- [ ] Lighthouse SEO audit (90+ score)
- [ ] Mobile-first design validation
- [ ] Core Web Vitals targets defined
- [ ] Link building strategy
- [ ] Content creation timeline
- [ ] Monthly monitoring checklist

### Tools & Templates
- Google Search Console (keyword insights)
- Google Analytics 4 (traffic tracking)
- Ahrefs or SEMrush (competitive analysis)
- SEO-specific files in files/ folder
- PROTOCOLO_AGENTES_FRONTEND_SEO.md (12-month plan)

### Integration with Other Agents

| Agent | Phase | Collaboration |
|-------|-------|---------------|
| **Briefing** | 1 | Understand business goals, target audience |
| **Front-end** | 2,4 | Align on technical SEO implementation |
| **UX/UI** | 3 | Design for UX + SEO (readability, hierarchy) |
| **QA** | 5 | Validate technical SEO in audit |

### Success Criteria

✅ **Keyword Targeting**: 50-100 keywords documented  
✅ **Technical SEO**: 90+ Lighthouse score  
✅ **Performance**: Core Web Vitals all green  
✅ **Indexation**: All pages indexable in Google  
✅ **Organic Growth**: 10,000+ organic searches/month (12 months)  
✅ **Ranking**: Top 10 for primary keywords (6 months)  

---

## 🎨 Agente UX/UI 🎨

### Core Responsibility
**Designer e especialista em conversão que otimiza experiência do usuário**

The UX/UI Agent ensures the product is not just functional but delightful to use, optimized for conversions, and accessible to all users.

### Key Responsibilities

#### Phase-by-Phase

**Phase 1: Discovery (Days 1-3)**

1. **User Research**
   - Review personas from Briefing agent
   - Understand pain points
   - Identify user goals
   - Document user needs
   - Create user journey maps

2. **Competitive Design Analysis**
   - Study competitor interfaces
   - Identify good patterns to adopt
   - Identify bad patterns to avoid
   - Document design trends in industry
   - Create inspiration board

**Phase 2: Planning (Days 4-5)**

1. **Information Architecture**
   - Create sitemap visualization
   - Design navigation structure
   - Plan information hierarchy
   - Create user flows
   - Plan interaction patterns

2. **Design System Planning**
   - Define color palette (primary, secondary, semantic)
   - Select typography (heading, body, code fonts)
   - Define spacing system (8px grid)
   - Define component inventory
   - Plan responsive breakpoints

**Phase 3: Design (Days 6-8)**

1. **Wireframing**
   - Create low-fidelity wireframes
   - Get feedback from team
   - Iterate on structure
   - Plan component layouts

2. **High-Fidelity Design**
   - Create complete visual designs
   - Apply design system
   - Add interactions
   - Create prototypes
   - User testing if time allows

3. **Design System Documentation**
   - Component specifications
   - Design tokens
   - Color palette
   - Typography scales
   - Spacing system
   - Icon library
   - Interactive components

### Design System Components Checklist

**Foundation**
- [ ] Color system (primary, secondary, semantic)
- [ ] Typography scale (6+ sizes)
- [ ] Spacing scale (8px grid)
- [ ] Shadows/elevation
- [ ] Border radius values
- [ ] Animations/transitions

**Components** (50+ total)
- [ ] Buttons (primary, secondary, tertiary, states)
- [ ] Forms (input, textarea, select, checkbox, radio)
- [ ] Cards (variants, states)
- [ ] Navigation (nav, breadcrumbs, pagination)
- [ ] Modals (dialog, alert, confirmation)
- [ ] Tables (sortable, paginated)
- [ ] Alerts/toasts (info, warning, error, success)
- [ ] Dropdowns/menus
- [ ] Tooltips
- [ ] Progress indicators
- [ ] Sliders/range inputs
- [ ] Date pickers

**Page Templates**
- [ ] Homepage
- [ ] Landing pages
- [ ] Blog post
- [ ] Product/service page
- [ ] Contact form
- [ ] Search results
- [ ] Error pages (404, 500)

### Conversion Optimization Framework

| Element | Optimization |
|---------|--------------|
| **CTA Buttons** | High contrast, clear text, above fold |
| **Forms** | Minimal fields, smart validation, progress indicator |
| **Copy** | Benefit-focused, scannable, short sentences |
| **Social Proof** | Testimonials, reviews, trust badges visible |
| **Trust Signals** | Security badges, guarantees, contact info |
| **Mobile UX** | Thumb-friendly, tap targets 48px+, fast load |

### Accessibility (WCAG 2.1 AA) Checklist

- [ ] Color contrast ratio 4.5:1 (normal text), 3:1 (large text)
- [ ] Keyboard navigation (Tab, Enter, Escape, Arrow keys)
- [ ] Screen reader support (semantic HTML, ARIA labels)
- [ ] Form labels (proper association with inputs)
- [ ] Error messages (clear, linked to field)
- [ ] Focus indicators (visible on all interactive elements)
- [ ] Alternative text for images (descriptive, concise)
- [ ] Video captions and transcripts
- [ ] Readable fonts (16px minimum body text)
- [ ] Sufficient line height (1.5x minimum)
- [ ] Mobile accessibility (large touch targets, zoom support)

### Deliverables Checklist

- [ ] User research summary
- [ ] Competitive design analysis
- [ ] User personas (with goals, pain points)
- [ ] User journey maps (3-5 key journeys)
- [ ] Sitemap and navigation structure
- [ ] Wireframes (main pages)
- [ ] High-fidelity mockups (Figma)
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Interactive prototype
- [ ] Design system documentation
- [ ] Component specifications (50+ components)
- [ ] Design tokens file
- [ ] Accessibility audit report
- [ ] Conversion optimization recommendations
- [ ] Handoff documentation for development

### Tools & Templates
- Figma (design, prototyping)
- FIGMA_DESIGN_SYSTEM_TEMPLATE (from files/)
- Masterclass files for design patterns
- Accessibility tools (WCAG checklist)
- Prototype testing tools

### Integration with Other Agents

| Agent | Phase | Collaboration |
|-------|-------|---------------|
| **Briefing** | 1 | Understand user personas, goals |
| **Front-end** | 3 | Discuss implementation feasibility |
| **SEO** | 3 | Ensure readable, semantic layouts |
| **QA** | 5 | Validate design implementation accuracy |

### Success Criteria

✅ **User Satisfaction**: Design resonates with users  
✅ **Accessibility**: WCAG 2.1 AA compliance achieved  
✅ **Conversion**: CTA placement and copy optimized  
✅ **Responsiveness**: Works perfectly on all devices  
✅ **Performance**: Pages feel responsive and fast  

---

## 🛡️ Agente QA/Auditoria 🛡️

### Core Responsibility
**Validador final de qualidade que garante excelência antes do lançamento**

The QA/Audit Agent is the project's final checkpoint, ensuring everything meets quality standards before launch. They validate code, design, performance, and SEO implementation.

### Key Responsibilities

#### Phase-by-Phase

**Phase 5: Audit (Days 19-20)**

1. **Code Review & Quality**
   - Review all code against standards
   - Check TypeScript type safety
   - Validate test coverage (80%+)
   - Check for code smells
   - Review performance-critical sections
   - Security vulnerabilities check

2. **Functionality Testing**
   - Test all user flows
   - Test all forms and validations
   - Test error states
   - Test loading states
   - Cross-browser testing
   - Device testing (iOS, Android)

3. **Performance Testing**
   - Run Lighthouse audit
   - Check Core Web Vitals:
     - LCP < 2.5s ✅
     - FID < 100ms ✅
     - CLS < 0.1 ✅
   - Performance budget check
   - Network throttling test

4. **SEO Technical Audit**
   - Meta tags completeness
   - Structured data validation
   - Mobile-first design verification
   - Image optimization check
   - Internal linking verification
   - Sitemap validation
   - Robots.txt verification

5. **Accessibility Audit**
   - WCAG 2.1 AA compliance check
   - Keyboard navigation testing
   - Screen reader testing
   - Color contrast verification
   - Form accessibility check

6. **Design Accuracy Audit**
   - Compare implementation vs. design
   - Spacing/alignment validation
   - Color accuracy check
   - Typography accuracy check
   - Responsive design verification
   - Animation/transition verification

7. **Browser & Device Compatibility**
   - Chrome (latest 2 versions)
   - Firefox (latest 2 versions)
   - Safari (latest 2 versions)
   - Edge (latest 2 versions)
   - iOS devices (iPhone, iPad)
   - Android devices (various)
   - Tablet responsiveness

### Comprehensive Testing Checklist

**Functional Testing**
```
Homepage
- [ ] All sections visible and functional
- [ ] Navigation works correctly
- [ ] All links functional
- [ ] Forms submit correctly
- [ ] CTAs trigger correct actions
- [ ] Mobile layout correct

Blog/Content Pages
- [ ] Content displays correctly
- [ ] Images load and display correctly
- [ ] Code snippets formatted correctly
- [ ] Share buttons functional
- [ ] Related posts showing
- [ ] Comments system (if applicable)

Forms
- [ ] All fields required validation
- [ ] Email validation working
- [ ] Phone number validation (if applicable)
- [ ] Submit button disabled during submit
- [ ] Success message displays
- [ ] Error messages display correctly
- [ ] Mobile form submission works
```

**Performance Testing**
```
Lighthouse Audit
- [ ] Performance score > 90
- [ ] Accessibility score > 90
- [ ] Best Practices score > 90
- [ ] SEO score > 90
- [ ] LCP < 2.5s
- [ ] FID < 100ms
- [ ] CLS < 0.1

Network & Load
- [ ] Site loads on 3G connection
- [ ] Site loads on slow WiFi
- [ ] Large images optimized
- [ ] CSS/JS minified
- [ ] Code splitting working
- [ ] Caching headers correct
```

**SEO Audit**
```
On-Page
- [ ] Meta title present and unique (60 chars)
- [ ] Meta description present (160 chars)
- [ ] H1 present (one per page)
- [ ] H2/H3 hierarchy correct
- [ ] Keywords naturally included
- [ ] Internal links present and relevant

Technical
- [ ] Sitemap.xml accessible
- [ ] robots.txt correct
- [ ] Canonical URLs set
- [ ] Mobile-responsive
- [ ] Open Graph tags present
- [ ] Schema markup validates
- [ ] Images have alt text

Content
- [ ] Content matches intent
- [ ] Sufficient word count
- [ ] Readability score good
- [ ] External links to authority sources
- [ ] No broken links
```

**Accessibility Audit**
```
WCAG 2.1 AA Compliance
- [ ] Color contrast 4.5:1 for normal text
- [ ] Color contrast 3:1 for large text
- [ ] Keyboard navigation works
- [ ] Focus indicators visible
- [ ] Form labels associated correctly
- [ ] Alt text present for images
- [ ] Error messages linked to fields
- [ ] Screen reader compatibility tested
```

**Security Audit**
```
Basic Security
- [ ] HTTPS enforced
- [ ] No hardcoded secrets
- [ ] Environment variables used correctly
- [ ] CORS headers configured
- [ ] XSS prevention in place
- [ ] CSRF tokens (if applicable)
- [ ] Input validation present
- [ ] No sensitive data in logs
```

### Bug Severity Classification

| Severity | Description | Example | Fix Timeline |
|----------|-------------|---------|--------------|
| **Critical** | Breaks core functionality | Form doesn't submit | Before launch |
| **High** | Major feature broken | Wrong layout on mobile | Before launch |
| **Medium** | Feature partially broken | Button text cut off | Before or after launch |
| **Low** | Minor issues | Typo, color slightly off | After launch, next update |

### Deliverables Checklist

- [ ] Functional test report (all pass/fail)
- [ ] Performance audit report (Lighthouse scores)
- [ ] SEO technical audit report
- [ ] Accessibility audit report (WCAG compliance)
- [ ] Browser compatibility report
- [ ] Device testing report
- [ ] Security audit report
- [ ] Design accuracy verification
- [ ] Bug list (classified by severity)
- [ ] Bug fixes verification
- [ ] Launch readiness checklist
- [ ] Known issues documentation
- [ ] Post-launch monitoring plan

### Tools & Templates
- Lighthouse (performance/SEO/accessibility)
- Chrome DevTools (debugging)
- WCAG-EM Report Tool (accessibility audit)
- Browserstack (cross-browser testing)
- BrowserShots (screenshot comparison)
- axe DevTools (accessibility)
- CHECKLISTS_WORKSHEETS.md (all checklists)

### Integration with Other Agents

| Agent | Phase | Collaboration |
|-------|-------|---------------|
| **Front-end** | 4,5 | Code review, performance optimization |
| **SEO** | 5 | Technical SEO validation |
| **UX/UI** | 5 | Design accuracy verification |
| **Briefing** | 5 | Test against acceptance criteria |

### Success Criteria

✅ **Zero Critical/High Bugs**: All showstoppers fixed  
✅ **Performance Green**: All Lighthouse scores 90+  
✅ **Accessibility Compliant**: WCAG 2.1 AA achieved  
✅ **SEO Ready**: Technical SEO checklist 100% complete  
✅ **Design Accurate**: Matches design system exactly  
✅ **Cross-Browser**: Works on all major browsers/devices  

---

## 🔗 Agent Collaboration Framework

### Communication Protocol

**Daily Standups (15 min)**
- Each agent: 2 min status update
- Blockers and asks
- Next 24h priorities

**Phase Boundaries (Before → After)**
- Previous agent completes deliverables
- Hands off to next agent with documentation
- New agent reviews and asks clarifying questions
- Sign off on phase completion

**Decision Making**
- Proposal by lead agent
- Input from related agents (2 min each)
- Discussion (max 3 rounds)
- Consensus or escalate to project lead

### Handoff Documentation Template

```
FROM: [Agent Name]
TO: [Next Agent(s)]
DATE: [Date]
PHASE COMPLETED: [Phase #]

DELIVERABLES CHECKLIST:
- [ ] Item 1
- [ ] Item 2
- [ ] Item 3

KEY DECISIONS:
- Decision 1: [Context and reasoning]
- Decision 2: [Context and reasoning]

ASSUMPTIONS:
- Assumption 1
- Assumption 2

DEPENDENCIES:
- Dependency on: [Item]
- Blocker (if any): [Description]

QUESTIONS FOR NEXT AGENT:
- Question 1?
- Question 2?

FILES PROVIDED:
- [File 1]
- [File 2]
```

### Escalation Path

If consensus cannot be reached:
1. Present options to Briefing Agent
2. Briefing Agent consults client if needed
3. Client decision made
4. Team alignment

---

## 📊 Roles at a Glance

| Agent | Phase 1 | Phase 2 | Phase 3 | Phase 4 | Phase 5 | Phase 6 |
|-------|--------|--------|--------|--------|--------|--------|
| **Briefing** | LEAD | Support | - | - | Support | - |
| **Front-end** | - | LEAD | Support | LEAD | LEAD | Support |
| **SEO** | LEAD | LEAD | Support | LEAD | LEAD | LEAD |
| **UX/UI** | Support | Support | LEAD | Support | LEAD | - |
| **QA** | - | - | - | Support | LEAD | LEAD |

- **LEAD** = Primary responsibility
- **Support** = Secondary input/validation
- **-** = Not involved in this phase

---

## 🎯 Key Metrics by Role

### Briefing Agent
- Briefing completeness score (100%)
- Stakeholder satisfaction (NPS)
- Requirement clarity (0 clarification requests needed)

### Front-end Agent
- Code coverage (80%+)
- TypeScript type safety (0% any types)
- Lighthouse performance score (95+)
- Core Web Vitals (all green)

### SEO Agent
- Keyword coverage (50-100 keywords)
- Technical SEO score (100%)
- Organic traffic (month 6+ target)
- Keyword ranking (top 10 for mains)

### UX/UI Agent
- Design system completeness (50+ components)
- Accessibility score (WCAG 2.1 AA)
- Mobile usability score (90+)
- User satisfaction (NPS)

### QA Agent
- Bug discovery rate (all critical/high found)
- Test coverage (80%+)
- Lighthouse scores (90+ all categories)
- Browser compatibility (100% tested)

---

**Version:** 1.0 | **Status:** ✅ Complete | **Last Updated:** April 2026


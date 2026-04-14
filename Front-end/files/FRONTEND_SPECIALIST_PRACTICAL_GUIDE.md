# Frontend Specialist - Guia Prático & Exemplos

## Estrutura de Projeto React + Tailwind + shadcn/ui

```
meu-frontend/
├── src/
│   ├── components/
│   │   ├── Atoms/
│   │   │   ├── Button.jsx
│   │   │   ├── Badge.jsx
│   │   │   ├── Input.jsx
│   │   │   └── Label.jsx
│   │   ├── Molecules/
│   │   │   ├── FormGroup.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   ├── Pagination.jsx
│   │   │   └── Card.jsx
│   │   ├── Organisms/
│   │   │   ├── Header.jsx
│   │   │   ├── Navigation.jsx
│   │   │   ├── Footer.jsx
│   │   │   ├── Hero.jsx
│   │   │   └── FeatureGrid.jsx
│   │   └── layouts/
│   │       ├── MainLayout.jsx
│   │       ├── DashboardLayout.jsx
│   │       └── AuthLayout.jsx
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Product/
│   │   │   ├── index.jsx
│   │   │   ├── [id].jsx
│   │   │   └── new.jsx
│   │   └── 404.jsx
│   ├── styles/
│   │   ├── globals.css
│   │   ├── tailwind.css
│   │   └── animations.css
│   ├── hooks/
│   │   ├── useMedia.js
│   │   ├── useFetch.js
│   │   └── useLocalStorage.js
│   ├── utils/
│   │   ├── cn.js (class name merger)
│   │   ├── formatters.js
│   │   └── validators.js
│   └── App.jsx
├── public/
│   ├── fonts/
│   └── images/
├── tailwind.config.js
├── next.config.js (ou vite.config.js)
└── package.json
```

---

## 1️⃣ Exemplos de Componentes Básicos

### Button Atom

```jsx
// components/Atoms/Button.jsx
import { forwardRef } from 'react';
import { cn } from '@/utils/cn';

const Button = forwardRef(
  ({ 
    children, 
    variant = 'primary', 
    size = 'md',
    isLoading = false,
    disabled = false,
    className,
    ...props 
  }, ref) => {
    const baseStyles = "font-semibold transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2";
    
    const variants = {
      primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-500",
      secondary: "bg-gray-200 text-gray-900 hover:bg-gray-300 focus:ring-gray-400",
      outline: "border-2 border-blue-600 text-blue-600 hover:bg-blue-50 focus:ring-blue-500",
      ghost: "text-blue-600 hover:bg-blue-50 focus:ring-blue-500",
      danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-500"
    };
    
    const sizes = {
      sm: "px-3 py-1.5 text-sm rounded-md",
      md: "px-4 py-2 text-base rounded-lg",
      lg: "px-6 py-3 text-lg rounded-lg",
      icon: "p-2 rounded-lg"
    };
    
    return (
      <button
        ref={ref}
        disabled={disabled || isLoading}
        className={cn(
          baseStyles,
          variants[variant],
          sizes[size],
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        {...props}
      >
        {isLoading ? <span className="animate-spin">⏳</span> : children}
      </button>
    );
  }
);

Button.displayName = "Button";
export default Button;
```

### Input Atom

```jsx
// components/Atoms/Input.jsx
import { forwardRef } from 'react';
import { cn } from '@/utils/cn';

const Input = forwardRef(({ 
  error, 
  className, 
  ...props 
}, ref) => {
  return (
    <input
      ref={ref}
      className={cn(
        "w-full px-3 py-2 border rounded-lg font-base transition-colors",
        "focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
        "placeholder-gray-400 text-gray-900",
        error && "border-red-500 focus:ring-red-500",
        !error && "border-gray-300",
        className
      )}
      {...props}
    />
  );
});

Input.displayName = "Input";
export default Input;
```

---

## 2️⃣ Exemplos de Componentes Compostos

### Card Molecule

```jsx
// components/Molecules/Card.jsx
import { cn } from '@/utils/cn';

export function Card({ 
  className, 
  children, 
  variant = 'default',
  interactive = false,
  ...props 
}) {
  const variants = {
    default: "border border-gray-200 shadow-sm",
    elevated: "shadow-md",
    flat: "bg-gray-50"
  };
  
  return (
    <div
      className={cn(
        "rounded-lg p-4 bg-white transition-all",
        interactive && "cursor-pointer hover:shadow-lg",
        variants[variant],
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({ className, ...props }) {
  return <div className={cn("mb-4 pb-4 border-b", className)} {...props} />;
}

export function CardTitle({ className, ...props }) {
  return <h2 className={cn("text-xl font-bold text-gray-900", className)} {...props} />;
}

export function CardContent({ className, ...props }) {
  return <div className={cn("text-gray-600", className)} {...props} />;
}

export function CardFooter({ className, ...props }) {
  return <div className={cn("mt-4 pt-4 border-t flex gap-3", className)} {...props} />;
}
```

**Uso:**
```jsx
<Card variant="elevated">
  <CardHeader>
    <CardTitle>Bem-vindo</CardTitle>
  </CardHeader>
  <CardContent>
    Conteúdo principal aqui
  </CardContent>
  <CardFooter>
    <Button variant="primary">Salvar</Button>
  </CardFooter>
</Card>
```

### FormGroup Molecule

```jsx
// components/Molecules/FormGroup.jsx
import Input from '@/components/Atoms/Input';
import Label from '@/components/Atoms/Label';
import { cn } from '@/utils/cn';

export function FormGroup({ 
  label, 
  error, 
  required = false,
  helperText,
  className,
  ...inputProps 
}) {
  return (
    <div className={cn("flex flex-col gap-1", className)}>
      {label && (
        <Label>
          {label}
          {required && <span className="text-red-500 ml-1">*</span>}
        </Label>
      )}
      <Input error={error} {...inputProps} />
      {error && (
        <p className="text-sm text-red-500">{error}</p>
      )}
      {helperText && (
        <p className="text-sm text-gray-500">{helperText}</p>
      )}
    </div>
  );
}
```

---

## 3️⃣ Exemplos de Seções (Organisms)

### Hero Section

```jsx
// components/Organisms/HeroSection.jsx
import Button from '@/components/Atoms/Button';

export function HeroSection({ 
  title, 
  subtitle, 
  backgroundImage,
  cta1Text = "Get Started",
  cta2Text = "Learn More"
}) {
  return (
    <section 
      className="relative w-full min-h-screen flex items-center justify-center overflow-hidden"
      style={{
        backgroundImage: `linear-gradient(135deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.2) 100%), url(${backgroundImage})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }}
    >
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-transparent to-white/5" />
      
      <div className="relative z-10 text-center max-w-2xl mx-auto px-4 py-20">
        <h1 className="text-5xl md:text-6xl font-bold text-white mb-6 leading-tight">
          {title}
        </h1>
        
        {subtitle && (
          <p className="text-xl md:text-2xl text-gray-100 mb-8 font-light">
            {subtitle}
          </p>
        )}
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Button size="lg" variant="primary">
            {cta1Text}
          </Button>
          <Button size="lg" variant="outline" className="border-white text-white hover:bg-white/10">
            {cta2Text}
          </Button>
        </div>
      </div>
    </section>
  );
}
```

### Feature Grid Section

```jsx
// components/Organisms/FeatureGrid.jsx
import Card from '@/components/Molecules/Card';
import { cn } from '@/utils/cn';

export function FeatureGrid({ 
  title, 
  subtitle, 
  features = [],
  columns = 3 
}) {
  return (
    <section className="w-full py-20 px-4 bg-gray-50">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          {title && (
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              {title}
            </h2>
          )}
          {subtitle && (
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              {subtitle}
            </p>
          )}
        </div>
        
        {/* Grid */}
        <div className={cn(
          "grid gap-8",
          columns === 3 && "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
          columns === 2 && "grid-cols-1 md:grid-cols-2",
          columns === 4 && "grid-cols-1 md:grid-cols-2 lg:grid-cols-4"
        )}>
          {features.map((feature, idx) => (
            <Card key={idx} className="text-center hover:shadow-lg transition-shadow">
              {feature.icon && (
                <div className="text-4xl mb-4">{feature.icon}</div>
              )}
              <h3 className="text-lg font-bold text-gray-900 mb-2">
                {feature.title}
              </h3>
              <p className="text-gray-600">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
}
```

**Uso:**
```jsx
<FeatureGrid 
  title="Nossas Features"
  subtitle="Tudo que você precisa em um só lugar"
  features={[
    {
      icon: "⚡",
      title: "Rápido",
      description: "Otimizado para performance"
    },
    {
      icon: "🔒",
      title: "Seguro",
      description: "Encriptação end-to-end"
    },
    {
      icon: "🎨",
      title: "Lindo",
      description: "Design moderno e responsivo"
    }
  ]}
  columns={3}
/>
```

---

## 4️⃣ Exemplo de Page Completa

```jsx
// pages/Home.jsx
import MainLayout from '@/components/layouts/MainLayout';
import { HeroSection } from '@/components/Organisms/HeroSection';
import { FeatureGrid } from '@/components/Organisms/FeatureGrid';
import { PricingSection } from '@/components/Organisms/PricingSection';
import { TestimonialSection } from '@/components/Organisms/TestimonialSection';
import { CTASection } from '@/components/Organisms/CTASection';

export default function Home() {
  return (
    <MainLayout>
      {/* Hero */}
      <HeroSection 
        title="Transforme sua ideia em realidade"
        subtitle="Plataforma moderna para criar interfaces web incríveis"
        backgroundImage="/images/hero-bg.jpg"
      />
      
      {/* Features */}
      <FeatureGrid 
        title="Por que nos escolher?"
        subtitle="Tudo que você precisa para ter sucesso"
        features={[
          {
            icon: "⚡",
            title: "Super Rápido",
            description: "Carregamento instantâneo e performance otimizada"
          },
          {
            icon: "🛡️",
            title: "Segurança",
            description: "Proteção de dados com encriptação militar"
          },
          {
            icon: "📱",
            title: "Responsivo",
            description: "Funciona perfeito em qualquer dispositivo"
          },
          {
            icon: "🎨",
            title: "Customizável",
            description: "Temas e layouts personalizáveis"
          },
          {
            icon: "🌍",
            title: "Global",
            description: "Suportado em múltiplos idiomas e regiões"
          },
          {
            icon: "🚀",
            title: "Escalável",
            description: "Cresce com seu negócio"
          }
        ]}
        columns={3}
      />
      
      {/* Pricing */}
      <PricingSection />
      
      {/* Testimonials */}
      <TestimonialSection />
      
      {/* Final CTA */}
      <CTASection />
    </MainLayout>
  );
}
```

---

## 5️⃣ Tailwind CSS Úteis

### Paletas de Cores Padrão

```css
/* Primary Colors */
.bg-primary-50   /* Lightest */
.bg-primary-100
.bg-primary-200
...
.bg-primary-900  /* Darkest */

/* Common Utilities */
.text-gray-900   /* Dark text */
.bg-white        /* White background */
.border-gray-200 /* Light border */
.shadow-md       /* Medium shadow */
.rounded-lg      /* Border radius */
.hover:shadow-lg /* Hover state */
```

### Responsive Classes

```jsx
// Mobile-first approach
<div className="
  block              /* Default (mobile) */
  md:flex             /* Tablets and up */
  lg:grid             /* Large screens and up */
  lg:grid-cols-3      /* 3-column on large screens */
  gap-4               /* Gap on all sizes */
  md:gap-6            /* Bigger gap on tablets */
">
  {/* Content */}
</div>
```

### Dark Mode

```jsx
// tailwind.config.js
module.exports = {
  darkMode: 'class', // or 'media'
  // ...
}

// Usage
<div className="bg-white dark:bg-gray-900 text-gray-900 dark:text-white">
  Conteúdo que muda com dark mode
</div>
```

---

## 6️⃣ Padrões Úteis

### Utility Merge (cn function)

```jsx
// utils/cn.js
export function cn(...classes) {
  return classes
    .flat()
    .filter(Boolean)
    .join(' ');
}

// Uso
import { cn } from '@/utils/cn';

<Button className={cn(
  "w-full",
  isActive && "bg-blue-600",
  disabled && "opacity-50"
)}>
  Click
</Button>
```

### Hook para Media Queries

```jsx
// hooks/useMedia.js
import { useEffect, useState } from 'react';

export function useMedia(query) {
  const [matches, setMatches] = useState(false);
  
  useEffect(() => {
    const media = window.matchMedia(query);
    
    if (media.matches !== matches) {
      setMatches(media.matches);
    }
    
    const listener = () => setMatches(media.matches);
    media.addListener(listener);
    
    return () => media.removeListener(listener);
  }, [matches, query]);
  
  return matches;
}

// Uso
const isMobile = useMedia('(max-width: 768px)');

{isMobile ? <MobileNav /> : <DesktopNav />}
```

### Hook para Fetch com Loading

```jsx
// hooks/useFetch.js
import { useEffect, useState } from 'react';

export function useFetch(url) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) throw new Error('Failed to fetch');
        const json = await response.json();
        setData(json);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [url]);
  
  return { data, error, loading };
}

// Uso
const { data, loading, error } = useFetch('/api/users');

{loading && <Spinner />}
{error && <ErrorMessage message={error} />}
{data && <UserList users={data} />}
```

---

## 7️⃣ Checklist de Performance

### Imagens
- [ ] Use `<Image>` do Next.js (auto-optimization)
- [ ] Lazy load com `loading="lazy"`
- [ ] Use WebP com fallback
- [ ] Optimize file size (Tinypng, ImageOptim)

### Code
- [ ] Code splitting com `dynamic import`
- [ ] Tree shaking (remove unused code)
- [ ] Minify CSS, JS
- [ ] Remove console.logs em produção

### Assets
- [ ] Inline critical CSS
- [ ] Defer non-critical JS
- [ ] Async load fonts
- [ ] Cache-busting com hash

### Lighthouse Score
- [ ] Performance: 90+
- [ ] Accessibility: 90+
- [ ] Best Practices: 90+
- [ ] SEO: 90+

---

## 8️⃣ Checklist de Acessibilidade

- [ ] Semantic HTML (`<header>`, `<nav>`, `<main>`, `<footer>`)
- [ ] Color contrast 4.5:1 (normal text), 3:1 (large text)
- [ ] Keyboard navigation (Tab, Enter, Esc)
- [ ] Focus states visíveis
- [ ] ARIA labels e roles onde necessário
- [ ] Alt text em todas as imagens
- [ ] Form labels associados a inputs
- [ ] Error messages associadas a fields
- [ ] Screen reader support testado

---

**Última atualização**: Abril 2026
**Baseado em**: Padrões da indústria + boas práticas consolidadas

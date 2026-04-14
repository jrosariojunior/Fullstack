# Frontend Specialist - Guia de Decisão Tecnológica

## 🎯 Escolha seu tipo de projeto

---

## 1. SaaS / Aplicação Web Complexa

### Características
- Dashboard com dados em tempo real
- Múltiplas páginas e rotas
- Gerenciamento de estado complexo
- Autenticação e autorização
- APIs RESTful ou GraphQL

### Stack Recomendado
```
Frontend:  React + TypeScript + Next.js
Styling:   Tailwind CSS + shadcn/ui
State:     Redux / Zustand / Context API
API:       TanStack Query (React Query)
Forms:     React Hook Form + Zod
Testing:   Vitest + React Testing Library
```

### Estrutura de Pastas
```
src/
├── app/                    (Next.js App Router)
├── components/
│   ├── (components de UI)
│   └── (features específicas)
├── pages/                  (Routes)
├── hooks/
├── stores/                 (State management)
├── services/               (API calls)
├── types/                  (TypeScript types)
└── utils/
```

### Exemplo de Arquitetura
```
pages/dashboard/
├── page.tsx               (Page component)
├── layout.tsx             (Page layout)
└── components/
    ├── ChartCard.tsx
    ├── DataTable.tsx
    └── MetricsGrid.tsx

services/
├── api.ts                 (Axios/Fetch config)
├── userService.ts
├── dataService.ts
└── authService.ts

stores/
├── authStore.ts           (Zustand)
├── userStore.ts
└── appStore.ts

hooks/
├── useAuth.ts
├── useFetch.ts
└── useLocalStorage.ts
```

### Ferramentas Essenciais
- [ ] Next.js 14+ com App Router
- [ ] TypeScript para type safety
- [ ] Tailwind CSS + shadcn/ui
- [ ] TanStack Query para data fetching
- [ ] Zustand ou Redux para state
- [ ] Jest + React Testing Library
- [ ] Storybook para componentes

---

## 2. Landing Page / Marketing Site

### Características
- Conversão é objetivo principal
- SEO importante
- Múltiplas seções reutilizáveis
- Contato/Newsletter CTA
- Pode ser estático

### Stack Recomendado
```
Frontend:  Next.js (Static Generation)
Styling:   Tailwind CSS
Animações: GSAP / Framer Motion
CMS:       Contentful / Sanity (opcional)
Forms:     Formspree / Basin
Analytics: Google Analytics 4
```

### Estrutura
```
src/
├── app/
│   ├── page.tsx                    (Home)
│   ├── about/page.tsx
│   ├── pricing/page.tsx
│   ├── blog/[slug]/page.tsx
│   └── layout.tsx
├── components/
│   ├── sections/
│   │   ├── HeroSection.tsx
│   │   ├── FeatureSection.tsx
│   │   ├── PricingSection.tsx
│   │   ├── TestimonialSection.tsx
│   │   └── CTASection.tsx
│   ├── navigation/
│   │   ├── Header.tsx
│   │   └── Footer.tsx
│   └── forms/
│       └── ContactForm.tsx
├── content/
│   ├── blog/
│   │   ├── post-1.mdx
│   │   └── post-2.mdx
│   └── pages/
└── styles/
    └── globals.css
```

### Next.js Config
```javascript
// next.config.js
module.exports = {
  // Static generation padrão
  output: 'export', // Se for totalmente estático
  
  // Image optimization
  images: {
    unoptimized: true, // Para exportação estática
  },
  
  // ISR (Incremental Static Regeneration)
  // revalidate: 60 em getStaticProps
}
```

### Exemplo de Página com ISR
```typescript
// app/blog/[slug]/page.tsx
import { notFound } from 'next/navigation';

export const revalidate = 3600; // Revalidate a cada hora

export async function generateStaticParams() {
  const posts = await getPosts();
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({ params }) {
  const post = await getPost(params.slug);
  if (!post) notFound();
  
  return <Article post={post} />;
}
```

### SEO Setup
```typescript
// app/page.tsx
import { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Empresa X - Solução Inovadora',
  description: 'Descrição da empresa e serviços',
  openGraph: {
    title: 'Empresa X',
    description: 'Descrição breve',
    images: [
      {
        url: '/og-image.jpg',
        width: 1200,
        height: 630,
      },
    ],
  },
};

export default function Home() {
  // ...
}
```

---

## 3. E-commerce

### Características
- Catálogo de produtos
- Carrinho de compras
- Checkout
- Pagamento integrado
- Inventory management
- Recomendações

### Stack Recomendado
```
Frontend:  Next.js + React
Styling:   Tailwind CSS
E-commerce: Shopify (headless) / WooCommerce / Medusa
Payments:  Stripe / PayPal
Search:    Algolia / Elasticsearch
Cart:      Zustand
Analytics: Mixpanel / Amplitude
```

### Shopify Headless Example
```typescript
// services/shopifyService.ts
const query = `
  query GetProducts {
    products(first: 10) {
      edges {
        node {
          id
          title
          handle
          priceRange {
            minVariantPrice {
              amount
            }
          }
          images(first: 1) {
            edges {
              node {
                url
              }
            }
          }
        }
      }
    }
  }
`;

export async function getProducts() {
  const response = await fetch(
    `https://${SHOPIFY_STORE}.myshopify.com/api/2024-01/graphql.json`,
    {
      method: 'POST',
      headers: {
        'X-Shopify-Storefront-Access-Token': STOREFRONT_ACCESS_TOKEN,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    }
  );
  
  return response.json();
}
```

### Estrutura de E-commerce
```
src/
├── components/
│   ├── ProductCard.tsx
│   ├── ProductGallery.tsx
│   ├── ProductFilter.tsx
│   ├── ShoppingCart.tsx
│   ├── Checkout.tsx
│   └── PaymentForm.tsx
├── pages/
│   ├── products/index.tsx
│   ├── products/[handle].tsx
│   ├── cart/page.tsx
│   └── checkout/page.tsx
├── services/
│   ├── shopifyService.ts
│   ├── cartService.ts
│   └── orderService.ts
├── stores/
│   └── cartStore.ts          (Zustand)
└── hooks/
    ├── useCart.ts
    ├── useProductFilters.ts
    └── useCheckout.ts
```

### Cart Store Example
```typescript
// stores/cartStore.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface CartItem {
  id: string;
  title: string;
  price: number;
  quantity: number;
}

interface CartStore {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (id: string) => void;
  updateQuantity: (id: string, quantity: number) => void;
  clear: () => void;
  total: number;
}

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      
      addItem: (item) => set((state) => {
        const existing = state.items.find(i => i.id === item.id);
        if (existing) {
          existing.quantity += item.quantity;
          return { items: [...state.items] };
        }
        return { items: [...state.items, item] };
      }),
      
      removeItem: (id) => set((state) => ({
        items: state.items.filter(item => item.id !== id),
      })),
      
      updateQuantity: (id, quantity) => set((state) => ({
        items: state.items.map(item =>
          item.id === id ? { ...item, quantity } : item
        ),
      })),
      
      clear: () => set({ items: [] }),
      
      get total() {
        return get().items.reduce((sum, item) => sum + item.price * item.quantity, 0);
      },
    }),
    {
      name: 'cart-store',
    }
  )
);
```

---

## 4. Portfolio / Blog Pessoal

### Características
- Conteúdo estático em Markdown/MDX
- SEO importante
- Performance crítica
- Portfolio de trabalhos
- Posts e artigos

### Stack Recomendado
```
Frontend:  Astro (excelente para conteúdo)
Styling:   Tailwind CSS
Content:   Markdown / MDX
Search:    Pagefind (local)
Deploy:    Vercel / Netlify
```

### Estrutura Astro
```
src/
├── pages/
│   ├── index.astro           (Home)
│   ├── about.astro
│   ├── blog/
│   │   ├── index.astro
│   │   └── [slug].astro
│   └── projects/
│       └── [slug].astro
├── layouts/
│   ├── BaseLayout.astro
│   └── PostLayout.astro
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── ProjectCard.astro
│   └── PostCard.astro
└── content/
    ├── blog/
    │   ├── first-post.md
    │   └── second-post.mdx
    └── projects/
        └── project-1.md
```

### Astro Content Collections
```typescript
// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    author: z.string(),
    tags: z.array(z.string()),
    image: z.string().optional(),
  }),
});

export const collections = { blog };
```

### Página Dinâmica
```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';
import PostLayout from '../../layouts/PostLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map(post => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<PostLayout {post}>
  <Content />
</PostLayout>
```

---

## 5. Admin Dashboard

### Características
- Múltiplas páginas e seções
- Tabelas com dados dinâmicos
- Formulários complexos
- Análises e gráficos
- Real-time updates
- Multi-tenant

### Stack Recomendado
```
Frontend:  React + TypeScript + Next.js
Styling:   Tailwind CSS + shadcn/ui
State:     Redux / Zustand
Data:      TanStack Query
Charts:    Recharts / Chart.js
Tables:    TanStack Table (React Table)
Forms:     React Hook Form + Zod
Real-time: Socket.io / Supabase Realtime
```

### Template Estrutura
```
src/
├── app/
│   ├── dashboard/
│   │   ├── page.tsx                (Overview)
│   │   ├── layout.tsx
│   │   ├── users/
│   │   │   ├── page.tsx            (List)
│   │   │   ├── [id]/page.tsx       (Detail)
│   │   │   └── new/page.tsx        (Create)
│   │   ├── analytics/
│   │   │   └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
├── components/
│   ├── dashboard/
│   │   ├── Sidebar.tsx
│   │   ├── Header.tsx
│   │   ├── DataTable.tsx
│   │   ├── ChartCard.tsx
│   │   └── MetricsCard.tsx
│   └── forms/
│       ├── UserForm.tsx
│       └── SettingsForm.tsx
├── hooks/
│   ├── useUsers.ts
│   └── useAnalytics.ts
└── services/
    └── api.ts
```

### Exemplo Data Table com TanStack
```typescript
// components/dashboard/DataTable.tsx
import {
  flexRender,
  getCoreRowModel,
  getPaginationRowModel,
  getSortedRowModel,
  useReactTable,
} from '@tanstack/react-table';

export function DataTable({ columns, data }) {
  const [sorting, setSorting] = useState([]);
  const [pagination, setPagination] = useState({
    pageIndex: 0,
    pageSize: 10,
  });

  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    state: {
      sorting,
      pagination,
    },
    onSortingChange: setSorting,
    onPaginationChange: setPagination,
  });

  return (
    <div>
      <table className="w-full border-collapse border">
        <thead>
          {table.getHeaderGroups().map(headerGroup => (
            <tr key={headerGroup.id}>
              {headerGroup.headers.map(header => (
                <th
                  key={header.id}
                  onClick={header.column.getToggleSortingHandler()}
                  className="cursor-pointer border p-2 text-left"
                >
                  {flexRender(
                    header.column.columnDef.header,
                    header.getContext()
                  )}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <tbody>
          {table.getRowModel().rows.map(row => (
            <tr key={row.id}>
              {row.getVisibleCells().map(cell => (
                <td key={cell.id} className="border p-2">
                  {flexRender(
                    cell.column.columnDef.cell,
                    cell.getContext()
                  )}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>

      <div className="flex items-center justify-between p-4">
        <button
          onClick={() => table.previousPage()}
          disabled={!table.getCanPreviousPage()}
        >
          Previous
        </button>
        <span>
          Page {table.getState().pagination.pageIndex + 1} of{' '}
          {table.getPageCount()}
        </span>
        <button
          onClick={() => table.nextPage()}
          disabled={!table.getCanNextPage()}
        >
          Next
        </button>
      </div>
    </div>
  );
}
```

---

## 6. Single Page Application (SPA) - Sem Server-Side

### Características
- Totalmente client-side
- Local state gerenciamento
- PWA capabilities
- Offline support
- Pode usar service workers

### Stack Recomendado
```
Frontend:  React + TypeScript + Vite
Styling:   Tailwind CSS + shadcn/ui
Router:    TanStack Router / React Router v6
State:     Redux / Zustand
Storage:   IndexedDB / LocalStorage
Deploy:    Vercel / Netlify
```

### Vite Config
```javascript
// vite.config.ts
import react from '@vitejs/plugin-react';
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  build: {
    // Code splitting
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom'],
        },
      },
    },
  },
});
```

### TanStack Router Setup
```typescript
// src/routes/__root.tsx
import { createRootRoute, Outlet } from '@tanstack/react-router';
import Layout from '../components/Layout';

export const Route = createRootRoute({
  component: () => (
    <Layout>
      <Outlet />
    </Layout>
  ),
});

// src/routes/index.tsx
export const Route = createFileRoute('/')({
  component: HomePage,
});

// src/routes/users.$id.tsx
export const Route = createFileRoute('/users/$id')({
  component: UserDetailPage,
});
```

---

## 🎯 Matriz de Decisão Rápida

| Tipo de Projeto | Framework | Styling | State | Hospedagem |
|-----------------|-----------|---------|-------|------------|
| SaaS | Next.js | Tailwind | Zustand | Vercel |
| Landing Page | Next.js | Tailwind | Context | Vercel |
| E-commerce | Next.js | Tailwind | Zustand | Vercel |
| Blog/Portfolio | Astro | Tailwind | N/A | Vercel |
| Admin Dashboard | Next.js | Tailwind | Redux | Vercel |
| SPA | Vite + React | Tailwind | Zustand | Netlify |
| Mobile App | React Native | NativeWind | Redux | Expo |

---

## 🚀 Performance Checklist por Tipo

### Landing Page
- [ ] Lighthouse 95+ em todos os metrics
- [ ] First Contentful Paint < 1.5s
- [ ] Largest Contentful Paint < 2.5s
- [ ] Cumulative Layout Shift < 0.1
- [ ] SSG (Static Generation)
- [ ] Image optimization obrigatória

### SaaS Dashboard
- [ ] Time to Interactive < 3s
- [ ] API response caching
- [ ] Component code splitting
- [ ] Virtual scrolling para listas grandes
- [ ] Optimistic updates
- [ ] Error boundaries

### E-commerce
- [ ] Product images otimizadas (WebP + AVIF)
- [ ] Skeleton loading states
- [ ] Cart persists to local storage
- [ ] Checkout flow otimizado (< 3 steps)
- [ ] Payment gateway integração segura
- [ ] Analytics tracking

---

**Última atualização**: Abril 2026
**Baseado em**: Padrões da indústria e boas práticas consolidadas

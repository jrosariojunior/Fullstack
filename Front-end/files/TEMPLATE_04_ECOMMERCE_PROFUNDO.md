# 🛍️ TEMPLATE #4 PROFUNDO: E-COMMERCE STORE
## Next.js 16 + Tailwind CSS v4.2 - Análise Completa Visual + Técnica

---

## 📋 VISÃO GERAL DO TEMPLATE

**Nome:** CozyCommerce / NextMerce (SaaS E-commerce)  
**Tipo:** Full E-commerce Solution  
**Stack:** Next.js 16 + Tailwind CSS 4.2 + React 19 + TypeScript 5.9  
**Integrações:** Stripe (pagamentos), Sanity (CMS), Algolia (busca)  
**UI Components:** 100+  
**Páginas:** 20+  
**Funcionalidades:** Product catalog, cart, checkout, admin, search, filters, reviews  
**Design Pattern:** Modern, clean, conversion-focused  

---

## 🎨 PALETA DE CORES PADRÃO (E-commerce)

### Cores Principais

```
PRIMARY (Conversão):
├── Blue:            #3B82F6 (buttons, links)
├── Light Blue:      #EFF6FF (hover backgrounds)
├── Dark Blue:       #2563EB (hover state)
└── Teal accent:     #14B8A6 (highlights)

PRODUCT COLORS:
├── Price text:      #10B981 (green - positive)
├── Original price:  #9CA3AF (strikethrough gray)
├── Sale badge:      #EF4444 (red - urgent)
└── In stock:        #10B981 (green)

OUT OF STOCK:
├── Disabled state:  #D1D5DB (gray-300)
├── Text:            #9CA3AF (gray-400)
└── Opacity:         50%

NEUTRALS (Foundation):
├── White:           #FFFFFF
├── Gray 50:         #F9FAFB (card backgrounds)
├── Gray 100:        #F3F4F6 (subtle backgrounds)
├── Gray 200:        #E5E7EB (borders, dividers)
├── Gray 300:        #D1D5DB (input borders)
├── Gray 400:        #9CA3AF (placeholder text)
├── Gray 500:        #6B7280 (secondary text) ← DEFAULT
├── Gray 600:        #4B5563 (labels)
├── Gray 700:        #374151 (body text)
├── Gray 800:        #1F2937 (headings)
└── Gray 900:        #111827 (darkest)

SEMANTIC (Status):
├── Success:         #10B981 (green - in stock)
├── Error:           #EF4444 (red - error)
├── Warning:         #F59E0B (amber - limited)
├── Info:            #0EA5E9 (cyan - info)
└── Discount:        #EC4899 (pink - sale)
```

### Dark Mode Colors

```
:root {
  --bg-primary: #FFFFFF;
  --bg-secondary: #F9FAFB;
  --text-primary: #1F2937;
  --text-secondary: #6B7280;
  --border: #E5E7EB;
}

@media (prefers-color-scheme: dark) {
  --bg-primary: #0F172A;
  --bg-secondary: #1F2937;
  --text-primary: #F9FAFB;
  --text-secondary: #D1D5DB;
  --border: #4B5563;
}
```

---

## 📱 SEÇÃO #1: HOMEPAGE STOREFRONT

### Visual Layout (Desktop)

```
┌──────────────────────────────────────────────┐
│ [Logo] [Search] [Cart] [Account] [Menu]      │ ← Header 64px
├──────────────────────────────────────────────┤
│                                              │
│  [Hero Banner Image] (Full width)            │  ← 400px height
│  "Summer Collection 2026"                    │
│  "Save up to 50% on selected items"          │
│  [Shop Now]                                  │
│                                              │ ← 80px spacing
├──────────────────────────────────────────────┤
│ FEATURED CATEGORIES                          │
│ [Category 1] [Category 2] [Category 3] ...   │  ← 4 grid items
│  with icon                                   │
│                                              │ ← 64px spacing
├──────────────────────────────────────────────┤
│ NEW ARRIVALS                                 │
│ [Product] [Product] [Product] [Product]      │  ← 4-column grid
│ Images, name, price, rating, button          │
│                                              │ ← 64px spacing
├──────────────────────────────────────────────┤
│ SALE/PROMOTION SECTION                       │
│ [50% OFF Today Only]                         │  ← 2-column layout
│ [Limited Time Offer]                         │
│                                              │ ← 64px spacing
├──────────────────────────────────────────────┤
│ BESTSELLERS                                  │
│ [Product] [Product] [Product] [Product]      │  ← 4-column grid
│                                              │ ← 64px spacing
├──────────────────────────────────────────────┤
│ NEWSLETTER SIGNUP                            │
│ "Subscribe to get exclusive offers"          │  ← 300px width form
│ [Email input] [Subscribe button]             │
│                                              │
├──────────────────────────────────────────────┤
│ FOOTER                                       │
└──────────────────────────────────────────────┘
```

### Header Navigation (Sticky)

```
HEADER CONTAINER:
  Height:             64px
  Position:           sticky top-0 z-40
  Background:         #FFFFFF
  Border-bottom:      1px solid #E5E7EB
  Padding:            0 40px (desktop) / 16px (mobile)
  Display:            flex justify-between items-center
  Gap:                32px

LOGO:
  Height:             40px
  Aspect-ratio:       1/1
  Margin-right:       auto

SEARCH BAR:
  Width:              300px (hidden on mobile)
  Height:             40px
  Padding:            10px 12px
  Border:             1px solid #E5E7EB
  Border-radius:      8px
  Background:         #F9FAFB
  
  Icon (magnifying):  20px gray-400 left side
  Placeholder:        "Search products..."
  
  Focus:
    Border:           2px solid #3B82F6
    Background:       #FFFFFF
    Box-shadow:       0 0 0 3px rgba(59,130,246,0.1)

ICONS (Right side):
  Layout:             flex gap-16px items-center
  
  Icons:
    Wishlist:         ♡ heart outline
    Cart:             shopping bag
    Account:          user circle
  
  Each icon:
    Size:             24px
    Color:            #6B7280
    Hover:            #3B82F6
    Cursor:           pointer
  
  Badge (cart count):
    Position:         absolute top-right
    Size:             16px circular
    Background:       #EF4444
    Color:            #FFFFFF
    Font:             12px weight-600
    Border-radius:    full

MOBILE MENU ICON (Hamburger):
  Display:            none (desktop)
  Display:            block (< 768px)
  Size:               24px
  Color:              #1F2937
```

### Hero Banner Section

```
BANNER CONTAINER:
  Width:              100%
  Height:             400px
  Background:         linear-gradient(135deg, #3B82F6, #14B8A6)
  Or:                 background-image: url('hero.jpg')
  Background-size:    cover
  Background-position: center
  Overflow:           hidden
  Position:           relative

OVERLAY (optional):
  Position:           absolute inset-0
  Background:         rgba(0,0,0,0.3)
  Z-index:            1

CONTENT (centered):
  Position:           absolute inset-0
  Display:            flex flex-col justify-center items-center
  Z-index:            2
  Text-align:         center
  Color:              #FFFFFF

  MAIN TEXT:
    Font:             Inter weight-700
    Size:             56px
    Color:            #FFFFFF
    Text-shadow:      0 2px 8px rgba(0,0,0,0.2)
    Margin-bottom:    16px
  
  SUB TEXT:
    Font:             Inter weight-400
    Size:             20px
    Color:            rgba(255,255,255,0.9)
    Margin-bottom:    32px
  
  BUTTON:
    Height:           48px
    Padding:          12px 32px
    Background:       #FFFFFF
    Color:            #3B82F6
    Font:             weight-600
    Border-radius:    8px
    Hover:            opacity 90%
```

### Featured Categories Section

```
SECTION CONTAINER:
  Padding:            80px 40px
  Background:         #FFFFFF
  Max-width:          1400px
  Margin:             auto

HEADING:
  Font:               Inter weight-700
  Size:               36px
  Color:              #1F2937
  Margin-bottom:      48px

GRID:
  Display:            grid-cols-4 (desktop)
  Gap:                24px
  
  @media (768px):
    Display:          grid-cols-2
  @media (320px):
    Display:          grid-cols-1

CATEGORY CARD:
  Aspect-ratio:       1:1 (square)
  Position:           relative
  Border-radius:      12px
  Overflow:           hidden
  Cursor:             pointer
  
  BACKGROUND:
    Image/color:      category image or color
    Size:             cover
    
    HOVER STATE:
      Scale:          1.05
      Overlay:        rgba(0,0,0,0.4) → 0.6
      Transition:     300ms
  
  CONTENT (overlay):
    Position:         absolute inset-0
    Display:          flex flex-col justify-center items-center
    Background:       linear-gradient(180deg, transparent, rgba(0,0,0,0.4))
    
    ICON:
      Size:           48px
      Color:          #FFFFFF
      Margin-bottom:  16px
    
    NAME:
      Font:           Inter weight-600
      Size:           18px
      Color:          #FFFFFF
      Text-shadow:    0 2px 4px rgba(0,0,0,0.3)
```

---

## 🖼️ SEÇÃO #2: PRODUCT PAGE (Mais Importante)

### Visual Layout (Desktop)

```
LEFT COLUMN (50%):                 RIGHT COLUMN (50%):
┌─────────────────┐                ┌──────────────────┐
│                 │                │ "Wireless Headph"│ ← H2 32px
│                 │                │ ⭐⭐⭐⭐⭐              │
│  Main Image     │                │ (Based on 1,245) │
│  (600x700)      │                │                  │
│                 │                │ $199.99 ← Green  │
│                 │                │ $299.99 ← Strike │
│  ●●●●           │                │ [SAVE 33%]       │
│  Thumbs 100x100 │                │                  │
│                 │                │ ✓ In Stock       │
│                 │                │ ✓ Free Shipping  │
│                 │                │ ✓ 30-day Returns │
│                 │                │                  │
│                 │                │ COLOR SELECTION: │
│                 │                │ ● Black ● White  │
│                 │                │ ● Silver         │
│                 │                │                  │
│                 │                │ SIZE:            │
│                 │                │ XS S M L XL XXL  │
│                 │                │ [STOCK INDICATOR]│
│                 │                │                  │
│                 │                │ QUANTITY:        │
│                 │                │ - 1 +            │
│                 │                │                  │
│                 │                │ [Add to Cart]    │
│                 │                │ [❤ Add to Wishlist]
│                 │                │                  │
│                 │                │ SHARE:           │
│                 │                │ [f] [t] [in] [pin]
│                 │                │                  │
└─────────────────┘                └──────────────────┘
```

### Product Image Gallery (Left Column)

```
MAIN IMAGE CONTAINER:
  Width:              calc(100% - 120px)
  Aspect-ratio:       3:4 (portrait for clothes)
  Or:                 1:1 (for electronics)
  Border-radius:      12px
  Overflow:           hidden
  Background:         #F9FAFB
  Position:           relative
  
  IMAGE:
    100% width/height
    object-fit:       cover
    cursor:           zoom-in
  
  SALE BADGE (top-left):
    Position:         absolute top-16px left-16px
    Background:       #EF4444
    Color:            #FFFFFF
    Padding:          8px 12px
    Border-radius:    6px
    Font:             12px weight-600
    Content:          "SAVE 33%"

THUMBNAIL GALLERY (below main):
  Display:            flex gap-12px
  Margin-top:         16px
  Overflow-x:         auto (scrollable on mobile)
  
  EACH THUMBNAIL:
    Width/Height:     100px x 100px
    Aspect-ratio:     1:1
    Border:           2px solid transparent
    Border-radius:    8px
    Cursor:           pointer
    
    ACTIVE:
      Border:         2px solid #3B82F6
    
    HOVER:
      Opacity:        80%
    
    IMAGE:
      object-fit:     cover

ZOOM MODAL (on hover):
  Position:           fixed/modal
  Display:            none (unless hover)
  Scale:              1.5x or 2x
  Pan-enabled:        true (drag to move)
  Exit:               click outside
```

### Product Details (Right Column)

```
PRODUCT NAME:
  Font:               Inter weight-700
  Size:               32px
  Color:              #1F2937
  Line-height:        1.2
  Margin-bottom:      12px

RATING & REVIEWS:
  Display:            flex gap-8px items-center
  
  STARS:
    Stars:            ⭐⭐⭐⭐⭐
    Icon size:        18px
    Color:            #FBBF24 (amber)
  
  TEXT:
    Font:             Inter weight-500
    Size:             14px
    Color:            #6B7280
    Clickable:        link to reviews section
    Content:          "4.9 out of 5 (1,245 reviews)"

PRICE SECTION:
  Margin-bottom:      20px
  Display:            flex gap-12px items-center
  
  CURRENT PRICE:
    Font:             Inter weight-700
    Size:             36px
    Color:            #10B981 (green)
  
  ORIGINAL PRICE:
    Font:             Inter weight-400
    Size:             20px
    Color:            #9CA3AF
    Text-decoration:  line-through
  
  DISCOUNT BADGE:
    Background:       #FEF2F2 (light red)
    Color:            #DC2626
    Padding:          6px 12px
    Border-radius:    6px
    Font:             12px weight-600
    Content:          "SAVE 33%"

STOCK & SHIPPING SECTION:
  Margin-bottom:      24px
  Border:             1px solid #E5E7EB
  Padding:            16px
  Border-radius:      8px
  Background:         #F9FAFB
  
  EACH ROW:
    Display:          flex gap-8px
    Margin-bottom:    8px
    Font:             14px
  
    ICON:
      ✓ checkmark green
      OR
      ✕ X red
    
    TEXT:
      ✓ In Stock (ships within 24h)
      ✓ Free Shipping on orders $50+
      ✓ 30-Day Money Back Guarantee

PRODUCT OPTIONS:

Color Selection:
  Label:              "Color:" (weight-600)
  Margin-bottom:      12px
  Display:            flex gap-8px
  
  SWATCH:
    Size:             40px x 40px
    Border-radius:    full
    Border:           2px solid transparent
    Cursor:           pointer
    
    ACTIVE:
      Border:         2px solid #3B82F6
      Box-shadow:     0 0 0 3px rgba(59,130,246,0.1)
    
    HOVER:
      Scale:          1.1
      Transition:     200ms

Size Selection:
  Label:              "Size:" (weight-600)
  Margin-bottom:      12px
  Display:            flex gap-8px flex-wrap
  
  OPTION:
    Padding:          8px 16px
    Border:           2px solid #E5E7EB
    Border-radius:    6px
    Cursor:           pointer
    Font:             14px weight-500
    
    ACTIVE:
      Border-color:   #3B82F6
      Background:     #EFF6FF
      Color:          #3B82F6
    
    DISABLED:
      Opacity:        50%
      Cursor:         not-allowed
      Strikethrough:  text-decoration-line: line-through
    
    HOVER (enabled):
      Border-color:   #3B82F6

Quantity Selector:
  Label:              "Quantity:" (weight-600)
  Margin-bottom:      12px
  Display:            flex gap-8px items-center
  
  BUTTONS:
    Size:             36px x 36px
    Border:           1px solid #E5E7EB
    Background:       transparent
    Content:          - / +
    Font:             18px
    Cursor:           pointer
    Hover:            border-color #3B82F6
  
  INPUT:
    Width:            60px
    Height:           36px
    Text-align:       center
    Border:           1px solid #E5E7EB
    Border-radius:    6px
    Font:             16px weight-600
    Max:              max stock quantity
    Min:              1

BUTTONS:

Add to Cart:
  Width:              100%
  Height:             48px
  Background:         #3B82F6
  Color:              #FFFFFF
  Font:               weight-600 16px
  Border-radius:      8px
  Cursor:             pointer
  Margin-bottom:      12px
  
  Hover:
    Background:       #2563EB
    Box-shadow:       0 10px 15px rgba(59,130,246,0.2)
  
  Active:
    Transform:        scale(0.98)
  
  Disabled (out of stock):
    Background:       #D1D5DB
    Cursor:           not-allowed
    Opacity:          50%

Add to Wishlist:
  Width:              100%
  Height:             48px
  Border:             2px solid #E5E7EB
  Background:         transparent
  Color:              #6B7280
  Icon:               ♡ heart outline (20px left)
  Text:               "Add to Wishlist"
  Font:               weight-600 16px
  Border-radius:      8px
  
  Hover:
    Border-color:     #EC4899 (pink)
    Color:            #EC4899
  
  Active (added):
    Background:       #FECDD3 (pink light)
    Icon:             ♥ solid heart
    Color:            #EC4899

SHARE SECTION:
  Margin-top:         24px
  Label:              "Share:" (weight-600 14px)
  Display:            flex gap-12px
  
  ICONS:
    Facebook, Twitter, Instagram, Pinterest
    Size:             20px
    Color:            #6B7280
    Cursor:           pointer
    Hover:            color specific (blue for FB, etc)
```

### Product Details Tabs (Below main layout)

```
TAB CONTAINER:
  Margin-top:         64px
  Border-bottom:      1px solid #E5E7EB

TABS (horizontal):
  Display:            flex gap-32px
  Font:               16px weight-600
  
  EACH TAB:
    Padding:          12px 0
    Border-bottom:    3px solid transparent
    Cursor:           pointer
    Color:            #6B7280
    
    ACTIVE:
      Border-color:   #3B82F6
      Color:          #1F2937
    
    HOVER:
      Color:          #3B82F6

TAB CONTENT:
  Padding:            32px 0
  
  DESCRIPTION TAB:
    Font:             16px
    Line-height:      1.6
    Color:            #6B7280
    
    Headers (h3):     weight-600
    Lists:            • bullet points
  
  SPECIFICATIONS TAB:
    Table with 2 columns:
    [Spec Name] [Value]
    
    Cell padding:     12px
    Borders:          between rows
    Row hover:        #F9FAFB background
  
  REVIEWS TAB:
    Individual reviews below
    See section below
```

---

## 💬 SEÇÃO #3: REVIEWS SECTION

### Review List Layout

```
REVIEWS HEADER:
  Font:               Inter weight-700
  Size:               28px
  Content:            "Customer Reviews"
  Margin-bottom:      32px

RATING SUMMARY (left side):
  Display:            flex flex-col gap-12px
  
  AVERAGE RATING:
    Font:             weight-700
    Size:             48px
    Color:            #1F2937
    Content:          "4.9"
  
  STARS:
    ⭐⭐⭐⭐⭐
    Size:             20px
    Color:            #FBBF24
  
  TEXT:
    Font:             14px
    Color:            #6B7280
    Content:          "(1,245 verified purchases)"
  
  BREAKDOWN:
    5★ 78% [████████░░]
    4★ 15% [███░░░░░░░]
    3★ 5%  [█░░░░░░░░░]
    2★ 1%  [░░░░░░░░░░]
    1★ 1%  [░░░░░░░░░░]

INDIVIDUAL REVIEWS (right side):
  Display:            flex flex-col gap-20px

SINGLE REVIEW:
  Padding:            20px
  Border:             1px solid #E5E7EB
  Border-radius:      8px
  Background:         #FFFFFF
  
  HEADER:
    Display:          flex justify-between items-start
    
    LEFT:
      Avatar:         32px circular
      Name:           16px weight-600
      Date:           12px gray-500
      "John D. • Verified Purchase • 3 months ago"
    
    RIGHT:
      Stars:          ⭐⭐⭐⭐⭐ (18px)
      Helpful:        "Helpful? Yes (234) No (12)"

REVIEW TEXT:
  Font:               16px
  Line-height:        1.6
  Color:              #6B7280
  Margin:             12px 0

IMAGES (if attached):
  Display:            flex gap-8px
  
  EACH:
    Size:             80px x 80px
    Border-radius:    6px
    Cursor:           pointer (zoom on click)

PAGINATION:
  Margin-top:         32px
  Center-aligned
  
  Buttons:
    "← Previous" "1 2 3 4" "Next →"
    Height:     40px
    Padding:    10px 16px
```

---

## 🛒 SEÇÃO #4: SHOPPING CART PAGE

### Visual Layout (Desktop)

```
LEFT COLUMN (60%):              RIGHT COLUMN (40%):
┌───────────────────┐           ┌──────────────────┐
│ SHOPPING CART     │           │ ORDER SUMMARY    │
│                   │           │                  │
│ [Product 1]  qty  │           │ Subtotal:  $599  │
│ [Product 2]  qty  │           │ Shipping:  $10   │
│ [Product 3]  qty  │           │ Tax:       $55   │
│ [Product 4]  qty  │           │ ──────────────   │
│ [Product 5]  qty  │           │ TOTAL:     $664  │
│                   │           │                  │
│ [Continue Shop]   │           │ [Checkout]       │
│ [Proceed to Check]│           │ [Continue Shop]  │
│                   │           │                  │
│ COUPON CODE:      │           │ ORDER DETAILS:   │
│ [Code] [Apply]    │           │ • Free Shipping  │
│                   │           │ • 30-day Returns │
│                   │           │ • Secure Checkout│
│                   │           │                  │
└───────────────────┘           └──────────────────┘
```

### Cart Item (Line Item)

```
ITEM CONTAINER:
  Display:            grid grid-cols-5
  Gap:                20px
  Padding:            16px
  Border-bottom:      1px solid #E5E7EB
  Align-items:        center

COLUMN 1 - IMAGE:
  Width:              80px
  Height:             80px
  Border-radius:      8px
  Overflow:           hidden
  
  IMAGE:
    100% size
    object-fit:       cover

COLUMN 2 - PRODUCT INFO:
  Flex:               1
  
  NAME:
    Font:             16px weight-600
    Color:            #1F2937
  
  COLOR/SIZE:
    Font:             14px
    Color:            #6B7280
    Content:          "Black, Size M"
  
  REMOVE LINK:
    Font:             14px
    Color:            #3B82F6
    Cursor:           pointer
    Hover:            #2563EB

COLUMN 3 - PRICE:
  Font:               16px weight-600
  Color:              #1F2937
  Content:            "$199.99"

COLUMN 4 - QUANTITY SELECTOR:
  Display:            flex gap-8px items-center
  
  - button:          32px square, border
  Input:             40px width, centered
  + button:          32px square, border

COLUMN 5 - SUBTOTAL:
  Font:               16px weight-600
  Color:              #1F2937
  Content:            "$999.96" (price × qty)

ACTIONS (on hover):
  Move left:          wishlist, compare buttons fade in
```

### Order Summary (Right Column)

```
CONTAINER:
  Position:           sticky top-80px
  Padding:            24px
  Background:         #F9FAFB
  Border-radius:      12px
  Border:             1px solid #E5E7EB

HEADING:
  Font:               20px weight-600
  Color:              #1F2937
  Margin-bottom:      20px

ROWS (vertical):
  Margin-bottom:      12px
  Display:            flex justify-between
  Font:               16px

SUBTOTAL:
  Color:              #6B7280
  Value:              gray-700

SHIPPING:
  Color:              #6B7280
  Value:              gray-700
  Interactive:        click to change

TAX:
  Color:              #6B7280
  Value:              gray-700

DIVIDER:
  Border-top:         2px solid #E5E7EB
  Margin:             16px 0

TOTAL:
  Font:               18px weight-700
  Color:              #1F2937
  Value:              weight-700

COUPON INPUT:
  Margin-top:         20px
  Display:            flex gap-8px
  
  INPUT:
    Flex:             1
    Height:           40px
    Padding:          10px 12px
    Border:           1px solid #E5E7EB
    Border-radius:    6px
    Placeholder:      "Enter coupon code"
  
  BUTTON:
    Width:            auto
    Height:           40px
    Padding:          10px 16px
    Background:       #3B82F6
    Color:            #FFFFFF
    Border-radius:    6px

BUTTONS:
  Margin-top:         20px
  
  CHECKOUT:
    Width:            100%
    Height:           48px
    Background:       #3B82F6
    Color:            #FFFFFF
    Font:             weight-600
    Border-radius:    8px
    Margin-bottom:    12px
  
  CONTINUE SHOPPING:
    Width:            100%
    Height:           48px
    Border:           2px solid #E5E7EB
    Background:       transparent
    Color:            #1F2937
    Font:             weight-600
    Border-radius:    8px

BENEFITS:
  Margin-top:         16px
  Font:               14px
  Color:              #6B7280
  
  Each item:
    Padding:          8px 0
    Display:          flex gap-8px
    
    Icon:             ✓ checkmark
    Text:             benefit
```

---

## 💳 SEÇÃO #5: CHECKOUT PAGE

### Checkout Flow Layout

```
PROGRESS INDICATOR (top):
  1. Shipping
  2. Payment
  3. Review
  4. Confirmation
  
  Active: bold, blue
  Completed: checkmark, gray
  Next: light gray

MAIN FORM (2-column on desktop):

LEFT COLUMN (60%):
  
  SHIPPING SECTION:
    Heading:         "Shipping Address"
    
    Form fields:
      First Name / Last Name (2-column)
      Street Address
      City / State / ZIP (3-column)
      Country
      Phone Number
    
    EACH INPUT:
      Height:         40px
      Padding:        10px 12px
      Border:         1px solid #D1D5DB
      Border-radius:  6px
      Focus:          blue ring
  
  SHIPPING METHOD:
    Heading:         "Shipping Method"
    
    Radio options:
      ○ Standard (5-7 days) - Free
      ○ Express (2-3 days) - $10
      ○ Overnight - $25
    
    Selected:        filled circle, blue
  
  PAYMENT SECTION:
    Heading:         "Payment Information"
    
    Card input:
      Full width
      Height:         40px
      Placeholder:    "1234 5678 9012 3456"
      Input format:   XXXX XXXX XXXX XXXX
    
    Expiry / CVC (2-column):
      Expiry:         "MM/YY"
      CVC:            "123"

RIGHT COLUMN (40%):
  
  ORDER SUMMARY:
    Similar to cart page
    Sticky position
    Max-width: 400px

BUTTONS (bottom):
  [← Back] [Continue to Review] [Pay Now]
```

---

## 📦 SEÇÃO #6: CATEGORY/LISTING PAGE

### Visual Layout

```
SIDEBAR (25%):                   MAIN AREA (75%):
┌─────────────────┐             ┌──────────────────────┐
│ FILTERS         │             │ Results Header:      │
│ ───────────     │             │ "Headphones (234)"   │
│ CATEGORIES      │             │                      │
│ ✓ Headphones    │             │ Sort: [v]  View: [◻] │
│ ○ Speakers      │             │                      │
│ ○ Microphones   │             │ [Prod] [Prod] [Prod] │
│                 │             │ [Prod] [Prod] [Prod] │
│ PRICE RANGE     │             │ [Prod] [Prod] [Prod] │
│ $0    $1000 [▬]│             │ [Prod] [Prod] [Prod] │
│ [$0 - $1000]    │             │                      │
│                 │             │ Pagination:          │
│ BRAND           │             │ ◀ 1 2 3 4 5 ▶        │
│ ☐ Sony          │             │                      │
│ ☐ Bose          │             │                      │
│ ☐ Sennheiser    │             │                      │
│                 │             │                      │
│ COLOR           │             │                      │
│ ☐ Black         │             │                      │
│ ☐ White         │             │                      │
│ ☐ Silver        │             │                      │
│                 │             │                      │
│ RATING          │             │                      │
│ ☐ ⭐⭐⭐⭐⭐       │             │                      │
│ ☐ ⭐⭐⭐⭐        │             │                      │
│ ☐ ⭐⭐⭐         │             │                      │
│                 │             │                      │
│ [APPLY FILTERS] │             │                      │
│ [CLEAR ALL]     │             │                      │
│                 │             │                      │
└─────────────────┘             └──────────────────────┘
```

### Sidebar Filters

```
FILTER HEADING:
  Font:               16px weight-600
  Color:              #1F2937
  Margin-bottom:      16px

FILTER GROUP:
  Margin-bottom:      24px
  Padding-bottom:     20px
  Border-bottom:      1px solid #E5E7EB

CATEGORY CHECKBOX:
  Display:            flex gap-8px items-center
  Margin-bottom:      8px
  Cursor:             pointer
  
  CHECKBOX:
    Size:             20px square
    Border:           2px solid #D1D5DB
    Border-radius:    4px
    
    CHECKED:
      Background:     #3B82F6
      Border:         #3B82F6
      Checkmark:      white
  
  LABEL:
    Font:             14px
    Color:            #6B7280
    Cursor:           pointer

PRICE RANGE SLIDER:
  Display:            flex flex-col gap-8px
  
  SLIDER:
    Height:           4px
    Background:       #E5E7EB
    Track:            #3B82F6 (between thumbs)
    
    THUMB:
      Size:           16px circular
      Background:     #3B82F6
      Cursor:         grab
  
  INPUT FIELDS:
    Width:            calc(50% - 4px)
    Height:           32px
    Font:             12px
    Border:           1px solid #D1D5DB
    Border-radius:    4px
    Padding:          4px 8px

BUTTONS:
  Apply Filters:
    Width:            100%
    Height:           40px
    Background:       #3B82F6
    Color:            #FFFFFF
    Border-radius:    6px
    Margin-bottom:    12px
  
  Clear All:
    Width:            100%
    Height:           40px
    Border:           1px solid #E5E7EB
    Color:            #6B7280
    Background:       transparent
    Border-radius:    6px
```

### Product Card (Grid Item)

```
CARD:
  Width:              calc(25% - 18px) [4-column]
  Position:           relative
  Aspect-ratio:       3:4 (portrait)
  Border-radius:      8px
  Overflow:           hidden
  Background:         #FFFFFF
  
  Tablet:             calc(33.33% - 16px) [3-column]
  Mobile:             100% [1-column]

IMAGE CONTAINER:
  Width:              100%
  Aspect-ratio:       1:1
  Overflow:           hidden
  Background:         #F9FAFB
  Position:           relative
  
  IMAGE:
    100% size
    object-fit:       cover
  
  OVERLAY (on hover):
    Position:         absolute inset-0
    Background:       rgba(0,0,0,0.1)
    Opacity:          0 → 1 (200ms)
  
  QUICK VIEW BUTTON:
    Position:         absolute center
    Display:          none
    Opacity:          0
    
    On hover:
      Display:        flex
      Opacity:        1
      Transition:     200ms
    
    Button:           "Quick View" (24px padding)

BADGE (top-left):
  Position:           absolute top-8px left-8px
  Background:         #EF4444
  Color:              #FFFFFF
  Padding:            6px 12px
  Border-radius:      4px
  Font:               12px weight-600
  Content:            "SALE" or "NEW"

HEART (top-right):
  Position:           absolute top-8px right-8px
  Size:               24px
  Color:              #FFFFFF
  Cursor:             pointer
  Background:         rgba(0,0,0,0.3)
  Border-radius:      full
  Display:            flex items-center justify-center
  
  Hover:
    Background:       rgba(0,0,0,0.5)
  
  Click:
    Color:            #EC4899 (pink)
    Fill:             solid

CONTENT:
  Padding:            12px
  
  CATEGORY:
    Font:             12px
    Color:            #9CA3AF
    Margin-bottom:    4px
  
  NAME:
    Font:             14px weight-600
    Color:            #1F2937
    Line-height:      1.3
    Margin-bottom:    4px
    Truncate:         2 lines
  
  RATING:
    Display:          flex gap-4px items-center
    Font:             12px
    Color:            #6B7280
    
    Stars:            ⭐⭐⭐⭐⭐ (14px)
    Count:            "(123)"
  
  PRICE:
    Margin-top:       8px
    Display:          flex gap-8px items-center
    
    Current:
      Font:           16px weight-700
      Color:          #10B981 (green)
    
    Original:
      Font:           14px
      Color:          #9CA3AF
      Text-decoration: line-through
  
  ADD TO CART:
    Width:            100%
    Height:           36px
    Margin-top:       12px
    Background:       #3B82F6
    Color:            #FFFFFF
    Font:             14px weight-600
    Border-radius:    6px
    Cursor:           pointer
    
    Hover:
      Background:     #2563EB
```

---

## 📏 TIPOGRAFIA E-COMMERCE

```
HEADINGS:
  H1 (page):          56px / weight-700 / line-1.2
  H2 (section):       36px / weight-700 / line-1.2
  H3 (subsection):    28px / weight-600 / line-1.3
  H4:                 24px / weight-600 / line-1.4

PRODUCT INFO:
  Product name:       32px / weight-700
  Category:           14px / weight-500 / gray-500
  Price:              28px / weight-700 / green
  Discount:           14px / weight-600 / red

BODY & UI:
  Default text:       16px / weight-400 / line-1.6
  Small text:         14px / weight-400
  UI text:            14px / weight-600
  Labels:             12px / weight-600
```

---

## 📏 SPACING E-COMMERCE

```
SECTIONS:
  Top padding:        80px (desktop) / 40px (mobile)
  Bottom padding:     80px (desktop) / 40px (mobile)
  Margin between:     80px
  
GRIDS:
  Product grid gap:   20px
  Card padding:       12px
  
FORMS:
  Input height:       40px
  Form gap:           16px
  Label-input gap:    8px
```

---

## 🎬 ANIMAÇÕES E-COMMERCE

```
PRODUCT HOVER:
  Image:              scale(1.1) over 300ms
  Shadow:             0 10px 25px (on card)
  Price:              color change 200ms

ADD TO CART:
  Click feedback:     scale(0.98) 100ms
  Success toast:      fade in from top, 3s auto-dismiss
  Cart counter:       +1 animation (number change)

LOAD MORE:
  Infinite scroll     OR
  Load button + spinner
  New products fade in 300ms
```

---

## ✅ CHECKLIST E-COMMERCE

- ✅ Homepage (banner, categories, featured, bestsellers)
- ✅ Product page (images, variants, reviews, ratings)
- ✅ Category/listing (filters, sorting, pagination)
- ✅ Shopping cart (items, quantity, order summary)
- ✅ Checkout (shipping, payment, review)
- ✅ Colors exact (green pricing, red sale)
- ✅ Spacing consistent (8px grid base)
- ✅ Typography (product names, prices)
- ✅ Animations (hovers, transitions)
- ✅ Responsive (4-col → 3-col → 1-col)
- ✅ Accessibility (alt text, ARIA labels)
- ✅ Payment integration (Stripe)
- ✅ Search & filters
- ✅ Wishlist
- ✅ Reviews & ratings

---

**Próximo Template**: Qual você quer?

1. Material Dashboard 3 (Admin)
2. Spotlight (Portfolio)
3. SaaS Boilerplate (Vercel)

?


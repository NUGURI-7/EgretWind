# CLAUDE.md - AI Assistant Guide for EgretWind Project

## Project Overview

**EgretWind** is a full-stack web application built with Django REST Framework (backend) and Vue 3 (frontend). The project is a content management system focused on articles and user management, primarily configured in Chinese (zh-hans).

**Tech Stack:**
- **Backend:** Django 5.2.8, Django REST Framework 3.16.1, MySQL
- **Frontend:** Vue 3.5, TypeScript 5.9, Vite 7.1, Element Plus 2.11
- **State Management:** Pinia 3.0
- **Rich Text Editor:** TipTap 3.11
- **HTTP Client:** Axios 1.13
- **Python Version:** >=3.11
- **Node Version:** ^20.19.0 || >=22.12.0

---

## Repository Structure

```
EgretWind/
├── egretwind/              # Django backend project
│   ├── egretwind/          # Core Django configuration
│   │   ├── settings.py     # Django settings (loads config.yaml)
│   │   └── urls.py         # Root URL configuration (API prefix: nuguri/api/)
│   ├── article/            # Article management app
│   │   ├── models.py       # Article model
│   │   ├── serializer/     # Serializers with nested Query pattern
│   │   ├── views/          # API views
│   │   └── urls.py         # Article routes
│   ├── user/               # User management app
│   │   ├── models.py       # User model with MD5 password hashing
│   │   ├── serializer/     # User serializers
│   │   ├── views/          # User API views
│   │   └── urls.py         # User routes
│   ├── common/             # Shared utilities
│   │   ├── mixins/         # BaseModel mixin with timestamps
│   │   ├── result/         # Unified Result/Page response classes
│   │   └── database/       # Database utilities (pagination)
│   └── manage.py           # Django management script
├── frontend/               # Vue 3 frontend application
│   ├── src/
│   │   ├── api/            # API client modules
│   │   ├── assets/         # Static assets
│   │   ├── components/     # Vue components (globally registered)
│   │   ├── layout/         # Layout components
│   │   ├── router/         # Vue Router configuration
│   │   ├── stores/         # Pinia stores
│   │   ├── styles/         # Global styles
│   │   ├── type/           # TypeScript type definitions
│   │   ├── utils/          # Utility functions
│   │   ├── views/          # Page components
│   │   ├── App.vue         # Root component
│   │   └── main.ts         # Application entry point
│   ├── vite.config.ts      # Vite configuration (dev server: port 7777)
│   └── package.json        # Frontend dependencies
├── pyproject.toml          # Python project configuration (uv package manager)
├── uv.lock                 # Python dependency lock file
└── main.py                 # Simple hello world script
```

---

## Backend Architecture

### Django Configuration

**Settings Location:** `egretwind/egretwind/settings.py`

**Critical Configuration Requirements:**
- The project **requires** a `config.yaml` file at the project root
- Required keys in `config.yaml`:
  - `DB_ENGINE` - Database engine (e.g., django.db.backends.mysql)
  - `DB_NAME` - Database name
  - `DB_HOST` - Database host
  - `DB_USER` - Database user
  - `DB_PASSWORD` - Database password
  - `SECRET_KEY` - Django secret key
  - Optional: `DB_PORT` (default: 3306), `DEBUG`, `ALLOWED_HOSTS`

**Important Settings:**
- `DEBUG`: Defaults to `False`, controls allowed hosts
- `LANGUAGE_CODE`: "zh-hans" (Simplified Chinese)
- `TIME_ZONE`: "Asia/Shanghai"
- `API_PREFIX`: All API routes are prefixed with `nuguri/api/`
- `REST_FRAMEWORK`: Authentication/permissions disabled by default

### Model Patterns

**BaseModel Mixin** (`common/mixins/app_model_mixin.py`):
```python
class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True, db_index=True)
    update_time = models.DateTimeField(auto_now=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ['create_time']
```

**Usage Pattern:**
- All models should inherit from `BaseModel` for automatic timestamp tracking
- Models use verbose Chinese names (e.g., verbose_name='标题')
- Custom table names specified via `db_table` in Meta

**Example - Article Model** (`article/models.py`):
- Fields: title, content, author (FK to User), status, published_at
- Status choices: 'draft', 'published'
- Uses BaseModel for timestamps
- Table name: 'articles'

**Example - User Model** (`user/models.py`):
- Custom user model (not Django's built-in User)
- Password encryption: MD5 (via `password_encrypt()` function)
- Fields include: username, email, password, phone_number, nickname, avatar, gender, bio, location
- Status tracking: is_active, is_admin, status
- Table name: 'user'

### Serializer Patterns

**Unique Nested Serializer Pattern:**

The codebase uses a non-standard but consistent serializer pattern with nested classes:

```python
class ArticleSerializers(serializers.Serializer):

    class Query(serializers.Serializer):
        def get_queryset(self):
            # Build queryset with filters
            return QuerySet(Article)

        def list(self):
            # Return all results
            return [ArticleSerializer(row).data for row in self.get_queryset()]

        def page(self, current_page: int, page_size: int):
            # Return paginated results
            handler = lambda row: ArticleSerializer(row).data
            return page_search(current_page, page_size, self.get_queryset(), handler)
```

**Key Points:**
- Outer class (`ArticleSerializers`) groups related serializers
- Inner `Query` class handles GET operations
- `get_queryset()` method for building filtered queries
- `list()` method returns all records
- `page()` method returns paginated records
- List comprehensions preferred over map()

### View Patterns

**APIView Pattern** (`article/views/article.py`):
```python
from rest_framework.views import APIView
from common.result import result

class ArticleView(APIView):
    def get(self, request: Request):
        return result.success(
            ArticleSerializers.Query(data={}).list()
        )

    # Nested view for pagination
    class Page(APIView):
        def get(self, request: Request, current_page: int, page_size: int):
            return result.success(
                ArticleSerializers.Query(data={}).page(current_page, page_size)
            )
```

**Key Points:**
- Use `rest_framework.views.APIView` for class-based views
- Return responses via `result.success()` or `result.error()`
- Nested view classes for related endpoints (e.g., pagination)
- Type hints used for request parameters

### Response Utilities

**Unified Response Pattern** (`common/result/result.py`):

```python
# Success response
result.success(data)  # Returns: {"code": 200, "message": "Success", "data": ...}

# Error response
result.error(message)  # Returns: {"code": 500, "message": ..., "data": None}

# Page response
Page(total, records, current_page, page_size)
# Returns: {"total": 100, "records": [...], "current": 1, "size": 10}
```

**Always use these utilities for consistent API responses.**

### Database Utilities

**Pagination Helper** (`common/database/search.py`):
```python
page_search(current_page, page_size, queryset, post_records_handler)
```
- `post_records_handler`: Lambda or function to serialize each record
- Returns a `Page` object with total count and records
- Uses list comprehensions for record processing

### URL Routing

**Root URLs** (`egretwind/urls.py`):
- API prefix: `nuguri/api/`
- All app URLs included under this prefix
- Example: `/nuguri/api/articles/`, `/nuguri/api/users/`

---

## Frontend Architecture

### Project Setup

**Dev Server:**
- Host: `0.0.0.0` (accessible externally)
- Port: `7777` (strict port mode enabled)
- CORS: Enabled
- HMR: Enabled via Vite

**Path Aliases:**
- `@` → `./src` (configured in vite.config.ts)

### Application Structure

**Entry Point** (`main.ts`):
```typescript
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import App from './App.vue'
import router from './router'
import Components from '@/components'
import '@/styles/global.css'

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(ElementPlus)
app.use(Components)  // Global component registration
app.mount('#app')
```

### Key Technologies

**Vue 3 Features:**
- Composition API (recommended)
- `<script setup>` syntax
- TypeScript support
- Single File Components (.vue)

**Element Plus:**
- UI component library (imported globally)
- No need to import individual components
- Use `el-*` components directly in templates

**TipTap Editor:**
- Rich text editing capability
- Configured in `/views/tiptap/tiptap.vue`
- Uses starter-kit for basic functionality

**Pinia:**
- State management (Vuex successor)
- Stores located in `src/stores/`
- Use `defineStore()` pattern

**Router:**
- Vue Router 4
- Routes defined in `src/router/routes.ts`
- Lazy loading via `() => import('@/views/...')`
- History mode (HTML5 History API)

### Current Routes

```typescript
[
  { path: '/test', component: () => import('@/views/t1t/test.vue') },
  { path: '/tiptap', component: () => import('@/views/tiptap/tiptap.vue') },
  { path: '/home', component: () => import('@/views/home-page/index.vue') }
]
```

### Component Conventions

**Component Registration:**
- Components in `src/components/` are registered globally
- Use PascalCase for component files
- Import automatically via Components plugin

**File Naming:**
- Components: PascalCase or kebab-case
- Views: kebab-case directories with index.vue
- TypeScript: .ts extension
- Vue SFC: .vue extension

---

## Development Workflows

### Backend Development

**Setup:**
```bash
# Install dependencies (using uv)
uv sync

# Create config.yaml with required database credentials
# See settings.py for required keys

# Run migrations
cd egretwind
python manage.py makemigrations
python manage.py migrate

# Start development server
python manage.py runserver
```

**Adding New Features:**

1. **Create Model** in appropriate app's `models.py`:
   - Inherit from `BaseModel`
   - Use Chinese verbose_name
   - Define custom table name

2. **Create Serializer** in `serializer/` directory:
   - Create ModelSerializer for basic CRUD
   - Create nested Serializer class with Query inner class
   - Implement `get_queryset()`, `list()`, `page()` methods

3. **Create View** in `views/` directory:
   - Inherit from `APIView`
   - Use `result.success()` / `result.error()`
   - Add nested views for related operations

4. **Add URLs** in app's `urls.py`:
   - Register view classes
   - Follow REST conventions

5. **Run Migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Frontend Development

**Setup:**
```bash
cd frontend
npm install

# Start dev server (runs on port 7777)
npm run dev

# Type checking
npm run type-check

# Linting
npm run lint

# Build for production
npm run build
```

**Adding New Features:**

1. **Create View** in `src/views/`:
   - Create directory with `index.vue` or named `.vue` file
   - Use `<script setup lang="ts">`
   - Define types for props/emits

2. **Add Route** in `src/router/routes.ts`:
   - Use lazy loading: `() => import('@/views/...')`
   - Follow kebab-case for paths

3. **Create API Client** (if needed) in `src/api/`:
   - Use axios for HTTP requests
   - Define TypeScript interfaces for responses
   - Handle responses with proper typing

4. **Create Components** in `src/components/`:
   - Components are auto-registered globally
   - Use TypeScript for props
   - Follow Vue 3 best practices

5. **State Management** (if needed) in `src/stores/`:
   - Create Pinia store with `defineStore()`
   - Use Composition API style
   - Export typed store

**TypeScript Configuration:**
- `tsconfig.app.json` - Application code config
- `tsconfig.node.json` - Node/build tools config
- `tsconfig.json` - Base configuration
- Use `vue-tsc` for type checking

---

## Code Style & Conventions

### Backend (Python/Django)

**Naming:**
- Models: PascalCase (e.g., `Article`, `User`)
- Functions/methods: snake_case (e.g., `get_queryset()`)
- Variables: snake_case
- Constants: UPPER_SNAKE_CASE

**Comments:**
- File headers include: project, author, file, date, desc
- Author: 鹭岛听风 (Egret Wind)
- Use Chinese for user-facing strings
- Use English for code/comments (preferred)

**Code Organization:**
- One model per file (or related models)
- Serializers in dedicated `serializer/` directory
- Views in dedicated `views/` directory
- Imports grouped: Django, third-party, local

**Preferred Patterns:**
- List comprehensions over `map()` when returning lists
- Type hints for function parameters
- Explicit `QuerySet` initialization where needed

### Frontend (TypeScript/Vue)

**Naming:**
- Components: PascalCase files (e.g., `ArticleCard.vue`)
- Composables: camelCase with `use` prefix (e.g., `useArticles.ts`)
- Utilities: camelCase (e.g., `formatDate.ts`)
- Types/Interfaces: PascalCase (e.g., `Article`, `User`)

**Vue Component Structure:**
```vue
<script setup lang="ts">
// Imports
// Props/Emits
// Composables
// Reactive state
// Computed
// Methods
// Lifecycle hooks
</script>

<template>
  <!-- Template -->
</template>

<style scoped lang="scss">
/* Styles */
</style>
```

**TypeScript:**
- Always define interfaces for data structures
- Use type inference where possible
- Avoid `any` type
- Use `Ref<T>` and `ComputedRef<T>` for clarity

**Vue Best Practices:**
- Prefer Composition API over Options API
- Use `<script setup>` for conciseness
- Define typed props with `defineProps<T>()`
- Use `ref()` for primitives, `reactive()` for objects
- Use `computed()` for derived state

---

## Key Points for AI Assistants

### Understanding the Codebase

1. **Unique Patterns:**
   - The serializer pattern with nested Query classes is non-standard but consistent
   - Result utility provides unified response format
   - BaseModel mixin is used across all models
   - Components are globally registered in frontend

2. **Configuration:**
   - Backend requires `config.yaml` (not in repo)
   - Never commit sensitive data
   - Frontend dev server runs on port 7777

3. **Database:**
   - MySQL is the database backend
   - MD5 password hashing (consider upgrading to bcrypt/argon2)
   - Timestamps are handled automatically via BaseModel

4. **API Structure:**
   - All APIs prefixed with `/nuguri/api/`
   - REST pattern for endpoints
   - Pagination available via nested Page views
   - Standard response: `{code, message, data}`

### When Making Changes

**DO:**
- Follow existing patterns (nested serializers, result responses)
- Use BaseModel for new models
- Add type hints to Python code
- Use TypeScript for frontend code
- Test API endpoints manually
- Run migrations after model changes
- Use list comprehensions in Python
- Import Element Plus components directly
- Use path alias `@` in frontend imports
- Keep Chinese verbose_name in models

**DON'T:**
- Modify the result.py utility without good reason
- Change the API prefix without updating frontend
- Skip migrations after model changes
- Use Options API in new Vue components
- Commit `config.yaml` or sensitive data
- Break the nested serializer pattern
- Use `any` type in TypeScript
- Forget to update both frontend and backend for API changes

### Testing Checklist

**Backend:**
- Run migrations: `python manage.py migrate`
- Test API endpoints (use curl, Postman, or frontend)
- Check response format matches Result pattern
- Verify database queries are optimized
- Test pagination if implemented

**Frontend:**
- Run type check: `npm run type-check`
- Run linter: `npm run lint`
- Test in browser at `http://localhost:7777`
- Check console for errors
- Verify API calls work correctly
- Test responsive design (Element Plus)

### Common Tasks

**Add New API Endpoint:**
1. Create/update model in `models.py`
2. Create serializer following nested pattern
3. Create view using APIView
4. Add URL route
5. Run migrations
6. Test endpoint
7. Update frontend API client
8. Update types in frontend

**Add New Frontend Page:**
1. Create view component in `src/views/`
2. Add route in `routes.ts`
3. Create API client if needed
4. Add types for data structures
5. Test navigation and data loading

**Database Schema Change:**
1. Modify model
2. Run `makemigrations`
3. Review migration file
4. Run `migrate`
5. Update serializers
6. Update frontend types
7. Test thoroughly

---

## Architecture Decisions

### Why This Structure?

**Backend:**
- **Django REST Framework:** Robust, well-documented, scalable
- **Nested Serializers:** Groups related operations, clear organization
- **Result Utility:** Consistent API responses, easier frontend handling
- **BaseModel Mixin:** DRY principle, automatic timestamp tracking

**Frontend:**
- **Vue 3 + TypeScript:** Type safety, modern reactivity, composition API
- **Vite:** Fast HMR, optimized builds, modern tooling
- **Element Plus:** Comprehensive UI library, enterprise-ready
- **Pinia:** Lightweight, TypeScript-friendly, Vue 3 optimized
- **TipTap:** Modern, extensible rich text editor

### Potential Improvements

1. **Security:**
   - Replace MD5 password hashing with bcrypt/argon2
   - Add authentication/authorization (JWT, session)
   - Enable CSRF protection properly
   - Add rate limiting

2. **Testing:**
   - Add Django unit tests
   - Add Vue component tests (Vitest)
   - Add E2E tests (Playwright/Cypress)

3. **Documentation:**
   - Add API documentation (drf-spectacular/Swagger)
   - Add component documentation (Storybook)
   - Add inline code documentation

4. **Performance:**
   - Add database query optimization
   - Implement caching (Redis)
   - Add frontend code splitting
   - Optimize images and assets

5. **Development:**
   - Add pre-commit hooks (black, flake8, prettier)
   - Add CI/CD pipeline
   - Add Docker configuration
   - Add environment variable management

---

## Quick Reference

### Backend Commands
```bash
# Run dev server
python egretwind/manage.py runserver

# Make migrations
python egretwind/manage.py makemigrations

# Apply migrations
python egretwind/manage.py migrate

# Create superuser
python egretwind/manage.py createsuperuser

# Shell
python egretwind/manage.py shell
```

### Frontend Commands
```bash
# Development
npm run dev

# Build
npm run build

# Type check
npm run type-check

# Lint
npm run lint

# Format
npm run format
```

### Important Files
- **Backend Config:** `egretwind/egretwind/settings.py`
- **Database Config:** `config.yaml` (root, not in repo)
- **API Routes:** `egretwind/egretwind/urls.py`
- **Frontend Config:** `frontend/vite.config.ts`
- **Frontend Routes:** `frontend/src/router/routes.ts`
- **Frontend Entry:** `frontend/src/main.ts`

---

## Contact & Credits

**Author:** 鹭岛听风 (Egret Wind)
**Project:** EgretWind
**License:** Not specified

---

**Last Updated:** 2025-11-28
**Document Version:** 1.0.0

This document should be updated as the codebase evolves. When adding new patterns, conventions, or architectural decisions, update this file to keep AI assistants informed.

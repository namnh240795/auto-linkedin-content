# How to Set Up Playwright with React: The Right Way from Day One

## Introduction

We've all been there. You push a seemingly harmless change to production, and suddenly your tests are failing everywhere. Or worse, the tests pass but your app is broken. The frustration of flaky, unreliable tests is something every developer knows too well.

When I started using Playwright with React, I made the mistake of diving straight into writing tests without setting up the foundation properly. I was selecting elements by CSS classes, watching tests break every time I tweaked the UI, and wondering why E2E testing felt so fragile.

The truth is, reliable testing isn't about writing more tests—it's about setting up your frontend structure to support testing from the beginning. In this article, I'll show you how to build a React application with Playwright the right way: using test IDs, proper configuration, and a workflow that scales with your team.

By the end, you'll have a fully functional login form with a complete Playwright test suite, plus GitHub Actions to run everything automatically. Let's get started.

---

## Why Test IDs Matter

Before we write a single line of code, let's talk about the biggest mistake developers make with Playwright: relying on CSS selectors.

Here's what typically happens: You write a test that finds your submit button using `.btn-primary`. Next week, a designer changes the button to `.btn-submit` because it makes more sense. Your test fails. You update the test. The cycle repeats. This is the path to flaky tests and burnt-out developers.

The solution is **test IDs**—dedicated attributes that exist solely for testing purposes.

```html
<!-- Bad: Tied to CSS -->
<button className="btn-primary">Submit</button>

<!-- Good: Decoupled from implementation -->
<button className="btn-primary" data-testid="login-submit-button">Submit</button>
```

Test IDs create a contract between your UI and your tests. When you use `data-testid` attributes, your tests become immune to CSS changes, refactoring, and redesigns. They only break when you intentionally remove or change functionality—which is exactly when they *should* break.

This isn't just about convenience. It's about creating a frontend architecture that separates concerns: your HTML structure for accessibility, your CSS for styling, your JavaScript for behavior, and your test IDs for verification. When you get this right from the start, testing becomes a joy rather than a chore.

---

## Project Setup

Let's start by creating a new Vite + React + TypeScript project and installing Playwright.

**Create the project:**

```bash
npm create vite@latest playwright-react-app -- --template react-ts
cd playwright-react-app
npm install
```

**Install Playwright:**

```bash
npm install -D @playwright/test
npx playwright install
```

**Install additional dependencies for form handling:**

```bash
npm install react-hook-form zod
npm install -D @types/node
```

Now let's configure Playwright to work with our React app. Create or update `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'on-first-retry',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
});
```

This configuration:
- Sets `http://localhost:5173` as the base URL (Vite's default)
- Enables tracing on first retry for easy debugging
- Runs a dev server automatically during tests
- Reuses an existing dev server in local development for faster feedback

---

## Building the Login Form

Now let's build a login form with proper test ID attributes. Create `src/components/LoginForm.tsx`:

```typescript
import { useForm } from 'react-hook-form';
import { z } from 'zod';
import { zodResolver } from '@hookform/resolvers/zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});

type LoginFormData = z.infer<typeof loginSchema>;

export function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
    setError,
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  const onSubmit = async (data: LoginFormData) => {
    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      // Simulate authentication failure for demo
      if (data.email === 'test@example.com' && data.password === 'password123') {
        window.location.href = '/dashboard';
      } else {
        setError('root', {
          type: 'manual',
          message: 'Invalid email or password',
        });
      }
    } catch {
      setError('root', {
        type: 'manual',
        message: 'Something went wrong. Please try again.',
      });
    }
  };

  return (
    <div className="login-container" data-testid="login-form-container">
      <h1 data-testid="login-title">Welcome Back</h1>

      <form onSubmit={handleSubmit(onSubmit)} data-testid="login-form" noValidate>
        <div className="form-group">
          <label htmlFor="email" data-testid="email-label">
            Email
          </label>
          <input
            id="email"
            type="email"
            {...register('email')}
            data-testid="email-input"
            aria-invalid={errors.email ? 'true' : 'false'}
            aria-errormessage={errors.email ? 'email-error' : undefined}
          />
          {errors.email && (
            <span className="error" id="email-error" data-testid="email-error">
              {errors.email.message}
            </span>
          )}
        </div>

        <div className="form-group">
          <label htmlFor="password" data-testid="password-label">
            Password
          </label>
          <input
            id="password"
            type="password"
            {...register('password')}
            data-testid="password-input"
            aria-invalid={errors.password ? 'true' : 'false'}
            aria-errormessage={errors.password ? 'password-error' : undefined}
          />
          {errors.password && (
            <span className="error" id="password-error" data-testid="password-error">
              {errors.password.message}
            </span>
          )}
        </div>

        {errors.root && (
          <div className="error-banner" data-testid="login-error-banner">
            {errors.root.message}
          </div>
        )}

        <button
          type="submit"
          disabled={isSubmitting}
          data-testid="login-submit-button"
        >
          {isSubmitting ? 'Logging in...' : 'Log In'}
        </button>
      </form>
    </div>
  );
}
```

Update `src/App.tsx` to use our login form:

```typescript
import { LoginForm } from './components/LoginForm';

function App() {
  return (
    <div className="App">
      <LoginForm />
    </div>
  );
}

export default App;
```

Add some basic styles in `src/App.css`:

```css
.login-container {
  max-width: 400px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
}

.error {
  color: #dc2626;
  font-size: 0.875rem;
  margin-top: 0.25rem;
  display: block;
}

.error-banner {
  background-color: #fee2e2;
  color: #dc2626;
  padding: 0.75rem;
  border-radius: 4px;
  margin-bottom: 1rem;
}

button[type="submit"] {
  width: 100%;
  padding: 0.75rem;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
}

button[type="submit"]:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}
```

Notice what we did here:
- Every interactable element has a `data-testid` attribute
- We're using ARIA attributes for accessibility (`aria-invalid`, `aria-errormessage`)
- The form handles validation, loading states, and error states
- We're using React Hook Form with Zod for robust validation

This structure makes testing straightforward and maintainable.

---

## Writing Your First Playwright Test

Now let's write tests for our login form. Create the directory `e2e/` and add `e2e/login.spec.ts`:

```typescript
import { test, expect } from '@playwright/test';

test.describe('Login Form', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/');
  });

  test('should display login form elements', async ({ page }) => {
    // Check that main elements are visible
    await expect(page.getByTestId('login-title')).toHaveText('Welcome Back');
    await expect(page.getByTestId('email-label')).toHaveText('Email');
    await expect(page.getByTestId('password-label')).toHaveText('Password');
    await expect(page.getByTestId('login-submit-button')).toHaveText('Log In');
  });

  test('should show validation error for invalid email', async ({ page }) => {
    // Enter invalid email
    await page.getByTestId('email-input').fill('not-an-email');
    await page.getByTestId('password-input').fill('password123');

    // Submit form
    await page.getByTestId('login-submit-button').click();

    // Check for validation error
    await expect(page.getByTestId('email-error')).toBeVisible();
    await expect(page.getByTestId('email-error')).toHaveText(
      'Invalid email address'
    );
  });

  test('should show validation error for short password', async ({ page }) => {
    await page.getByTestId('email-input').fill('test@example.com');
    await page.getByTestId('password-input').fill('short');

    await page.getByTestId('login-submit-button').click();

    await expect(page.getByTestId('password-error')).toBeVisible();
    await expect(page.getByTestId('password-error')).toHaveText(
      'Password must be at least 8 characters'
    );
  });

  test('should show error banner for invalid credentials', async ({ page }) => {
    await page.getByTestId('email-input').fill('wrong@example.com');
    await page.getByTestId('password-input').fill('wrongpassword');

    await page.getByTestId('login-submit-button').click();

    // Wait for simulated API call
    await expect(page.getByTestId('login-error-banner')).toBeVisible();
    await expect(page.getByTestId('login-error-banner')).toHaveText(
      'Invalid email or password'
    );
  });

  test('should show loading state during submission', async ({ page }) => {
    await page.getByTestId('email-input').fill('test@example.com');
    await page.getByTestId('password-input').fill('password123');

    // Click submit and immediately check button text
    await page.getByTestId('login-submit-button').click();
    await expect(page.getByTestId('login-submit-button')).toHaveText(
      'Logging in...'
    );
  });

  test('should successfully login with valid credentials', async ({ page }) => {
    await page.getByTestId('email-input').fill('test@example.com');
    await page.getByTestId('password-input').fill('password123');

    await page.getByTestId('login-submit-button').click();

    // Wait for navigation to dashboard
    await page.waitForURL('/dashboard', { timeout: 2000 });
  });

  test('should be keyboard accessible', async ({ page }) => {
    // Tab through form
    await page.keyboard.press('Tab');
    await expect(page.getByTestId('email-input')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByTestId('password-input')).toBeFocused();

    await page.keyboard.press('Tab');
    await expect(page.getByTestId('login-submit-button')).toBeFocused();
  });
});
```

Run the tests:

```bash
npx playwright test
```

Or run tests in headed mode to see the browser:

```bash
npx playwright test --ui
```

Notice how clean and readable these tests are:
- We use `getByTestId()` for every element selection
- Test names clearly describe what's being tested
- Each test is independent and can run in any order
- We test success paths, error paths, validation, and accessibility

---

## Configuring Playwright

Let's fine-tune our Playwright configuration for better developer experience. Update `playwright.config.ts`:

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,

  // Reporter configuration
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['list'],
    ['json', { outputFile: 'test-results.json' }],
  ],

  use: {
    baseURL: 'http://localhost:5173',
    trace: 'retain-on-failure', // Keep trace only when test fails
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
    // Mobile viewport testing
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

Key configuration choices:
- **Multiple reporters**: HTML for detailed analysis, list for quick feedback, JSON for CI integration
- **Trace/screenshots/video only on failure**: Saves disk space while preserving debugging info
- **Multi-browser testing**: Chromium, Firefox, and WebKit (Safari)
- **Mobile viewport testing**: Ensures your form works on phones

Add these scripts to `package.json`:

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview",
    "test": "playwright test",
    "test:ui": "playwright test --ui",
    "test:headed": "playwright test --headed",
    "test:debug": "playwright test --debug",
    "test:report": "playwright show-report"
  }
}
```

---

## GitHub Actions CI/CD

Now let's set up automated testing with GitHub Actions. Create `.github/workflows/playwright.yml`:

```yaml
name: Playwright Tests

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    timeout-minutes: 60
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: lts/*
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Install Playwright Browsers
        run: npx playwright install --with-deps

      - name: Run Playwright tests
        run: npm run test

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 30

      - name: Upload test results JSON
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results-json
          path: test-results.json
          retention-days: 30
```

For even better feedback on pull requests, add a comment bot. Update the workflow:

```yaml
# Add this after the "Upload test results JSON" step

      - name: Comment PR with results
        if: github.event_name == 'pull_request' && always()
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const testResults = JSON.parse(fs.readFileSync('test-results.json', 'utf8'));

            const passed = testResults.stats.filter(s => s.expected === s.actual).length;
            const failed = testResults.stats.filter(s => s.expected !== s.actual).length;
            const flaky = testResults.stats.filter(s => s.actual === 0).length;

            const comment = `## 🧪 Test Results

            ✅ Passed: ${passed}
            ❌ Failed: ${failed}
            ⚠️ Flaky: ${flaky}

            ${failed > 0 ? '❌ Some tests failed. Please check the artifacts for details.' : '✅ All tests passed!'}

            [View full report](https://github.com/${{ github.repository }}/actions/runs/${{ github.run_id }})`;

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: comment
            });
```

This workflow will:
- Run on every push to main/develop and on every PR
- Install dependencies and Playwright browsers
- Run all tests across Chromium, Firefox, and WebKit
- Upload test reports as artifacts
- Comment on PRs with test results

---

## Best Practices & Common Pitfalls

After setting up Playwright on multiple projects, here are the lessons I've learned:

### **Do's ✅**

- **Use test IDs consistently**: Make them part of your component checklist
- **Name test IDs descriptively**: `login-submit-button` is better than `submit-btn`
- **Test user behavior, not implementation**: Test that a user can log in, not that a specific function was called
- **Keep tests independent**: Each test should be able to run alone
- **Use meaningful test names**: `should show error for invalid email` vs `test validation`
- **Test accessibility**: Include keyboard navigation and ARIA tests
- **Mock external dependencies**: Don't hit real APIs in tests

### **Don'ts ❌**

- **Don't use CSS selectors**: They break when styling changes
- **Don't test third-party libraries**: Trust that React Hook Form works
- **Don't ignore flaky tests**: They're a sign of deeper problems
- **Don't test everything**: Focus on critical user paths
- **Don't hardcode waits**: Use `waitFor` or `waitForSelector` instead
- **Don't share state between tests**: Use `beforeEach` to reset state

### **Common Pitfalls 🚨**

1. **Testing implementation details**: `expect(mockFunction).toHaveBeenCalled()` tells you nothing about whether your app works
2. **Skipping test IDs**: "I'll add them later" means they never get added
3. **Not testing mobile**: Bugs often appear only on small screens
4. **Forgetting accessibility**: Keyboard navigation and screen readers matter
5. **Too many assertions per test**: One logical assertion per test makes failures easier to debug

---

## What's Next

This is just the beginning of building a robust testing foundation with Playwright and React. In future articles, I'll cover:

- **Advanced Selectors**: Filtering lists, working with dynamic content
- **Visual Regression Testing**: Catching unintended UI changes with Percy and Playwright
- **API Mocking**: Testing edge cases without backend dependencies
- **Component Testing**: Using Playwright to test React components in isolation
- **Performance Testing**: Measuring and improving load times with Playwright
- **Authentication Strategies**: Testing login flows, sessions, and permissions

The foundation we've built here—test IDs, proper configuration, and a CI/CD pipeline—will make all of these advanced topics much easier to implement.

---

## Conclusion

We've covered a lot of ground: setting up a React project with Vite, installing and configuring Playwright, building a login form with proper test IDs, writing comprehensive tests, and automating everything with GitHub Actions.

But more importantly, we've established a **testing philosophy** that will scale with your project:

1. **Test IDs create a stable contract** between your UI and tests
2. **Configuration matters**—invest time upfront in setup
3. **Test user behavior, not implementation details**
4. **Automate everything** with CI/CD from day one
5. **Plan for accessibility** and cross-browser compatibility

When you follow these principles, testing becomes a tool for confidence rather than a chore to dread. You can refactor, redesign, and evolve your application without fear of breaking things.

The next time you start a React project, take ten minutes to set up Playwright with test IDs. Your future self will thank you.

---

**Resources:**
- [Playwright Documentation](https://playwright.dev)
- [React Hook Form](https://react-hook-form.com)
- [Testing Best Practices](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

*Have questions or run into issues? Drop a comment below or reach out to me on LinkedIn. Happy testing!*

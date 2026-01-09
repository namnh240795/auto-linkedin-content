# How to Use Claude to Write Clean, Testable Code in Docker

🎯 **We've all been there.**

You write code that works locally, fails in staging, and causes incidents in production.

Or worse, the code works but is untestable, undocumented, and impossible for anyone else to maintain. 😱

The frustration of legacy codebases and technical debt is something every developer knows too well.

***

⚠️ **THE PROBLEM: CODE QUALITY IS HARD TO MAINTAIN**

When I started working with <a href='https://claude.ai'>Claude</a> (Anthropic's AI), I made a critical mistake. 🚫

I was treating it as a chatbot for quick answers, not as a partner for writing production-quality code.

My code had issues like:
- ❌ No proper error handling
- ❌ Missing edge case coverage
- ❌ Inconsistent naming conventions
- ❌ Poor separation of concerns
- ❌ Hard to test in isolation

📌 **Here's what typically happens:**

✏️ You ask Claude for a quick code snippet
🎨 You copy-paste it into your project
❌ Tests fail because of missing dependencies
🔧 Integration breaks because of assumptions
🔄 Tech debt accumulates, sprint after sprint

This is the path to legacy codebases and weekend debugging sessions.

***

✨ **THE SOLUTION: CLAUNE + DOCKER FOR TDD**

**Claude-supported Test-Driven Development** means you write clean, testable code from the start.

Build a robust development workflow with:
✅ <a href='https://claude.ai'>Claude</a> - AI coding partner with strong testing knowledge
✅ <a href='https://www.docker.com/'>Docker</a> - Consistent local environment
✅ <a href='https://nodejs.org'>Node.js</a> / <a href='https://nestjs.com'>NestJS</a> - Backend framework
✅ <a href='https://react.dev'>React</a> / <a href='https://vuejs.org'>Vue</a> - Frontend framework
✅ <a href='https://jestjs.io/'>Jest</a> / <a href='https://vitest.dev'>Vitest</a> - Testing framework

👇 **Look at the difference:**

```typescript
// ❌ Bad: Quick Claude snippet without testing
async function getUser(id: number) {
  const user = await db.users.findOne({ id });
  return user; // What if user doesn't exist?
}
```

```typescript
// ✅ Good: Claude-guided TDD approach
// Test first
describe('getUser', () => {
  it('should return user for valid id', async () => {
    const user = await getUser(1);
    expect(user).toBeDefined();
    expect(user.email).toBe('test@example.com');
  });

  it('should throw for invalid id', async () => {
    await expect(getUser(999)).rejects.toThrow('User not found');
  });
});

// Implementation with error handling
async function getUser(id: number): Promise<User> {
  const user = await db.users.findOne({ id });

  if (!user) {
    throw new NotFoundException(`User with id ${id} not found`);
  }

  return user;
}
```

💡 **Why this works:**

✅ Tests define the contract upfront
✅ Claude writes production-ready code
✅ Docker ensures environment consistency
✅ Edge cases are handled from day one
✅ Code is modular and testable

***

🚀 **QUICK PROJECT SETUP**

Let's set up a full-stack project with <a href='https://claude.ai'>Claude</a> and <a href='https://www.docker.com/'>Docker</a>.

📦 **Project structure:**

```
fullstack-app/
├── backend/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── frontend/
│   ├── src/
│   ├── tests/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── CLAUDE_WORKFLOW.md
```

⚙️ **Initialize backend:**

```bash
mkdir backend && cd backend
npm init -y
npm install @nestjs/common @nestjs/core @nestjs/platform-express
npm install @nestjs/testing jest
npm install -D @types/node
```

⚙️ **Initialize frontend:**

```bash
mkdir frontend && cd frontend
npm create vite@latest . --template react-ts
npm install -D vitest @testing-library/react @testing-library/jest-dom
```

🐳 **Create docker-compose.yml:**

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "3000:3000"
    volumes:
      - ./backend:/app
      - /app/node_modules
    environment:
      - NODE_ENV=development

  frontend:
    build: ./frontend
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:3000
```

Start everything:

```bash
docker-compose up -d
```

***

🤖 **THE CLAUDE WORKFLOW**

Here's how to use Claude effectively for TDD.

**Step 1: Ask Claude for test coverage**

```
I need to create a user authentication service for NestJS.
Write comprehensive tests first (TDD approach).
Cover: successful login, invalid credentials,
missing fields, and edge cases.
```

Claude generates:

```typescript
// backend/src/auth/auth.service.spec.ts
describe('AuthService', () => {
  let service: AuthService;
  let usersRepository: Repository<User>;

  beforeEach(async () => {
    const module = await Test.createTestingModule({
      providers: [
        AuthService,
        {
          provide: getRepositoryToken(User),
          useValue: mockRepository,
        },
      ],
    }).compile();

    service = module.get<AuthService>();
    usersRepository = module.get<Repository<User>>();
  });

  describe('login', () => {
    it('should return user and token for valid credentials', async () => {
      // Arrange
      const loginDto: LoginDto = {
        email: 'test@example.com',
        password: 'password123',
      };

      // Act
      const result = await service.login(loginDto);

      // Assert
      expect(result.user).toBeDefined();
      expect(result.access_token).toBeDefined();
      expect(result.user.email).toBe('test@example.com');
    });

    it('should throw UnauthorizedException for invalid email', async () => {
      const loginDto: LoginDto = {
        email: 'wrong@example.com',
        password: 'password123',
      };

      await expect(service.login(loginDto)).rejects.toThrow(
        UnauthorizedException
      );
    });

    it('should throw UnauthorizedException for wrong password', async () => {
      const loginDto: LoginDto = {
        email: 'test@example.com',
        password: 'wrongpassword',
      };

      await expect(service.login(loginDto)).rejects.toThrow(
        UnauthorizedException
      );
    });
  });
});
```

**Step 2: Ask Claude to implement**

```
Now implement the AuthService to make these tests pass.
Use proper error handling, DTOs, and JWT tokens.
```

Claude generates:

```typescript
// backend/src/auth/auth.service.ts
@Injectable()
export class AuthService {
  constructor(
    @InjectRepository(User)
    private usersRepository: Repository<User>,
    private jwtService: JwtService,
  ) {}

  async login(loginDto: LoginDto): Promise<LoginResponseDto> {
    const user = await this.usersRepository.findOne({
      where: { email: loginDto.email },
    });

    if (!user) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const isPasswordValid = await bcrypt.compare(
      loginDto.password,
      user.password
    );

    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid credentials');
    }

    const payload = { sub: user.id, email: user.email };
    const access_token = this.jwtService.sign(payload);

    return {
      access_token,
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
      },
    };
  }
}
```

**Step 3: Ask Claude for edge cases**

```
Add tests for these edge cases:
1. SQL injection attempt in email field
2. Very long password (>100 chars)
3. Empty/null/undefined fields
4. Concurrent login attempts
```

Claude generates validation and security tests.

***

🎨 **FRONTEND WITH CLAUDE**

For frontend development, use Claude for component-driven development.

**Ask for component test first:**

```
Create a LoginForm component with tests.
Requirements:
- Email and password fields
- Client-side validation
- Error display
- Loading state
- Accessibility attributes
```

Claude generates test:

```typescript
// frontend/src/components/LoginForm.test.tsx
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { LoginForm } from './LoginForm';

describe('LoginForm', () => {
  it('should render form fields', () => {
    render(<LoginForm onLogin={jest.fn()} />);

    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i }))
      .toBeInTheDocument();
  });

  it('should show validation error for invalid email', async () => {
    render(<LoginForm onLogin={jest.fn()} />);

    const emailInput = screen.getByLabelText(/email/i);
    const submitButton = screen.getByRole('button', { name: /submit/i });

    await userEvent.type(emailInput, 'not-an-email');
    await userEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/invalid email/i))
        .toBeInTheDocument();
    });
  });

  it('should be keyboard accessible', async () => {
    render(<LoginForm onLogin={jest.fn()} />);

    const emailInput = screen.getByLabelText(/email/i);

    await userEvent.tab();
    expect(emailInput).toHaveFocus();

    await userEvent.tab();
    expect(screen.getByLabelText(/password/i)).toHaveFocus();
  });
});
```

Then Claude implements the component.

***

🧪 **RUNNING TESTS IN DOCKER**

One of the biggest advantages: test locally in Docker before committing.

```bash
# Run backend tests in Docker container
docker-compose exec backend npm test

# Run frontend tests in Docker container
docker-compose exec frontend npm test

# Run all tests
docker-compose exec -T backend npm test &
docker-compose exec -T frontend npm test &
wait
```

**benefits of Docker testing:**

✅ Same environment as production
✅ No "works on my machine" issues
✅ Easy CI/CD integration
✅ Reproducible test results

***

💡 **WHY THIS APPROACH IS POWERFUL**

**1. Testability First**

When you ask Claude for tests first, it creates comprehensive coverage:

```typescript
// Claude generates tests for:
✅ Happy path
✅ Error cases
✅ Edge cases
✅ Security scenarios
✅ Performance benchmarks
```

**2. Consistent Code Quality**

Claude follows best practices:

```typescript
// ✅ Claude writes:
- Clear function names (getUserById, not getUser)
- JSDoc comments
- Type annotations
- Error handling
- Input validation
```

**3. Docker Environment Consistency**

```yaml
# docker-compose.yml ensures:
✅ Same Node version for all developers
✅ Same dependency versions
✅ Same database versions
✅ Easy onboarding for new team members
```

**4. Faster Development Cycle**

```
❌ Old way: Code → Commit → CI fails → Fix → Repeat (30 min cycle)
✅ New way: Test locally in Docker → Commit → CI passes (5 min cycle)
```

**5. Better Collaboration**

With Claude + Docker:
- Code is self-documenting (tests as documentation)
- New developers run `docker-compose up` and start contributing
- Pull requests are smaller and more focused
- Code reviews focus on logic, not formatting

***

🎯 **BEST PRACTICES**

✅ **DO:**

- Always ask Claude for tests first (TDD)
- Run tests in Docker before committing
- Ask Claude for edge cases you haven't considered
- Use Claude to refactor code for better testability
- Keep tests fast and focused
- Use Docker for all development environments

❌ **DON'T:**

- Skip tests to "move faster"
- Run tests only in CI/CD
- Accept Claude code without review
- Ignore Docker environment setup
- Test logic without testing error cases
- Mix local and Docker environments inconsistently

***

🎓 **KEY TAKEAWAYS**

1️⃣ **Claude + TDD** produces production-ready code from day one

2️⃣ **Docker ensures** consistent environments across all developers

3️⃣ **Test-first approach** catches edge cases Claude might miss

4️⃣ **Local Docker testing** prevents CI/CD failures

5️⃣ **Clean architecture** emerges naturally from testable code

🚀 **The next time you start a feature, write the tests first with Claude, run them in Docker, and build from there.**

Your future self (and your team) will thank you! 🙏

***

📚 **RESOURCES**

🔗 <a href='https://docs.anthropic.com/claude/docs'>Claude Documentation</a>
🔗 <a href='https://docs.anthropic.com/claude/docs/testing'>Testing with Claude</a>
🔗 <a href='https://jestjs.io/docs/getting-started'>Jest Testing Framework</a>
🔗 <a href='https://vitest.dev/guide/'>Vitest Documentation</a>
🔗 <a href='https://docs.docker.com/compose/'>Docker Compose Guide</a>
🔗 <a href='https://nestjs.com/techniques/testing'>NestJS Testing</a>

💬 **Have questions? Drop a comment below or reach out to me on LinkedIn!**

**Happy clean coding! 🎉**

#claude #ai #coding #testing #docker #tdd #fullstack #nestjs #react #cleancode #createdbyzai

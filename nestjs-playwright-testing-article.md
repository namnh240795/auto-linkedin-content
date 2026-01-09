# How to Set Up NestJS API Testing with PostgreSQL, Docker, and Playwright

🎯 **We've all been there.**

You push a backend API change to production, and suddenly integration tests are failing everywhere.

Or worse, the tests pass but the API contract is broken and frontend apps are crashing. 😱

The frustration of unreliable API tests is something every backend developer knows too well.

***

⚠️ **THE PROBLEM: API CONTRACTS ARE FRAGILE**

When I started building REST APIs with <a href='https://nestjs.com'>NestJS</a>, I made a critical mistake. 🚫

I was testing APIs without proper type safety, and tests broke every time I:
- Changed a field name in the database
- Modified validation rules
- Updated response structures

📌 **Here's what typically happens:**

✏️ You write API tests assuming specific response fields
🎨 Database schema changes
❌ API contract breaks
🔧 Frontend integration fails
🔄 You update tests, fix frontend, panic in production

This is the path to fragile APIs and sleepless nights.

***

✨ **THE SOLUTION: TYPE-SAFE API TESTING**

**Type-safe API development** means your tests catch contract issues before production.

Build a robust testing foundation with:
✅ <a href='https://nestjs.com'>NestJS</a> - Type-safe Node.js framework
✅ <a href='https://www.postgresql.org/'>PostgreSQL</a> - Production database
✅ <a href='https://www.docker.com/'>Docker</a> - Containerized testing environment
✅ <a href='https://playwright.dev'>Playwright</a> - Reliable API testing
✅ <a href='https://swagger.io'>Swagger</a> - Auto-generated API documentation

👇 **Look at the difference:**

```typescript
// ❌ Bad: Untyped API request
const response = await fetch('/api/auth/login');
const data = await response.json(); // What fields exist here?

// ✅ Good: Type-safe with validation
const response = await fetch('/api/auth/login', {
  method: 'POST',
  body: JSON.stringify(loginDto)
});
const data = await response.json() as LoginResponseDto; // Typed!
```

💡 **Why this works:**

✅ Tests catch contract violations
✅ TypeScript ensures type safety
✅ Docker provides consistent test environment
✅ Swagger documents API automatically
✅ Validation prevents invalid data

***

🚀 **QUICK PROJECT SETUP**

Let's set up a new <a href='https://nestjs.com'>NestJS</a> project with <a href='https://www.postgresql.org/'>PostgreSQL</a> and <a href='https://playwright.dev'>Playwright</a>.

📦 **Step 1: Create NestJS project**

```bash
npm i -g @nestjs/cli
nest new nestjs-playwright-api
cd nestjs-playwright-api
```

⚙️ **Step 2: Install dependencies**

```bash
# Database and validation
npm install @nestjs/typeorm typeorm pg
npm install class-validator class-transformer
npm install @nestjs/swagger

# Testing
npm install -D @playwright/test
npx playwright install
```

📚 **Step 3: Install Docker dependencies**

```bash
# Docker environment
npm install -D docker-compose
```

***

🎨 **BUILDING THE LOGIN API**

Create a type-safe authentication endpoint with proper DTOs.

First, define your DTOs with validation:

`src/auth/dto/login.dto.ts`

```typescript
import { IsEmail, IsString, MinLength } from 'class-validator';

export class LoginDto {
  @IsEmail({}, { message: 'Invalid email address' })
  email: string;

  @IsString()
  @MinLength(8, { message: 'Password must be at least 8 characters' })
  password: string;
}
```

`src/auth/dto/login-response.dto.ts`

```typescript
import { ApiProperty } from '@nestjs/swagger';

export class LoginResponseDto {
  @ApiProperty()
  access_token: string;

  @ApiProperty()
  user: {
    id: number;
    email: string;
    name: string;
  };
}
```

Create the auth controller:

`src/auth/auth.controller.ts`

```typescript
import { Body, Controller, Post } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
import { LoginResponseDto } from './dto/login-response.dto';

@ApiTags('auth')
@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  @Post('login')
  @ApiOperation({ summary: 'Login user' })
  @ApiResponse({ status: 200, type: LoginResponseDto })
  @ApiResponse({ status: 401, description: 'Unauthorized' })
  async login(@Body() loginDto: LoginDto): Promise<LoginResponseDto> {
    return this.authService.login(loginDto);
  }
}
```

Enable global validation pipe:

`src/main.ts`

```typescript
import { ValidationPipe } from '@nestjs/common';
import { NestFactory } from '@nestjs/core';
import { SwaggerModule, DocumentBuilder } from '@nestjs/swagger';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // Enable validation
  app.useGlobalPipes(new ValidationPipe({
    whitelist: true,
    forbidNonWhitelisted: true,
    transform: true,
  }));

  // Swagger documentation
  const config = new DocumentBuilder()
    .setTitle('NestJS API')
    .setVersion('1.0')
    .addBearerAuth()
    .build();
  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api', app, document);

  await app.listen(3000);
}
bootstrap();
```

***

🗄️ **ADDING POSTGRESQL WITH TYPEORM**

Configure database connection:

`src/app.module.ts`

```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AuthModule } from './auth/auth.module';

@Module({
  imports: [
    TypeOrmModule.forRoot({
      type: 'postgres',
      host: process.env.DB_HOST || 'localhost',
      port: parseInt(process.env.DB_PORT) || 5432,
      username: process.env.DB_USER || 'postgres',
      password: process.env.DB_PASSWORD || 'postgres',
      database: process.env.DB_NAME || 'test_db',
      entities: [__dirname + '/**/*.entity{.ts,.js}'],
      synchronize: true, // Only for development!
    }),
    AuthModule,
  ],
})
export class AppModule {}
```

Create user entity:

`src/users/entities/user.entity.ts`

```typescript
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity('users')
export class User {
  @PrimaryGeneratedColumn()
  id: number;

  @Column({ unique: true })
  email: string;

  @Column()
  password: string;

  @Column()
  name: string;
}
```

***

🐳 **DOCKER SETUP FOR LOCAL TESTING**

Create `docker-compose.yml` for local development:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    container_name: nestjs_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: test_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

Create `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=test_db
```

Start the database:

```bash
docker-compose up -d
```

***

✅ **WRITING PLAYWRIGHT API TESTS**

Create API tests that verify the entire contract.

`tests/api/auth.spec.ts`

```typescript
import { test, expect } from '@playwright/test';

const API_URL = process.env.API_URL || 'http://localhost:3000';

test.describe('Auth API', () => {
  test('should login with valid credentials', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/login`, {
      data: {
        email: 'test@example.com',
        password: 'password123',
      },
    });

    expect(response.status()).toBe(200);

    const data = await response.json();

    // Verify response structure matches LoginResponseDto
    expect(data).toHaveProperty('access_token');
    expect(data).toHaveProperty('user');
    expect(data.user).toHaveProperty('id');
    expect(data.user).toHaveProperty('email', 'test@example.com');
    expect(data.user).toHaveProperty('name');
  });

  test('should reject invalid email', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/login`, {
      data: {
        email: 'not-an-email',
        password: 'password123',
      },
    });

    expect(response.status()).toBe(400);

    const data = await response.json();
    expect(data).toHaveProperty('message');
    expect(data.message).toContain('email');
  });

  test('should reject short password', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/login`, {
      data: {
        email: 'test@example.com',
        password: 'short',
      },
    });

    expect(response.status()).toBe(400);

    const data = await response.json();
    expect(data.message).toContain('password');
  });

  test('should reject invalid credentials', async ({ request }) => {
    const response = await request.post(`${API_URL}/auth/login`, {
      data: {
        email: 'test@example.com',
        password: 'wrongpassword',
      },
    });

    expect(response.status()).toBe(401);
  });
});
```

Create `playwright.config.ts`:

```typescript
import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: process.env.API_URL || 'http://localhost:3000',
  },
});
```

▶️ **Run the tests:**

```bash
# Start the API
npm run start:dev

# In another terminal, run tests
npm run test
```

***

🤖 **DOCKER SETUP FOR TEST AUTOMATION**

Create a test-specific Docker setup:

`docker-compose.test.yml`

```yaml
version: '3.8'

services:
  postgres-test:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: test_user
      POSTGRES_PASSWORD: test_password
      POSTGRES_DB: test_db
    ports:
      - "5433:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test_user"]
      interval: 5s
      timeout: 3s
      retries: 5

  api-test:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      DB_HOST: postgres-test
      DB_PORT: 5432
      DB_USER: test_user
      DB_PASSWORD: test_password
      DB_NAME: test_db
    ports:
      - "3000:3000"
    depends_on:
      postgres-test:
        condition: service_healthy
    command: npm run test:e2e
```

Create test script in `package.json`:

```json
{
  "scripts": {
    "test": "playwright test",
    "test:docker": "docker-compose -f docker-compose.test.yml up --build",
    "test:local": "docker-compose up -d && npm run start:dev & npm run test"
  }
}
```

🎯 **Test automation workflow:**

```bash
# Run tests with Docker
npm run test:docker

# Or test locally against Docker database
npm run test:local
```

***

💡 **BEST PRACTICES**

✅ **DO:**

- Use DTOs for all API inputs/outputs
- Validate all input with class-validator
- Type all responses as DTOs
- Use Docker for consistent test environments
- Test both success and failure cases
- Document APIs with Swagger
- Run tests in CI/CD pipeline
- Use environment-specific configs

❌ **DON'T:**

- Skip DTO validation
- Use `any` types
- Hardcode database URLs
- Test without proper cleanup
- Forget to test validation
- Ignore error responses
- Mix test and production databases

***

🎓 **KEY TAKEAWAYS**

1️⃣ **DTOs create type-safe contracts** between frontend and backend

2️⃣ **Validation prevents bad data** from entering your system

3️⃣ **Docker ensures consistency** across development and testing

4️⃣ **Swagger documents automatically** when you use decorators

5️⃣ **Playwright tests verify contracts** end-to-end

🚀 **The next time you build a NestJS API, take the time to set up proper DTOs, validation, Docker, and automated tests.**

Your future self (and your frontend team) will thank you! 🙏

***

📚 **RESOURCES**

🔗 <a href='https://nestjs.com/'>NestJS Documentation</a>
🔗 <a href='https://docs.nestjs.com/techniques/validation'>Validation with NestJS</a>
🔗 <a href='https://playwright.dev/docs/api-testing'>Playwright API Testing</a>
🔗 <a href='https://swagger.io/specification/'>OpenAPI Specification</a>
🔗 <a href='https://www.postgresql.org/docs/'>PostgreSQL Documentation</a>
🔗 <a href='https://docs.docker.com/compose/'>Docker Compose Documentation</a>

💬 **Have questions? Drop a comment below or reach out to me on LinkedIn!**

**Happy testing! 🚀**

#nestjs #postgresql #docker #playwright #testing #backend #api #typescript #swagger #createdbyzai

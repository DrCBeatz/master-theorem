# Master Theorem Evaluation Web App

This web application allows users to evaluate recursive divide-and-conquer algorithms using the Master Theorem to determine their time complexity, providing valuable insights into algorithm performance.

Algorithms with the following recurrence relation (Master Recurrence) can be evaluated:

```
T(n) = aT(n/b) + f(n)
```

where:

- **a** = number of recursive subproblems (a > 0)
- **b** = factor by which the problem size is reduced (b > 1)
- **k** = exponent of the work outside the recursion

## Features

- Evaluate the time complexity of divide-and-conquer algorithms.
- Visualize algorithm performance.
- Compare preset algorithms (e.g., binary search, merge sort).
- View Python code and descriptions for preset algorithms.

## How to Use the App

1. Enter your values for **a**, **b**, and **k** in the input fields.
2. Select 'User Input' under 'Enter Values or Choose Algorithm'.
3. Click **Evaluate** to see results.

### Example Inputs:

- a = 4, b = 2, k = 1
- a = 4, b = 2, k = 2
- a = 4, b = 2, k = 3

Or choose preset algorithms from the dropdown, then click **Evaluate** to see algorithm details.

## Local Installation

### Prerequisites:

- Docker CLI
- Node Package Manager (NPM)
- Material Design for Bootstrap Pro for React (MDB Pro)

### MDB Pro Setup

This project requires Material Design for Bootstrap Pro for React to run locally. You must include your MDB Pro key using the `MDB_PRO_KEY` environment variable.

Before starting the Docker container, run:

```bash
cd frontend
npm run add-mdb-key
cd ..
```

Before committing changes to GitHub, ensure your MDB key is not included by running:

```bash
cd frontend
npm run remove-mdb-key
cd ..
```

### Clone and Setup

Clone and navigate to the project:

```bash
git clone https://github.com/drcbeatz/master-theorem.git
cd master-theorem
```

Build and run Docker containers:

```bash
docker compose build
docker compose up -d
```

Containers launched:

- Backend service at **port 8000**
- Frontend service at **port 5173**
- Local DynamoDB at **port 8001**

## Running Tests

### Backend Tests

From the project's root directory:

**Run tests with coverage (recommended)**:

```bash
docker compose run --rm test /bin/bash -c "
  python backend/scripts/init_db.py || true
  pytest --cov=backend --cov-report=term-missing --cov-report=html:coverage/html backend/tests
"
```

This will:

- Initialize DynamoDB if required.
- Run `pytest` with coverage reports.

**Simpler approach (no coverage)**:

```bash
docker compose exec backend pytest backend/tests
```

> **Note:** The first approach matches the CI pipeline.

### Frontend Tests

Run React/Vitest tests from the `frontend` directory:

```bash
npm test
```

To view test coverage:

```bash
npm run test:coverage
```

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). _Introduction to Algorithms_ (4th ed.). MIT Press.

---

Happy Coding! If you encounter issues, please open an issue or submit a pull request.

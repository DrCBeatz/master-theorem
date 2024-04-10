# Master Theorem Evaluation Web App

This web application allows users to evaluate recursive divide and conquer algorithms using the Master Theorem and determine their time complexity, providing valuable insights into algorithm performance.

Algorithms with the following recurrence relation (known as the Master Recurrence) can be evaluated using the Master Theorem:

`T(n) = aT(n/b) + f(n)`

where a > 0 and b > 1

- a = the number of recursive subproblems
- b = the factor by which the problem size is reduced
- k = the exponent of the work outside the recursion

## Features

- Evaluate the time complexity of divide and conquer algorithms.
- Visualization of algorithm performance.
- Comparison between different algorithms through preset options.
- Python code and description of preset algorithms.

## How to use the app:

1. Enter your own values for a, b, and k in the respective input fields.
2. Ensure the 'User Input' option is selected under 'Enter Values or Choose Algorithm'.
3. Click the 'Evaluate' button to see the results.

Try the following sample inputs:

- a = 4, b = 2, k = 1
- a = 4, b = 2, k = 2
- a = 4, b = 2, k = 3

You can also choose from various preset algorithms (e.g., binary search or merge sort) by clicking the 'Enter Values or Choose Algorithm' select field, then click 'Evaluate'. You'll be able to see sample code and a description of the algorithm below the evaluation.

## How to install locally

### Installation requirements:

- Docker CLI
- NPM

At the command line/terminal, type the following commands.

```bash
git clone https://github.com/drcbeatz/master-theorem.git

cd master-theorem

docker compose build

docker compose up -d

cd frontend

npm install

npm run dev
```

(then click on the link to view the React front end in your web browser).

You can also run the backend tests in the root directory with the following command:

```bash
docker compose exec web pytest
```

To run the front end tests, go to the 'frontend' directory and type the following command:

```bash
npm test
```

## References

- Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). _Introduction to Algorithms_ (4th ed.). MIT Press.

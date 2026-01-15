# SQLite `GROUP BY` vs `DENSE_RANK`

Simple benchmark of SQLite3 using Python to test comparable queries for a test case

## How to run

1. Make sure that you have uv installed.
2. After installing it, run `uv run main.py`.
3. Next, run `uv run bench.py`.
4. To view the results, open up the benchmark_results.png image to see the box and whisker plot.

Here is an example:

Table schema:
```
CREATE TABLE Department (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
CREATE TABLE Employee (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    salary INTEGER NOT NULL,
    departmentId INTEGER,
    FOREIGN KEY (departmentId) REFERENCES Department(id)
);
```

Query 1:
```sql
SELECT departmentId, MAX(salary)
FROM Employee
GROUP BY departmentId;
```

Query 2:
```sql
SELECT departmentId, salary
FROM (
    SELECT departmentId, salary,
           DENSE_RANK() OVER (
               PARTITION BY departmentId
               ORDER BY salary DESC
           ) AS rnk
    FROM Employee
)
WHERE rnk = 1;
```

![bench_results](benchmark_results.png)

You can change the executing code in `bench.py` to test different configurations of the query.

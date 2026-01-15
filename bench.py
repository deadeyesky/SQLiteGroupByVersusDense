import sqlite3
import time
import statistics
import matplotlib.pyplot as plt

DB_PATH = "company.db"
REPS = 100
WARMUP_RUNS = 10
OUTPUT_IMAGE = "benchmark_results.png"

QUERY_GROUP_BY = """
SELECT departmentId, MAX(salary)
FROM Employee
GROUP BY departmentId;
"""

QUERY_DENSE_RANK = """
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
"""

def benchmark(query):
    times = []

    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        # Warmup runs (discarded)
        for _ in range(WARMUP_RUNS):
            cursor.execute(query)
            cursor.fetchall()

        # Timed runs
        for _ in range(REPS):
            start = time.perf_counter()
            cursor.execute(query)
            cursor.fetchall()
            end = time.perf_counter()
            times.append(end - start)

    return times

print("Running benchmarks...")

times_group_by = benchmark(QUERY_GROUP_BY)
times_dense_rank = benchmark(QUERY_DENSE_RANK)

print("GROUP BY avg:", statistics.mean(times_group_by))
print("DENSE_RANK avg:", statistics.mean(times_dense_rank))

# Create box-and-whisker plot
plt.figure(figsize=(8, 5))
plt.boxplot(
    [times_group_by, times_dense_rank],
    labels=["GROUP BY + MAX", "DENSE_RANK"],
    showmeans=True
)
plt.ylabel("Execution time (seconds)")
plt.title("SQLite Query Performance (100 runs)")
plt.grid(True, linestyle="--", alpha=0.6)

plt.tight_layout()

# Save image instead of (or in addition to) showing it
plt.savefig(OUTPUT_IMAGE, dpi=300)
plt.close()

print(f"Benchmark plot saved as '{OUTPUT_IMAGE}'")


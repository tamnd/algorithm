---
tag: KEY8Q5
kind: algorithm
slug: moore-hodgson-algorithm
name: Moore-Hodgson algorithm
aliases:
- Hodgson's algorithm
- Moore's algorithm
area: systems/scheduling
level: advanced
summary: "Scan jobs by due date and keep them in a max-heap by length; when the new job would be late, drop the longest kept job. Minimizes late jobs, 1||ΣUj, in O(n log n)."
solves: [minimizing-late-jobs]
model: word-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: O(n log n), average: O(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1968
  people: [J. Michael Moore, Thom J. Hodgson]
  note: Moore published the algorithm in 1968 in Management Science, together with a simpler form that he credits to Hodgson.
prereqs: [minimizing-late-jobs, earliest-due-date-first, binary-heap]
see_also: [minimizing-tardy-jobs, minimizing-number-of-late-jobs, weighted-tardy-jobs, priority-queue, single-machine-scheduling, knapsack-problem, exchange-argument, lawler-algorithm]
sources:
  - paper: doi:10.1287/mnsc.15.1.102
    title: J. Michael Moore, An n job, one machine sequencing algorithm for minimizing the number of late jobs, Management Science 15(1), 1968
    locator: pages 102 to 109 (the algorithm, its proof, and the simpler form credited to Hodgson)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Section 3.3, The Number of Tardy Jobs
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (the number of late jobs)
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84 (the O(n Σp) dynamic program for the weighted number of late jobs)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972
    locator: pages 85 to 103 (sequencing with deadlines and penalties, NP-complete)
---

The Moore-Hodgson algorithm solves the problem of [minimizing the number of late jobs](/minimizing-late-jobs/) on one machine, $1 \| \sum U_j$. It scans the jobs in [earliest due date](/earliest-due-date-first/) order and keeps the accepted jobs in a [max-heap](/binary-heap/) keyed by processing time. When the newest job would complete after its due date, it removes the longest accepted job, which may be the newest one or an earlier one. The jobs that remain are all on time, there are as many of them as possible, and their total time is as small as possible. It runs in $O(n \log n)$ time. This page is the implementation view, with a heap, a proof by a sorted-vector invariant, and tests against all subsets; the [approximation-area page](/minimizing-tardy-jobs/) proves the same result by deleting one job from an optimal set.

## In plain words

Go through the jobs from the earliest due date to the latest. Add each job to a plan, and keep a running total of the time that the plan needs. If the newest job would now finish too late, something has to go. Throw out the longest job in the plan, even if it came much earlier. That frees the most time with the loss of only one job. At the end, run the jobs that are still in the plan, in due date order. They are all on time. Run the thrown-out jobs after them. They are late, but no other plan has fewer late jobs.

## The problem

There are $n$ jobs, all present at time $0$, on one machine without preemption. Job $j$ has a processing time $p_j \ge 0$ and a due date $d_j$. It is late if it completes after $d_j$. The goal is an order with the fewest late jobs. A set of jobs can all be on time exactly when, in due date order, each job completes by its due date, so the task is to choose a largest such set and run it first in due date order.

## The algorithm

```pseudo id=main
MOORE-HODGSON(p[1 .. n], d[1 .. n])
L1  renumber the jobs so that d[1] ≤ d[2] ≤ … ≤ d[n]
L2  H ← empty max-heap keyed by p; t ← 0; late ← empty list
L3  for k ← 1 to n do
L4      INSERT(H, k); t ← t + p[k]
L5      if t > d[k] then                    ▷ job k would be late
L6          j ← EXTRACT-MAX(H)              ▷ the longest job kept so far
L7          t ← t − p[j]; append j to late
L8  return the jobs in H in due date order, then the jobs in late
```

The variable $t$ is always the total time of the jobs in $H$, which is the completion time of job $k$ if the jobs in $H$ run in due date order. Line L5 needs only this one test: the jobs that were in $H$ before job $k$ were all on time, and adding job $k$ at the end does not move them. After line L7 the set in $H$ is again all on time; the proof shows why. Ties in line L6 can be broken in any way.

## Example

Seven jobs, already in due date order.

| job | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| $p_j$ | 3 | 2 | 4 | 1 | 6 | 2 | 3 |
| $d_j$ | 4 | 5 | 8 | 9 | 12 | 13 | 14 |

| step $k$ | $t$ after L4 | late? | removed by L6 | $t$ after L7 | jobs in $H$ |
|---|---|---|---|---|---|
| 1 | 3 | no | | 3 | 1 |
| 2 | 5 | no | | 5 | 1, 2 |
| 3 | 9 | yes, $9 > 8$ | 3 ($p = 4$) | 5 | 1, 2 |
| 4 | 6 | no | | 6 | 1, 2, 4 |
| 5 | 12 | no | | 12 | 1, 2, 4, 5 |
| 6 | 14 | yes, $14 > 13$ | 5 ($p = 6$) | 8 | 1, 2, 4, 6 |
| 7 | 11 | no | | 11 | 1, 2, 4, 6, 7 |

The output order is $1, 2, 4, 6, 7, 3, 5$. The first five jobs complete at $3, 5, 6, 8, 11$, all by their due dates. Jobs $3$ and $5$ are late. No set of $6$ jobs can all be on time, so $2$ late jobs is the least possible. At step 3 the removed job is the new one. At step 6 it is job $5$, which was accepted two steps earlier; this is the move that a simpler greedy misses. The rule "reject the new job when it would be late" keeps job $5$ at step 6, then must also reject job $7$, and ends with only $4$ jobs on time. Running all jobs in due date order makes $5$ jobs late.

## Correctness

Number the jobs in due date order and let $E_k$ be the set in $H$ after step $k$. Compare sets of jobs by their processing times sorted in increasing order: say $E$ *dominates* $S$ if $|S| \le |E|$ and, for each $i \le |S|$, the $i$-th smallest time in $E$ is at most the $i$-th smallest time in $S$. The invariant is that $E_k$ is on time in due date order and dominates every set of jobs among $1, \ldots, k$ that can all be on time. The step uses two facts. Adding one value to two sorted lists keeps the domination, because the $i$-th smallest of a list plus $x$ is $\min(a_i, \max(a_{i-1}, x))$, which is monotone in the list. And a set $S \subseteq \{1, \ldots, k\}$ that is all on time has total time at most $d_k$, since its last job in due date order completes at that total. If line L5 fires and some such $S$ with $k \in S$ had $|E_{k-1}| + 1$ jobs, the domination would give a total time of $E_{k-1} \cup \{k\}$ at most that of $S$, so at most $d_k$, against the test of line L5. Removing the largest time then keeps the domination. For the feasibility after a removal of job $\ell \ne k$: $p_\ell \ge p_k$, so job $k$ now completes by the old total of $E_{k-1}$, which is at most the due date of the last job of $E_{k-1}$, which is at most $d_k$. At $k = n$ the invariant says that $E_n$ is as large as any on-time set and has the least total time among them. The full proof is below.

## Complexity

- **Time.** Line L1 is a sort, $O(n \log n)$. Each job enters the heap once and leaves it at most once, so lines L3 to L7 make $n$ insertions and at most $n$ extractions, $O(n \log n)$ in all. Line L8 is a filter of the sorted order, $O(n)$.
- **Space.** $\Theta(n)$ for the heap and the output.
- **Without a heap.** Moore's form, which rescans for the first late job and removes the longest job before it, takes $O(n^2)$ time.

## Properties

- **Exact.** The number of late jobs is the minimum.
- **Least total time.** Among all largest on-time sets, the output has the least total processing time. In a server this means the accepted work frees the machine as early as possible.
- **One pass.** After the sort, each job is looked at once, in due date order. A new job with a due date later than all seen so far can be added with one more step. A job with an earlier due date cannot; the algorithm is not online in general.
- **Ties do not matter.** Any tie-break in the sort or in line L6 gives an optimal set.

## Variants and improvements

- **Weights.** $1 \| \sum w_j U_j$ is NP-hard: its decision form, sequencing with deadlines and penalties, is one of Karp's 21 problems (Karp 1972). The dynamic program of Lawler and Moore 1969 solves it in $O(n \sum_j p_j)$ time, so it is only weakly NP-hard; see [weighted tardy jobs](/weighted-tardy-jobs/). A heap rule that removes the job of least weight is only a heuristic there.
- **Unit times.** With $p_j = 1$ the weighted problem is [job sequencing with deadlines](/job-sequencing-with-deadlines/), solved greedily by weight.
- **Release dates.** With release dates, $1 \mid r_j \mid \sum U_j$ is strongly NP-hard, and the scan is no longer exact; the [approximation-area page](/minimizing-tardy-jobs/) lists the special cases that stay polynomial.

## When to use it

Use it when a single server must decide which jobs to promise, each job has a hard due date, all jobs are known at the start, and every job is worth the same. Typical cases are a batch window with deadlines, order acceptance in a workshop, and a controller that must refuse the fewest tasks. If jobs have different values, use the Lawler-Moore dynamic program for small integer times. If jobs arrive over time, this algorithm is not optimal.

## Pitfalls

- **Dropping the new job.** Rejecting the job that would be late, rather than the longest job kept, is wrong; the example loses one job this way.
- **Not sorting by due date.** The single test in line L5 is valid only because the kept jobs are in due date order. In any other order a kept job can become late without a test seeing it.
- **Forgetting to subtract.** Line L7 must lower $t$ by the time of the removed job, not of the new job.
- **Min-heap by default.** Many libraries give a min-heap. Push $-p_j$, as the implementation does, or the algorithm removes the shortest job.
- **Reporting the order.** The kept jobs must run in due date order, first. Any order of the late jobs after them is fine.

## Implementations

## History

J. Michael Moore published the algorithm in Management Science in 1968. His form scans the due date order for the first late job, removes the longest job up to it, and repeats. The same paper gives a simpler form that it credits to Thom J. Hodgson, the one-pass scan of this page, which is why both names are attached to it. Lawler and Moore extended the problem to weights in 1969 with a dynamic program, and Karp's 1972 list of NP-complete problems showed that the weighted problem is hard.

## References

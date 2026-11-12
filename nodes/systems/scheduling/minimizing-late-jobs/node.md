---
tag: XREAH5
kind: problem
slug: minimizing-late-jobs
name: "Minimizing late jobs on one machine"
aliases:
- largest on-time set on one machine
- admission of jobs with due dates on one server
area: systems/scheduling
level: advanced
summary: "Choose which jobs one machine finishes by their due dates so that the fewest are late, 1||ΣUj. The Moore-Hodgson algorithm solves it in O(n log n) time."
prereqs: [single-machine-scheduling, lateness-and-tardiness]
see_also: [moore-hodgson-algorithm, minimizing-tardy-jobs, minimizing-number-of-late-jobs, weighted-tardy-jobs, earliest-due-date-first, job-sequencing-with-deadlines, knapsack-problem, scheduling-with-rejection]
sources:
  - paper: doi:10.1287/mnsc.15.1.102
    title: J. Michael Moore, An n job, one machine sequencing algorithm for minimizing the number of late jobs, Management Science 15(1), 1968
    locator: pages 102 to 109 (the problem, the reduction to choosing a set, and the algorithm)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Section 3.3, The Number of Tardy Jobs
  - paper: "James R. Jackson, Scheduling a production line to minimize maximum tardiness, Research Report 43, Management Science Research Project, University of California, Los Angeles, 1955"
    locator: the whole report (the due date order, which decides whether a set of jobs can all be on time)
  - paper: doi:10.1287/mnsc.16.1.77
    title: Eugene L. Lawler and J. Michael Moore, A functional equation and its application to resource allocation and sequencing problems, Management Science 16(1), 1969
    locator: pages 77 to 84 (the dynamic program for the weighted number of late jobs)
  - paper: doi:10.1007/978-1-4684-2001-2_9
    title: Richard M. Karp, Reducibility among combinatorial problems, in Complexity of Computer Computations, 1972
    locator: pages 85 to 103 (sequencing with deadlines and penalties, NP-complete)
---

Minimizing the number of late jobs asks for a schedule of $n$ jobs on one machine, each with a processing time $p_j$ and a due date $d_j$, in which as few jobs as possible complete after their due dates. In [Graham's notation](/scheduling-notation/) it is $1 \| \sum U_j$. Since late jobs can all go at the end, the real decision is which set of jobs to finish on time, so a systems reader can see it as admission control: which requests does a server accept so that each accepted one meets its deadline. The [Moore-Hodgson algorithm](/moore-hodgson-algorithm/) solves it exactly in $O(n \log n)$ time. The approximation-area page [minimizing the number of tardy jobs](/minimizing-tardy-jobs/) has the long table of variants and the proof by deleting one job; the greedy-technique page [minimizing the number of late jobs](/minimizing-number-of-late-jobs/) treats the same problem as a greedy exercise.

## In plain words

A server gets a set of requests. Each request needs some time and has a time by which it must be done. If the server tries to do all of them, some will miss their times. So it decides which requests to accept. All accepted requests must be done in time. The rest are refused, or done later without a promise. The goal is to accept as many requests as possible. Usually a long request blocks several short ones, so the best choice often refuses the long requests.

## Definition

**Input.** $n$ jobs, all present at time $0$. Job $j$ has a processing time $p_j \ge 0$ and a due date $d_j$.

**Schedule.** An order of the jobs, run back to back from time $0$. Job $j$ is late if $C_j > d_j$, and $U_j = 1$ if it is late and $0$ otherwise.

**Goal.** Minimize $\sum_j U_j$.

**The set form.** Call a set $S$ of jobs *feasible* if the jobs of $S$ can all be on time. Jackson's due date order decides this: $S$ is feasible if and only if, with the jobs of $S$ sorted by due date, each prefix has total time at most the due date of its last job. Given a feasible $S$, the schedule "jobs of $S$ in due date order, then the other jobs in any order" has exactly $n - |S|$ late jobs. So the problem is the same as: find a feasible set of largest size.

## Variants

- **Weights.** $1 \| \sum w_j U_j$ asks for a feasible set of largest total weight. It is NP-hard, because the decision form "sequencing with deadlines and penalties" is one of [Karp's 21 problems](/karps-21-np-complete-problems/) (Karp 1972). It is solved in pseudo-polynomial time $O(n \sum p_j)$ by the dynamic program of Lawler and Moore 1969; see [weighted tardy jobs](/weighted-tardy-jobs/).
- **Unit times with weights.** With $p_j = 1$ the weighted problem is [job sequencing with deadlines](/job-sequencing-with-deadlines/), which a greedy algorithm by weight solves.
- **Rejection with a cost.** If each refused job costs a penalty and the accepted ones are scheduled for some other objective, the problem is [scheduling with rejection](/scheduling-with-rejection/).
- **Release dates, precedence, several machines.** These make the problem NP-hard; the [approximation-area page](/minimizing-tardy-jobs/) lists each case with its source.

## Examples

**A server with five requests.** All arrive at time $0$.

| request | $p_j$ | $d_j$ |
|---|---|---|
| $a$ | 3 | 4 |
| $b$ | 4 | 6 |
| $c$ | 2 | 7 |
| $d$ | 5 | 9 |
| $e$ | 1 | 10 |

- **All requests in due date order** ($a, b, c, d, e$) complete at $3, 7, 9, 14, 15$. Only $a$ is on time, so $4$ are late. The due date order is best for the worst lateness, not for the count.
- **Shortest first** ($e, c, a, b, d$) completes at $1, 3, 6, 10, 15$. Requests $e$ and $c$ are on time, $3$ are late.
- **The optimum** has $2$ late requests. Five sets of $3$ requests are feasible: $\{a, c, e\}$, $\{a, d, e\}$, $\{b, c, e\}$, $\{b, d, e\}$ and $\{c, d, e\}$. No set of $4$ is feasible. For example $\{a, c, d, e\}$ in due date order completes at $3, 5, 10, 11$, and $d$ is late.
- **Which optimum to pick.** The five optimal sets have total times $6$, $9$, $7$, $10$ and $8$. The Moore-Hodgson algorithm returns $\{a, c, e\}$, the one with the least total time, so the server is free again from time $6$. Its run on this input drops $b$ at the step of $b$ and $d$ at the step of $d$.

## Known algorithms

- **[Moore-Hodgson algorithm](/moore-hodgson-algorithm/).** Scan the jobs in due date order, keep the accepted jobs in a max-heap by processing time, and when the newest job would be late, drop the longest accepted job. $O(n \log n)$ time, $O(n)$ space. It returns a largest feasible set and, among those, one of least total time.
- **Moore's original form.** The same idea without a heap: find the first late job in the current sequence and remove the longest job up to it. $O(n^2)$ time.
- **Brute force.** Test all $2^n$ subsets with the due date check, in $O(2^n n)$ time. A test oracle for $n \le 15$ or so.
- **Lawler-Moore dynamic program.** For the weighted case, $O(n \sum p_j)$ time over due date prefixes and the total on-time length.

## Bounds

- **Upper bound.** $O(n \log n)$ time by Moore-Hodgson, with a sort and $O(n)$ heap operations.
- **A quick upper bound on the answer.** If the $k$ shortest jobs have total time more than $\max_j d_j$, then no $k$ jobs can all be on time.
- **The feasibility test.** Checking a given set takes one sort and one scan, $O(n \log n)$ time, or $O(n)$ if the jobs are already in due date order.

## Reductions

- **To a set problem.** As in the definition, $1 \| \sum U_j$ is the problem of a largest feasible set, where feasibility is a prefix test in due date order. The feasible sets do not form a matroid in general: with $p = (2, 1, 1)$ and all due dates $2$, the feasible set $\{1\}$ cannot be extended by any job of the larger feasible set $\{2, 3\}$. So a plain greedy by one key can fail, as the example shows for both due date order and shortest first.
- **From knapsack, for the weighted case.** With one common due date $d$, a set is feasible if and only if its total time is at most $d$, so $1 \mid d_j = d \mid \sum w_j U_j$ is the [knapsack problem](/knapsack-problem/) with sizes $p_j$, values $w_j$ and capacity $d$.
- **To maximum lateness.** All jobs can be on time if and only if the optimum of $1 \| L_{\max}$ is at most $0$, which [EDD](/earliest-due-date-first/) decides.

## Applications

- **Admission control.** A server or a real-time controller that may refuse tasks accepts the set that Moore-Hodgson returns. It meets every promise it makes and refuses the fewest tasks, and the accepted work is as short as possible, which leaves the most room for new tasks.
- **Order acceptance.** A workshop that is paid a fixed amount per order shipped on time uses the same rule to decide which orders to accept.
- **A lower bound for other objectives.** The least number of late jobs is a bound that branch-and-bound methods for tardiness problems use.

## References

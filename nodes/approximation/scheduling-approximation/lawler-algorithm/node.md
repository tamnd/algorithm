---
tag: TBK2E7
kind: algorithm
slug: lawler-algorithm
name: Lawler's algorithm for precedence-constrained lateness
aliases:
- Lawler's algorithm for 1|prec|Lmax
- Lawler's algorithm for 1|prec|fmax
- least cost last rule
area: approximation/scheduling-approximation
level: advanced
summary: Exact backward rule for 1|prec|fmax; among the jobs with no unplaced successor, put last the one that is cheapest at the current end time. O(n^2) time.
solves: [maximum-lateness-minimization]
model: word-ram
complexity:
  vars: {n: the number of jobs, e: the number of precedence pairs}
  time: {worst: O(n^2 + e)}
  space: {extra: Θ(n + e)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1973
  people: [Eugene L. Lawler]
  note: Lawler published the backward rule for one machine with precedence constraints and any nondecreasing costs in Management Science in 1973.
prereqs: [earliest-due-date-first, lateness-and-tardiness, precedence-constrained-scheduling, topological-sort]
see_also: [maximum-lateness-minimization, earliest-due-date-first, minimizing-maximum-lateness, sidney-decomposition, scheduling-with-release-dates, exchange-argument, directed-acyclic-graph]
sources:
  - paper: doi:10.1287/mnsc.19.5.544
    title: Eugene L. Lawler, Optimal sequencing of a single machine subject to precedence constraints, Management Science 19(5), 1973
    locator: pages 544 to 546
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 3, Single Machine Models (Deterministic), the maximum lateness and the algorithm for 1|prec|hmax
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 4, Single Machine Scheduling Problems (minimax criteria, Lawler's algorithm for 1|prec|fmax)
  - paper: "Kenneth R. Baker, Eugene L. Lawler, Jan Karel Lenstra and Alexander H. G. Rinnooy Kan, Preemptive scheduling of a single machine to minimize maximum cost subject to release dates and precedence constraints, Operations Research 31(2), 1983"
    locator: pages 381 to 386
---

Lawler's algorithm solves $1 \mid prec \mid f_{\max}$ in the [three-field notation](/scheduling-notation/): one machine, jobs with [precedence constraints](/precedence-constrained-scheduling/), and a nondecreasing cost function $f_j$ for each job, where the goal is to minimize $\max_j f_j(C_j)$. It builds the schedule from the end. The last job must have no successor, and the end time of the last job is the total processing time, whatever the order. So the algorithm puts last the job that is cheapest at that time, and repeats on the rest. This gives an optimal schedule in $O(n^2)$ time. The [maximum lateness](/maximum-lateness-minimization/) $L_{\max}$, the maximum tardiness and the maximum weighted tardiness are all special cases.

## In plain words

You must do a set of tasks one after another. Some tasks must come before others. Each task has a penalty that grows the later it ends, and you want the largest penalty to be as small as possible.

Think about the last task first. It must be a task that no other task waits for. It always ends at the same moment: when all the work is done. So pick, among the tasks that may go last, the one whose penalty at that moment is smallest, and put it last. Then forget it and do the same with the tasks that are left, which now end a little earlier.

Building the plan from the front does not work, because at the front you do not know which task will suffer at the end.

## The problem

There are $n$ jobs and one machine. Job $j$ has a processing time $p_j \ge 0$ and a cost function $f_j$ that is nondecreasing in the completion time. A [directed acyclic graph](/directed-acyclic-graph/) on the jobs gives the precedence constraints: an arc $(a, b)$ means that $a$ completes before $b$ starts. All jobs are available at time 0 and preemption is not allowed. The goal is

$$\min_{\sigma} f_{\max}(\sigma), \qquad f_{\max}(\sigma) = \max_j f_j(C_j(\sigma)),$$

over the orders $\sigma$ that respect the graph, run back to back from time 0. Idle time only delays jobs, and the costs are nondecreasing, so this is no loss. Examples of $f_j$ are $C_j - d_j$ (giving $L_{\max}$), $\max(0, C_j - d_j)$, $w_j \max(0, C_j - d_j)$, and step functions. This page uses $n$ for the number of jobs and $e$ for the number of arcs. The algorithm is exact.

## The algorithm

```pseudo id=main
LAWLER(p[1 .. n], f[1 .. n], G)
L1  J ← all jobs, P ← p[1] + ... + p[n]
L2  out[j] ← number of successors of j in G, for each j
L3  for k ← n downto 1 do
L4      j* ← a job j ∈ J with out[j] = 0 that minimizes f[j](P)
L5      σ[k] ← j*, J ← J − {j*}, P ← P − p[j*]
L6      for each predecessor i of j* in G do out[i] ← out[i] − 1
L7  return σ and max over j of f[j](C[j])
```

Here "successor" and "predecessor" mean an arc of $G$, and $out[j]$ counts the successors of $j$ that are still in $J$. If no job of $J$ has $out[j] = 0$ in line L4, the graph has a cycle. The implementation then raises an error.

## Example

Take five jobs with $p = (2, 3, 1, 4, 2)$, the arcs $0 \to 1$, $2 \to 1$ and $1 \to 3$, and the weighted tardiness costs $f_j(t) = w_j \max(0, t - d_j)$ with $d = (2, 5, 3, 9, 4)$ and $w = (3, 1, 2, 1, 2)$. The total time is $P = 12$.

| step | $P$ | jobs that may go last, with $f_j(P)$ | placed last |
|---|---|---|---|
| 1 | 12 | job 3: 3, job 4: 16 | 3 |
| 2 | 8 | job 1: 3, job 4: 8 | 1 |
| 3 | 5 | job 0: 9, job 2: 4, job 4: 2 | 4 |
| 4 | 3 | job 0: 3, job 2: 0 | 2 |
| 5 | 2 | job 0: 0 | 0 |

The order is $0, 2, 4, 1, 3$ with completion times $2, 3, 5, 8, 12$ and costs $0, 0, 2, 3, 3$, so $f_{\max} = 3$. The graph allows $10$ orders. The best of them has value $3$ and the worst has value $16$.

## Correctness

The proof in `proofs/correctness.md` is an [exchange argument](/exchange-argument/) on the last position. Take an optimal order and move the job $j^*$ of line L4 to the end. This keeps the precedence constraints, because $j^*$ has no successor. The jobs that were after $j^*$ now end $p_{j^*}$ earlier, so their costs do not grow. The job $j^*$ now ends at $P$, and its cost $f_{j^*}(P)$ is at most the cost of the job that was last before, since that job was also allowed to go last. So there is an optimal order that ends with $j^*$. Its value is the maximum of $f_{j^*}(P)$ and the value of its first $n - 1$ jobs, which is an instance of the same problem on $J - \{j^*\}$. Induction on $n$ finishes the proof.

## Complexity

- **Time.** Line L4 scans at most $n$ jobs and evaluates their costs, so the $n$ rounds take $O(n^2)$ evaluations. Line L6 handles each arc once in total, $O(e)$. With $O(1)$ time for each evaluation of an $f_j$, the time is $O(n^2 + e)$, which is $O(n^2)$ since $e \le n(n-1)/2$ in a DAG without parallel arcs.
- **Space.** $\Theta(n + e)$ for the lists of predecessors and the counters.
- **Faster special cases.** For $L_{\max}$ with no precedence constraints, all $f_j(P) = P - d_j$ in line L4, so the rule puts the largest due date last, and the result is the [EDD](/earliest-due-date-first/) order in $O(n \log n)$ time. In general, a heap keyed by $f_j(P)$ does not help, because the key of every job changes when $P$ changes.

## Properties

- **Exact for any nondecreasing costs.** The functions need not be linear, continuous or of one type. Different jobs may have different kinds of cost.
- **Minimax only.** The argument uses that the value is a maximum. For a sum of costs, such as the [total tardiness](/total-tardiness-minimization/) $\sum_j T_j$, the problem is NP-hard even without precedence constraints.
- **Optimal among preemptive schedules too.** With all jobs available at time 0, preemption cannot help on one machine. Order the jobs of a preemptive schedule by their completion times and run them back to back. Each job then ends no later than before, because all jobs that end before it were fully processed by its old completion time, and the order of completion respects the precedence constraints.
- **Deterministic.** Ties in line L4 can be broken in any way; each choice gives an optimal order.

## Variants and improvements

- **Release dates with preemption.** Baker, Lawler, Lenstra and Rinnooy Kan (1983) solve $1 \mid prec, r_j, pmtn \mid f_{\max}$ in $O(n^2)$ time by splitting the time line into blocks and applying the backward rule inside each block.
- **Release dates without preemption.** $1 \mid r_j \mid L_{\max}$ is strongly NP-hard, so no such rule exists unless P = NP. See [scheduling with release dates](/scheduling-with-release-dates/) and the delivery time form on the page about [maximum lateness](/maximum-lateness-minimization/).
- **Modified due dates.** For $L_{\max}$ with precedence, an equivalent method changes each due date to $d'_j = \min(d_j, \min_{(j,k) \in G} (d'_k - p_k))$ and runs EDD. Lawler's rule needs no such step and works for all nondecreasing costs.
- **Weighted completion time with precedence.** The sum objective $1 \mid prec \mid \sum w_j C_j$ is NP-hard. Its 2-approximations use the [Sidney decomposition](/sidney-decomposition/), not a backward rule.

## When to use it

Use Lawler's algorithm when one machine must respect precedence constraints and the cost of a schedule is its worst job cost, for example the worst delay with job-specific penalty rates. When all costs are lateness costs and there are no precedence constraints, sort by due date instead.

## Pitfalls

- **Building from the front fails.** Take $p = (3, 4, 1)$, $d = (7, 0, 2)$ and the arc $0 \to 1$. Running the available job with the earliest due date first gives the order $2, 0, 1$, where job 1 ends at $8$ with lateness $8$. The order $0, 1, 2$ gives $L_{\max} = 7$, which is optimal, and Lawler's rule finds it.
- **Costs must be nondecreasing.** With $p = (2, 1)$, $f_0(t) = 3(5 - t)$, an earliness cost, and $f_1(t) = t - 2$, the rule puts job 1 last because $f_1(3) = 1 < 6 = f_0(3)$. The order $0, 1$ has value $f_0(2) = 9$, but the order $1, 0$ has value $6$. The exchange step fails, because moving job 1 to the end makes job 0 end earlier, which raises its cost.
- **Evaluate at the end time, not at a start time.** The rule compares $f_j(P)$, the cost if $j$ ends at $P$. Using $P - p_j$, the start time, gives wrong choices.
- **Recompute $P$.** Line L5 must subtract $p_{j^*}$. Using the full total at every step puts every job at the same end time.

## Implementations

## History

Lawler (1973) gave the rule and its proof in a short note in Management Science. It generalizes Jackson's EDD rule (1955) to precedence constraints and to arbitrary nondecreasing costs. Baker, Lawler, Lenstra and Rinnooy Kan (1983) extended it to release dates with preemption.

## References

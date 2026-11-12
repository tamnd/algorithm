---
tag: PRJWZC
kind: problem
slug: job-sequencing-with-deadlines
name: Job sequencing with deadlines
aliases:
- unit-time jobs with deadlines and profits
- scheduling unit-time tasks with deadlines and penalties
area: techniques/greedy
level: core
summary: Select and order unit-time jobs with deadlines and profits to maximize total profit.
prereqs: [greedy-algorithm, matroid]
see_also: [matroid-greedy-algorithm, disjoint-set, minimizing-number-of-late-jobs, minimizing-maximum-lateness, maximum-weight-matroid-basis, priority-queue, exchange-argument, earliest-deadline-first]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Section 16.5, A task-scheduling problem as a matroid
  - book: isbn:9780929306414
    title: Ellis Horowitz, Sartaj Sahni and Sanguthevar Rajasekaran, Computer Algorithms, second edition
    locator: Chapter 4, The Greedy Method (job sequencing with deadlines)
  - book: isbn:9780486414539
    title: Eugene L. Lawler, Combinatorial Optimization, Networks and Matroids
    locator: Chapter 7, Matroid Optimization
---

Job sequencing with deadlines is the problem of choosing which of $n$ unit-time jobs to run on one machine, and in which time slots, so that the total profit of the jobs that finish by their deadlines is as large as possible. The feasible sets of jobs form a [matroid](/matroid/), so the [matroid greedy algorithm](/matroid-greedy-algorithm/) is optimal: take the jobs by decreasing profit and keep each one that still fits. Placing each kept job in the latest free slot before its deadline, with a [disjoint-set](/disjoint-set/) structure to find that slot, gives $O(n \log n)$ time, dominated by the sort.

## In plain words

A machine can do one job per hour. Each job takes exactly one hour, has a deadline, and pays a profit if it is done by its deadline. A job that misses its deadline pays nothing, so you may as well skip it. Which jobs should you do?

Take the jobs from the most profitable down. For each job, ask whether it still fits together with the jobs you already took. If it does, take it; if not, skip it. To make room for later jobs, put each taken job in the latest free hour before its deadline, so that the early hours stay free for jobs with early deadlines.

This simple rule is always optimal. The reason is a structure called a matroid, which is exactly the setting where "take the best item that still fits" works.

## Definition

**Input.** A set $J$ of $n$ jobs. Job $j$ has an integer deadline $d_j \ge 1$ and a profit $w_j \ge 0$. Each job takes one unit of time, and the machine runs one job in each slot $[t - 1, t)$ for $t = 1, 2, \ldots$.

**Schedules.** A job is on time if it runs in a slot $t \le d_j$. Jobs that are not on time earn nothing and can be dropped or run at the end. A set $S \subseteq J$ is *independent* (feasible) if its jobs can all be on time.

**Objective.** Find an independent set $S$ that maximizes $w(S) = \sum_{j \in S} w_j$. Equivalently, with $w_j$ read as a penalty for missing the deadline, minimize the total penalty of the late jobs; this is the form in CLRS.

**Feasibility test.** For a set $S$ and $t \ge 0$, let $N_t(S)$ be the number of jobs in $S$ with deadline at most $t$. Then $S$ is independent if and only if $N_t(S) \le t$ for all $t$. The condition is necessary, because the $N_t(S)$ jobs with deadline at most $t$ all need slots among the first $t$. It is sufficient, because running $S$ in order of deadline puts the job with the $i$-th smallest deadline $d$ in slot $i$, and $i \le N_d(S) \le d$.

**Theorem.** The independent sets form a matroid on $J$.

*Proof.* The empty set is independent, and a subset of an independent set is independent, because $N_t$ can only go down. For the exchange property, let $A$ and $B$ be independent with $|B| > |A|$. Deadlines larger than $n$ can be replaced by $n$ without changing independence, so $N_n(A) = |A| < |B| = N_n(B)$. Let $k$ be the largest $t$ with $N_t(B) \le N_t(A)$; then $0 \le k < n$, since $N_0 = 0$ for both. Because $N_{k+1}(B) > N_{k+1}(A)$ and $N_k(B) \le N_k(A)$, the set $B$ has more jobs with deadline exactly $k + 1$ than $A$, so some $x \in B \setminus A$ has $d_x = k + 1$. Adding $x$ to $A$ leaves $N_t$ unchanged for $t \le k$, and for $t \ge k + 1$ gives $N_t(A \cup \{x\}) = N_t(A) + 1 \le N_t(B) \le t$, by the choice of $k$. So $A \cup \{x\}$ is independent. $\square$

By the [matroid greedy theorem](/matroid-greedy-theorem/), the greedy algorithm by decreasing profit returns an independent set of largest profit. In the language of matroids, the problem is a [maximum-weight basis](/maximum-weight-matroid-basis/) problem with nonnegative weights.

## Variants

- **Penalties instead of profits.** Minimize the total penalty of the jobs that miss their deadlines. Since the total penalty of all jobs is fixed, this is the same problem.
- **Arbitrary processing times.** If jobs have lengths $p_j$, the feasible sets no longer form a matroid. The weighted problem $1 \| \sum w_j U_j$ is NP-hard, and with unit weights the [Moore-Hodgson algorithm](/minimizing-number-of-late-jobs/) solves it.
- **Several machines.** With $m$ identical machines, slot $t$ can hold $m$ jobs. A set is feasible if and only if $N_t(S) \le m t$ for all $t$, the sets still form a matroid, and the same greedy algorithm works.
- **Release times.** If job $j$ can only run in slots between a release time and its deadline, the feasible sets are the matchable sets of a bipartite graph between jobs and slots. These still form a matroid (a transversal matroid), so greedy by profit with a matching test remains optimal.

## Examples

**Seven jobs.** Let $(d_j, w_j)$ be $a = (2, 100)$, $b = (1, 19)$, $c = (2, 27)$, $d = (1, 25)$, $e = (3, 15)$, $f = (4, 30)$, $g = (3, 35)$. The greedy algorithm takes them by profit: $a, g, f, c, d, b, e$.

| job | $d_j$ | $w_j$ | latest free slot $\le d_j$ | action | slots 1 to 4 after the step |
| --- | --- | --- | --- | --- | --- |
| $a$ | 2 | 100 | 2 | take | $-, a, -, -$ |
| $g$ | 3 | 35 | 3 | take | $-, a, g, -$ |
| $f$ | 4 | 30 | 4 | take | $-, a, g, f$ |
| $c$ | 2 | 27 | 1 | take | $c, a, g, f$ |
| $d$ | 1 | 25 | none | skip | $c, a, g, f$ |
| $b$ | 1 | 19 | none | skip | $c, a, g, f$ |
| $e$ | 3 | 15 | none | skip | $c, a, g, f$ |

The schedule is $c, a, g, f$ with profit $27 + 100 + 35 + 30 = 192$. Over all subsets, 192 is the largest profit of an independent set, and $\{a, c, f, g\}$ is the only set that reaches it.

**The latest slot matters.** If each taken job goes into the *earliest* free slot instead, $a$ takes slot 1, $g$ slot 2 and $f$ slot 3, and then $c$, with deadline 2, finds no free slot. The profit is 165. The set $\{a, c, f, g\}$ was independent, but the slot choice blocked it. With the feasibility test $N_t(S) \le t$ instead of a fixed slot, the order of placement does not matter.

**Deadline order fails.** Taking the jobs by deadline, with ties going to the larger profit, and keeping each one that fits gives $d, a, g, f$ with profit 190. It keeps $d$ with profit 25 in slot 1, where the optimum puts $c$ with profit 27.

## Known algorithms

- **Greedy with a slot array.** Sort by decreasing profit. For each job, scan down from slot $\min(d_j, n)$ to the first free slot. $O(n^2)$ time in the worst case.
- **Greedy with disjoint sets.** Keep each slot in a [disjoint-set](/disjoint-set/) structure whose root is the latest free slot at or below it, with slot 0 as a sentinel. A find gives the slot for a job, and taking slot $t$ unites it with slot $t - 1$. After the sort, the $n$ operations take $O(n\, \alpha(n))$ time, so the total is $O(n \log n)$.
- **Scan by deadline with a min-heap.** Sort by deadline, and keep the taken jobs in a min-[priority queue](/priority-queue/) keyed by profit. Add each job; if the heap now holds more jobs than the current deadline, remove the job of smallest profit. This also takes $O(n \log n)$ time and gives the same profit.
- **Matroid greedy with an independence test.** The general [matroid greedy algorithm](/matroid-greedy-algorithm/) with the test $N_t(S) \le t$ gives $O(n^2)$ time.

## Bounds

- **Upper bound.** $O(n \log n)$ time in the comparison model, by one sort and near-linear work after it. If the profits are already sorted, $O(n\, \alpha(n))$.
- **Size of the answer.** At most $\min(n, \max_j d_j)$ jobs are on time.

## Reductions

- **To a maximum-weight matroid basis.** The theorem above makes the problem an instance of [maximum-weight matroid basis](/maximum-weight-matroid-basis/), so all results on matroid greedy algorithms apply.
- **To bipartite matching.** Jobs on one side, slots $1, \ldots, n$ on the other, and an edge from job $j$ to each slot $t \le d_j$. An independent set is a set of jobs that can be matched, and the problem is a maximum-weight matching in which the weight sits on the job side.

## Applications

- **Unit tasks with deadlines.** Packets, print jobs or batch tasks of equal length that earn a reward only when done in time.
- **Teaching matroids.** CLRS uses this problem as the example of a matroid that is not a graph, to show the reach of the matroid greedy theorem.

## References

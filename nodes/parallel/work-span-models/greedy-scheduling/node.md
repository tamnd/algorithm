---
tag: 7BR0CN
kind: algorithm
slug: greedy-scheduling
name: Greedy scheduling
aliases:
- greedy scheduler
- list scheduling of DAGs
area: parallel/work-span-models
level: core
summary: Run a computation DAG on p processors by running, at each step, as many ready strands as possible, up to p. Each such schedule takes at most T_1/p + T_infinity steps.
solves: [precedence-constrained-scheduling]
model: word-ram
complexity:
  vars: {n: the number of strands, m: the number of edges, p: the number of processors}
  time: {worst: Θ(n + m), average: Θ(n + m), best: Θ(n + m)}
  space: {extra: Θ(n + m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1966
  people: [Ronald L. Graham, Robert D. Blumofe, Charles E. Leiserson]
  note: Graham analysed list schedules of tasks with precedence constraints in 1966. Blumofe and Leiserson showed that any greedy schedule of a multithreaded computation takes at most T_1/P + T_infinity steps.
prereqs: [computation-dag, work-law, span-law]
see_also: [brent-theorem, list-scheduling, list-scheduling-bound, work-stealing, precedence-constrained-scheduling, coffman-graham-algorithm, hu-algorithm, parallel-slackness]
sources:
  - book: isbn:9780262033848
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, third edition
    locator: Chapter 27, Section 27.1, the part on scheduling (greedy schedulers, complete and incomplete steps, Theorem 27.1, Corollaries 27.2 and 27.3, Exercises 27.1-3 and 27.1-4)
  - paper: doi:10.1002/j.1538-7305.1966.tb01709.x
    title: "R. L. Graham, Bounds for certain multiprocessing anomalies, Bell System Technical Journal 45(9), 1966"
    locator: list schedules of tasks with a precedence order and the bound 2 - 1/m (pp. 1563-1581 for the paper)
  - paper: doi:10.1137/0117039
    title: "R. L. Graham, Bounds on multiprocessing timing anomalies, SIAM Journal on Applied Mathematics 17(2), 1969"
    locator: the restatement of the bound 2 - 1/m for list schedules (pp. 416-429 for the paper)
  - paper: doi:10.1145/324133.324234
    title: "Robert D. Blumofe and Charles E. Leiserson, Scheduling multithreaded computations by work stealing, Journal of the ACM 46(5), 1999"
    locator: the bound T_1/P + T_infinity for any greedy schedule
  - paper: doi:10.1016/S0022-0000(75)80008-0
    title: "J. D. Ullman, NP-complete scheduling problems, Journal of Computer and System Sciences 10(3), 1975"
    locator: the NP-completeness of scheduling unit-time tasks with precedence constraints on a given number of processors
  - paper: doi:10.1109/12.21127
    title: "Derek L. Eager, John Zahorjan and Edward D. Lazowska, Speedup versus efficiency in parallel systems, IEEE Transactions on Computers 38(3), 1989"
    locator: the lower bound on speedup in terms of the average parallelism
---

Greedy scheduling runs a [computation DAG](/computation-dag/) on $p$ processors by never leaving a processor idle while a strand is ready: at each step it runs $\min(p, r)$ of the $r$ ready strands. Every greedy schedule takes $T_p \le T_1/p + T_\infty$ steps, and more precisely $T_p \le (T_1 - T_\infty)/p + T_\infty$. Since every schedule needs $\max(T_1/p, T_\infty)$ steps, any greedy schedule is within a factor $2 - 1/p$ of the best one. Which ready strands run when there are more than $p$ is left to a tie rule, and the bound holds for every tie rule.

## In plain words

A team of workers has a list of tasks, and some tasks must wait until others are done. The greedy rule is: whenever a worker is free and some task is ready, give that worker a ready task. Nobody waits while there is something they could do.

This rule does not think ahead, and it can pick badly when many tasks are ready at once. Even so, it is never far from the best plan. At each moment either every worker is busy, which uses up the total work fast, or every ready task is being done, which shortens the longest chain of waiting tasks. So the time is at most the share of the work for each worker plus the longest chain, and that is never more than twice the best possible time.

## The problem

The input is a DAG $G$ of $n$ unit-time strands with $m$ edges, and a number $p \ge 1$ of identical processors. A *schedule* gives each strand a step $f(v) \ge 1$, with at most $p$ strands in each step and $f(u) < f(v)$ for each edge $u \to v$. Its length is $T_p = \max_v f(v)$. A strand is *ready* at a step if all its predecessors ran in earlier steps. Finding a shortest schedule is the [precedence-constrained scheduling](/precedence-constrained-scheduling/) problem with unit jobs, which is NP-hard when $p$ is part of the input (Ullman 1975). Greedy scheduling does not solve it exactly. It gives a schedule within a factor $2 - 1/p$ of the optimum.

The cost model for the schedule length is the [work-span model](/work-span-model/). The running time of the scheduler itself is in the [word RAM](/word-ram/).

| Symbol | Meaning |
|---|---|
| $n$ | the number of strands (on this page, not the input size of the program) |
| $m$ | the number of edges |
| $p$ | the number of processors |
| $W$, $T_1$ | the work, equal to $n$ |
| $S$, $D$, $T_\infty$ | the span, the number of strands on a longest path |
| $T_p$ | the length of the schedule on $p$ processors |
| $W/S$ | the parallelism |

## The algorithm

```pseudo id=main
GREEDY-SCHEDULE(G, p)                     ▷ G is a DAG of unit strands, p ≥ 1
L1  for each edge u → v do append v to succ[u], indeg[v] ← indeg[v] + 1
L2  R ← the strands v with indeg[v] = 0  ▷ the ready strands
L3  steps ← an empty list
L4  while R is not empty do
L5      k ← min(p, |R|)
L6      X ← any k strands of R           ▷ the tie rule chooses which
L7      R ← R − X, N ← ∅
L8      for each u ∈ X and each edge u → v do
L9          indeg[v] ← indeg[v] − 1
L10         if indeg[v] = 0 then N ← N ∪ {v}
L11     R ← R ∪ N
L12     append X to steps                ▷ X runs in step |steps|
L13 return steps
```

Line L5 is the greedy rule. Line L6 is where tie rules differ: first ready first run (a queue), a fixed priority, or a random choice. A step is *complete* if $k = p$ and *incomplete* if $k < p$, in which case $X = R$ and every ready strand runs. The strands that become ready during a step are kept apart in $N$ and join $R$ only after the step (line L11), so a strand never runs in the same step as its predecessor.

## Example

Take the DAG of a parallel sum of four numbers, with 10 strands: strand 0 splits the input, strands 1 and 5 split the halves, strands 2, 3, 6 and 7 are the leaves, strands 4 and 8 add the halves, and strand 9 adds the two half sums. So $W = 10$ and $S = 5$. Run GREEDY-SCHEDULE with $p = 2$ and first ready first run.

| step | $R$ at line L4 | $X$ | $N$ | kind |
|---|---|---|---|---|
| 1 | 0 | 0 | 1, 5 | incomplete |
| 2 | 1, 5 | 1, 5 | 2, 3, 6, 7 | complete |
| 3 | 2, 3, 6, 7 | 2, 3 | 4 | complete |
| 4 | 6, 7, 4 | 6, 7 | 8 | complete |
| 5 | 4, 8 | 4, 8 | 9 | complete |
| 6 | 9 | 9 | none | incomplete |

The schedule has $T_2 = 6$ steps: 4 complete and 2 incomplete. The bound gives $T_2 \le (10 - 5)/2 + 5 = 7.5$, and the lower bound is $\max(10/2, 5) = 5$. No schedule takes 5 steps, because step 1 can run only strand 0 and the last step only strand 9, and the other 8 strands need 4 more steps. So this schedule is optimal. With $p = 3$ the steps are $\{0\}, \{1, 5\}, \{2, 3, 6\}, \{7, 4\}, \{8\}, \{9\}$, again 6 steps.

For a larger case, the DAG of a parallel Fibonacci of 5 (split, the two calls in parallel, join, with leaves for 0 and 1) has $W = 22$ and $S = 9$. First ready first run gives:

| $p$ | $T_p$ | $\max(W/p, S)$ | $(W - S)/p + S$ |
|---|---|---|---|
| 1 | 22 | 22 | 22 |
| 2 | 13 | 11 | 15.5 |
| 3 | 10 | 9 | 13.3 |
| 4 | 9 | 9 | 12.25 |
| 8 | 9 | 9 | 10.6 |

## Correctness

Two things are claimed: the output is a valid greedy schedule, and its length is at most $(W - S)/p + S$. The first is proved in [proofs/correctness.md](proofs/correctness.md). In short, $indeg[v]$ counts the predecessors of $v$ that have not run, so a strand enters $R$ exactly when all its predecessors have run in earlier steps, and line L5 runs $\min(p, |R|)$ of the ready strands at each step. Each strand runs once, and on a DAG every strand runs.

**Theorem (greedy bound).** Each greedy schedule has $T_p \le (T_1 - T_\infty)/p + T_\infty \le T_1/p + T_\infty$.

*Proof.* Let $C$ and $I$ be the numbers of complete and incomplete steps. Let $G_t$ be the DAG of the strands that have not run before step $t$, whose sources are the ready strands. At an incomplete step, $X = R$, so all sources of $G_t$ run. Then the first strand of each path of $G_{t+1}$ has a predecessor in $G_t$, so each path of $G_{t+1}$ is shorter by at least one than some path of $G_t$, and $S(G_{t+1}) \le S(G_t) - 1$. The span starts at $T_\infty$, never grows, and stays at least 1 while strands are left, so $I \le T_\infty$. Each complete step runs $p$ strands and each incomplete step at least one, so $pC + I \le T_1$. So

$$T_p = C + I \le \frac{T_1 - I}{p} + I = \frac{T_1}{p} + \Big(1 - \frac 1p\Big) I \le \frac{T_1 - T_\infty}{p} + T_\infty. \qquad \blacksquare$$

The same count, with the history of the bound and Brent's original level-by-level form, is on [Brent's theorem](/brent-theorem/).

**Corollary (within a factor $2 - 1/p$ of optimal).** Let $T^*$ be the length of a shortest schedule on $p$ processors. Then each greedy schedule has $T_p \le (2 - 1/p)\,T^*$.

*Proof.* By the [work law](/work-law/), $T_1/p \le T^*$, and by the [span law](/span-law/), $T_\infty \le T^*$. So $T_p \le T_1/p + (1 - 1/p) T_\infty \le T^* + (1 - 1/p) T^* = (2 - 1/p) T^*$. $\blacksquare$

## Complexity

**The scheduler.** With first ready first run, $R$ is a queue. Line L1 takes $\Theta(n + m)$ time. Each strand enters $R$ once and leaves it once, and each edge is looked at once in line L8, so the whole loop takes $\Theta(n + m)$ time, and the space is $\Theta(n + m)$ for the lists, the counts and the output. A priority rule keeps $R$ in a binary heap and takes $O(n \log n + m)$ time.

**The schedule.** For unit strands, $\max(\lceil T_1/p \rceil, T_\infty) \le T_p \le (T_1 - T_\infty)/p + T_\infty$, proved above. In terms of the [parallelism](/parallelism/) $A = T_1/T_\infty$, the [speedup](/speedup/) is

$$\frac{T_1}{T_p} \ge \frac{T_1}{T_1/p + (1 - 1/p) T_\infty} = \frac{pA}{A + p - 1},$$

which is close to $p$ when $p \ll A$ and close to $A$ when $p \gg A$. Eager, Zahorjan and Lazowska (1989) gave the same lower bound on speedup in terms of the average parallelism.

## Properties

- **Online.** The rule needs only the set of ready strands, not the rest of the DAG. A runtime system can follow it while the program unfolds.
- **Deterministic** with a fixed tie rule. Different tie rules give different schedules of one DAG, and their lengths can differ by a factor close to 2 (see below).
- **Some greedy schedule is optimal for unit strands.** Take a shortest schedule. If at some step $t$ a processor is idle and a strand $v$ is ready but runs later, move $v$ to step $t$. The schedule stays valid, since the predecessors of $v$ ran before $t$ and its successors run after its old step, and it does not get longer. Each move lowers the sum of the steps of all strands, so the moves stop, and the result is a greedy schedule of length at most the optimum. So the hard part of the problem is the choice in line L6, not the decision to keep processors busy.
- **Greedy schedules are list schedules.** For unit strands, a greedy schedule is the list schedule whose list orders the strands by their step. So Graham's bound for list scheduling with precedence constraints applies to it directly (see [Graham's bound](/list-scheduling-bound/)).

**Bad tie breaking.** Take a chain of $k$ strands and $pk$ strands with no edges, so $W = k + pk$ and $S = k$. A tie rule that prefers the independent strands fills the first $k$ steps with them, and then the chain runs alone, for $T_p = 2k = (W - S)/p + S$. A rule that always runs the next chain strand takes $k + \lceil k/p \rceil$ steps, which is optimal. For $p = 4$ and $k = 8$, $W = 40$ and $S = 8$: the bad rule takes 16 steps, the good one 10, and $W/p + S = 18$. The ratio of the two greedy schedules tends to $2p/(p + 1)$ as $k$ grows, which is close to 2 for large $p$ (compare CLRS, third edition, Exercise 27.1-4).

## Variants and improvements

- **Critical path first.** Give priority in line L6 to the strand with the longest path below it. For in-trees this is [Hu's algorithm](/hu-algorithm/), which is optimal on any number of processors. For $p = 2$ the [Coffman-Graham algorithm](/coffman-graham-algorithm/) is optimal for any DAG of unit tasks.
- **Strands of any length.** Run a ready strand whenever a processor becomes free. This is [list scheduling](/list-scheduling/) with precedence constraints, and Graham's proof gives the bound $(2 - 1/p)$ times the optimum.
- **Work stealing.** A central ready set is a bottleneck on a real machine. [Work stealing](/work-stealing/) keeps a deque on each processor and steals from a random processor when idle. It is not greedy at each step, but it reaches $\mathbb{E}[T_p] \le T_1/p + O(T_\infty)$ in expectation (Blumofe and Leiserson 1999, cited, not proved here).
- **Level-by-level schedules.** Running the strands level by level, with a barrier between levels, is not greedy, but it meets the same bound by Brent's original lemma (see [Brent's theorem](/brent-theorem/)).

## When to use it

Use greedy scheduling as the model of a good runtime scheduler when you analyse a fork-join algorithm: once the work and the span are known, $T_p \le T_1/p + T_\infty$ follows for free. Use the simulation to see how a given DAG behaves on $p$ processors, or to test span bounds. On a real machine, a central greedy scheduler costs too much synchronization when strands are short, and work stealing is the usual choice. When the exact optimum matters for small DAGs, use a priority rule such as critical path first, or an exact method.

## Pitfalls

- **Running a strand in the same step as its predecessor.** If line L10 adds $v$ straight to $R$, and the strands of a step are chosen one at a time from $R$, then $v$ can be chosen in the same step as the strand that made it ready. The right form keeps new strands in $N$ (line L10) and adds them after the step (line L11).
- **Waiting to fill the processors.** A rule such as "if $|R| < p$ then wait for more ready strands" in place of line L5 is not greedy. On a chain with $p \ge 2$ it never runs anything. Line L5 must run $\min(p, |R|)$ strands, even when that is fewer than $p$.
- **Expecting one exact $T_p$.** The bound holds for every tie rule, but the exact length depends on the rule in line L6. A test that checks an exact $T_p$ must fix the rule.
- **Span in edges.** The bound uses $T_\infty$ as the number of strands on a longest path. With the span counted in edges, the bound is $T_1/p + T_\infty + 1$ in that count, not $T_1/p + T_\infty$.

## Implementations

The Python function takes the strands as $0, \ldots, n - 1$ and the edges as pairs, and returns the list of steps. The tie rule is first ready first run by default, or a priority key, or a seeded random choice. The tests build DAGs from fork-join programs and from seeded random series-parallel and random DAGs, check on every run that the schedule is valid and greedy and that $\max(W/p, S) \le T_p \le (W - S)/p + S$, and compare with a brute-force optimum on small DAGs.

## History

Graham (1966) studied list schedules of tasks with a precedence order on identical processors and proved that each has length at most $2 - 1/m$ times the optimum on $m$ processors, and in 1969 he restated the bound and studied its anomalies. Brent (1974) proved the level-by-level form of the bound for the evaluation of arithmetic expressions. Ullman (1975) proved that finding a shortest schedule of unit tasks with precedence constraints is NP-complete. Blumofe and Leiserson (1994, journal version 1999) stated the bound $T_1/P + T_\infty$ for any greedy schedule of a multithreaded computation, and CLRS (third edition, 2009, Theorem 27.1) gives the proof by complete and incomplete steps.

## References

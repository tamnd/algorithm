---
tag: 7X27J2
kind: algorithm
slug: coffman-graham-algorithm
name: Coffman-Graham algorithm
aliases:
- Coffman-Graham scheduling
- Coffman-Graham labeling
- lexicographic labeling for two-processor scheduling
area: approximation/scheduling-approximation
level: advanced
summary: Labels jobs lexicographically, then list-schedules; a (2-2/m)-approximation for unit jobs.
solves: [precedence-constrained-scheduling]
model: word-ram
complexity:
  vars: {n: the number of jobs, e: the number of precedence arcs, m: the number of machines}
  time: {worst: O(n (n + e))}
  space: {extra: O(n^2)}
properties: {deterministic: true, recursive: false, online: false}
history:
  year: 1972
  people: [Edward G. Coffman Jr., Ronald L. Graham]
  note: Coffman and Graham gave the labeling and proved it optimal for two processors in 1972; Lam and Sethi proved the ratio 2 - 2/m for m processors in 1977.
prereqs: [precedence-constrained-scheduling, list-scheduling, transitive-reduction, topological-sort]
see_also: [hu-algorithm, critical-path-lower-bound, list-scheduling-bound, graham-anomalies, transitive-reduction]
sources:
  - paper: doi:10.1007/BF00288685
    title: "E. G. Coffman Jr. and R. L. Graham, Optimal scheduling for two-processor systems, Acta Informatica 1(3), 1972"
    locator: the labeling rule and the proof that the list schedule by decreasing label is optimal on two processors
  - paper: doi:10.1137/0206037
    title: "S. Lam and R. Sethi, Worst case analysis of two scheduling algorithms, SIAM Journal on Computing 6(3), 1977"
    locator: the bound 2 - 2/m for the Coffman-Graham schedule on m processors
  - paper: "R. Sethi, Scheduling graphs on two processors, SIAM Journal on Computing 5(1), 1976, pages 73 to 82"
    locator: a fast implementation of the lexicographic labeling
  - paper: "H. N. Gabow, An almost-linear algorithm for two-processor scheduling, Journal of the ACM 29(3), 1982, pages 766 to 780"
    locator: an optimal two-processor schedule without the transitive reduction
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 5 (parallel machines), the section on unit jobs and two machines with general precedence
---

The Coffman-Graham algorithm schedules unit-time jobs with arbitrary precedence constraints on $m$ identical machines. It first gives each job a label by a lexicographic rule, and then runs [list scheduling](/list-scheduling/) with the jobs in order of decreasing label. For $m = 2$ the schedule is optimal, so $P2 \mid \text{prec}, p_j = 1 \mid C_{\max}$ is solvable in polynomial time (Coffman and Graham 1972). For general $m$ the [makespan](/makespan/) is at most $(2 - 2/m)\,\mathrm{OPT}$ (Lam and Sethi 1977), a little better than Graham's $2 - 1/m$ for any list schedule.

## In plain words

Some tasks of one hour each must be done by two workers, and some tasks must wait for others. A good plan keeps both workers busy and starts early the tasks that hold up a lot of later work.

The algorithm first ranks the tasks, from the last ones back to the first ones. A task gets a high rank if the tasks that wait for it have high ranks. When two tasks look equal, the one whose waiting tasks rank higher wins. Then, each hour, the two free workers take the ready tasks of highest rank. For two workers this simple plan always finishes as early as possible. For more workers it can be late, but never by much more than a factor of two.

## The problem

There are $n$ jobs, each of length 1, and $m \ge 2$ identical machines. A directed acyclic graph $G$ on the jobs gives the precedence: an arc $u \to w$ means that $w$ starts only after $u$ ends. A schedule gives each job a slot $\sigma(j) \in \{1, 2, \ldots\}$ (the job runs in $[\sigma(j) - 1, \sigma(j))$), with at most $m$ jobs in each slot and $\sigma(u) < \sigma(w)$ for each arc. The goal is to minimize $C_{\max} = \max_j \sigma(j)$. $\mathrm{OPT}$ is the least makespan, and $\mathrm{ALG}$ is the makespan of the Coffman-Graham schedule. For $m$ in the input the problem is NP-hard (Ullman 1975), see [precedence-constrained scheduling](/precedence-constrained-scheduling/).

For a job $u$, let $N(u)$ be the sequence of labels of its immediate successors, sorted in decreasing order. Sequences are compared in lexicographic order, and a proper prefix is smaller than the longer sequence: $(3) < (3, 2, 1)$ and $(2, 1) < (3)$.

## The algorithm

```pseudo id=main
COFFMAN-GRAHAM(G, m)
L1  G ← the transitive reduction of G
L2  for k ← 1 to n do
L3      R ← the unlabeled jobs whose immediate successors all have labels
L4      N(j) ← the labels of the immediate successors of j, in decreasing order, for each j in R
L5      j* ← the job of R with the lexicographically smallest N(j)
L6      α(j*) ← k
L7  t ← 0
L8  while some job has no slot do
L9      t ← t + 1
L10     σ(j) ← t for the min(m, |A|) jobs j of A with the largest labels, where A is the set of jobs without a slot whose predecessors all have slots below t
L11 return σ
```

Line L1 removes each arc $u \to w$ that is implied by a longer path from $u$ to $w$. The reduction has the same paths, so a schedule for it is a schedule for $G$, but the labels depend on it. Lines L2 to L6 label the jobs from the end of the graph to the start: the sinks first, and later a job only after all of its immediate successors. Ties in line L5 between equal sequences can be broken in any way. Lines L7 to L10 are list scheduling with the priority list sorted by decreasing label.

## Example

Take $m = 2$ and six jobs with the arcs $0 \to 5$, $1 \to 3$, $2 \to 3$, $2 \to 4$ and $2 \to 5$. The graph is already transitively reduced.

| step $k$ | ready jobs and $N(j)$ | labeled job |
|---|---|---|
| 1, 2, 3 | 3, 4, 5, each with $N = ()$ | 3, 4, 5 get labels 1, 2, 3 |
| 4 | 0 with $(3)$, 1 with $(1)$, 2 with $(3, 2, 1)$ | 1, since $(1)$ is smallest |
| 5 | 0 with $(3)$, 2 with $(3, 2, 1)$ | 0, since $(3)$ is a prefix of $(3, 2, 1)$ |
| 6 | 2 with $(3, 2, 1)$ | 2 |

| slot | available jobs (label) | chosen |
|---|---|---|
| 1 | 0 (5), 1 (4), 2 (6) | 2, 0 |
| 2 | 1 (4), 4 (2), 5 (3) | 1, 5 |
| 3 | 3 (1), 4 (2) | 3, 4 |

The makespan is 3, and 6 jobs on 2 machines need at least 3 slots, so the schedule is optimal. All of jobs 0, 1 and 2 start a chain of 2 jobs, so a rule that uses only the chain length can take 0 and 1 first. Then job 2 runs alone in slot 2, and the makespan is 4. The labels see that job 2 frees three jobs and job 0 frees job 5, so they put both in slot 1.

## Correctness

Feasibility is clear: a job gets a slot only after all of its predecessors in the reduced graph, and the reduced graph has the same paths as $G$.

For $m = 2$ the proof builds a chain of job sets $S_r, \ldots, S_1, S_0$ in the schedule, such that each job of $S_{i+1}$ must come before each job of $S_i$ in every schedule, and $\sum_i \lceil |S_i|/2 \rceil = \mathrm{ALG}$. The sets are cut at the slots where a machine is idle or where the schedule had to run a job of low label. Two facts drive the argument. First, a job with a larger label has a lexicographically larger successor sequence. Second, in a transitively reduced graph, a job cannot have an arc to a job that it also reaches by a longer path. Together they show that each job of $S_{i+1}$ has a path to every job of $S_i$. Then every schedule needs $\lceil |S_r|/2 \rceil + \cdots + \lceil |S_0|/2 \rceil = \mathrm{ALG}$ slots, so $\mathrm{OPT} \ge \mathrm{ALG}$. The lower bound is a refinement of the [critical path lower bound](/critical-path-lower-bound/) that counts the work along a chain of sets. The full proof is in the proofs section.

For $m \ge 3$, Lam and Sethi (1977) proved $\mathrm{ALG} \le (2 - 2/m)\,\mathrm{OPT}$. Their proof is long and is not repeated here.

## Complexity

- Line L1 takes $O(n (n + e))$ time with one graph search from each job, or matrix multiplication time with Boolean matrices. The reachability sets take $O(n^2)$ space.
- Lines L2 to L6 can be done in $O(n + e)$ time with a careful order of the sequences (Sethi 1976). A direct version that sorts the sequences at each step takes $O(n^2 + n e \log n)$ time.
- Lines L7 to L10 take $O(n \log n + e)$ time with a heap of available jobs keyed by label and a counter of unfinished predecessors for each job.

The transitive reduction dominates, so the total is $O(n (n + e))$ time in the worst case. Gabow (1982) gave an almost linear time algorithm for two processors that does not compute the reduction.

## Properties

- **Exact for two machines.** For $m = 2$ the makespan is optimal, for every tie-breaking rule in line L5.
- **Ratio $2 - 2/m$ for $m$ machines.** The ratio is absolute. It is measured against $\mathrm{OPT}$, and it is better than the bound $2 - 1/m$ of [Graham's analysis](/list-scheduling-bound/) for an arbitrary list.
- **Not optimal for three machines.** Take $m = 3$ and nine jobs with arcs $0 \to 7$, $2 \to 3$, $3 \to 1, 6, 8$, $4 \to 1, 8$ and $5 \to 1, 6, 8$. The labels are $5, 1, 9, 7, 6, 8, 2, 3, 4$ for jobs $0, \ldots, 8$, and the schedule is $\{2, 5, 4\}, \{0, 3\}, \{8, 7, 6\}, \{1\}$ with makespan 4. The schedule $\{2, 0, 4\}, \{3, 5, 7\}, \{1, 6, 8\}$ has makespan 3.
- **A list schedule.** The second phase is list scheduling, so no machine is idle while a job is available.
- **Contains Hu's rule on trees.** On an in-forest, a job with a longer chain to the root gets a larger label, so the schedule is one of [Hu's](/hu-algorithm/) schedules.

## Variants and improvements

- **Without the transitive reduction.** If line L1 is left out, the labels change, and the proof above no longer works. Gabow (1982) gave a different optimal method for $m = 2$ that works on the graph as given.
- **Fixed $m \ge 3$.** The complexity of $P3 \mid \text{prec}, p_j = 1 \mid C_{\max}$ is a well known open problem. For $m$ in the input the problem is NP-hard, and no polynomial algorithm has ratio below $4/3$ unless P = NP; see [precedence-constrained scheduling](/precedence-constrained-scheduling/).
- **Trees on many machines.** If the precedence graph is an in-forest or an out-forest, [Hu's algorithm](/hu-algorithm/) is optimal for every $m$.

## When to use it

Use the Coffman-Graham algorithm for two machines and unit jobs with general precedence constraints, where it is optimal. For more machines it is a cheap list order with a slightly better worst case guarantee than an arbitrary list. For jobs of different lengths the optimality proof fails; use [list scheduling](/list-scheduling/) with a critical path order and its $2 - 1/m$ guarantee.

## Pitfalls

- **Skipping the transitive reduction.** The labels are defined on the reduced graph. Redundant arcs change the successor sequences and the proof.
- **The order of the comparison.** The smallest sequence gets the *next* label, which is the next *larger* number, because labels grow from the sinks to the sources. Then the schedule takes the *largest* labels first. Reversing one of these rules gives a bad schedule.
- **Prefixes.** In the lexicographic order a proper prefix is smaller. A job with successor labels $(3)$ gets its label before a job with $(3, 2, 1)$.
- **Starting a job in the slot of its predecessor.** A job is available in slot $t$ only if its predecessors are in slots below $t$, not in slot $t$.

## Implementations

## History

Coffman and Graham published the algorithm in Acta Informatica in 1972, as a two-processor rule for unit tasks with a precedence graph. Earlier, Fujii, Kasami and Ninomiya (1969) had solved the same two-processor problem with matching. In 1975 Ullman showed that the problem with $m$ in the input is NP-hard. Sethi (1976) gave a fast implementation of the labeling, and Lam and Sethi (1977) proved that the same algorithm has ratio $2 - 2/m$ on $m$ processors. Gabow (1982) gave an almost linear time algorithm for two processors.

## References

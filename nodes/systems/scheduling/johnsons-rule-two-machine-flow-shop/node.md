---
tag: 8HDKEZ
kind: algorithm
slug: johnsons-rule-two-machine-flow-shop
name: Johnson's rule for two-machine flow shop
aliases:
- Scheduling jobs on two machines
- Johnson's smallest-time procedure
area: systems/scheduling
level: core
summary: "Johnson's 1954 procedure: take the smallest remaining time; a machine 1 time sends its job to the front, a machine 2 time to the back. It minimizes the two-machine makespan."
solves: [two-machine-flow-shop]
model: word-ram
complexity:
  vars: {n: the number of jobs}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, online: false, recursive: false}
history:
  year: 1954
  people: [S. M. Johnson]
  note: Johnson stated the procedure in this smallest-time form and proved it optimal for two-stage production.
prereqs: [johnsons-rule]
see_also: [two-machine-flow-shop, three-machine-flow-shop, flow-shop-scheduling, exchange-argument, makespan-lower-bounds, job-shop-scheduling, open-shop-scheduling, sorting-problem]
sources:
  - paper: doi:10.1002/nav.3800010110
    title: S. M. Johnson, Optimal two- and three-stage production schedules with setup times included, Naval Research Logistics Quarterly 1(1), 1954
    locator: pages 61 to 68 (the smallest-time procedure, its proof, and the remark that one order serves both machines)
  - book: "Richard W. Conway, William L. Maxwell and Louis W. Miller, Theory of Scheduling, Addison-Wesley, 1967"
    locator: Chapter 5, the flow shop (permutation schedules are optimal for two and three machines, not for four)
  - book: isbn:9783319265780
    title: Michael L. Pinedo, Scheduling, Theory, Algorithms, and Systems, fifth edition
    locator: Chapter 6, Section 6.1, Flow Shops with Unlimited Intermediate Storage (permutation schedules for m ≤ 3, and Johnson's rule)
  - book: isbn:9783540695158
    title: Peter Brucker, Scheduling Algorithms, fifth edition
    locator: Chapter 6, Shop Scheduling Problems (the two-machine flow shop)
---

Johnson's rule for the two-machine flow shop is the result that makes $F2 \| C_{\max}$ easy, in the form Johnson first gave it: look at all $2n$ processing times, take the smallest one whose job is not yet placed, and put that job at the front of the open positions if the time is on machine 1, or at the back if it is on machine 2. This page proves two things. First, for two machines (and for three) one order on all machines is as good as any schedule, which fails for four machines. Second, the smallest-time procedure gives an order in which every pair of jobs satisfies Johnson's condition, and every such order is optimal. The [two-list page](/johnsons-rule/) gives the form of the rule that most code uses, with its own proof; this page is the theorem behind both.

## In plain words

Write down every job's time at the first station and at the second station, and sort all these numbers. Go through the list from the smallest number. If the number belongs to a job that already has a place, skip it. If it is a job's time at the first station, put that job as early as possible in the plan. If it is a job's time at the second station, put the job as late as possible. A job that is very quick somewhere gets placed early in this process, and its quick station decides whether it opens or closes the plan. In the end every job has a place, and no other plan finishes sooner.

## The problem

There are $n$ jobs; job $j$ needs $a_j \ge 0$ on machine 1 and then $b_j \ge 0$ on machine 2, with no preemption and an unlimited buffer. A schedule may in principle use different orders on the two machines. The goal is the least makespan. See [two-machine flow shop](/two-machine-flow-shop/).

**Johnson's condition.** For two jobs $i$ and $j$, write $i \preceq j$ if $\min(a_i, b_j) \le \min(a_j, b_i)$. An order satisfies the condition if $i \preceq j$ for every pair with $i$ before $j$.

## The algorithm

```pseudo id=main
JOHNSON-SMALLEST-TIME(a[1 .. n], b[1 .. n])
L1  T ← the 2n triples (a[j], 1, j) and (b[j], 2, j), sorted increasing
L2  lo ← 1; hi ← n
L3  for each (x, m, j) in T, in order do
L4      if job j is already placed then skip it
L5      mark job j placed
L6      if m = 1 then π[lo] ← j; lo ← lo + 1      ▷ front
L7      else π[hi] ← j; hi ← hi − 1              ▷ back
L8  return π
```

Line L1 sorts by value; on equal values it puts the machine 1 time first. Any tie rule gives an optimal order. Each job is placed at its first triple in $T$, which is its smaller time, so the jobs placed by line L6 are those with $a_j \le b_j$ in increasing $a_j$, and the jobs placed by line L7 fill the back in increasing $b_j$, which reads as decreasing $b_j$ from the front. This is the same order as the [two-list form](/johnsons-rule/).

## Example

Five jobs.

| job | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| $a_j$ | 7 | 3 | 9 | 4 | 6 |
| $b_j$ | 5 | 8 | 2 | 4 | 7 |

Line L1 sorts the ten times. The procedure reads them in order:

| time | machine | job | action | positions after |
|---|---|---|---|---|
| 2 | 2 | 3 | back | $\_, \_, \_, \_, 3$ |
| 3 | 1 | 2 | front | $2, \_, \_, \_, 3$ |
| 4 | 1 | 4 | front | $2, 4, \_, \_, 3$ |
| 4 | 2 | 4 | skip | |
| 5 | 2 | 1 | back | $2, 4, \_, 1, 3$ |
| 6 | 1 | 5 | front | $2, 4, 5, 1, 3$ |

The other five times all belong to placed jobs. The order $2, 4, 5, 1, 3$ runs as follows.

| job | machine 1 | machine 2 |
|---|---|---|
| 2 | 0 to 3 | 3 to 11 |
| 4 | 3 to 7 | 11 to 15 |
| 5 | 7 to 13 | 15 to 22 |
| 1 | 13 to 20 | 22 to 27 |
| 3 | 20 to 29 | 29 to 31 |

The makespan is $31 = \sum_j a_j + \min_j b_j = 29 + 2$: machine 1 is busy without a gap until $29$, and job 3, the job with the least time on machine 2, is last. The input order takes $36$.

**Four machines.** Job 1 needs $(1, 4, 4, 1)$ and job 2 needs $(4, 1, 1, 4)$ on machines 1 to 4. The order $1, 2$ on all machines ends at $14$, and so does $2, 1$. Running $1, 2$ on machines 1 and 2 and $2, 1$ on machines 3 and 4 gives

| machine | first operation | second operation |
|---|---|---|
| 1 | job 1, 0 to 1 | job 2, 1 to 5 |
| 2 | job 1, 1 to 5 | job 2, 5 to 6 |
| 3 | job 2, 6 to 7 | job 1, 7 to 11 |
| 4 | job 2, 7 to 11 | job 1, 11 to 12 |

which ends at $12$. So no order alone is optimal here.

## Correctness

The proof has four parts. (1) For $m \le 3$ machines there is an optimal schedule with one order on all machines: if machine 1 runs $i$ right before $j$ but machine 2 runs $j$ before $i$, swap them on machine 1, and symmetrically for the last two machines with a swap on the last machine; neither swap delays anything. (2) Swapping adjacent jobs $i$ then $j$ in an order changes only two terms of the makespan formula, and the pair costs a fixed amount minus $\min(a_j, b_i)$, so $i$ first is no worse when $i \preceq j$. (3) The procedure outputs an order that satisfies Johnson's condition for every pair: of the four times of $i$ and $j$, the first one in $T$ decides, and if $i$ ends before $j$ that time is $a_i$, placing $i$ at the front, or $b_j$, placing $j$ at the back; in both cases it is the least of the four, which gives $\min(a_i, b_j) \le \min(a_j, b_i)$. (4) Any optimal order can be turned into the output by adjacent swaps of pairs that the output orders the other way, and by (2) and (3) none of them raises the makespan. The full proof is below.

## Complexity

- **Time.** The sort of line L1 takes $\Theta(n \log n)$. The loop handles $2n$ triples in $O(1)$ each.
- **Space.** $\Theta(n)$ for $T$, the marks and the order.

## Properties

- **Exact** for $F2 \| C_{\max}$, over all schedules, not only permutation schedules.
- **One order serves both machines.** This is also true for three machines and false for four.
- **The condition is not transitive.** With ties, $\preceq$ can hold for adjacent pairs and fail for a distant pair. For $a = (5, 2, 3)$ and $b = (2, 2, 3)$, the order $1, 2, 3$ has $1 \preceq 2$ and $2 \preceq 3$, yet not $1 \preceq 3$. It takes $13$, while the procedure gives $2, 3, 1$ with makespan $12$.
- **Any tie rule works.** Equal times may be read in any order in line L1.

## Variants and improvements

- **The two-list form.** Split by $a_j \le b_j$ and sort each list; see [Johnson's rule](/johnsons-rule/). It gives the same order up to ties and is easier to write.
- **Three machines.** The dominance of permutation schedules still holds, but the problem is strongly NP-hard. Johnson's paper gives the special case where the middle machine is dominated; see [three-machine flow shop](/three-machine-flow-shop/).
- **Setup times.** Johnson's title mentions setup times: a setup that does not depend on the order is added to the processing time of its operation, and the procedure applies unchanged.
- **Open and job shops.** For two machines, the open shop and the job shop with routes of length two are also solved in polynomial time by related rules; see [open shop scheduling](/open-shop-scheduling/) and [job shop scheduling](/job-shop-scheduling/).

## When to use it

Use it to schedule a batch of jobs through two stages in fixed order with a buffer between them, when all jobs are known and the batch should finish as early as possible. The smallest-time form is handy by hand, as on a planning board: one scan of a sorted list of times places every job. In code, the two-list form is shorter.

## Pitfalls

- **Sorting with the condition as a comparator.** Because $\preceq$ is not transitive with ties, a comparison sort that uses it can return an order such as $1, 2, 3$ above, which is not optimal. Sort by a real key, as this procedure does.
- **Placing a job twice.** Each job has two times in $T$; the second one must be skipped, as in line L4.
- **Back positions.** Jobs placed at the back fill the order from the end, so the first one placed at the back is the last job.
- **Four or more machines.** One order is no longer enough, and the problem is strongly NP-hard already for three machines.

## Implementations

## History

S. M. Johnson published the procedure in 1954 in the Naval Research Logistics Quarterly, as the optimal rule for two-stage production, and noted that the same order should be used on both machines. The proof that one order on all machines suffices for three machines, and the four-machine example where it fails, became standard in the textbook of Conway, Maxwell and Miller in 1967. Garey, Johnson and Sethi showed in 1976 that three machines are strongly NP-hard, so the two-machine case is the edge of what a sort can solve.

## References

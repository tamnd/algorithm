---
tag: PME9E7
kind: algorithm
slug: shortest-seek-time-first
name: Shortest seek time first
aliases:
- SSTF
- shortest seek first
area: systems/scheduling
level: intro
summary: Disk scheduling that always serves the pending request nearest the head. It cuts head movement, but it is not optimal and a far request can starve.
solves: [disk-scheduling]
model: word-ram
complexity:
  vars: {n: the number of requests in a static batch}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 1967
  people: [Peter J. Denning]
  note: Denning compared the shortest seek time first rule with first come first served and with his SCAN policy in a 1967 AFIPS paper.
prereqs: [disk-scheduling, greedy-algorithm]
see_also: [scan-algorithm, look, fcfs-scheduling, nearest-neighbor-tsp, starvation, aging]
sources:
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10, Section 10.4, Disk Scheduling (SSTF on the queue 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53, and its starvation)
  - paper: doi:10.1145/1465482.1465485
    title: "Peter J. Denning, Effects of scheduling on file memory operations, AFIPS Spring Joint Computer Conference 30 (1967), 9-21"
    locator: the comparison of first come first served, shortest seek time first and SCAN
  - paper: doi:10.1145/359024.359034
    title: "Micha Hofri, Disk scheduling: FCFS vs. SSTF revisited, Communications of the ACM 23(11) (1980), 645-653"
    locator: the simulation that compares the mean wait and its variance under FCFS and SSTF, with analytic results for FCFS
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, 313-324"
    locator: Section 2 (shortest seek first among the earlier policies) and Section 5 (shortest time first and its aged form)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 37, Hard Disk Drives, the part on disk scheduling (SSTF and its starvation)
---

Shortest seek time first (SSTF) is the [disk scheduling](/disk-scheduling/) policy that always moves the head to the pending request nearest to it. It is the greedy rule for the problem, and on a static batch it is the [nearest neighbor](/nearest-neighbor-tsp/) heuristic for a path on a line. SSTF moves the head much less than [FCFS](/fcfs-scheduling/), but it does not reach the least head movement, and in the dynamic model a stream of near requests can make a far request wait without bound.

## In plain words

The disk arm stands at some place. Many requests wait at other places. SSTF looks at all of them and goes to the closest one. When it gets there, it looks again and goes to the closest of the rest, and so on.

This keeps each trip short, so the arm travels much less than when it serves requests in the order they came. But short trips now do not always mean a short trip in total: the arm can wander away from a request and have to come all the way back for it later.

There is a worse problem. If new requests keep coming near the arm, the arm stays there. A request at the far side of the disk can wait for as long as the near requests keep coming.

## The problem

The input is the static batch of [disk scheduling](/disk-scheduling/): a multiset $R$ of $n$ cylinder requests on a disk with cylinders $0, \ldots, C - 1$, the head at cylinder $r$, and a direction $d \in \{+1, -1\}$, where $+1$ means toward higher cylinders. The output is the order in which SSTF serves the requests, and its cost is the total head movement $M$. In the dynamic model the requests arrive over time and SSTF picks the nearest request among those that have arrived.

**Tie rule.** When the nearest pending requests lie at the same distance on both sides of the head, SSTF keeps the direction of its last move. Before the first move it uses the direction $d$ that the caller gives. The policy as usually stated leaves ties open; this rule makes it deterministic.

## The algorithm

A direct version scans all pending requests at each step, in $O(n^2)$ time. On a static batch the served requests always form a contiguous run of the sorted array, so two indices around that run are enough.

```pseudo id=main
SSTF(R, r, d)                ▷ requests R, head r, direction d ∈ {+1, −1}
L1  A ← R sorted in increasing order; n ← |A|
L2  i ← (number of A[k] < r) − 1; j ← i + 1     ▷ A[i] < r ≤ A[j]
L3  p ← r; out ← empty list
L4  while i ≥ 0 or j < n do
L5      dl ← p − A[i] if i ≥ 0, else ∞           ▷ nearest pending below
L6      du ← A[j] − p if j < n, else ∞           ▷ nearest pending above
L7      if du < dl or (du = dl and d = +1) then x ← A[j]; j ← j + 1
L8      else x ← A[i]; i ← i − 1
L9      if x ≠ p then d ← sign(x − p)            ▷ the direction of the last move
L10     p ← x; append x to out
L11 return out
```

Line L2 is a binary search. Line L7 takes the upper candidate when it is nearer, or when the two are at the same distance and the last move went up. A request at the head cylinder has distance 0 and is taken at once. The dynamic version keeps the pending requests in a map from cylinder to queue, and at each tick moves the head one cylinder toward the nearest pending cylinder with the same tie rule.

## Example

The queue of Silberschatz, Galvin and Gagne is 98, 183, 37, 122, 14, 124, 65, 67 on cylinders 0 to 199, with the head at 53. No tie occurs, so the direction does not matter. Line L1 gives $A = 14, 37, 65, 67, 98, 122, 124, 183$, and line L2 gives the candidates 37 below and 65 above.

| step | head $p$ | below, distance | above, distance | served | move |
|---|---|---|---|---|---|
| 1 | 53 | 37, 16 | 65, 12 | 65 | 12 |
| 2 | 65 | 37, 28 | 67, 2 | 67 | 2 |
| 3 | 67 | 37, 30 | 98, 31 | 37 | 30 |
| 4 | 37 | 14, 23 | 98, 61 | 14 | 23 |
| 5 | 14 | none | 98, 84 | 98 | 84 |
| 6 | 98 | none | 122, 24 | 122 | 24 |
| 7 | 122 | none | 124, 2 | 124 | 2 |
| 8 | 124 | none | 183, 59 | 183 | 59 |

The total head movement is 236. The optimum is 208, by the order 37, 14, 65, 67, 98, 122, 124, 183. At step 3 the choice of 37 over 98 is good locally, by 1 cylinder, but the head must then cross the whole range from 14 back up to 183.

**Ties.** From 50 with requests 40 and 60, SSTF serves 60 then 40 when $d = +1$, and 40 then 60 when $d = -1$. From 10 with requests 7, 9, 11, 13 and $d = -1$, 9 and 11 are both at distance 1, so it serves 9; then 7 and 11 are both at distance 2 and the last move went down, so it serves 7; then 11 and 13. With $d = +1$ it serves 11, 13, 9, 7.

## Correctness

SSTF serves each request exactly once, and each step serves a nearest pending request. The key fact is the invariant before each run of line L4:

- the pending requests are exactly $A[0..i]$ and $A[j..n-1]$, and the served ones are $A[i+1..j-1]$, in the order of `out`;
- $A[i] \le p \le A[j]$ whenever these entries exist.

So the nearest pending request below or at $p$ is $A[i]$, the nearest above or at $p$ is $A[j]$, and lines L5 to L8 pick the nearer one with the tie rule. Each run of the loop moves $i$ down or $j$ up by one, so the loop ends after $n$ runs. The full proof is below, with the two negative results: SSTF is not optimal, and its wait is unbounded in the dynamic model.

## Complexity

- **Static batch.** Line L1 sorts in $O(n \log n)$ time; line L2 is a binary search; the loop does $O(1)$ work per request. The total is $O(n \log n)$ time and $\Theta(n)$ extra space.
- **Naive version.** A scan of all pending requests at each step takes $\Theta(n^2)$ time. It gives the same order under the same tie rule; the tests compare the two.
- **Dynamic version.** With a balanced search tree over the pending cylinders, each step finds the predecessor and the successor of the head in $O(\log m)$ time, where $m$ is the number of pending cylinders. The test code scans the map instead, in $O(m)$ per tick, which is enough for a simulation.
- **Head movement.** The ratio of SSTF to the optimum can come close to 2. Put the head at 10, a request at 8 and a chain of requests at $11, 13, 15, \ldots, t$. Each step up the chain is 2 cylinders, which is less than the way back to 8, so SSTF climbs to $t$ first and moves $(t - 10) + (t - 8) = 2t - 18$ cylinders. The optimum goes to 8 first and moves $2 + (t - 8) = t - 6$.

## Properties

- **Greedy and online.** SSTF looks only at the current head and the pending set. It needs no knowledge of future requests.
- **Not optimal.** With the head at 50 and requests at 46, 53 and 58, SSTF serves 53, 58, 46 for a movement of $3 + 5 + 12 = 20$. The optimum serves 46, 53, 58 for $4 + 7 + 5 = 16$, and a search over all 6 orders confirms 16.
- **Contiguous service.** On a static batch the served cylinders always form an interval of the sorted batch around the start. The head is always at one end of that interval.
- **Unbounded wait.** In the dynamic model no bound on the wait of a request holds; see the pitfalls and the proof.
- **Favors the middle.** A request in the middle of the disk is near the head more often than a request at an edge. In the stream of the [disk scheduling](/disk-scheduling/) page, the mean wait is 94.0 ticks on the middle cylinders and 199.2 ticks on the edge cylinders.

## Variants and improvements

- **Aged SSTF.** Subtract a multiple of the age of a request from its distance, as [aging](/aging/) does for [priority scheduling](/priority-scheduling/). A large enough weight bounds the wait and makes the policy act more like FCFS.
- **Shortest positioning time first.** Count the rotational delay as well as the seek, and pick the request with the least total positioning time. Seltzer, Chen and Ousterhout (1990) call it shortest time first; Jacobson and Wilkes (1991) call it shortest access time first and add an aged form.
- **Batched SSTF.** Freeze the queue, serve the frozen batch in SSTF order, and only then admit new requests. The wait is then bounded by the time of two batches.
- **Sweep policies.** [SCAN](/scan-algorithm/) and [LOOK](/look/) keep one direction until no request remains ahead. They give up a little movement for a bound on the wait.

## When to use it

Use SSTF when the throughput of the disk matters most and the load is moderate, so that the queue empties from time to time and no request waits for long. It is a good baseline against which to measure other policies. Do not use it alone under heavy load or with requests that need a bounded response time; add aging, batch the queue, or use a sweep policy. On a static batch where only the total movement counts, use [LOOK](/look/) toward the nearer end, which is optimal.

## Pitfalls

- **Starvation.** Let the head be at 100 on a disk of 200 cylinders, a request at cylinder 0 arrive at tick 0, and one request arrive at cylinder 100 at each tick $0, 1, \ldots, k - 1$, with no service time. The head moves between 99 and 100 while the stream lasts, since the request at 100 is at distance at most 1 and the one at 0 at distance at least 99. The request at 0 finishes at tick $k + 100$: the tests give 110, 200 and 1100 for $k = 10$, 100 and 1000. An endless stream would hold it forever.
- **Calling it optimal.** The nearest request at each step does not give the least total movement. On the textbook queue SSTF moves 236 cylinders and the optimum 208.
- **No tie rule.** "The nearest request" is not well defined when two requests are at the same distance on both sides. Without a stated rule, two correct implementations can give different orders and different costs.
- **Distance is not time.** On a real drive the seek time is not linear in the distance, and the rotation adds a delay. The nearest cylinder is not always the request that the drive can reach first.
- **Stale requests at the head cylinder.** A request at the head cylinder has distance 0. With a positive service time, a stream of requests on that one cylinder holds the head there.

## Implementations

## History

Peter Denning studied the shortest seek time first rule in 1967, next to first come first served, in the AFIPS paper where he also proposed SCAN. Hofri (1980) compared FCFS and SSTF in a large simulation with stationary arrivals and found SSTF generally better when the goal is a small mean wait and a small variance, mostly at medium and heavy loads. Seltzer, Chen and Ousterhout (1990) and Jacobson and Wilkes (1991) extended the greedy rule to positioning time, which includes the rotation, and added aging to bound the wait.

## References

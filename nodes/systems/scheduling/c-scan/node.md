---
tag: PAACQ9
kind: algorithm
slug: c-scan
name: C-SCAN
aliases:
- circular SCAN
area: systems/scheduling
level: intro
summary: Disk scheduling that serves requests only while the head sweeps in one direction, then jumps back to the first cylinder. Each cylinder gets the same mean wait.
solves: [disk-scheduling]
model: word-ram
complexity:
  vars: {n: the number of requests in a static batch}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [scan-algorithm]
see_also: [scan-algorithm, c-look, look, disk-scheduling, shortest-seek-time-first, scheduling-metrics]
sources:
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10, Section 10.4, Disk Scheduling (C-SCAN on the queue 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53, and the cylinders as a circular list)
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, 313-324"
    locator: Section 4.3 (C-SCAN against SCAN, with one long seek per sweep, nearly the same throughput and a smaller maximum and variance of the response time)
  - paper: doi:10.1145/361268.361278
    title: "Toby J. Teorey and Tad B. Pinkerton, A comparative analysis of disk scheduling policies, Communications of the ACM 15(3) (1972), 177-184"
    locator: the comparison of five policies by the mean seek time, the mean wait and the variance of the wait
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 37, Hard Disk Drives, the part on disk scheduling (the elevator, F-SCAN and C-SCAN)
---

C-SCAN, or circular SCAN, is the [disk scheduling](/disk-scheduling/) policy that serves requests only while the head moves in one direction. When the head reaches the end of the disk, it returns to the other end without serving anything and starts the next sweep. So the disk acts as if its cylinders formed a circle. C-SCAN moves the head more than [SCAN](/scan-algorithm/), but each cylinder is passed once per cycle at the same point of the cycle, so all cylinders get the same mean wait.

## In plain words

Think of a bus that drives along one street and picks up people at each stop. At the end of the street it does not pick up anybody on the way back. It drives empty to the start and begins again.

C-SCAN moves the disk arm in this way. It serves requests only on the way up. At the top edge it returns to the bottom edge without serving, and sweeps up again.

The return trip costs time. But now every place on the disk waits the same time, on average, for the arm to come back. With SCAN, places near the edges wait about twice as long as places in the middle, because the arm passes the middle twice in each round trip and the edges only once.

## The problem

The input is the static batch of [disk scheduling](/disk-scheduling/): a multiset $R$ of $n$ cylinder requests on cylinders $0, \ldots, C - 1$, the head at $r$, and the service direction $d \in \{+1, -1\}$. The output is the service order and the head path. The cost is the length of the path, and the path includes the return from one end of the disk to the other. Texts differ on whether this return counts as head movement, so the page gives both values. In the dynamic model, requests arrive over time, the head moves one cylinder per tick while it sweeps, and the return takes $J$ ticks. The default in the implementation is $J = C - 1$, one tick per cylinder; a smaller $J$ models a fast return seek.

## The algorithm

The pseudocode is for $d = +1$. For $d = -1$, exchange "above" with "below" and the two ends.

```pseudo id=main
C-SCAN(R, r, C)            ▷ requests R, head r, service direction +1
L1  ahead ← the requests x ≥ r, in increasing order
L2  behind ← the requests x < r, in increasing order
L3  ends ← C − 1, then 0                     ▷ the return goes from C − 1 to 0
L4  path ← r, ahead, then the ends only if behind is not empty, then behind
L5  return the order ahead followed by behind, and the path
```

Both lists are sorted in increasing order, since both are served while the head goes up. If no request is behind the head, the cost is $\max R - r$. Otherwise the cost is $(C - 1 - r) + (C - 1) + b$, where $b$ is the largest request behind the head, or $(C - 1 - r) + b$ without the return.

The dynamic version serves all pending requests at the head cylinder, or moves up one cylinder. At cylinder $C - 1$ it jumps to 0 in $J$ ticks and serves nothing during the jump; requests that arrive during the jump join the queue when it ends. With no pending request the head waits.

## Example

Take the queue of Silberschatz, Galvin and Gagne: 98, 183, 37, 122, 14, 124, 65, 67 on cylinders 0 to 199, with the head at 53.

**Serving toward 199.** Line L1 gives 65, 67, 98, 122, 124, 183 and line L2 gives 14, 37.

| from | to | move | note |
|---|---|---|---|
| 53 | 65 | 12 | |
| 65 | 67 | 2 | |
| 67 | 98 | 31 | |
| 98 | 122 | 24 | |
| 122 | 124 | 2 | |
| 124 | 183 | 59 | |
| 183 | 199 | 16 | the disk end, no request |
| 199 | 0 | 199 | the return, no service |
| 0 | 14 | 14 | |
| 14 | 37 | 23 | |

The total is $146 + 199 + 37 = 382$ cylinders, or 183 without the return.

**Serving toward 0.** The order is 37, 14, then the end 0, the return to 199, then 183, 124, 122, 98, 67, 65. The total is $53 + 199 + 134 = 386$, or 187 without the return.

For comparison, [SCAN](/scan-algorithm/) moves 331 and 236 in the two directions, and the optimum is 208. C-SCAN pays for its even waits with more movement.

## Correctness

Lines L1 and L2 split $R$ into two parts and line L5 returns both, so each request is served once. Each part is served in increasing order, so between the start and the return, and after the return, the head only goes up. The cost formula follows: the head rises from $r$ to $C - 1$, returns over $C - 1$ cylinders, and rises from 0 to $b$.

In the dynamic model with service time 0 and $J \ge 1$, while a request is pending the head runs around a cycle of length $L = (C - 1) + J$ ticks: $C - 1$ ticks up and $J$ ticks for the return. It is at each cylinder exactly once per cycle. So a request waits less than one cycle, at most $L - 1 = (C - 1) + J - 1$ ticks. In a steady sweep, with a request at each cylinder at each tick, the waits at each cylinder are exactly $0, 1, \ldots, L - 1$ once per cycle, and the mean wait is $(L - 1)/2$ on every cylinder. The proofs are below.

## Complexity

- **Static batch.** Sorting takes $O(n \log n)$ time and $\Theta(n)$ extra space. The cost alone needs $\max R$ and the largest request below $r$, so it takes $O(n)$ time.
- **Dynamic version.** With a balanced search tree over the pending cylinders, each arrival and each "next request above" query takes $O(\log m)$ time for $m$ pending cylinders.
- **Wait.** At most $(C - 1) + J - 1$ ticks with service time 0 and $J \ge 1$. With $J = C - 1$ this is $2(C - 1) - 1$, the same as the SCAN bound.

## Properties

- **Even mean wait.** Every cylinder has the same mean wait $(L - 1)/2$ in a steady sweep, where SCAN gives about $C - 1$ at the edges and about $(C - 1)/2$ in the middle. In the stream of the [disk scheduling](/disk-scheduling/) page, C-SCAN with a slow return has mean waits of 228.2 ticks at the edges and 227.9 in the middle.
- **A larger mean with a slow return.** With $J = C - 1$, the steady mean is $C - 1.5$ on every cylinder, which is the SCAN mean at its worst cylinder. The SCAN mean over all cylinders is $(2C - 1)/3 - 1/2$, about two thirds of it. In the stream of the [disk scheduling](/disk-scheduling/) page, the mean wait is 223.2 ticks for C-SCAN and 149.4 for SCAN.
- **A fast return helps.** A long seek costs much less than the same number of short moves on a real drive, since the arm accelerates. With a return of 10 ticks, the same stream gives a mean of 116.1 ticks and a maximum of 248, against 149.4 and 438 for SCAN.
- **Smaller spread.** Seltzer, Chen and Ousterhout (1990) report that C-SCAN pays one long seek per sweep, keeps nearly the throughput of SCAN, and has a much smaller maximum and variance of the response time.

## Variants and improvements

- **[C-LOOK](/c-look/).** Turn at the last request ahead and jump to the first request behind, not to the disk end. This saves the empty parts of the sweep and of the return.
- **Frozen queues.** Admit new requests only at the start of each sweep, as FSCAN does for SCAN, so that requests at the head cylinder cannot hold the arm when service takes time.
- **Deadlines.** Keep the one-way order by sector, and serve a request out of order when it has waited too long. Schedulers of this kind sort in one direction, as C-SCAN does.

## When to use it

Use C-SCAN when the load is heavy and the spread of the waits matters more than the mean, for example when each request belongs to an interactive user. It pays off most when the return seek is fast compared with a full sweep. If the return is slow, compare it with SCAN or LOOK on the real workload first. On a static batch where only total movement counts, use [LOOK](/look/) toward the nearer end instead.

## Pitfalls

- **The return in the cost.** Some texts count the return as head movement and some do not: 382 or 183 on the textbook queue. State the convention.
- **Serving on the return.** C-SCAN serves nothing while it returns. A program that serves requests on the way back is SCAN.
- **Equal mean, not equal wait.** C-SCAN makes the mean wait the same for each cylinder. A single request can still wait almost a full cycle.
- **A stuck arm.** With a positive service time, a stream of requests at the head cylinder holds the arm, as under SCAN.
- **The direction.** The service direction is fixed for the whole run. The two directions give different costs on a batch: 382 against 386 on the textbook queue.

## Implementations

## History

C-SCAN is the circular form of [SCAN](/scan-algorithm/), which Peter Denning proposed in 1967. Its purpose is to remove the bias of SCAN against the edges of the disk. Teorey and Pinkerton (1972) compared five disk scheduling policies and used the variance of the wait as a measure of how much a policy works against single requests. Seltzer, Chen and Ousterhout (1990) found that C-SCAN keeps nearly the throughput of SCAN with a much smaller maximum and variance of the response time.

## References

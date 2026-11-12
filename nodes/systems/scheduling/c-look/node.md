---
tag: GARAAY
kind: algorithm
slug: c-look
name: C-LOOK
aliases:
- circular LOOK
area: systems/scheduling
level: intro
summary: Disk scheduling that serves requests in one direction only, up to the last request ahead, then jumps back to the farthest request behind and sweeps again.
solves: [disk-scheduling]
model: word-ram
complexity:
  vars: {n: the number of requests in a static batch}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [c-scan, look]
see_also: [c-scan, look, scan-algorithm, disk-scheduling, shortest-seek-time-first, scheduling-metrics]
sources:
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10, Section 10.4, Disk Scheduling (C-LOOK on the queue 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53)
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, 313-324"
    locator: Section 4.3 (the one-way scan against the two-way scan, and the cost of the long return seek)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 37, Hard Disk Drives, the part on disk scheduling (the elevator and its circular form)
---

C-LOOK, or circular LOOK, is the [disk scheduling](/disk-scheduling/) policy that serves requests only while the head moves in one direction, as [C-SCAN](/c-scan/) does, but turns at the last pending request ahead, as [LOOK](/look/) does. Then it jumps back to the farthest pending request behind the head and starts the next sweep there. It removes the empty parts of the C-SCAN cycle, so it moves less than C-SCAN, and it keeps the one-way order, which makes the waits more even than under LOOK when the return is fast.

## In plain words

C-LOOK is like a bus on a one-way loop that skips the empty part of the street. It drives along and picks up people at each stop. When nobody waits farther along, it does not drive on to the end of the street. It goes straight back to the first person who waits behind it, and begins again from there.

The disk arm does the same. It serves requests only while it moves one way. When no request is left ahead, it jumps back to the farthest request on the other side, and serves nothing on the way back.

So the arm skips the empty edges of the disk, and every place still gets served in the same one-way order.

## The problem

The input is the static batch of [disk scheduling](/disk-scheduling/): a multiset $R$ of $n$ cylinder requests on cylinders $0, \ldots, C - 1$, the head at $r$, and the service direction $d \in \{+1, -1\}$. The output is the service order. The cost is the total head movement, and it includes the return jump from the last request of the first sweep (or from $r$, if no request lies ahead) to the first request of the second sweep. Texts differ on whether this jump counts, so the page gives both values. In the dynamic model, requests arrive over time and the head moves one cylinder per tick while it sweeps. The return jump takes one tick per cylinder by default, or a fixed number $J$ of ticks for a fast return seek. A request at the head cylinder counts as ahead.

## The algorithm

The pseudocode is for $d = +1$. For $d = -1$, exchange "above" with "below" and "increasing" with "decreasing".

```pseudo id=main
C-LOOK(R, r)               ▷ requests R, head r, service direction +1
L1  ahead ← the requests x ≥ r, in increasing order
L2  behind ← the requests x < r, in increasing order
L3  return ahead followed by behind      ▷ jump from the last of ahead to the first of behind
```

Let $t$ be the last request ahead, or $r$ if no request is ahead, and let $lo$ and $b$ be the smallest and the largest request behind. If no request is behind, the cost is $t - r$. Otherwise the cost is $(t - r) + (t - lo) + (b - lo)$ with the jump counted, and $(t - r) + (b - lo)$ without it.

The dynamic version serves all pending requests at the head cylinder, or moves one cylinder up if some pending request lies strictly above the head. If none does, it picks the smallest pending cylinder and jumps there, serving nothing during the jump. The target is fixed when the jump starts; requests that arrive during the jump join the queue when it ends. With no pending request the head waits.

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
| 124 | 183 | 59 | the last request ahead |
| 183 | 14 | 169 | the return jump, no service |
| 14 | 37 | 23 | |

The total is $130 + 169 + 23 = 322$ cylinders, or 153 without the jump.

**Serving toward 0.** The order is 37, 14, then the jump from 14 to 183, then 124, 122, 98, 67, 65. The total is $39 + 169 + 118 = 326$, or 157 without the jump.

[C-SCAN](/c-scan/) on the same batch moves 382 and 386 (183 and 187 without the return), and the optimum is 208. C-LOOK saves 60 cylinders in each direction with the return counted, and 30 without it:

| policy | toward 199 | toward 0 |
|---|---|---|
| C-SCAN, return counted | 382 | 386 |
| C-LOOK, jump counted | 322 | 326 |
| C-SCAN, return not counted | 183 | 187 |
| C-LOOK, jump not counted | 153 | 157 |

## Correctness

Lines L1 and L2 split $R$ into two parts and line L3 returns both, so each request is served once. Both parts are in increasing order, so the head goes up through `ahead`, makes one jump down, and goes up through `behind`. The cost formula follows from the lengths of these three monotone parts.

C-LOOK never moves more than C-SCAN on the same batch: its path is the C-SCAN path with the stretch from $t$ to $C - 1$ and the stretch from 0 to $lo$ cut out of the sweep and the return, and the tests check this on random batches.

In the dynamic model with service time 0 and a return of one tick per cylinder, each request waits at most $3(C - 1) - 2$ ticks. The bound is larger than the C-SCAN bound because the jump target is fixed when the jump starts: a request that arrives during the jump, below the landing cylinder, must wait for the rest of the jump, a full sweep, and a second jump. The proof is below.

## Complexity

- **Static batch.** Sorting takes $O(n \log n)$ time and $\Theta(n)$ extra space. The cost alone needs only $t$, $lo$ and $b$, so it takes $O(n)$ time.
- **Dynamic version.** With a balanced search tree over the pending cylinders, the test "is any request above the head" and the jump target are queries for the maximum and the minimum, $O(\log m)$ for $m$ pending cylinders.
- **Wait.** At most $3(C - 1) - 2$ ticks with service time 0 and a return of one tick per cylinder. The tests find streams with waits above $2(C - 1)$.

## Properties

- **Never more movement than C-SCAN.** C-LOOK cuts the empty ends of the sweep and of the return.
- **One-way service.** Within each cycle, requests are served in increasing order of cylinder, as under C-SCAN.
- **A wait bound above two sweeps.** Unlike LOOK, whose waits stay below $2(C - 1)$, C-LOOK with a slow return can make a request wait nearly three sweeps. With the head at 199, requests at 199 and 10 at tick 0, and requests at 5 and 198 at tick 1, the head jumps to 10 during ticks 0 to 189, sweeps up to 198, and jumps back to 5: the request at 5 finishes at tick 570, a wait of 569 ticks.
- **Even waits need a fast return.** In the stream of the [disk scheduling](/disk-scheduling/) page, C-LOOK with a return of 10 ticks has the smallest mean (97.0 ticks) and maximum (230) of all the policies there, with 103.8 at the edges and 93.2 in the middle. With a return of one tick per cylinder, the mean is 210.0 and the edges wait 250.8 against 192.4 in the middle.

## Variants and improvements

- **Fixed return time.** Model the jump as one long seek with a fixed time. On a real drive a long seek costs much less than many short moves, which is the reason to use a circular policy.
- **Look again after the jump.** When the jump ends, check for requests that arrived below the landing cylinder and seek down to the lowest of them before the sweep starts. This removes the case above where a request waits for a full sweep and a second jump, at the cost of one more short seek.
- **Frozen queues.** Admit new requests only at the start of each sweep, so that a stream at the head cylinder cannot hold the arm when service takes time.
- **Deadlines.** Keep the requests sorted by sector and give each an expiry time; serve in sector order, but serve an expired request first. The Linux mq-deadline scheduler works in this general way.

## When to use it

Use C-LOOK for a moving-head disk under heavy load when the return seek is fast and the spread of the waits matters. It moves less than C-SCAN and keeps the one-way order. If the return is slow, LOOK did better in the stream of the [disk scheduling](/disk-scheduling/) page: a mean of 140.5 ticks and a maximum of 452, against 210.0 and 623. On a static batch where only total movement counts, use [LOOK](/look/) toward the nearer end, which is optimal.

## Pitfalls

- **The jump in the cost.** Some texts count the jump as head movement and some do not: 322 or 153 on the textbook queue toward 199. State the convention.
- **The wrong jump target.** C-LOOK jumps to the farthest request behind the head, the lowest one when it serves upward, not to the nearest one. A jump to the nearest one behind serves the rest in a downward order and is LOOK.
- **Assuming the C-SCAN bound.** The wait bound of C-SCAN, about two sweeps, does not hold for C-LOOK with a fixed jump target: the example above waits 569 ticks on a disk of 200 cylinders.
- **A stuck arm.** With a positive service time, a stream of requests at the head cylinder holds the arm, as under the other sweep policies.

## Implementations

## History

C-LOOK combines the two refinements of [SCAN](/scan-algorithm/), which Peter Denning proposed in 1967: the one-way sweep of [C-SCAN](/c-scan/) and the early turn of [LOOK](/look/). Textbooks such as Silberschatz, Galvin and Gagne present it with the same example queue as the other policies. Seltzer, Chen and Ousterhout (1990) found that a one-way scan pays one long seek per sweep in exchange for a much smaller maximum and variance of the response time, which is the trade that C-LOOK makes as well.

## References

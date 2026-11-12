---
tag: 6RZ6QE
kind: algorithm
slug: look
name: LOOK
aliases:
- LOOK scheduling
area: systems/scheduling
level: intro
summary: SCAN that reverses at the last pending request, not at the disk end. On a static batch it is optimal when it starts toward the nearer end of the requests.
solves: [disk-scheduling]
model: word-ram
complexity:
  vars: {n: the number of requests in a static batch}
  time: {worst: O(n log n)}
  space: {extra: Θ(n)}
properties: {online: true, deterministic: true, recursive: false}
prereqs: [scan-algorithm]
see_also: [disk-scheduling, scan-algorithm, c-look, c-scan, shortest-seek-time-first, online-dial-a-ride-problem]
sources:
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10, Section 10.4, Disk Scheduling (LOOK and C-LOOK as the forms of SCAN and C-SCAN that turn at the last request)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 37, Hard Disk Drives, the part on disk scheduling (the elevator, SCAN and its variants)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 5, Section 5.4.3, Disk Arm Scheduling Algorithms (the elevator algorithm, which turns when no request lies ahead)
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, 313-324"
    locator: Section 2 (the scan policies in earlier work) and Section 4.3 (SCAN against C-SCAN)
---

LOOK is the [disk scheduling](/disk-scheduling/) policy that sweeps the head in one direction and serves the requests it passes, as [SCAN](/scan-algorithm/) does, but reverses as soon as no pending request lies ahead, instead of going on to the end of the disk. It never moves more than SCAN on the same batch. On a static batch, LOOK started toward the nearer end of the requests gives the least total head movement, and this is the order that proves the optimum formula on the [disk scheduling](/disk-scheduling/) page.

## In plain words

LOOK is the elevator as it works in a real building. It goes up and stops where people wait. When nobody waits higher up, it does not go on to the top floor. It turns at once and goes down.

The disk arm does the same. It sweeps in one direction and serves the requests on its way. When no request is left ahead, it turns back.

This saves the empty trip to the edge of the disk that SCAN makes. Each request still gets its turn within about two sweeps. And when all requests are known at the start, LOOK gives the shortest possible trip, if it first goes toward the closer end of the group of requests.

## The problem

The input is the static batch of [disk scheduling](/disk-scheduling/): a multiset $R$ of $n$ cylinder requests on cylinders $0, \ldots, C - 1$, the head at $r$, and a start direction $d \in \{+1, -1\}$. The output is the service order, and the cost is the total head movement. In the dynamic model, requests arrive over time and the head moves one cylinder per tick. A request at the head cylinder counts as ahead in both directions.

## The algorithm

The pseudocode is for $d = +1$. For $d = -1$, exchange "above" with "below".

```pseudo id=main
LOOK(R, r)                 ▷ requests R, head r, start direction +1
L1  ahead ← the requests x ≥ r, in increasing order
L2  behind ← the requests x < r, in decreasing order
L3  return ahead followed by behind      ▷ turn at the last request ahead
```

The head path is $r$, then the requests in the returned order, with no stop at the disk end. Let $lo = \min R$ and $hi = \max R$. With $d = +1$ the cost is $hi - r$ if $lo \ge r$, it is $r - lo$ if $hi < r$, and otherwise it is $(hi - r) + (hi - lo)$.

The dynamic version moves the head one cylinder per tick in its direction while some pending request lies strictly ahead, and reverses when none does. It serves all pending requests at a cylinder when the head reaches it. With no pending request the head waits.

## Example

Take the queue of Silberschatz, Galvin and Gagne: 98, 183, 37, 122, 14, 124, 65, 67 on cylinders 0 to 199, with the head at 53. Here $lo = 14$ and $hi = 183$.

**Moving toward 0.** This is the nearer end, since $53 - 14 = 39 < 183 - 53 = 130$.

| from | to | move |
|---|---|---|
| 53 | 37 | 16 |
| 37 | 14 | 23 |
| 14 | 65 | 51 |
| 65 | 67 | 2 |
| 67 | 98 | 31 |
| 98 | 122 | 24 |
| 122 | 124 | 2 |
| 124 | 183 | 59 |

The total is $39 + 169 = 208$. The formula $M_{\min} = (hi - lo) + \min(r - lo, hi - r) = 169 + 39$ gives the same value, so this order is optimal. [SCAN](/scan-algorithm/) in the same direction goes on from 14 to 0 and moves 236.

**Moving toward 199.** The order is 65, 67, 98, 122, 124, 183, 37, 14, and the cost is $(183 - 53) + (183 - 14) = 130 + 169 = 299$. SCAN in this direction moves 331, since it goes on to 199.

## Correctness

Lines L1 and L2 split $R$ into two parts, and line L3 returns both, so each request is served once. The path rises from $r$ through `ahead` and then falls through `behind`: it changes direction at most once, and its cost is the formula above.

**Optimality.** Suppose the head starts toward the nearer end of the requests, that is, $d = -1$ when $r - lo \le hi - r$ and $d = +1$ otherwise. Then the LOOK order is the order in the upper bound of the theorem on the [disk scheduling](/disk-scheduling/) page: first the requests on the near side in order of distance, then the others in order of distance. Its cost is $(hi - lo) + \min(|r - lo|, |r - hi|)$, and the lower bound of the same theorem shows that no order costs less. So LOOK, started toward the nearer end, solves the static batch exactly. In the other direction its cost is $(hi - lo) + \max(|r - lo|, |r - hi|)$ when $lo \le r \le hi$, which is at most $2(hi - lo)$, so LOOK in either direction costs at most twice the optimum.

**Bounded wait.** In the dynamic model with service time 0, a request ahead of the head is reached without a reversal, and a request behind is reached after one reversal at a cylinder no farther than the disk end. So each request waits at most $2(C - 1) - 1$ ticks, as under SCAN. The full proof is below.

## Complexity

- **Static batch.** Sorting takes $O(n \log n)$ time and $\Theta(n)$ extra space. The cost and the optimal start direction need only $\min R$, $\max R$ and $r$, so they take $O(n)$ time.
- **Dynamic version.** With the pending cylinders in a balanced search tree, an arrival costs $O(\log m)$ for $m$ pending cylinders, and the test "is any request ahead" is a comparison with the minimum or the maximum, $O(\log m)$. The test code scans a map, which is enough for a simulation.
- **Wait.** At most $2(C - 1) - 1$ ticks with service time 0 and one cylinder per tick.

## Properties

- **Never worse than SCAN.** On the same batch and direction, the LOOK path is the SCAN path without the trip from the last request to the disk end and back. The tests check $\mathrm{LOOK} \le \mathrm{SCAN}$ on random batches.
- **Exact for the static batch.** Toward the nearer end, LOOK gives $M_{\min}$; the tests compare it with a search over all orders for batches of up to 7 requests.
- **One reversal per batch.** The path changes direction at most once.
- **Bounded wait, uneven across cylinders.** The middle of the disk is passed more often than the edges, so, as under SCAN, a request in the middle waits less on average. In the stream of the [disk scheduling](/disk-scheduling/) page, the mean wait is 194.3 ticks on the edge cylinders and 104.4 in the middle, against 205.5 and 110.7 for SCAN.
- **Quick response to a lone request.** With the head at 100 going up and only a request at cylinder 0 pending, LOOK turns at once and serves it after 100 ticks, where SCAN goes to 199 first and needs 298.

## Variants and improvements

- **[C-LOOK](/c-look/).** Serve only in one direction and jump from the last request back to the farthest request behind. The waits become more even.
- **Nearer end first.** For a static batch, pick the start direction toward the nearer of $\min R$ and $\max R$. This makes LOOK optimal for total movement.
- **Frozen queues.** Freeze the queue for each sweep, as FSCAN and N-step SCAN do, so that new requests at the head cylinder cannot hold the arm.
- **Deadlines.** Keep the sweep order, but serve a request out of order when it has waited too long. The Linux mq-deadline scheduler is built on this idea, with requests sorted by sector and an expiry time for each.

## When to use it

Use LOOK for a moving-head disk under moderate to heavy load, when you want low head movement and a bounded wait. Use it toward the nearer end on a static batch, where it is optimal. Prefer C-LOOK when the spread of the waits matters. Use a frozen-queue form when service takes real time and requests can pile up on one cylinder.

## Pitfalls

- **Mixing up SCAN and LOOK.** Many texts and programs call LOOK "SCAN". The costs differ: 236 against 208 on the textbook queue moving toward 0.
- **The wrong start direction.** LOOK is optimal only toward the nearer end. Toward the farther end it can cost up to about twice the optimum: 299 against 208 on the textbook queue.
- **Optimal is not the same as fast.** The optimality holds for total head movement on a static batch. With a seek time that is not linear in the distance, or with rotational latency, the best order can reverse more than once.
- **A stuck arm.** With a positive service time, a stream of requests at the head cylinder holds the arm, as under SCAN. Freeze the queue to fix it.
- **"Ahead" includes the head cylinder.** A request at the head cylinder must be served at once, in either direction. If the code puts it in `behind`, the head leaves and comes back for it.

## Implementations

## History

LOOK is a refinement of [SCAN](/scan-algorithm/), which Peter Denning proposed in 1967. Textbooks such as Silberschatz, Galvin and Gagne present LOOK and C-LOOK as the forms of SCAN and C-SCAN that look for a request before they continue. The optimality of a single reversal at the nearer end, for a static batch with head movement as the cost, follows from the fact that the problem is a path on a line.

## References

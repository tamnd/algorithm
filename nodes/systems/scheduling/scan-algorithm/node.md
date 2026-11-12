---
tag: 5V7681
kind: algorithm
slug: scan-algorithm
name: SCAN
aliases:
- elevator algorithm
area: systems/scheduling
level: intro
summary: Disk scheduling that sweeps the head to one end of the disk, serving requests on the way, then reverses. Each request waits at most about two sweeps.
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
  note: Denning proposed SCAN in his 1967 AFIPS paper on the effects of scheduling on file memory operations.
prereqs: [disk-scheduling]
see_also: [look, c-scan, c-look, shortest-seek-time-first, fcfs-scheduling, online-dial-a-ride-problem]
sources:
  - paper: doi:10.1145/1465482.1465485
    title: "Peter J. Denning, Effects of scheduling on file memory operations, AFIPS Spring Joint Computer Conference 30 (1967), 9-21"
    locator: the SCAN policy and its comparison with first come first served and shortest seek time first
  - paper: doi:10.1137/0201018
    title: "E. G. Coffman, Jr., L. A. Klimko and B. Ryan, Analysis of scanning policies for reducing disk seek times, SIAM Journal on Computing 1(3) (1972), 269-279"
    locator: the queueing analysis of SCAN and of FSCAN
  - paper: doi:10.1145/361268.361278
    title: "Toby J. Teorey and Tad B. Pinkerton, A comparative analysis of disk scheduling policies, Communications of the ACM 15(3) (1972), 177-184"
    locator: the simulation that compares the scan policies with FCFS and shortest seek time first
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10, Section 10.4, Disk Scheduling (SCAN on the queue 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53 moving toward 0)
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, 313-324"
    locator: Section 2 (the scan policies in earlier work) and Section 4.3 (SCAN against C-SCAN, and the longer waits at the edges)
---

SCAN is the [disk scheduling](/disk-scheduling/) policy that moves the head in one direction, serves each request it passes, goes on to the end of the disk, and then reverses. It works like an elevator in a building, which is why it is also called the elevator algorithm. On the textbook queue SCAN moves the head as little as [SSTF](/shortest-seek-time-first/), and unlike SSTF it bounds the wait of each request: with no service time, a request waits less than two full sweeps of the disk.

## In plain words

Think of an elevator in a tall building. It goes up and stops at every floor where someone waits. At the top floor it turns and goes down, and stops again on the way. It does not turn around to pick up one person below.

SCAN moves the disk arm in the same way. The arm sweeps from one side of the disk to the other and serves each request it passes. At the edge it turns back.

No request is left behind for long: the arm comes past every place at least once in each round trip. The cost is that the arm sometimes travels to the edge of the disk when no request is there, and that places in the middle are passed more often than places near the edges.

## The problem

The input is the static batch of [disk scheduling](/disk-scheduling/): a multiset $R$ of $n$ cylinder requests on cylinders $0, \ldots, C - 1$, the head at $r$, and a start direction $d \in \{+1, -1\}$. The output is the service order and the head path, and the cost is the length of the path, which includes the trip to the disk end. In the dynamic model, requests arrive over time, the head moves one cylinder per tick, and SCAN serves the pending requests at each cylinder it reaches. A request at the head cylinder counts as ahead in both directions.

## The algorithm

On a static batch SCAN splits the requests at the head. The pseudocode is for $d = +1$; for $d = -1$, exchange "above" with "below" and $C - 1$ with 0.

```pseudo id=main
SCAN(R, r, C)              ▷ requests R, head r, start direction +1
L1  ahead ← the requests x ≥ r, in increasing order
L2  behind ← the requests x < r, in decreasing order
L3  end ← C − 1                                  ▷ the disk end in the start direction
L4  path ← r, ahead, then end only if behind is not empty, then behind
L5  return the order ahead followed by behind, and the path
```

The cost of the path has a closed form. If no request is behind the head, the path goes up to the largest request and the cost is $\max R - r$. Otherwise the head goes to $C - 1$ and back down to the smallest request, so the cost is $(C - 1 - r) + (C - 1 - \min R)$.

The dynamic version keeps the pending requests in a map from cylinder to queue. At each tick it serves the requests at the head cylinder, or moves one cylinder in its direction, and it reverses only at cylinder 0 or $C - 1$. With no pending request the head waits.

## Example

Take the queue of Silberschatz, Galvin and Gagne: 98, 183, 37, 122, 14, 124, 65, 67 on cylinders 0 to 199, with the head at 53.

**Moving toward 0.** Lines L1 and L2, mirrored, give ahead $= 37, 14$ and behind $= 65, 67, 98, 122, 124, 183$.

| from | to | move | note |
|---|---|---|---|
| 53 | 37 | 16 | |
| 37 | 14 | 23 | |
| 14 | 0 | 14 | the disk end, no request |
| 0 | 65 | 65 | reverse |
| 65 | 67 | 2 | |
| 67 | 98 | 31 | |
| 98 | 122 | 24 | |
| 122 | 124 | 2 | |
| 124 | 183 | 59 | |

The total is $53 + 183 = 236$ cylinders. The trip from 14 to 0 and back costs 28 cylinders and serves nothing, so [LOOK](/look/) on the same batch moves 208, which is the optimum.

**Moving toward 199.** The order is 65, 67, 98, 122, 124, 183, then the end 199, then 37 and 14. The cost is $(199 - 53) + (199 - 14) = 146 + 185 = 331$. The head first goes the long way, so the start direction alone changes the cost by 95 cylinders.

## Correctness

On a static batch SCAN serves each request once: lines L1 and L2 split $R$ into two parts, and line L5 returns both. The path has at most one reversal: it goes up through the sorted part `ahead` to $C - 1$, then down through the part `behind`, which is sorted in decreasing order. So each request is served when the head first reaches its cylinder in the sweep. The path cost formula follows from the fact that a monotone path has length equal to the distance between its ends.

The main claim is about the dynamic model with service time 0. The head, while some request is pending, follows the bouncing walk $0, 1, \ldots, C - 1, C - 2, \ldots, 0, 1, \ldots$ with one cylinder per tick. A cylinder $x$ is visited once in each stretch of $2x$ ticks and $2(C - 1 - x)$ ticks, in turn. So a request that arrives when the head is not on its cylinder is served within $2(C - 1) - 1$ ticks. The full proof is below, with the mean wait per cylinder.

## Complexity

- **Static batch.** Lines L1 and L2 sort in $O(n \log n)$ time and $\Theta(n)$ extra space. The cost alone takes $O(n)$ time from the formula, since it needs only $\min R$, $\max R$ and whether a request lies behind the head.
- **Dynamic version.** With the pending cylinders in a balanced search tree, each arrival costs $O(\log m)$, where $m$ is the number of pending cylinders, and the next stop in the sweep is a successor or predecessor query, also $O(\log m)$. The test code uses a map and one tick per cylinder, which is enough for a simulation.
- **Wait.** With service time 0 and one cylinder per tick, each request waits at most $2(C - 1) - 1$ ticks. With a positive service time, there is no such bound; see the pitfalls.

## Properties

- **Bounded wait.** The bound $2(C - 1) - 1$ does not depend on the load. In the test with a request at cylinder 0 and a stream at cylinder 100, SCAN serves the far request after 298 ticks for each length of the stream, where [SSTF](/shortest-seek-time-first/) waits for the whole stream.
- **The middle is served more often.** In a steady sweep where requests arrive at each cylinder at each tick, the mean wait at cylinder $x$ is
$$\frac{x^2 + (C - 1 - x)^2}{C - 1} - \frac{1}{2}$$
ticks. This is $C - 1.5$ at the two edges and about $(C - 1)/2$ in the middle: the edges wait about twice as long. The mean over all cylinders is $(2C - 1)/3 - 1/2$. In the stream of the [disk scheduling](/disk-scheduling/) page, the mean wait is 205.5 ticks on the edge cylinders and 110.7 in the middle.
- **One reversal per batch.** On a static batch the head path changes direction at most once.
- **Not optimal for movement.** The trip to the disk end serves nothing when no request lies there. LOOK removes it.

## Variants and improvements

- **[LOOK](/look/).** Reverse at the last pending request in the current direction, not at the disk end. On a static batch it is optimal when it starts toward the nearer end.
- **[C-SCAN](/c-scan/) and [C-LOOK](/c-look/).** Serve only in one direction and jump back to the start. This makes the mean wait the same on each cylinder.
- **FSCAN.** Keep two queues. A sweep serves only the requests that were pending when it began; new requests go to the other queue. Coffman, Klimko and Ryan (1972) analyzed SCAN and FSCAN.
- **N-step SCAN.** Split the queue into groups of $N$ requests and serve each group in one sweep before the next group. Both FSCAN and N-step SCAN stop new requests from holding the arm.
- **Deadline schedulers.** Serve in sweep order, but serve a request out of order when its deadline expires, as the Linux deadline scheduler does.

## When to use it

Use SCAN, or in practice LOOK, when the load is heavy and each request needs a bounded wait. It is the standard textbook choice for a moving-head disk. Prefer C-SCAN or C-LOOK when the spread of the waits matters more than the mean. Use FSCAN or N-step SCAN when service takes real time and new requests can arrive at the head cylinder. On an SSD, which has no seek, none of these policies helps.

## Pitfalls

- **The trip to the end.** By the strict definition SCAN goes on to cylinder 0 or $C - 1$ even when no request lies there. Many texts and programs say SCAN but stop at the last request, which is LOOK. State which one you mean, since the costs differ: 236 against 208 on the textbook queue.
- **A stuck arm.** With a positive service time, the bound fails. Let the head be at 100 going down, a request wait at 0, and a request arrive at cylinder 100 at each tick. The head serves the new request at 100 at each tick and never moves, so the request at 0 waits at least as long as the stream lasts. FSCAN and N-step SCAN fix this.
- **The start direction.** The direction at the start is part of the input. On the textbook queue it changes the cost from 236 to 331.
- **Equal waits.** SCAN is fair in the sense of a bound, not in the sense of equal waits. A request at an edge waits about twice as long as one in the middle on average.

## Implementations

## History

Peter Denning proposed SCAN in 1967 at the AFIPS Spring Joint Computer Conference, in a paper on the effects of scheduling on file memory operations. He compared it with first come first served and with shortest seek time first. Coffman, Klimko and Ryan (1972) gave a queueing analysis of SCAN and FSCAN, and Teorey and Pinkerton (1972) compared the scan policies by simulation. The name elevator algorithm comes from the analogy with an elevator, which serves calls in its direction of travel.

## References

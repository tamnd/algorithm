---
tag: 683RCB
kind: problem
slug: disk-scheduling
name: Disk scheduling
aliases:
- disk head scheduling
- disk arm scheduling
- seek scheduling
area: systems/scheduling
level: intro
summary: Choose the order in which a hard disk serves its pending cylinder requests, to cut total head movement or seek time and to keep the wait of each request bounded.
prereqs: [scheduling-problem]
see_also: [fcfs-scheduling, shortest-seek-time-first, scan-algorithm, c-scan, look, c-look, online-traveling-salesman-problem, traveling-salesman-problem]
sources:
  - book: isbn:9781118063330
    title: Abraham Silberschatz, Peter B. Galvin and Greg Gagne, Operating System Concepts, ninth edition, Wiley, 2013
    locator: Chapter 10 (Mass-Storage Structure), Section 10.4, Disk Scheduling (FCFS, SSTF, SCAN, C-SCAN and LOOK on the queue 98, 183, 37, 122, 14, 124, 65, 67 with the head at 53)
  - url: https://pages.cs.wisc.edu/~remzi/OSTEP/file-disks.pdf
    title: Remzi H. Arpaci-Dusseau and Andrea C. Arpaci-Dusseau, Operating Systems, Three Easy Pieces
    locator: Chapter 37, Hard Disk Drives (the disk model, and the section on disk scheduling with SSTF, the elevator and SPTF)
  - book: isbn:9780133591620
    title: Andrew S. Tanenbaum and Herbert Bos, Modern Operating Systems, fourth edition, Pearson, 2015
    locator: Chapter 5, Section 5.4.3, Disk Arm Scheduling Algorithms
  - url: https://www.seltzer.com/assets/publications/Disk-Scheduling-Revisited.pdf
    title: "Margo Seltzer, Peter Chen and John Ousterhout, Disk scheduling revisited, Proceedings of the USENIX Winter 1990 Technical Conference, Washington, DC, 313-324"
    locator: Section 2 (previous work on FCFS, SSF and the scan policies) and Section 5 (shortest time first, which adds rotational latency)
  - url: https://john.e-wilkes.com/papers/HPL-CSP-91-7rev1.pdf
    title: David M. Jacobson and John Wilkes, Disk scheduling algorithms based on rotational position, HP Laboratories technical report HPL-CSP-91-7, 1991 (revised March 1991)
    locator: the shortest access time first policy and its aged variant
  - paper: "Chris Ruemmler and John Wilkes, An introduction to disk drive modeling, IEEE Computer 27(3) (1994), 17-28"
    title: An introduction to disk drive modeling
    locator: the seek time curve as a function of the seek distance, and rotational latency
  - url: https://docs.kernel.org/block/index.html
    title: The Linux kernel documentation, Block
    locator: the documents on the deadline, BFQ and Kyber I/O schedulers, and on switching the scheduler
---

Disk scheduling is the problem of choosing the order in which a hard disk serves its pending requests. Each request names a cylinder, and the disk head must move to that cylinder before it can read or write, so the order decides the total head movement and the wait of each request. For a static batch of requests on a line the best order is easy: sweep to the nearer end of the requests, then sweep to the other end. When requests arrive over time there is no single best order, and the policies [FCFS](/fcfs-scheduling/), [SSTF](/shortest-seek-time-first/), [SCAN](/scan-algorithm/), [C-SCAN](/c-scan/), [LOOK](/look/) and [C-LOOK](/c-look/) trade total movement against fairness.

## In plain words

A hard disk has one arm that moves across the disk. Programs ask for data at many places on the disk. The arm must travel to each place, and the travel is slow. So when several requests wait, the disk can save much time if it picks a good order.

If you serve the requests in the order they came, the arm swings back and forth across the disk. If you always go to the nearest request, the arm travels less, but a request far away can wait for a long time. If the arm sweeps from one side to the other, like an elevator in a building, each request gets its turn within about two sweeps.

When all the requests are known at the start, the best plan is simple: go to the closer end of the group of requests, then turn and go to the other end.

## Definition

**The disk.** The cylinders are the integers $0, 1, \ldots, C-1$. The head is at cylinder $r$ and, for the sweep policies, it has a direction $d \in \{+1, -1\}$, where $+1$ means toward higher cylinders. A request is a cylinder $x \in \{0, \ldots, C-1\}$. Several requests can name the same cylinder.

**The static batch.** The input is a multiset $R = \{x_1, \ldots, x_n\}$ of requests, all known at time 0, and the start $r$. A schedule is an order $\pi$ of the requests. Its *total head movement* is

$$M(\pi) = |x_{\pi(1)} - r| + \sum_{i=1}^{n-1} |x_{\pi(i+1)} - x_{\pi(i)}|,$$

measured in cylinders. The goal is an order of least $M(\pi)$. Some policies also move the head to cylinders with no request (SCAN goes to the disk end); their cost is the length of the whole head path.

**Seek time.** On a real drive the time of a seek over $\delta$ cylinders is a function $s(\delta)$, not $\delta$ itself. The arm accelerates and then settles, so $s$ grows roughly like a constant plus $\sqrt{\delta}$ for short seeks and roughly linearly for long seeks (Ruemmler and Wilkes). The cost of an order is then $\sum s(\delta_i)$ over its seeks. Total head movement is the special case $s(\delta) = \delta$.

**The dynamic model.** Requests arrive over time: request $k$ is a pair $(a_k, x_k)$ of an arrival time and a cylinder. The scheduler is an [online algorithm](/online-algorithm/): it sees a request only when it arrives. In the model that the implementations on these pages use, time is an integer clock, the head moves at most one cylinder per tick, a request is served when the head is on its cylinder at a tick at or after its arrival, and each service takes $s$ ticks (with $s = 0$, all requests at the head cylinder finish at once). The wait of request $k$ is $f_k - a_k$, where $f_k$ is its finish time. The measures are the mean, the spread and the maximum of the waits, and the throughput, as on [scheduling metrics](/scheduling-metrics/).

## Variants

- **Static or dynamic.** The static batch is an offline problem with an exact answer, given below. The dynamic problem is online, and the policies are judged by the waits they give on a stream of arrivals.
- **Head movement or seek time.** With $s(\delta) = \delta$ the static problem is solved by a sweep. With a concave seek curve it is not, as the example below shows.
- **Rotational latency.** After the seek, the head waits until the sector turns under it. A policy that counts the seek and the rotation together picks the request with the least *positioning time*. Seltzer, Chen and Ousterhout (1990) call it shortest time first, Jacobson and Wilkes (1991) call it shortest access time first, and it is now often called shortest positioning time first (SPTF). The cost from one request to the next then depends on angles as well as cylinders, it is not symmetric, and the sweep argument below does not apply.
- **Deadlines and fairness.** A request may carry a deadline or a priority. Then the goal mixes head movement with the number of late requests or with a fair share for each process.
- **Several heads or disks.** With several independent arms, the problem also assigns requests to arms.

## Examples

**The textbook queue.** Silberschatz, Galvin and Gagne use the queue 98, 183, 37, 122, 14, 124, 65, 67 on a disk with cylinders 0 to 199, with the head at 53. The head movement of each policy is:

| policy | start direction | service order | head movement |
|---|---|---|---|
| [FCFS](/fcfs-scheduling/) | none | 98, 183, 37, 122, 14, 124, 65, 67 | 640 |
| [SSTF](/shortest-seek-time-first/) | either | 65, 67, 37, 14, 98, 122, 124, 183 | 236 |
| [SCAN](/scan-algorithm/) | toward 0 | 37, 14, (0), 65, 67, 98, 122, 124, 183 | 236 |
| [SCAN](/scan-algorithm/) | toward 199 | 65, 67, 98, 122, 124, 183, (199), 37, 14 | 331 |
| [LOOK](/look/) | toward 0 | 37, 14, 65, 67, 98, 122, 124, 183 | 208 |
| [LOOK](/look/) | toward 199 | 65, 67, 98, 122, 124, 183, 37, 14 | 299 |
| [C-SCAN](/c-scan/) | toward 199 | 65, 67, 98, 122, 124, 183, (199, 0), 14, 37 | 382, or 183 without the return |
| [C-SCAN](/c-scan/) | toward 0 | 37, 14, (0, 199), 183, 124, 122, 98, 67, 65 | 386, or 187 without the return |
| [C-LOOK](/c-look/) | toward 199 | 65, 67, 98, 122, 124, 183, 14, 37 | 322, or 153 without the return |
| [C-LOOK](/c-look/) | toward 0 | 37, 14, 183, 124, 122, 98, 67, 65 | 326, or 157 without the return |
| optimum | | 37, 14, 65, 67, 98, 122, 124, 183 | 208 |

A cylinder in parentheses is a turn point with no request. The requests span $lo = 14$ to $hi = 183$, and $r = 53$ is nearer to 14, so the optimum is $(183 - 14) + (53 - 14) = 169 + 39 = 208$. A search over all $8! = 40320$ orders gives the same value. SSTF does not reach it: it goes up to 65 and 67 first and must then cross the range twice.

**A concave seek curve.** Let a seek over $\delta \ge 1$ cylinders take $1 + \sqrt{\delta}$ time units. Put the head at 3 and the requests at 0, 4 and 10. The order 4, 0, 10 has head movement $1 + 4 + 10 = 15$ and takes $2 + 3 + (1 + \sqrt{10}) \approx 9.162$. The best sweep 0, 4, 10 has head movement 13, the least possible, but takes $(1 + \sqrt 3) + 3 + (1 + \sqrt 6) \approx 9.182$, and the other sweep 4, 10, 0 takes about $9.612$. So under this seek curve the fastest order reverses twice, and the least movement is not the least time.

**A dynamic stream.** The table below comes from the implementations on the policy pages. The disk has 200 cylinders. At each of 50000 ticks one request arrives with probability 0.05 at a uniform cylinder, drawn with `random.Random(7)`, which gives 2533 requests. The head starts at 100 going up, it moves one cylinder per tick, and each service takes 2 ticks. FCFS seeks to the oldest request each time. For C-SCAN and C-LOOK the return jump takes one tick per cylinder, or a fixed 10 ticks, which models a fast return seek. "Edge" is the mean wait of the requests on cylinders 0 to 19 and 180 to 199, and "middle" on cylinders 90 to 109. All waits are in ticks.

| policy | mean wait | standard deviation | maximum | edge | middle |
|---|---|---|---|---|---|
| FCFS | 62964.1 | 36205.3 | 124400 | 61908.3 | 61153.4 |
| SSTF | 139.9 | 126.0 | 874 | 199.2 | 94.0 |
| SCAN | 149.4 | 106.6 | 438 | 205.5 | 110.7 |
| LOOK | 140.5 | 98.5 | 452 | 194.3 | 104.4 |
| C-SCAN, slow return | 223.2 | 128.2 | 457 | 228.2 | 227.9 |
| C-LOOK, slow return | 210.0 | 122.6 | 623 | 250.8 | 192.4 |
| C-SCAN, return of 10 ticks | 116.1 | 65.8 | 248 | 121.0 | 111.9 |
| C-LOOK, return of 10 ticks | 97.0 | 57.7 | 230 | 103.8 | 93.2 |

FCFS cannot keep up: its mean seek is about a third of the disk, more than the 20 ticks between arrivals, so its queue grows during the whole run and its waits depend on the length of the run. SSTF has a low mean and the largest maximum of the reordering policies. SCAN and LOOK serve the middle nearly twice as fast as the edges. C-SCAN gives the edges and the middle the same mean wait. These are numbers from one synthetic workload, not measurements of a real drive.

## Known algorithms

- **[FCFS](/fcfs-scheduling/).** Serve in arrival order. It is fair and simple, and it ignores the geometry, so its head movement can be $n$ times the optimum: with the head at 0 and $n$ requests that alternate between cylinders $C - 1$ and 0, FCFS moves $n(C-1)$ cylinders and one sweep moves $C - 1$.
- **[Shortest seek time first](/shortest-seek-time-first/).** Serve the nearest pending request. It cuts movement but can starve far requests, and it is not optimal even on a static batch.
- **[SCAN](/scan-algorithm/).** The elevator: sweep to the end of the disk, reverse, and sweep back. Each request waits at most about two sweeps when service takes no time.
- **[C-SCAN](/c-scan/).** Serve only in one direction and jump back to the start. Each cylinder gets the same mean wait in a steady sweep.
- **[LOOK](/look/) and [C-LOOK](/c-look/).** As SCAN and C-SCAN, but turn at the last pending request instead of the disk end. LOOK, started toward the nearer end, is optimal on a static batch.
- **Fixes for starvation.** N-step SCAN and FSCAN freeze the queue for each sweep, so new requests at the head cylinder cannot hold the arm. An age term, as in [aging](/aging/) for [priority scheduling](/priority-scheduling/), bounds the wait under SSTF or SPTF.
- **Rotational policies.** Shortest positioning time first and its aged variants, from Seltzer, Chen and Ousterhout and from Jacobson and Wilkes.
- **Operating systems today.** Drives reorder requests in their own firmware, and solid-state drives have no seek at all. The Linux block layer now offers mq-deadline (requests sorted by sector, each with an expiry time), BFQ (a proportional share of the disk for each process), Kyber (latency targets for fast devices) and no scheduler at all. The classic seek policies matter for hard disks, and they survive as parts of these schedulers.

## Bounds

**The static optimum.** Let $R$ be a nonempty multiset of requests with $lo = \min R$ and $hi = \max R$, and let the head be at $r$. Then the least total head movement over all orders is

$$M_{\min} = (hi - lo) + \min(|r - lo|, |r - hi|).$$

When $lo \le r \le hi$ this is the smaller of $(r - lo) + (hi - lo)$ and $(hi - r) + (hi - lo)$. When $r < lo$ it is $hi - r$, and when $r > hi$ it is $r - lo$.

*Proof of the lower bound.* Take any order, and let $p_0 = r, p_1, \ldots, p_n$ be the positions of the head, so $M = \sum_{t=1}^{n} |p_t - p_{t-1}|$. Let $i$ be the first index with $p_i = lo$ and $j$ the first index with $p_j = hi$. If $lo = hi$, then $M \ge |p_i - p_0| = |r - lo|$ and the claim holds. Otherwise $i \ne j$. If $i < j$, the [triangle inequality](/triangle-inequality/) on the real line gives $\sum_{t=1}^{i} |p_t - p_{t-1}| \ge |lo - r|$ and $\sum_{t=i+1}^{j} |p_t - p_{t-1}| \ge hi - lo$, so $M \ge |r - lo| + (hi - lo)$. If $j < i$, the same argument gives $M \ge |r - hi| + (hi - lo)$. In both cases $M \ge M_{\min}$.

*Proof of the upper bound.* Suppose $|r - lo| \le |r - hi|$; the other case is the mirror image. Serve the requests below $r$ in decreasing order, then the requests at or above $r$ in increasing order. A path that only goes down has length equal to the drop, and a path that only goes up has length equal to the rise. If $lo < r$, the first part goes from $r$ down to $lo$ (length $r - lo$) and the second part goes from $lo$ up to the largest request at or above $r$, which is $hi$ (length $hi - lo$); if no request is at or above $r$, then $hi < r$, and $|r - hi| \ge |r - lo|$ forces $hi = lo$, so the path has length $r - lo = M_{\min}$. If $lo \ge r$, the first part is empty and the path goes up from $r$ to $hi$, with length $hi - r = (hi - lo) + (lo - r) = M_{\min}$. $\square$

The order of the upper bound is [LOOK](/look/) started toward the nearer end of the requests. So LOOK is an exact algorithm for the static batch, in $O(n \log n)$ time for the sort, and $M_{\min}$ itself takes $O(n)$ time. When the head lies inside the range, $\min(r - lo, hi - r) \le (hi - lo)/2$, so $hi - lo \le M_{\min} \le \frac{3}{2}(hi - lo)$.

**Waits in the dynamic model.** With service time 0 and the head moving one cylinder per tick, each request waits at most $2(C - 1) - 1$ ticks under SCAN and LOOK, at most $(C - 1) + J$ ticks under C-SCAN with a return jump of $J$ ticks, and less than $3(C - 1)$ ticks under C-LOOK with a return of one tick per cylinder. Under SSTF and FCFS no bound exists. The proofs are on the policy pages. With a positive service time, a stream of requests at the head cylinder can hold the arm under SCAN, LOOK and their circular forms as well.

## Reductions

- **TSP on a line.** The static batch is the shortest path that starts at $r$ and visits all points of $R$ on the real line: the [traveling salesman](/traveling-salesman-problem/) path problem in one dimension. The general problem is NP-hard, but on a line the formula for $M_{\min}$ solves it, and SSTF is the [nearest neighbor](/nearest-neighbor-tsp/) heuristic. With rotational positioning, in a model where each request ends at a fixed angle, the cost from one request to the next is fixed but not symmetric, so the static problem becomes a path version of the [asymmetric TSP](/asymmetric-tsp/).
- **Online TSP and dial-a-ride.** With arrivals over time, zero service time and the goal to finish all requests as early as possible, dynamic disk scheduling is the open [online traveling salesman problem](/online-traveling-salesman-problem/) on a line segment. A building elevator, which carries people between floors, is the [online dial-a-ride problem](/online-dial-a-ride-problem/). Those pages give the competitive ratios; the disk pages here study the waits of fixed policies instead.
- **Not the k-server problem.** In the [k-server problem](/k-server-problem/) each request must be served at once, in the given order, so one server has no choice to make. Disk scheduling keeps a queue and chooses the order, which is the whole point.

## Applications

- **Hard disk drivers and firmware.** The operating system sorts its queue by block address before it sends requests, and the drive reorders its own command queue with rotational information.
- **Batch I/O.** A program that reads many blocks of a file or of a database table can sort the block addresses first, which is the static optimum when it starts at an end.
- **Other one-dimensional servers.** Tape drives, optical drives and building elevators face the same geometry: one server on a line, and many places to visit.

## References

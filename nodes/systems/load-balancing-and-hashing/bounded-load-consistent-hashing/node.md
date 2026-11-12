---
tag: 5BJKG5
kind: algorithm
slug: bounded-load-consistent-hashing
name: Consistent hashing with bounded loads
aliases:
- bounded-load consistent hashing
area: systems/load-balancing-and-hashing
level: advanced
summary: Give every bin of a hash ring the capacity ceil((1 + eps) m / n), and put each ball in the first bin clockwise that is not full. No bin is ever over the cap.
solves: [dynamic-partitioning-problem]
model: word-ram
complexity:
  vars: {n: the number of bins, m: the number of balls}
  time: {worst: O(n)}
  space: {extra: Θ(n + m)}
properties: {online: true, deterministic: true, recursive: false}
history:
  year: 2016
  people: [Vahab Mirrokni, Mikkel Thorup, Morteza Zadimoghaddam]
  note: The arXiv version appeared in 2016 and the SODA paper in 2018. Google Cloud Pub/Sub and, through an HAProxy patch, Vimeo used the scheme before the conference version.
prereqs: [consistent-hashing, linear-probing]
see_also: [hash-ring, multi-probe-consistent-hashing, power-of-two-choices, consistent-hashing-max-load-bound, balance-property, linear-probing-analysis, load-skew, least-connections]
sources:
  - paper: doi:10.1137/1.9781611975031.39
    title: Vahab Mirrokni, Mikkel Thorup and Morteza Zadimoghaddam, Consistent hashing with bounded loads, Proceedings of the 29th ACM-SIAM Symposium on Discrete Algorithms (SODA), 2018, pages 587-604 (arXiv 1608.01350, 2016)
    locator: the abstract and the introduction (the capacity ceil((1 + eps) m / n), the first non-full bin clockwise, the expected moves per update within O(1/eps^2) of the lower bound), and the remarks on Google Cloud Pub/Sub and Vimeo
  - url: https://medium.com/vimeo-engineering-blog/improving-load-balancing-with-a-new-consistent-hashing-algorithm-9f1bd75709ed
    title: Andrew Rodland, Improving load balancing with a new consistent-hashing algorithm, Vimeo Engineering Blog, December 19, 2016
    locator: the HAProxy implementation for the video caches of Vimeo (the option hash-balance-factor with hash-type consistent)
  - paper: doi:10.1145/258533.258660
    title: David Karger, Eric Lehman, Tom Leighton, Rina Panigrahy, Matthew Levine and Daniel Lewin, Consistent hashing and random trees, Proceedings of the 29th ACM Symposium on Theory of Computing (STOC), 1997
    locator: the ring that the scheme starts from, and the balance and monotonicity properties
---

Consistent hashing with bounded loads adds a hard cap to the [hash ring](/hash-ring/). Each bin may hold at most $\lceil (1 + \varepsilon) m / n \rceil$ of the $m$ balls, where $n$ is the number of bins. A ball goes to the first bin clockwise from its hash that still has room. So no bin ever has more than $1 + \varepsilon$ times the mean load, whatever the hashes are, and a change of the bins or the balls still moves few balls: Mirrokni, Thorup and Zadimoghaddam proved that the expected number of moves per update is at most $O(1/\varepsilon^2)$ times the minimum. The price is that the assignment is no longer a pure function of the key: it depends on which other balls are present.

## In plain words

Each server has a seat limit, a little more than its fair share. A request starts at its usual place on the ring. If that server is full, the request walks clockwise to the next server, and the next, until one has a free seat.

Most requests find a seat at their first server, so they keep the cache benefit of consistent hashing. Only requests for a crowded part of the ring walk on, and they spill to the nearest neighbors. When a seat becomes free, a request that had to walk past that server moves back into it, so the spill always stays as short as possible.

## The problem

The input is a ring with $n$ bins and a changing set of $m$ balls, for example cache servers and the keys or the open connections they serve. The goals are those of the [dynamic partitioning problem](/dynamic-partitioning-problem/): clients agree on where a ball goes, and an update moves few balls. Here the balance goal is a hard bound. Every bin must have load at most $\lceil c\, m / n \rceil$ for a fixed $c = 1 + \varepsilon > 1$, also when a few keys are hot. A plain ring only has a bound with high probability, and with one point per bin the largest bin has about $\ln n$ times the mean load (see the [consistent hashing max-load bound](/consistent-hashing-max-load-bound/)).

## The algorithm

$\text{CAP} = \lceil c\, m / n \rceil$ is always computed from the current $m$ and $n$. A ball *passes* a bin when the bin is on its walk from its first bin to its own bin, and is not its own bin. A bin is *full* when its load is at least CAP.

```pseudo id=main
INSERT(x)
L1  m ← m + 1
L2  b ← the first bin at or after h(x) on the ring
L3  while load(b) ≥ CAP do
L4      b ← the next bin clockwise
L5  put x in b
L6  REPAIR()

DELETE(x)
L7  take x out of its bin, m ← m − 1
L8  REPAIR()

REPAIR()
L9   for each bin b in ring order do                                   ▷ shed
L10      while load(b) > CAP do
L11          move a ball of b to the first bin after b with load < CAP
L12  repeat                                                            ▷ fill
L13      moved ← false
L14      for each bin b in ring order do
L15          while load(b) < CAP and a ball x in the bins after b, up to the next bin with load < CAP, passes b do
L16              move x into b, moved ← true
L17  until not moved
```

The insertion of lines L2 to L5 is the rule of the paper. REPAIR keeps two invariants after every update: no bin is over CAP, and every bin that a ball passes is full. The shed phase is needed when CAP drops, after a deletion or when a bin is added. The fill phase is needed when a bin gets room: after a deletion, after a bin is added, or when CAP grows. To add a bin, insert its point and run REPAIR. To remove a bin, take its balls out, put each one into the first bin with room from its start, and run REPAIR.

In a load balancer such as HAProxy, the balls are open connections and each request is placed once by lines L2 to L5. A connection that ends frees a seat, and nothing is moved back: a new request simply finds the seat. The fill phase matters when the balls are stored items, for example keys of a cache, that must stay at their canonical place.

## Example

Take a ring of 100 positions with bins A at 20, B at 50 and C at 80, and $\varepsilon = 1/2$. Five balls hash to 10, 12, 15, 17 and 19, all in the arc of A. A plain ring puts all five in A.

| step | $m$ | CAP | what happens | A | B | C |
|---|---|---|---|---|---|---|
| insert p (10) | 1 | 1 | A has room | p | | |
| insert q (12) | 2 | 1 | A is full, walk to B | p | q | |
| insert r (15) | 3 | 2 | CAP grows, A has room | p r | q | |
| insert s (17) | 4 | 2 | A is full, walk to B | p r | q s | |
| insert t (19) | 5 | 3 | CAP grows, A has room | p r t | q s | |
| delete s | 4 | 2 | A is over CAP, shed p to B | r t | q p | |
| delete r | 3 | 2 | A has room and q, p pass it, pull p back | t p | q | |

The last two steps each move one ball that is not the one deleted. After each step the loads are at most CAP, and every ball in B passes only the full bin A.

**Random hashes.** With 50 bins and 2,000 balls hashed by BLAKE2b, a plain ring with one point per bin has a largest load of 176, which is 4.4 times the mean of 40, and two empty bins. With the cap, the largest load is exactly CAP. Then 400 random updates, half insertions and half deletions, give these counts of moved balls:

| $\varepsilon$ | CAP | mean walk of a ball | longest walk | moves per update | moves to add a bin | moves to remove a bin |
|---|---|---|---|---|---|---|
| 0.1 | 44 | 1.98 | 29 | 11.3 | 251 | 377 |
| 0.25 | 50 | 1.18 | 13 | 5.9 | 202 | 177 |
| 0.5 | 60 | 0.60 | 10 | 3.4 | 81 | 135 |
| 1 | 80 | 0.21 | 3 | 1.05 | 52 | 98 |
| 2 | 120 | 0.04 | 1 | 0.22 | 44 | 98 |

A walk of 0 means that the ball is at its plain-ring bin. The bins hold about 40 balls each, so a bin change must move at least about 40 balls. The counts of moves grow fast as $\varepsilon$ shrinks, which is the $1/\varepsilon^2$ factor of the theory.

## Correctness

The insertion stops, because $n \cdot \text{CAP} \ge c\, m > m - 1$, so some bin has room. The shed phase only moves a ball from a bin over CAP to a bin under it. The fill phase only moves a ball into a bin under CAP, and the move shortens that ball's walk, so the sum of all walk lengths drops and the phase stops. A sweep with no move means that no ball passes a bin with room: the last such bin on the walk of a ball would have found the ball. So after each update, no bin is over CAP and every bin that a ball passes is full. These two facts fix the loads: going round the ring from a bin with room, each load is $\min(\text{CAP}, r)$, where $r$ counts the balls that start at the bin plus the balls that pass the bin before it. So the loads do not depend on the order of the updates. The full proof is below.

## Complexity

- **Insertion walk.** At most $n$ bins, so $O(n)$ in the worst case. The walk is a linear probe with buckets of size CAP at a fill of $1/c$, which is short in practice: in the table above, the mean walk is under 2 bins even for $\varepsilon = 0.1$. See [linear probing](/linear-probing/) and its [analysis](/linear-probing-analysis/).
- **Moves.** For $\varepsilon \le 1$, the expected number of balls that move per update is $O(1/\varepsilon^2)$ times the lower bound. For larger $c$ the factor is $1 + O(\log c / c)$. Both bounds are from the paper and assume random hashes.
- **REPAIR in this form.** Each sweep looks at each bin and each ball a constant number of times, so it costs $O(n + m)$, and the loop runs until a sweep with no move. This form is simple to prove, not fast; a faster version keeps, for each bin, the balls that pass it.
- **Space.** $\Theta(n + m)$: the ring and the place of each ball. A pure ring needs only $\Theta(n)$.

## Properties

- **Hard balance.** Every load is at most $\lceil (1 + \varepsilon) m / n \rceil$ at all times, for every input, not only with high probability. Compare the [balance property](/balance-property/), which plain consistent hashing has only in expectation.
- **Not monotone in the strict sense.** Adding a bin can move a ball between two old bins, because CAP drops and a bin sheds. The [monotonicity property](/monotonicity-property/) fails, but the number of such moves is small.
- **Stateful.** The bin of a key depends on the other keys, so a client cannot compute it from the key alone. In a load balancer, one process holds the loads.
- **Order-independent loads.** The loads depend only on the hashes and CAP (Theorem 2 of the proof).

## Variants and improvements

- **Virtual bins.** Each bin can have several points on the ring, as with [virtual nodes](/virtual-nodes/). The cap then removes the high peaks, and the virtual nodes shorten the walks.
- **Weights.** A bin with weight $w$ gets the capacity $\lceil c\, w\, m / W \rceil$, where $W$ is the total weight.
- **Request-level use.** HAProxy's option `hash-balance-factor` with `hash-type consistent` sets $c$ as a percentage and counts active connections as the balls.
- **Other ways to cut the peak.** [Multi-probe consistent hashing](/multi-probe-consistent-hashing/) reduces the peak with no state but gives no hard cap. [The power of two choices](/power-of-two-choices/) uses the current loads of two random bins, but does not keep the locality of the ring.

## When to use it

Use bounded loads in a load balancer or a cache tier where a hot key must not overload one server, and the cache benefit of sending a key to the same server most of the time is still important. Vimeo used it to spread video segments over cache servers, and Google Cloud Pub/Sub to spread topics over servers. If clients must find a key with no shared state, use a pure function such as [rendezvous hashing](/rendezvous-hashing/) or a ring with virtual nodes instead.

## Pitfalls

- **A small $\varepsilon$.** With $\varepsilon = 0.1$ the walks and the moves are many times longer than with $\varepsilon = 1$. Choose $\varepsilon$ from the peak you can accept, and measure the moves.
- **A capacity from a stale $m$.** CAP depends on the current number of balls. If the count is old, the cap is too loose or too tight, and either balls overflow or many balls walk on.
- **Rounding.** Use the ceiling. With the floor, $n \cdot \text{CAP}$ can be less than $m$, and the walk of line L3 never finds room.
- **Expecting hot keys to be split.** One key is one ball. A cap on balls does not limit the traffic of one hot key; for that, see [load skew](/load-skew/).
- **A cascade on removal of a bin.** Its balls walk to the next bins, which may shed in turn. The moves stay bounded in expectation, but a burst of moves comes with each removal.

## Implementations

## History

Vahab Mirrokni, Mikkel Thorup and Morteza Zadimoghaddam posted the paper on arXiv in August 2016, and it appeared at SODA 2018. Before the conference version, Andrew Rodland added the rule to HAProxy for the video caches of Vimeo, and described it in the Vimeo Engineering Blog in December 2016. The paper names Google Cloud Pub/Sub as the first industrial use. The rule is an old idea from hashing, linear probing with buckets, applied to the ring of Karger et al. (1997).

## References

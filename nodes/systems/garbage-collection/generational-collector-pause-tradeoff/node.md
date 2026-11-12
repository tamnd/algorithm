---
tag: RPKRXJ
kind: concept
slug: generational-collector-pause-tradeoff
name: Pause-time versus throughput tradeoff
aliases:
- GC pause time tradeoff
- nursery size tradeoff
area: systems/garbage-collection
level: advanced
summary: "In a generational collector, a larger nursery or a later promotion means longer minor pauses but less work per allocation and fewer promoted objects."
prereqs: [generational-garbage-collection]
see_also: [generational-hypothesis, gc-space-time-tradeoff, stop-the-world-collection, incremental-garbage-collection, garbage-first-collector, generational-collector-beltway, remembered-set]
sources:
  - paper: doi:10.1145/62083.62085
    title: David Ungar and Frank Jackson, Tenuring policies for generation-based storage reclamation, OOPSLA 1988, 1-17
    locator: the cost of premature tenuring, and the policy that chooses the tenuring threshold from the survivor demographics to bound the pause
  - paper: doi:10.1002/spe.4380190206
    title: Andrew W. Appel, Simple generational garbage collection and fast allocation, Software Practice and Experience 19(2), 171-183, 1989
    locator: the nursery that takes all free space, so that minor collections are as rare as possible
  - paper: doi:10.1145/320384.320425
    title: Darko Stefanovic, Kathryn S. McKinley and J. Eliot B. Moss, Age-based garbage collection, OOPSLA 1999, 370-381
    locator: the comparison of youngest-first, oldest-first and older-first collection by the copying work they do
  - book: isbn:9781032218038
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, second edition, CRC Press, 2023
    locator: Chapter 9, Sections 9.6 (Age recording), 9.7 (Adapting to program behaviour) and 9.12 (Analytic support for generational collection)
---

## In plain words

A collector that stops the program to clean memory has to choose how often to stop. If it stops often and cleans a small area each time, each stop is short, but the many stops add up to more total work. If it stops rarely and cleans a large area, the total work is smaller, but each stop is long and the program can freeze for a moment.

In a generational collector this choice is the size of the area for new objects. A bigger area gives new objects more time to die before the collector looks at them, so fewer survive and less work is done in total. But each look takes longer. Keeping survivors in the new area for a few extra rounds before moving them to the old area has a similar effect.

## The idea

Any collector that stops the mutator trades three things: the length of each pause, the total collection work per unit of allocation (which sets the throughput), and the memory it needs. For a single stop-the-world collector of a heap of size $H$ with $L$ live data, each collection costs about the work to process $L$, and it runs after $H - L$ allocated words, so the work per allocated word is about $L/(H - L)$. A larger heap gives fewer collections, less total work, and the same pause. A generational collector splits this tradeoff into a part for the nursery, which this page models exactly, and a part for the old generation.

**The model.** The mutator allocates one object per time unit. Lifetimes are independent with survival function $S(a) = \Pr[\text{lifetime} > a]$, which is nonincreasing in $a$. A minor collection runs after every $N$ allocations. A young object that survives $T$ minor collections is promoted at the $T$-th one; until then it is copied within the young generation. Let

$$P(n) = \sum_{a=0}^{n-1} S(a),$$

the expected number of the last $n$ allocated objects that are still alive.

**Pause work.** At a collection in the steady state, the young objects that are alive are those born in the last $T$ windows of $N$ allocations. An object born in the $k$-th window back is at an age between $(k-1)N$ and $kN - 1$. So the expected number of objects copied or promoted is

$$C(N, T) = \sum_{k=1}^{T} \sum_{a=(k-1)N}^{kN-1} S(a) = P(TN).$$

The pause is $c_0 + c_r R + c\, P(TN)$, with a fixed cost $c_0$, a cost $c_r$ per root and remembered slot ($R$ of them) and a cost $c$ per copied object.

**Promotion.** The objects promoted at a collection are those of the oldest window that are still alive:

$$\text{promoted per collection} = P(TN) - P((T-1)N), \qquad \text{promotion rate} = \frac{P(TN) - P((T-1)N)}{N}$$

per allocated object. Promoted objects fill the old generation and so set how often a major collection runs.

**Throughput.** The minor collection work per allocated object is $(c_0 + c_r R + c\, P(TN))/N$.

**Claim.** For $T = 1$, the pause $P(N)$ is nondecreasing in $N$, and the work per allocation $P(N)/N$ and the promotion rate $P(N)/N$ are nonincreasing in $N$.

*Proof.* $P(N+1) - P(N) = S(N) \ge 0$. For the ratio, $P(N+1)/(N+1) \le P(N)/N$ is the same as $N\, S(N) \le P(N) = \sum_{a<N} S(a)$, which holds because $S(a) \ge S(N)$ for each $a < N$. $\blacksquare$

So the nursery size moves the pause and the throughput in opposite directions, and how far depends on the shape of $S$. When the [weak generational hypothesis](/generational-hypothesis/) holds strongly, $P$ flattens fast and a large nursery is cheap per allocation. Under constant mortality, with $S(a) = q^a$, $P(N) = (1 - q^N)/(1 - q)$, and once $N$ is large compared with the mean lifetime, every bigger nursery only lengthens the pause less and less while the work per allocation still falls as $1/N$.

**Premature tenuring.** An object promoted shortly before it dies costs a copy into the old generation and old-generation space until the next major collection. A small $N$ or a small $T$ promotes many such objects. Raising $T$ lowers the promotion rate, but each survivor is copied up to $T$ times, and the pause grows from $P(N)$ to $P(TN)$.

**Nepotism.** The model assumes the collector keeps only live objects. In a real collector, a promoted object that died keeps alive the young objects it points to, through the [remembered set](/remembered-set/), until a major collection. Those objects are promoted in turn and can keep others alive. Nepotism makes premature tenuring more costly than the model shows.

## Examples

Use the lifetime mixture of the [generational hypothesis](/generational-hypothesis/) page: 90% of objects have a geometric lifetime of mean 10 and 10% of mean 10000, so $P(n) = 9\,(1 - 0.9^n) + 1000\,(1 - 0.9999^n)$. Take $c_0 = c_r = 0$ and $c = 1$, so the pause is the number of objects copied.

| nursery $N$ | threshold $T$ | pause $P(TN)$ | work per allocation | promotion rate | short-lived objects promoted per allocation |
|---|---|---|---|---|---|
| 100 | 1 | 18.95 | 0.1895 | 0.1895 | 0.0900 |
| 1000 | 1 | 104.17 | 0.1042 | 0.1042 | 0.0090 |
| 10000 | 1 | 641.14 | 0.0641 | 0.0641 | 0.0009 |
| 500 | 2 | 104.17 | 0.2083 | 0.0928 | about 0 |
| 1000 | 2 | 190.28 | 0.1903 | 0.0861 | about 0 |

The first three rows show the claim: each tenfold increase of the nursery makes the pause longer and the work per allocation smaller. With $N = 100$, almost half of the promoted objects come from the short-lived group: they are promoted at an age below 100 and die within a few more allocations. This is premature tenuring. The rows for $N = 500, T = 2$ and $N = 1000, T = 1$ have the same pause, but the first collects twice as often: it does twice the work per allocation, and promotes 11% fewer objects. Aging buys a lower promotion rate with more copying.

A memoryless program shows the other extreme. If every lifetime is geometric with mean 10000, then $P(1000) = 951.7$, and 95% of each nursery survives: a larger nursery lowers the work per allocation, but the generations give no gain over a full collection of a heap of the same size.

The implementation checks the formulas for $C(N, T)$ and the promotion count against an exact expectation over all lifetime vectors of a finite distribution, with rational arithmetic, against a seeded simulation, and checks the claim on random nonincreasing survival functions.

## Where it is used

- **Choosing the nursery size.** Appel's collector gives the nursery all the free space, which minimizes the work per allocation and accepts long minor pauses. Interactive systems use a small fixed nursery. Some virtual machines size the young generation from a pause-time goal: Garbage-First, for example, picks the number of young regions so that the predicted pause stays below a target.
- **Choosing the tenuring threshold.** Ungar and Jackson set the threshold at each collection from the ages of the survivors, so that the expected next pause stays within a limit. HotSpot adjusts its threshold from the occupancy of the survivor space.
- **Collecting the old generation.** Fewer promotions mean fewer major collections, which are the long pauses. Incremental schemes such as the [train algorithm](/train-algorithm/), [Beltway](/generational-collector-beltway/) and [incremental](/incremental-garbage-collection/) or concurrent collectors cut the major pause into pieces, at a cost in barriers and total work.
- **Age-based collectors.** Stefanovic, McKinley and Moss compared collecting the youngest objects first with collecting older objects first. When lifetimes are close to memoryless, older-first copies less, because the youngest objects have not had time to die.

## References

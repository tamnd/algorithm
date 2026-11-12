---
tag: 4J3Z1T
kind: theorem
slug: gc-space-time-tradeoff
name: Garbage collection space-time tradeoff
aliases:
- Appel heap size tradeoff
- heap size versus collection cost
area: systems/garbage-collection
level: research
summary: "With L live words and memory H, a copying collector costs c L / (H/2 - L) per allocated word and mark-sweep (m L + s H) / (H - L). More memory means less collection work."
prereqs: [copying-collection, mark-and-sweep]
see_also: [mark-compact, cheney-copying-collector, generational-garbage-collection, generational-hypothesis, lazy-sweeping, stop-the-world-collection, tracing-garbage-collection, bump-pointer-allocation]
sources:
  - paper: doi:10.1016/0020-0190(87)90175-X
    title: Andrew W. Appel, Garbage collection can be faster than stack allocation, Information Processing Letters 25(4), 275-279, 1987
    locator: the cost of a copying collection per allocated word, which falls towards zero as the memory grows relative to the live data
  - paper: doi:10.1145/1094811.1094836
    title: Matthew Hertz and Emery D. Berger, Quantifying the performance of garbage collection vs. explicit memory management, Proceedings of OOPSLA 2005, 313-326
    locator: the results on heap size; with five times the memory the best collector matches explicit management, with three times it is about 17% slower, with twice about 70% slower
  - book: isbn:9781420082791
    title: Richard Jones, Antony Hosking and Eliot Moss, The Garbage Collection Handbook, The Art of Automatic Memory Management, first edition, CRC Press, 2011
    locator: Chapter 6, Sections 6.1 (throughput) and 6.3 (space), and Section 11.11 (choosing the heap size)
  - book: isbn:9780471941484
    title: Richard Jones and Rafael Lins, Garbage Collection, Algorithms for Automatic Dynamic Memory Management, Wiley, 1996
    locator: Chapter 6, the cost of copying collection compared with mark-sweep
---

A tracing garbage collector does work in proportion to what it traces, and it runs once each time the free memory is used up. So the more memory it has beyond the live data, the less often it runs, and the less work it does for each word the program allocates. For a copying collector with $L$ live words and $H$ words of memory, the cost per allocated word is exactly $cL/(H/2 - L)$, which falls towards zero as $H$ grows. For mark-sweep it is $(mL + sH)/(H - L)$, which falls towards the cost $s$ of sweeping one word. Appel (1987) used the first formula to argue that, with enough memory, garbage collection is cheaper than freeing memory by hand.

## Statement

**Model.** A program allocates memory, and a collector reclaims it when the free memory is used up.

- At each collection, exactly $L$ words of the heap are live.
- A collection reclaims every word that is not live, and the reclaimed words can all be allocated again (no fragmentation; for example, all objects have the same size).
- A [copying collector](/copying-collection/) with $H$ words of memory uses two semispaces of $H/2$ words. A collection copies the live words to the other semispace at a cost $c$ for each live word, and never touches the garbage.
- A [mark-sweep collector](/mark-and-sweep/) with $H$ words of memory marks the live words at a cost $m$ for each, and sweeps all $H$ words at a cost $s$ for each.

The *amortized collection cost* is the total cost of the collections divided by the total number of words allocated, over any whole number of cycles from one collection to the next.

**Theorem.**

1. If $H > 2L$, a copying collector has the amortized cost
$$C_{\mathrm{copy}}(H) = \frac{cL}{H/2 - L}.$$
2. If $H > L$, a mark-sweep collector has the amortized cost
$$C_{\mathrm{ms}}(H) = \frac{mL + sH}{H - L} = s + \frac{(m + s)L}{H - L}.$$
3. Both costs strictly decrease as $H$ grows. As $H \to \infty$, $C_{\mathrm{copy}} \to 0$ and $C_{\mathrm{ms}} \to s$.
4. With the heap ratio $k = H/L$, the costs are $C_{\mathrm{copy}} = 2c/(k - 2)$ and $C_{\mathrm{ms}} = (m + sk)/(k - 1)$, which depend only on $k$.

## In plain words

A collector has to clean up each time the free space runs out. If you give it twice as much spare room, it runs half as often.

A copying collector only touches the live data, so the cost of one run is fixed. Spread over more allocations, the cost of each allocation goes down, and with very much memory it is close to zero.

A mark-sweep collector also walks over the whole heap in its sweep. That part grows with the heap, so it never goes away: each allocated word costs at least the sweep of about one word.

## Proof

Consider one cycle: a collection, then the allocations until the next collection, then that collection. The amortized cost over any number of whole cycles is the cost of one collection divided by the words allocated in one cycle, if both are the same for every cycle. We show that they are.

*Copying.* A collection copies exactly the $L$ live words into the empty semispace, which has $H/2$ words; this fits because $L < H/2$. It costs $cL$, because each live word is copied once and the garbage is not touched. After it, to-space holds the $L$ copies and $H/2 - L$ free words, which the program allocates one after another until to-space is full. So the cycle allocates $H/2 - L$ words, and the next collection again finds $L$ live words and costs $cL$. Dividing gives
$$C_{\mathrm{copy}} = \frac{cL}{H/2 - L}.$$

*Mark-sweep.* A collection marks the $L$ live words, at a cost $mL$, and sweeps all $H$ words, at a cost $sH$. Every word that is not live is returned to the free list, and all of them can be allocated again, so the free space is $H - L > 0$ words. The program allocates exactly these words before the next collection. Dividing gives
$$C_{\mathrm{ms}} = \frac{mL + sH}{H - L} = \frac{s(H - L) + (m + s)L}{H - L} = s + \frac{(m + s)L}{H - L}.$$

*Monotonicity and limits.* In $C_{\mathrm{copy}}$ the numerator $cL$ is fixed and the denominator $H/2 - L$ grows with $H$, so the cost strictly decreases (for $L > 0$) and tends to $0$. In the second form of $C_{\mathrm{ms}}$, the term $(m + s)L/(H - L)$ strictly decreases (for $L > 0$) and tends to $0$, so $C_{\mathrm{ms}}$ strictly decreases and tends to $s$.

*Ratio form.* Put $H = kL$. Then $C_{\mathrm{copy}} = cL/(kL/2 - L) = 2c/(k - 2)$ and $C_{\mathrm{ms}} = (mL + skL)/(kL - L) = (m + sk)/(k - 1)$. $\blacksquare$

**A check by simulation.** The implementation runs a real semispace collector and a real mark-sweep collector on a heap of one-word objects, where the program holds the $L$ most recently allocated objects. It counts the costs exactly with fractions. Over 600 random choices of $H$, $L$, $c$, $m$, $s$ and the number of cycles, the measured cost equals the formula exactly. For example, with $L = 10$ and unit costs:

| $H$ | $k = H/L$ | copying | mark-sweep |
|---|---|---|---|
| 40 | 4 | $1$ | $5/3$ |
| 80 | 8 | $1/3$ | $9/7$ |
| 160 | 16 | $1/7$ | $17/15$ |

Each doubling of the memory roughly halves the copying cost (exactly, it goes from $2c/(k-2)$ to $2c/(2k-2)$), while mark-sweep approaches its floor $s = 1$.

## Consequences

- **Memory buys time.** Doubling $H$ cuts the collection cost of a copying collector to less than half when $H > 2L$; the cost of a collector is not a fixed number but a function of the heap ratio $k$. Any comparison of collectors must fix $k$.
- **Garbage collection can be cheaper than freeing by hand.** Freeing each object explicitly costs at least a constant for each object. The copying cost per word tends to $0$, so with enough memory it falls below that constant. This is the argument of Appel (1987), who compared it with popping a stack frame.
- **The sweep floor.** Mark-sweep never costs less than $s$ for each allocated word, because the sweep visits the whole heap. [Lazy sweeping](/lazy-sweeping/) does not remove this cost but moves it into allocation, and a bitmap or a block summary makes $s$ small. [Mark-compact](/mark-compact/) collectors have a similar term in $H$.
- **Generational collection.** In a nursery, $L$ is the small amount of data that survives, so $k$ is large and a copying collection is cheap; this is why most young generations are copied ([generational hypothesis](/generational-hypothesis/)).
- **Measurements.** Hertz and Berger (2005) compared collectors with an oracle that frees each object at its last use. With five times as much memory as explicit freeing needed, the best collector matched its speed; with three times as much it was about 17% slower, and with twice as much about 70% slower. This is the shape that the theorem predicts.
- **Heap sizing.** Runtimes choose $H$ as a multiple of the live data after each collection, to keep $k$, and so the collection cost, roughly constant.

## Tightness

- **The formulas are exact in the model.** They are equalities, not bounds, and the simulator meets them with no error.
- **The thresholds are sharp.** As $H \to 2L$ from above, $C_{\mathrm{copy}} \to \infty$: each collection frees almost nothing. A copying collector cannot run at all with $H \le 2L$, and mark-sweep cannot run with $H \le L$.
- **Which collector is cheaper depends on $k$.** Copying is cheaper than mark-sweep for large $k$, because its cost tends to $0$ and that of mark-sweep to $s > 0$. Near $k = 2$, copying is far more costly, and mark-sweep wins.
- **Where the model breaks.** The live size changes over time. Fragmentation makes some free words of a non-moving collector unusable, so the true denominator of $C_{\mathrm{ms}}$ is smaller than $H - L$. The costs $c$, $m$ and $s$ are not constant, because of caches. And when $H$ exceeds the physical memory, paging makes a larger heap slower, not faster, as Hertz and Berger measured.

## History

Appel (1987) stated the copying cost per allocated word and the conclusion that, with enough memory, collection is cheaper than stack allocation. Textbook treatments of the costs of copying and mark-sweep collection, as in Jones and Lins (1996) and the Garbage Collection Handbook (2011), use the same reasoning. Hertz and Berger (2005) measured the tradeoff on Java programs against an oracle for explicit freeing.

## References

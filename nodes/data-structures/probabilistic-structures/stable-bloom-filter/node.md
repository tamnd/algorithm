---
tag: XYQ2CR
kind: data-structure
slug: stable-bloom-filter
name: Stable Bloom filter
area: data-structures/probabilistic-structures
level: research
summary: Bloom variant for unbounded streams that randomly decrements counters to keep a stable false positive rate.
model: word-ram
complexity:
  vars: {m: the number of cells, d: the bits per cell, K: the number of hash functions, P: the number of cells decremented per element}
  time: {worst: Θ(K + P)}
  space: {extra: Θ(m d)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [counting-bloom-filter, streaming-model, geometric-distribution]
see_also: [bloom-filter, scalable-bloom-filter, false-positive-rate, approximate-membership, spectral-bloom-filter, one-sided-error]
sources:
  - paper: doi:10.1145/1142473.1142477
    title: Fan Deng and Davood Rafiei, Approximately detecting duplicates for streaming data using stable Bloom filters, Proceedings of the 2006 ACM SIGMOD International Conference on Management of Data
    locator: pages 25 to 36 (the cells with values up to Max, the P random decrements, the stable fraction of zero cells, and the false positive and false negative rates)
  - paper: doi:10.1080/15427951.2004.10129096
    title: Andrei Broder and Michael Mitzenmacher, Network applications of Bloom filters, a survey, Internet Mathematics 1(4), 2004
    locator: pages 485 to 509, Section 2 (the Bloom filter and its false positive rate, which a full Bloom filter loses on a long stream)
---

A stable Bloom filter detects duplicates in an unbounded stream with a fixed amount of memory. It is an array of $m$ cells of $d$ bits, with largest value $\mathrm{Max} = 2^d - 1$, and $K$ hash functions. For each arriving element $x$, it first reports $x$ as a duplicate if all $K$ cells of $x$ are nonzero. Then it subtracts 1 from $P$ randomly chosen cells, and sets the $K$ cells of $x$ to Max. Old elements fade out of the array, so it never fills up: the fraction of zero cells tends to the constant $\big(1/(1 + 1/(P(1/K - 1/m)))\big)^{\mathrm{Max}}$, and the rate of false duplicates stays at a stable level however long the stream is. The price is false negatives: a duplicate whose earlier copy is too old may be reported as new. Deng and Rafiei introduced it in 2006.

## In plain words

A Bloom filter that watches an endless stream fills up: after a while every switch is on, and every new item looks like one it has seen. To stay useful, the filter must forget.

A stable Bloom filter gives each place a small counter in its place of a switch. When an item arrives, the filter first checks if all its counters are above zero, which means "seen recently". Then it lowers a few counters, chosen at random, by one, and sets the item's own counters to the top value.

An item seen a short time ago still has high counters and is found. An item seen long ago has had its counters worn down to zero and is forgotten. Wearing down and setting up balance out, so the share of zero counters settles at a fixed level.

## The abstract type

The filter serves the duplicate detection problem in the [streaming model](/streaming-model/): for a stream $x_1, x_2, \ldots$, report at each time $t$ whether $x_t$ equals an earlier element. With bounded memory this cannot be exact, and the filter answers with two kinds of error. A *false positive* reports a new element as a duplicate. A *false negative* reports a duplicate as new, which happens more often the longer ago its last copy came. Unlike a [Bloom filter](/bloom-filter/), the error is not [one-sided](/one-sided-error/), but its rates do not grow with the length of the stream.

## Representation

The filter is an array $C[0 \ldots m-1]$ of cells with values in $\{0, \ldots, \mathrm{Max}\}$, $K$ [hash functions](/hash-function/) that give each element a set $H(x)$ of $K$ distinct cells, and a source of random numbers for the decrements. The parameters are $m$, $d$ (so $\mathrm{Max} = 2^d - 1$), $K$ and $P$.

**Invariant (D).** For each cell $j$, let $t_j$ be the last time at which an element with $j \in H(x)$ arrived. Then $C[j] = \max(0, \mathrm{Max} - D_j)$, where $D_j$ is the number of later steps that chose $j$ among their $P$ decremented cells; and $C[j] = 0$ if no such element has arrived.

So a cell remembers only the last element that set it, and loses that memory after Max decrements.

## Operations

```pseudo id=main
CREATE(m, K, d, P)
L1  C ← an array of m cells of d bits, all 0;  Max ← 2^d − 1

PROCESS(C, x)
L2  dup ← (C[j] > 0 for every j in H(x))
L3  choose P distinct cells uniformly at random, and subtract 1 from each of them that is above 0
L4  for each j in H(x) do C[j] ← Max
L5  return dup
```

**Order of the steps.** The check comes first, so that $x$ is compared with the earlier elements only. The decrements come before the sets, so that the cells of $x$ end the step at Max and $x$ is found if it arrives again at once.

**The decrements.** Deng and Rafiei choose a random start and decrement $P$ cells in a row, which needs only one random number. This page and the Python code choose $P$ distinct cells at random, which is the model of the analysis.

**Why it is stable.** Each step sets $K$ cells to Max and removes $P$ units of value from the array at random. If the array is nearly full, the decrements hit many nonzero cells; if it is nearly empty, many decrements hit zeros and are lost. This feedback makes the fraction of zero cells converge, as the theorem below states.

## Example

Let $m = 8$, $K = 2$, $d = 2$ so $\mathrm{Max} = 3$, and $P = 2$. The cells of the elements and the decremented cells of the eight steps are given, with the stream a, b, a, c, d, e, f, c.

| step | element | $H$ | dup? | decremented | $C[0 \ldots 7]$ after |
|---|---|---|---|---|---|
| 1 | a | 0, 3 | no | 2, 7 | 3 0 0 3 0 0 0 0 |
| 2 | b | 1, 5 | no | 0, 4 | 2 3 0 3 0 3 0 0 |
| 3 | a | 0, 3 | yes | 3, 5 | 3 3 0 3 0 2 0 0 |
| 4 | c | 3, 6 | no | 0, 1 | 2 2 0 3 0 2 3 0 |
| 5 | d | 0, 5 | yes | 6, 3 | 3 2 0 2 0 3 2 0 |
| 6 | e | 2, 4 | no | 6, 7 | 3 2 3 2 3 3 1 0 |
| 7 | f | 2, 7 | no | 6, 1 | 3 1 3 2 3 3 0 3 |
| 8 | c | 3, 6 | no | 5, 0 | 2 1 3 3 3 2 3 3 |

Step 3 finds the duplicate a, with cells 0 and 3. Step 5 reports d as a duplicate although it is new: cells 0 and 5 were set by a and b, a false positive. Steps 5, 6 and 7 each decrement cell 6, which c set to 3 at step 4, so at step 8 cell 6 is 0 and the second c is reported as new, a false negative.

## Correctness

Invariant (D) holds by induction over the steps, since line L3 lowers a cell by 1 with a floor at 0 and line L4 resets it to Max. So an element is reported as a duplicate exactly when each of its cells was set at some earlier step and has had fewer than Max decrements since the last time it was set. In particular, if $x$ arrives at two consecutive steps, the second is always found, and more generally a duplicate is found whenever none of its cells had Max decrements since its last copy. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time |
|---|---|
| process | $K$ hash evaluations, $K$ reads and writes, and $P$ random decrements, $\Theta(K + P)$ |
| space | $m d$ bits |

**The stable fraction of zeros.** Assume that each step's set $H(x_t)$ is a uniform random $K$-subset, independent of the past, as it is for a stream of new elements under ideal hashing. Then for each cell
$$ \lim_{t \to \infty} \Pr[C_t[j] = 0] = \left(\frac{1}{1 + \frac{1}{P(1/K - 1/m)}}\right)^{\mathrm{Max}}. $$
The proof is in [the complexity proof](proofs/complexity.md). It looks back from time $t$ at the steps that set cell $j$ or only decrement it, and these form a sequence of independent trials with a [geometric](/geometric-distribution/) wait for the first set.

**The stable false positive rate.** A new element is a false positive when all $K$ of its cells are nonzero. If the cells were independent, this would be $(1 - z)^K$, where $z$ is the stable zero fraction above; Deng and Rafiei use this as the stable rate. For $m = 2000$, $K = 3$, $d = 3$ and $P = 50$ the limit is $z = 0.664$, so $(1 - z)^3 = 0.038$. In a simulation of the Python code, after 20000 new elements the fraction of zero cells was 0.666, and 3.7 percent of 20000 further new elements were false positives.

**False negatives.** A cell is decremented with probability $P/m$ at each step, so it loses its value after about $\mathrm{Max} \cdot m/P$ steps if no other element sets it again. With the parameters above this is $7 \cdot 40 = 280$ steps. In the same simulation, a duplicate whose last copy came 100 steps before was missed 3 percent of the time, at 200 steps 44 percent, and at 500 steps 97 percent. So the filter remembers a window of recent elements whose length is set by $\mathrm{Max}\, m / P$.

## Variants

- **Consecutive decrements.** The original decrements $P$ consecutive cells from a random start, which is faster and has about the same behaviour.
- **One-bit cells.** With $d = 1$ the cells are bits, and the filter is a Bloom filter whose bits are cleared at random.
- **Sliding-window filters.** Exact windows of the last $W$ elements can be kept with timestamps in the cells, or with a sequence of Bloom filters that are dropped in turn, at a larger cost in space. The stable filter has no exact window, only a decay.
- **Growing instead of forgetting.** A [scalable Bloom filter](/scalable-bloom-filter/) keeps every element and grows its memory. It has no false negatives but needs space that grows with the number of distinct elements.

## When to use it

Use a stable Bloom filter to remove most duplicates from an unbounded stream with fixed memory, when recent duplicates matter most and some missed duplicates are acceptable: for example, click streams in which repeated clicks within a short time are discounted, or crawlers that should not fetch the same URL again soon. When every duplicate must be found, use an exact set, or a [Bloom filter](/bloom-filter/) sized for the whole stream.

## Pitfalls

- **Reading the false positive formula as exact.** The cells of one element are not independent, and the formula $(1 - z)^K$ is an approximation, close for large $m$.
- **Too few decrements.** With small $P$ the array stays nearly full, and almost every element is a false positive. The stable zero fraction must be well above 0.
- **Too many decrements.** With large $P$, even recent duplicates are missed. The window length $\mathrm{Max}\, m / P$ should match how far back duplicates must be found.
- **Repeated elements in the analysis.** The stable fraction is derived for a stream of new elements. Many repeats set the same cells again and leave more zeros elsewhere, which only lowers the false positive rate.
- **Using it as a membership filter.** It has false negatives, so it cannot replace a Bloom filter where every stored key must be found.

## Implementations

The Python class follows the main block with BLAKE2b for $K$ distinct cells, a seeded random generator for the $P$ decremented cells, and the stable zero fraction as a method.

## History

Deng and Rafiei (2006) introduced the stable Bloom filter for approximate duplicate detection in data streams. They proved that the fraction of zero cells converges to a constant, gave the stable false positive rate and bounds on the false negative rate, and showed how to choose $P$ from $m$, $K$, Max and a target rate. They compared it with Bloom filters over sliding windows.

## References

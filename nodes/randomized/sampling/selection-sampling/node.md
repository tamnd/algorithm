---
tag: 2YMG5Q
kind: algorithm
slug: selection-sampling
name: Selection sampling (Knuth's Algorithm S)
aliases:
- Knuth's Algorithm S
- sequential sampling
- selection sampling technique
area: randomized/sampling
level: intro
summary: One scan over N items that selects each item with probability (number still needed)/(number of items left), giving a uniform n-subset in input order.
solves: [uniform-random-subset]
model: word-ram
complexity:
  vars: {N: the number of items, n: the sample size}
  time: {worst: Θ(N), expected: Θ(N)}
  space: {extra: O(1)}
properties: {online: true, deterministic: false, recursive: false}
history:
  year: 1962
  people: [C. T. Fan, Mervin E. Muller, Ivan Rezucha]
  note: Fan, Muller and Rezucha described sequential item by item selection for sampling with computers in the Journal of the American Statistical Association in 1962; Knuth presents it as Algorithm S.
prereqs: [uniform-distribution, binomial-coefficient]
see_also: [reservoir-sampling, floyd-sampling, uniform-random-subset, fisher-yates-shuffle, bernoulli-sampling, vitter-reservoir-skip]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.4.2, Algorithm S (selection sampling technique) and the analysis of the number of records looked at
  - paper: doi:10.1080/01621459.1962.10480667
    title: C. T. Fan, Mervin E. Muller and Ivan Rezucha, Development of sampling plans by using sequential (item by item) selection techniques and digital computers, Journal of the American Statistical Association 57(298), 387 to 402, 1962
    locator: the sequential selection method with probability (n - m)/(N - t)
---

Selection sampling, Knuth's Algorithm S, picks a uniform random $n$-subset of $N$ items in one scan, when $N$ is known in advance. It looks at the items in order and selects the next item with probability
$$\frac{\text{number of items still needed}}{\text{number of items not yet seen}} = \frac{n - m}{N - t},$$
where $m$ items are already selected and $t$ items already seen. It stops as soon as it has $n$ items. The sample comes out in input order, it has exactly $n$ items, and each $n$-subset has probability $1/\binom{N}{n}$. It uses $O(1)$ extra space and one random number per item looked at. The method is from C. T. Fan, Mervin Muller and Ivan Rezucha (1962). When $N$ is not known, use [reservoir sampling](/reservoir-sampling/) instead.

## In plain words

You must pick 3 names from a list of 8, fairly, reading the list once from the top. At each name, ask: how many names do I still need, and how many names are left, this one included? Take this name with that chance.

At the first name you need 3 of 8, so you take it with chance 3 in 8. If you skip it, the next has chance 3 in 7. If you take one, the chance drops. The rule fixes itself: if you have skipped too many, the chance rises, and when the names left are exactly the names you need, the chance is 1 and you take all of them. When you have enough, the chance is 0 and you stop. Every group of 3 names comes out equally often.

## The problem

The input is a sequence of $N$ items and a sample size $n$ with $0 \le n \le N$. The output is a uniform random $n$-subset of the positions, listed in input order. This is the [uniform random subset](/uniform-random-subset/) problem, in the form where the items come as a sequence of known length, for example records in a file, and the sample must keep their order.

## The algorithm

```pseudo id=main
SELECTION-SAMPLE(x[1..N], n)               ▷ 0 ≤ n ≤ N
L1  m ← 0; t ← 0; S ← an empty list         ▷ m selected, t seen
L2  while m < n
L3      if a uniform random integer in {0, ..., N − t − 1} is less than n − m
L4          append x[t + 1] to S; m ← m + 1
L5      t ← t + 1
L6  return S
```

Line L3 is an event of probability $(n - m)/(N - t)$. Knuth writes it with a uniform real $U$ as "if $(N - t)U \ge n - m$, skip", which is the same event. The integer form is exact.

## Example

Take $N = 8$ items $a, \ldots, h$ and $n = 3$.

| $t$ | item | still needed $n - m$ | left $N - t$ | integer drawn | selected? | $S$ |
|---|---|---|---|---|---|---|
| 0 | $a$ | 3 | 8 | 5 | no | |
| 1 | $b$ | 3 | 7 | 2 | yes | $b$ |
| 2 | $c$ | 2 | 6 | 1 | yes | $b, c$ |
| 3 | $d$ | 1 | 5 | 4 | no | $b, c$ |
| 4 | $e$ | 1 | 4 | 2 | no | $b, c$ |
| 5 | $f$ | 1 | 3 | 0 | yes | $b, c, f$ |

Now $m = 3$ and the loop stops. Items $g$ and $h$ are never looked at. The sample is $\{b, c, f\}$, after 6 random integers. On average the scan looks at $3 \cdot 9/4 = 6.75$ items here.

## Correctness

**Theorem (Fan, Muller and Rezucha 1962; Knuth, Algorithm S).** SELECTION-SAMPLE stops, returns exactly $n$ items in input order, and returns each $n$-subset with probability $1/\binom{N}{n}$.

The invariant $0 \le n - m \le N - t$ shows that the method never needs more items than remain, and that it is forced to take all remaining items when $n - m = N - t$. For uniformity, fix a subset $A$ whose largest position is $L$. The probability of the exact run of decisions that gives $A$ is a product of $L$ fractions. The denominators are $N, N - 1, \ldots, N - L + 1$. The numerators of the selections are $n, n - 1, \ldots, 1$, and those of the skips are $N - n, N - n - 1, \ldots$, one for each position not in $A$ that is passed. The product is $n!\,(N-n)!/N!$, the same for every $A$. The full proof is below.

## Complexity

- **Time.** One random integer and $O(1)$ work per item looked at. The scan ends at the last selected item, whose position $L$ is the maximum of a uniform $n$-subset, so for $n \ge 1$
$$E[L] = \frac{n(N + 1)}{n + 1}.$$
In the worst case $L = N$, so the time is $\Theta(N)$. The expected time is also $\Theta(N)$ for every fixed $n \ge 1$, because $E[L] \ge (N + 1)/2$.
- **Random numbers.** Exactly $L$, at most $N$.
- **Space.** $O(1)$ besides the output. Nothing is stored about skipped items.

## Properties

- **Output in input order.** The sample is sorted by position, with no extra work. [Floyd's algorithm](/floyd-sampling/) and a partial [Fisher-Yates shuffle](/fisher-yates-shuffle/) give the subset in a random order, and need a sort to give it in order.
- **Exact size.** Unlike [Bernoulli sampling](/bernoulli-sampling/), which takes each item with a fixed probability, the size is exactly $n$.
- **Each decision is final.** An item is selected or skipped when it is seen, and is never revisited. This suits tape, files and streams of known length.
- **Exact.** With integer draws there is no rounding.

## Variants and improvements

- **Reservoir sampling.** When $N$ is not known, [Algorithm R](/reservoir-sampling/) keeps a reservoir of $n$ items and may replace them later. It gives the same law, but not in one decision per item.
- **Skips.** Instead of one decision per item, one can draw the number of items skipped before the next selection, which has a known law. This takes the cost from $\Theta(N)$ to about $O(n)$ when skipping is cheap. Vitter (1984) gave such methods for this setting, and [Vitter's reservoir methods](/vitter-reservoir-skip/) apply the same idea when $N$ is unknown.
- **Small n, huge N.** If $n$ is much smaller than $N$ and random access is cheap, [Floyd's algorithm](/floyd-sampling/) uses $n$ random numbers and $O(n)$ space.

## When to use it

Use selection sampling when $N$ is known, the items come in order, and the sample must keep that order, for example to pick $n$ records from a sorted file or rows from a table in a single pass. It is the simplest exact method and needs no memory beyond the output. If $N$ is not known, use [reservoir sampling](/reservoir-sampling/). If $n$ is tiny and the items can be reached by index, [Floyd's algorithm](/floyd-sampling/) avoids the scan.

## Pitfalls

- **A fixed probability $n/N$.** Taking each item with probability $n/N$ is Bernoulli sampling: the size is random, not $n$.
- **Wrong counts.** The denominator is the number of items not yet seen, *including* the current one: $N - t$, not $N - t - 1$. With $N - t - 1$ the last item would be taken with probability $(n - m)/0$.
- **Floating-point rounding.** With real $U$, $\lfloor (N - t) U \rfloor$ can round to $N - t$ for large $N$ if $U$ can be close to 1, which would skip an item that must be taken. Use integer draws or check the forced case $n - m = N - t$.
- **Reading past the end.** The loop stops at $m = n$. There is no need to read the rest of the input, and code that does so wastes time.

## Implementations

## History

C. T. Fan, Mervin Muller and Ivan Rezucha published sequential item by item selection in the Journal of the American Statistical Association in 1962, for sampling plans run on digital computers. Knuth presents the method as Algorithm S, the "selection sampling technique", in Section 3.4.2 of The Art of Computer Programming, next to the reservoir method Algorithm R for the case of unknown $N$.

## References

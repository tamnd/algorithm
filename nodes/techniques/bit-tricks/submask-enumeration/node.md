---
tag: 06FS9F
kind: technique
slug: submask-enumeration
name: Submask enumeration
aliases:
- enumerating submasks
- enumerating submasks of a bitmask
- sub = (sub-1) & mask
- subset enumeration over bitmasks
area: techniques/bit-tricks
level: core
summary: Iterating over all submasks of a mask m with sub = (sub - 1) & m in O(2^k) total time.
prereqs: [bitmask, bitwise-operations, twos-complement]
see_also: [bitmask-dp, sum-over-subsets, sos-dp, sum-over-subsets-dp, gospers-hack, lawler-chromatic-number, steiner-tree-problem]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1
    locator: Section 7.1.3, Bitwise Tricks and Techniques
  - book: isbn:9780321842688
    title: Henry S. Warren, Jr., Hacker's Delight, second edition
    locator: Section 2-1, Manipulating Rightmost Bits
  - book: isbn:9783642165320
    title: Fedor V. Fomin and Dieter Kratsch, Exact Exponential Algorithms, Springer, 2010
    locator: Chapter 3, Dynamic Programming (the O(3^n) subset recurrences) and Chapter 7, Subset Convolution
---

Submask enumeration is the loop that visits every submask $s \subseteq m$ of a [bitmask](/bitmask/) $m$ by the step $s \leftarrow (s - 1) \mathbin{\&} m$. It visits the $2^{\operatorname{pop}(m)}$ submasks in decreasing order with $O(1)$ work each, and never touches a word that is not a submask. Run for every $m$ of $n$ bits, it does $3^n$ steps in total, which is the cost of the classic subset recurrences of [bitmask DP](/bitmask-dp/), such as [Lawler's chromatic number algorithm](/lawler-chromatic-number/).

## In plain words

A mask is a row of switches, and some of them are on. A submask turns on only switches that are already on in the mask. You want to visit every such choice, and none of the others.

Subtract one, then keep only the switches of the mask. Subtracting one turns off the lowest switch that is on and turns on all switches below it. Keeping only the mask throws away the switches that are not allowed. The result is the next smaller choice. Start from the full mask and repeat until you reach the empty choice.

A mask with ten switches on has about a thousand submasks, and the loop visits each one exactly once, with no wasted steps.

## When it applies

- The state is a set of at most about 25 items, stored as a mask, and a step must look at each subset of the current set: split a set into a part and the rest, or try each group that can be removed.
- A recurrence has the form $f(m) = \bigoplus_{s \subseteq m} g(s, m \setminus s)$, where $\bigoplus$ is a sum, a minimum or another fold.
- A loop over all $2^n$ words with a test `(s & ~m) == 0` would waste time on words that are not submasks.
- The total $3^n$ is fast enough. For $n = 15$ it is about $1.4 \times 10^7$; for $n = 20$ it is about $3.5 \times 10^9$, which is too slow in most settings, and a [sum over subsets](/sum-over-subsets/) structure or [SOS DP](/sos-dp/) with $n 2^n$ steps may replace it.

## The template

```pseudo id=main
FOR-EACH-SUBMASK(m)                ▷ m: a mask of n bits
L1  s ← m
L2  loop
L3      VISIT(s)                   ▷ hole: the work for the submask s
L4      if s = 0 then exit
L5      s ← (s − 1) AND m          ▷ the next smaller submask of m

SUBSET-RECURRENCE(n)               ▷ the usual use, O(3^n) steps
L6  for m ← 0 to 2^n − 1 do
L7      f[m] ← INIT(m)             ▷ hole
L8      for each submask s of m, by L1 to L5, do
L9          f[m] ← COMBINE(f[m], s, m XOR s)   ▷ hole, may read f[m XOR s]
```

**Why line L5 gives the next smaller submask.** Let $s \ne 0$ be a submask of $m$, and let bit $j$ be its lowest one. Then $s - 1$ has a 0 at bit $j$, ones at bits $0$ to $j - 1$, and the bits of $s$ above $j$. The AND with $m$ gives $s' = (s \text{ above } j) + (m \bmod 2^j)$. This is a submask of $m$ and $s' < s$. Each submask $y$ of $m$ with $y < s$ has a highest bit $p$ where it differs from $s$, with a 1 in $s$ and a 0 in $y$. Since bit $j$ is the lowest one of $s$, $p \ge j$. If $p > j$, then $s'$ agrees with $s$ at bit $p$ and above, so $y$ and $s'$ agree above $p$, $s'$ has a 1 at bit $p$ and $y$ a 0, and $y < s'$. If $p = j$, then $y$ agrees with $s$ above $j$, has a 0 at $j$, and its low $j$ bits are a submask of $m \bmod 2^j$, so $y \le s'$. So $s'$ is the largest submask of $m$ below $s$. By induction from $s = m$, the loop visits every submask of $m$ once, in decreasing order, and stops after $0$. It runs $2^{\operatorname{pop}(m)}$ times.

**The total cost.** For $n$ bits,
$$ \sum_{m=0}^{2^n - 1} 2^{\operatorname{pop}(m)} = \sum_{k=0}^{n} \binom{n}{k} 2^k = (1 + 2)^n = 3^n , $$
by the binomial theorem, since $\binom{n}{k}$ masks have $k$ ones. Another way to see it: each pair $(s, m)$ with $s \subseteq m$ gives each of the $n$ bits one of three states, in neither, in $m$ only, or in both. So SUBSET-RECURRENCE does $3^n$ calls of COMBINE.

**Example.** For $m = 1101_2 = 13$ the loop visits 13, 12, 9, 8, 5, 4, 1, 0, in binary 1101, 1100, 1001, 1000, 0101, 0100, 0001, 0000. That is $2^3 = 8$ submasks. From $s = 12 = 1100_2$, $s - 1 = 1011_2$ and $1011_2 \mathbin{\&} 1101_2 = 1001_2 = 9$.

## Classic examples

- **All sums of a set function, the slow way.** $F(m) = \sum_{s \subseteq m} f(s)$ for all $m$ in $3^n$ steps. This is the [sum over subsets](/sum-over-subsets/) problem; [SOS DP](/sos-dp/) does it in $n 2^n$ steps, so submask enumeration is the baseline it improves.
- **Partition into groups.** The least cost to split a set into groups, $f(m) = \min_{\emptyset \ne s \subseteq m} (c(s) + f(m \setminus s))$, takes $O(3^n)$ steps. To count each partition only once, restrict $s$ to the submasks that hold the lowest bit of $m$.
- **[Lawler's chromatic number algorithm](/lawler-chromatic-number/).** It colors a graph by removing one maximal independent set at a time, with a recurrence over the subsets of the vertices; the subset loops give $O(2.4423^n)$ time with Lawler's bound on the number of maximal independent sets, and plain submask enumeration gives $O^*(3^n)$.
- **Dreyfus and Wagner for the [Steiner tree problem](/steiner-tree-problem/).** The table indexed by a subset of the $k$ terminals and a vertex merges two trees, one for a submask and one for the rest, which costs $O(3^k n)$ for this step.
- **[Bitmask DP](/bitmask-dp/) with a split of the state.** Any DP whose transition picks a subset of the current set, for example a set of jobs done on one machine.

## Variations

- **Increasing order.** $s \leftarrow (s - m) \mathbin{\&} m$, starting from $s = 0$ and stopping when $s$ returns to 0, visits the submasks in increasing order. Here $s - m$ is computed modulo $2^w$; the carry chain jumps over the bits not in $m$.
- **Proper and nonempty submasks.** Start from $s = (m - 1) \mathbin{\&} m$ to skip $m$, and stop before $0$ to skip the empty set.
- **Supersets.** $s \leftarrow (s + 1) \mathbin{|} m$, starting from $s = m$ and stopping when $s \ge 2^n$, visits every superset of $m$ inside $n$ bits in increasing order. Over all $m$ this is also $3^n$ steps.
- **Submasks of a fixed size.** Visit the submasks of $m$ with exactly $k$ ones by running [Gosper's hack](/gospers-hack/) on the indices $0, \ldots, \operatorname{pop}(m) - 1$ and mapping each result into the positions of $m$ (a bit deposit, PDEP on x86).
- **Each unordered split once.** To visit each pair $\{s, m \setminus s\}$ once, keep only the submasks that contain the lowest bit of $m$, or stop when $s < m \oplus s$.

## Pitfalls

- **Stopping at zero too early.** The loop `for (s = m; s > 0; s = (s - 1) & m)` never visits the empty set. Use the form with the test after the visit (lines L3 and L4), or visit 0 after the loop.
- **Infinite loop.** The form `for (s = m; s >= 0; s = (s - 1) & m)` never stops, for a signed or an unsigned `s`, since $(0 - 1) \mathbin{\&} m = m$ starts the cycle again.
- **Counting the cost as $4^n$ or $2^n \cdot 2^n$.** The nested loop over all masks and all their submasks costs $3^n$, not $4^n$. The other way round, it is not $2^n$: for $n = 20$ it is about $3.5 \times 10^9$ steps.
- **Reading a value that is not ready.** In SUBSET-RECURRENCE, $f[m \setminus s]$ must be final before $f[m]$ reads it. The loop of line L6 in increasing $m$ is safe, because $m \setminus s \le m$, but when $s = \emptyset$ the term $f[m]$ refers to itself.
- **Double counting a partition.** Without the rule on the lowest bit, the recurrence for partitions counts each split twice and each partition into $j$ groups $j!$ times when it counts rather than minimizes.

## Exercises

1. List the submasks of $m = 10110_2$ in the order of the loop, and check that there are $2^3$ of them.
2. Prove that $(s - m) \mathbin{\&} m$, computed modulo $2^w$, is the next larger submask of $m$ after the submask $s$, and that it is 0 after $m$.
3. Prove that the loop $s \leftarrow (s + 1) \mathbin{|} m$ visits all supersets of $m$ inside $n$ bits, in increasing order.
4. Give an $O(3^n)$ algorithm that counts, for each set $m$ of $n$ items, the number of ways to split $m$ into nonempty groups whose sizes are all even.
5. Show that the number of pairs $(s, m)$ with $s \subseteq m \subseteq \{0, \ldots, n - 1\}$ and $\operatorname{pop}(s) = \operatorname{pop}(m) - 1$ is $n 2^{n-1}$, and relate it to the number of steps of [SOS DP](/sos-dp/).

## References

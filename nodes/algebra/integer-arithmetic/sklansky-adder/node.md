---
tag: JA4QR9
kind: algorithm
slug: sklansky-adder
name: Sklansky adder
aliases:
- divide-and-conquer prefix adder
- Sklansky prefix adder
- conditional-sum adder
area: algebra/integer-arithmetic
level: advanced
summary: Parallel-prefix adder with logarithmic depth and high fan-out at each level.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n log n)}
properties: {deterministic: true, recursive: true}
prereqs: [ripple-carry-adder, parallel-prefix, divide-and-conquer-paradigm]
see_also: [kogge-stone-adder, brent-kung-adder, carry-lookahead-adder, carry-select-adder, ripple-carry-adder, parallel-prefix, carry-propagation, boolean-circuit]
sources:
  - paper: J. Sklansky, Conditional-sum addition logic, IRE Transactions on Electronic Computers EC-9(2), 1960
    title: Jack Sklansky, Conditional-sum addition logic
    locator: pp. 226 to 231 (conditional sums for both carry values, combined by halves in a tree)
  - paper: R. E. Ladner and M. J. Fischer, Parallel prefix computation, Journal of the ACM 27(4), 1980
    title: Richard E. Ladner and Michael J. Fischer, Parallel prefix computation
    locator: pp. 831 to 838 (the recursive prefix circuit of depth log n and size (n/2) log n, and the family between it and smaller circuits)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 6, Carry-lookahead adders (parallel prefix networks), and Chapter 7, Variations in fast adders (conditional-sum adders)
  - paper: D. Harris, A taxonomy of parallel prefix networks, Proceedings of the 37th Asilomar Conference on Signals, Systems and Computers, 2003
    title: David Harris, A taxonomy of parallel prefix networks
    locator: the Sklansky network as the extreme of high fan-out among minimal-depth networks
---

The Sklansky adder computes the carries of an $n$-bit addition with a divide-and-conquer parallel prefix network. It finds the carries of the low half and of the high half of the word separately and at the same time. Then it combines every position of the high half with the carry signal at the top of the low half, in one more level. The recursion has $\lceil \log_2 n \rceil$ levels, the least possible for two-input cells, and about $\frac{n}{2}\log_2 n$ cells, fewer than the [Kogge-Stone adder](/kogge-stone-adder/). The cost is fan-out: the top signal of each low half drives every cell of its high half, up to $n/2$ of them at the last level, and a heavily loaded signal is slow. The structure comes from Sklansky's conditional-sum adder of 1960, and as a prefix network it is also the recursive circuit of Ladner and Fischer.

## In plain words

To find all the carries of a long addition, split the number into a right half and a left half. Work out the carries inside each half on its own, both at once, as if no carry came into the left half from outside.

Then fix the left half. The right half now knows whether it sends a carry out of its top. Every position of the left half checks this one signal, together with what it knows about its own stretch, and gets its true carry. Each half is split the same way, and so on down to single positions. The halving makes it fast, about $\log_2 n$ rounds. But one signal must reach half of the positions at once, and in a chip that slows it down.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$ and a carry-in bit $c_0$. The output is the $n + 1$ bits $s_n \cdots s_0$ of $a + b + c_0$, the fixed-width [integer addition](/integer-addition/).

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates of fan-in 2. The size, in the field `time`, is the number of gates, and the depth is the longest path from an input to an output, in gates. The model does not charge for fan-out; its effect on real delay is discussed below as an observation about technology.

## The algorithm

As in every prefix adder, position $i$ has a *generate* bit $g_i = a_i \wedge b_i$ and a *propagate* bit $p_i = a_i \oplus b_i$, and the pairs combine by the associative carry operator $(G, P) \circ (G', P') = (G \vee (P \wedge G'), P \wedge P')$, high block on the left. With the carry in folded into position 0, the carry $c_{i+1}$ is the $G$ part of the block $0..i$. The Sklansky network computes all these blocks recursively.

```pseudo id=main
SKLANSKY-ADD(a[0 .. n − 1], b[0 .. n − 1], c_in)
L1  for all i in parallel: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  g[0] ← g[0] ∨ (p[0] ∧ c_in)                    ▷ fold the carry in
L3  (G, P) ← (g, p);  PREFIX(0, n)
L4  c[0] ← c_in;  for all i in parallel: c[i + 1] ← G[i]
L5  for all i in parallel: s[i] ← p[i] ⊕ c[i]
L6  return s[0 .. n − 1] and the carry out c[n]

PREFIX(lo, hi)            ▷ afterwards (G[i], P[i]) is the pair of the block lo..i, for lo ≤ i < hi
L7  if hi − lo ≤ 1 then return
L8  mid ← lo + ⌈(hi − lo) / 2⌉
L9  PREFIX(lo, mid) and PREFIX(mid, hi), in parallel
L10 for all i in [mid, hi) in parallel: (G[i], P[i]) ← (G[i], P[i]) ∘ (G[mid − 1], P[mid − 1])
```

Line L10 is where the fan-out arises: the single pair at position $mid - 1$, which after line L9 describes the whole low half, enters every cell of the high half.

## Example

Add $a = 182 = 10110110_2$ and $b = 91 = 01011011_2$ with $c_0 = 0$, as on the [Kogge-Stone](/kogge-stone-adder/) page. The strings run from position 7 down to position 0. After the level that merges blocks of size $k/2$ into blocks of size $k$, position $i$ holds the block from $k\lfloor i/k \rfloor$ to $i$.

| level | block size $k$ | $G$ | $P$ |
|---|---|---|---|
| start | 1 | $00010010$ | $11101101$ |
| 1 | 2 | $00110010$ | $11001101$ |
| 2 | 4 | $11111110$ | $00000001$ |
| 3 | 8 | $11111110$ | $00000001$ |

At level 2, positions 6 and 7 both use the pair of position 5, and positions 2 and 3 both use that of position 1; at level 3, positions 4 to 7 all use position 3. The final $G$ gives the carries $c_8 \cdots c_1 = 11111110$, and the sum is $p \oplus c = 11101101 \oplus 11111100 = 00010001$ with carry out 1: $273 = 182 + 91$. In this 8-bit circuit there are 12 prefix cells, against 17 for Kogge-Stone, and the depth is 10 gates. The table and the counts were checked by script.

## Correctness

The proof is by induction on the length $hi - lo$ of the call. For length 1 the pair at position $lo$ is $(g_{lo}, p_{lo})$, the pair of the block $lo..lo$. For a longer range, after line L9 position $i < mid$ holds the block $lo..i$ and position $i \ge mid$ holds $mid..i$, by the induction hypothesis on the two halves, which are shorter because $lo < mid < hi$. Line L10 combines, for $i \ge mid$, the block $mid..i$ with the adjacent lower block $lo..mid - 1$ held at position $mid - 1$, which gives the block $lo..i$, because the carry operator composes adjacent blocks. So PREFIX$(0, n)$ leaves the pair of $0..i$ at every position, its $G$ part is $c_{i+1}$, and the sum bits follow as in a [full adder](/ripple-carry-adder/). The full proof is below.

## Complexity

**Levels.** The recursion halves the range, rounding the low half up, so its depth is $\lceil \log_2 n \rceil$, and the levels of line L10 for different calls at the same depth run in parallel. The prefix network has $\lceil \log_2 n \rceil$ levels, the minimum for two-input cells, since the last carry depends on all $n$ positions.

**Cells.** A call of length $\ell$ adds $\lfloor \ell/2 \rfloor$ cells, so the count satisfies $C(n) = C(\lceil n/2 \rceil) + C(\lfloor n/2 \rfloor) + \lfloor n/2 \rfloor$, which is $\frac{n}{2}\log_2 n$ for $n$ a power of two and at most $\frac{n}{2}\lceil \log_2 n \rceil + 1$ in general. Each cell has 3 gates, so the size is $\Theta(n \log n)$.

**Depth.** Each level adds 2 gates to the path of $G$; with the 3 gates of lines L1 and L2 and the final XOR, the depth is at most $2\lceil \log_2 n \rceil + 4$. These counts were checked by script for all $n \le 130$.

**Fan-out.** At the level that merges two blocks of size $k/2$, the signal at the top of each low block drives $k/2$ cells, so the maximum fan-out is $\lfloor n/2 \rfloor$, at the last level; the test checks this. In a real circuit the delay of a gate grows with its load, so either the cells of the high half wait for a slow signal or buffer trees are inserted, which add about $\log_2$ of the fan-out in levels. This makes Sklansky adders slower in practice than their level count suggests; how much depends on the technology, and is observed, not proved.

All bounds in this section are proved for the model; the remarks on delay are observations.

## Properties

- **Minimal depth, fewer cells.** The same number of levels as Kogge-Stone with about half the cells.
- **High fan-out.** Up to $n/2$ at the last level, against 2 for Kogge-Stone and [Brent-Kung](/brent-kung-adder/).
- **Few wires.** Each level needs only short local wiring plus the broadcast of one signal per block.
- **Recursive.** The network for $n$ is two networks for $n/2$ and one row of cells, which makes it easy to generate and to reason about.

## Variants and improvements

- **Conditional-sum addition.** Sklansky's original form computes, for every block, the sum bits for both values of the incoming carry, and selects with multiplexers when the carry of the block below is known, merging blocks by halves. It is the same divide-and-conquer structure applied to sums instead of generate and propagate pairs, and the ancestor of the [carry-select adder](/carry-select-adder/).
- **Ladner-Fischer networks.** Ladner and Fischer gave a family of prefix circuits from this recursive one, of depth $\lceil \log_2 n \rceil$, to smaller ones of slightly larger depth and linear size.
- **Buffered Sklansky.** Insert buffer trees on the high fan-out signals, or duplicate the cells that drive them, to trade area for delay.
- **[Kogge-Stone adder](/kogge-stone-adder/).** Removes the fan-out by computing each block separately, with about twice the cells and long wires.
- **Knowles networks.** Intermediate between Sklansky and Kogge-Stone: minimal depth, with fan-out and wiring traded against each other.

## When to use it

Use a Sklansky adder when minimal logic depth is wanted with fewer cells than Kogge-Stone, and the fan-out can be handled by sizing or buffering, which is often the case for moderate widths. For the widest and fastest adders, Kogge-Stone or a Knowles hybrid usually wins; for small area, use Brent-Kung or a [ripple-carry adder](/ripple-carry-adder/). As a design for parallel prefix in software or on parallel machines, the recursive scheme is simple and has the minimum number of rounds.

## Pitfalls

- **Ignoring fan-out.** The gate depth is minimal, but the broadcast signal of the last level drives $n/2$ inputs; a timing estimate from levels alone is too optimistic.
- **Splitting with the low half too small.** The split must put $\lceil \ell/2 \rceil$ positions in the low half, or at least make the depth of both halves $\lceil \log_2 \ell \rceil - 1$; an unbalanced split adds levels.
- **Using the updated value of position $mid - 1$.** All cells of line L10 must read the pair of $mid - 1$ after line L9 and before line L10; in a sequential simulation the low half is not changed by line L10, so this holds, but merging the two loops breaks it.
- **The carry in.** It must be folded into position 0 (line L2) or added as an extra position; otherwise the adder computes only $a + b$.

## Implementations

## History

Sklansky described conditional-sum addition in 1960: every block computes its sum for both possible incoming carries, and blocks are merged by halves, the faster one selecting from the slower. Seen as a parallel prefix of carry signals, the same divide-and-conquer pattern is the recursive prefix circuit that Ladner and Fischer analysed in 1980, and in adder design it is called the Sklansky network. Kogge and Stone's network of 1973 and Brent and Kung's of 1982 are the other classical prefix adders; Harris's taxonomy of 2003 places Sklansky's network at the corner of minimal depth and maximal fan-out.

## References

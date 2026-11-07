---
tag: PABN90
kind: algorithm
slug: kogge-stone-adder
name: Kogge-Stone adder
aliases:
- Kogge-Stone prefix adder
- KS adder
- recursive doubling adder
area: algebra/integer-arithmetic
level: advanced
summary: Parallel-prefix adder with logarithmic depth and minimal fan-out-free wiring depth.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n log n), average: Θ(n log n), best: Θ(n log n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n log n)}
properties: {deterministic: true, recursive: false}
prereqs: [ripple-carry-adder, parallel-prefix, boolean-circuit]
see_also: [sklansky-adder, brent-kung-adder, carry-lookahead-adder, ripple-carry-adder, carry-select-adder, parallel-prefix, carry-propagation, prefix-sums]
sources:
  - paper: P. M. Kogge and H. S. Stone, A parallel algorithm for the efficient solution of a general class of recurrence equations, IEEE Transactions on Computers C-22(8), 1973
    title: Peter M. Kogge and Harold S. Stone, A parallel algorithm for the efficient solution of a general class of recurrence equations
    locator: pp. 786 to 793 (recursive doubling for first-order recurrences, of which the carry recurrence is a case)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 6, Carry-lookahead adders (carry determination as prefix computation, and alternative parallel prefix networks)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (prefix adders and their networks)
  - paper: D. Harris, A taxonomy of parallel prefix networks, Proceedings of the 37th Asilomar Conference on Signals, Systems and Computers, 2003
    title: David Harris, A taxonomy of parallel prefix networks
    locator: the comparison of the Sklansky, Kogge-Stone and Brent-Kung networks by levels, fan-out and wiring tracks
---

The Kogge-Stone adder is a parallel-prefix adder: it computes all the carries of an $n$-bit addition in $\lceil \log_2 n \rceil$ levels of a regular network, and then the sum bits in one more step. Each bit position starts with a pair of signals, *generate* and *propagate*. At level $j$, every position $i \ge 2^j$ combines its pair with the pair of position $i - 2^j$, so after level $j$ each position knows the carry behaviour of the $2^{j+1}$ positions ending at it. This is recursive doubling, the method Kogge and Stone gave in 1973 for linear recurrences. The adder has the smallest possible number of levels, and every cell drives only two others, which keeps each level fast. The price is size and wiring: about $n \log_2 n$ cells, and long wires that cross half the width at the last level. It is the fastest of the classical prefix adders and is used where delay matters most, as in the adders of high-speed processors.

## In plain words

In a [ripple-carry adder](/ripple-carry-adder/) the carry walks from the right end to the left, one position at a time. A Kogge-Stone adder finds all the carries at once by asking a question about blocks of positions: will this block produce a carry, and will it pass on a carry that comes in?

At first every position knows the answer only for itself. In the first round each position combines its answer with its right neighbor's, and now knows it for a block of 2. In the next round it combines with the position 2 places away, for a block of 4, then 4 places away, and so on. After about $\log_2 n$ rounds every block reaches the right end, and each position knows its carry.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$ and a carry-in bit $c_0$. The output is the $n + 1$ bits $s_n \cdots s_0$ of $a + b + c_0$, the fixed-width [integer addition](/integer-addition/).

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates of fan-in 2. The size, given in the field `time`, is the number of gates; the depth is the number of gates on the longest path from an input to an output. Fan-out and wire length are not counted by the model, but they decide the real delay; they are discussed separately below and are observations about layouts, not theorems of the model.

## The algorithm

For each position, $g_i = a_i \wedge b_i$ says that position $i$ creates a carry, and $p_i = a_i \oplus b_i$ that it passes an incoming carry on. For a block of positions $k..i$, the pair $(G_{i:k}, P_{i:k})$ says the same for the block. Two adjacent blocks, a high one $(G, P)$ and a low one $(G', P')$, combine by the *carry operator*

$$(G, P) \circ (G', P') = (G \vee (P \wedge G'),\; P \wedge P') ,$$

which is associative. The carry into position $i + 1$ is $c_{i+1} = G_{i:0}$ once the carry in has been folded into position 0. Computing all $G_{i:0}$ is a [parallel prefix](/parallel-prefix/) computation with $\circ$, and Kogge-Stone is one network for it.

```pseudo id=main
KOGGE-STONE-ADD(a[0 .. n − 1], b[0 .. n − 1], c_in)
L1  for all i in parallel: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  g[0] ← g[0] ∨ (p[0] ∧ c_in)                     ▷ fold the carry in
L3  (G, P) ← (g, p);  d ← 1
L4  while d < n do                                  ▷ ⌈log2 n⌉ levels
L5      for all i ≥ d in parallel: (G[i], P[i]) ← (G[i], P[i]) ∘ (G[i − d], P[i − d])
L6      d ← 2d
L7  c[0] ← c_in;  for all i in parallel: c[i + 1] ← G[i]
L8  for all i in parallel: s[i] ← p[i] ⊕ c[i]
L9  return s[0 .. n − 1] and the carry out s[n] = c[n]
```

Line L5 reads the values of the previous level for all $i$ at once. After the level with distance $d$, position $i$ holds the pair of the block $\max(0, i - 2d + 1)..i$. A cell whose block already reaches position 0 needs only the $G$ part; the $P$ part is needed only for $i \ge 2d$.

## Example

Add $a = 182 = 10110110_2$ and $b = 91 = 01011011_2$ with $c_0 = 0$. The bit strings are written from position 7 down to position 0.

| level | $d$ | $G$ | $P$ |
|---|---|---|---|
| start | | $00010010$ | $11101101$ |
| 1 | 1 | $00110110$ | $11001000$ |
| 2 | 2 | $11111110$ | $00000000$ |
| 3 | 4 | $11111110$ | $00000000$ |

After level 3 every $G_i = G_{i:0}$, so the carries $c_8 \cdots c_1$ are $11111110$ and $c_0 = 0$. The sum bits are $p \oplus c = 11101101 \oplus 11111100 = 00010001$, with carry out $c_8 = 1$: the result is $100010001_2 = 273 = 182 + 91$. The table was computed by script, and the test of this page checks the sum and the depth 9 of this 8-bit circuit.

## Correctness

The operator $\circ$ is associative, and $(G_{i:k}, P_{i:k}) = (G_{i:j+1}, P_{i:j+1}) \circ (G_{j:k}, P_{j:k})$ for every split $k \le j < i$: a carry leaves the block $k..i$ if the high part creates one, or the high part propagates and the low part sends one. By induction on the levels, after the level with distance $d$ position $i$ holds the pair of the block $\max(0, i - 2d + 1)..i$: it combines its own block of length $d$ with the block of length $d$ just below, held by position $i - d$. After $\lceil \log_2 n \rceil$ levels, $2d \ge n > i$, so every position holds the pair of $0..i$, and with the carry in folded into $g_0$, $G_{i:0} = c_{i+1}$. Then $s_i = p_i \oplus c_i$ is the sum bit, as in the full adder. The full proof is below.

## Complexity

**Levels and cells.** The loop runs $L = \lceil \log_2 n \rceil$ times, and the level with distance $2^j$ has $n - 2^j$ cells, so there are $\sum_{j<L} (n - 2^j) = nL - 2^L + 1$ prefix cells; for $n = 2^L$ this is $n\log_2 n - n + 1$. With 2 gates for each $G$ and 1 for each needed $P$, plus $2n$ gates for line L1, 2 for line L2 and $n$ for line L8, the size is $\Theta(n \log n)$. For $n = 8$ there are 17 cells and 70 gates.

**Depth.** Line L1 has depth 1, line L2 depth 3 for $g_0$, each level adds 2, and line L8 adds 1. The depth is at most $2\lceil \log_2 n \rceil + 3$, with equality when $n$ is a power of two, $\Theta(\log n)$. The cell counts and depths were checked by script for all $n \le 129$. The number of levels, $\lceil \log_2 n \rceil$, is the minimum for any prefix network built from two-input cells, because $G_{n-1:0}$ depends on all $n$ positions.

**Fan-out and wires.** Each cell output feeds at most two cells of the next level, its own position and the position $d$ places higher, so no level is slowed by a heavily loaded wire. But at the level with distance $d$ the wires span $d$ positions, so the last level has wires across half the width, and the number of wiring tracks grows with $n$. In real layouts this area and wire delay, not the gate count, are the limit; that is an observation about technology, not a bound in the model.

**Software.** The same rounds work on whole machine words: with $G$ and $P$ held as $n$-bit integers, one round is $G \leftarrow G \vee (P \wedge (G \ll d))$ and $P \leftarrow P \wedge (P \ll d)$. The implementation includes this form. On a sequential machine it is slower than a single add instruction, but it shows that addition is a prefix computation on bit vectors.

## Properties

- **Minimal depth.** $\lceil \log_2 n \rceil$ prefix levels, the least possible.
- **Bounded fan-out.** Every cell drives two others, unlike the [Sklansky adder](/sklansky-adder/), whose fan-out grows to about $n/2$.
- **Large and wire-heavy.** About $n \log_2 n$ cells, against about $2n$ for [Brent-Kung](/brent-kung-adder/), and long wires.
- **Regular.** Every level has the same structure, a shift by $d$, which suits automatic layout.
- **All prefixes.** It computes every carry, not just the carry out, so it also serves as a comparator, an incrementer or the carry network of a [carry-select adder](/carry-select-adder/).

## Variants and improvements

- **[Brent-Kung adder](/brent-kung-adder/).** About $2\log_2 n - 1$ levels, $2n - \log_2 n - 2$ cells and fan-out 2: half the depth advantage traded for much less area and wiring.
- **[Sklansky adder](/sklansky-adder/).** Minimal depth and $\frac{n}{2}\log_2 n$ cells, but high fan-out.
- **Han-Carlson adder.** Kogge-Stone on the odd positions only, with one Brent-Kung level before and after: one more level, about half the cells and wires.
- **Knowles adders.** A family of minimal-depth networks between Kogge-Stone and Sklansky, trading wiring tracks against fan-out.
- **Ladner-Fischer networks.** A family between Sklansky and Brent-Kung, trading depth against size.
- **Sparse trees.** Compute only every fourth or eighth carry with a Kogge-Stone tree, and the rest with short ripple or carry-select blocks, which reduces the wiring in practice.
- **Ling's carries.** A reformulation of the generate signal that removes one gate from the critical path of each level.

## When to use it

Use a Kogge-Stone adder for wide adders on the critical path of a fast circuit, such as the integer adders and address generators of a processor, when area and power can be spent for speed. Use Brent-Kung or Han-Carlson when area or wiring is the constraint, and a [ripple-carry adder](/ripple-carry-adder/) when delay does not matter. For a model of computation, the Kogge-Stone network is the standard example of a parallel prefix of depth $\log_2 n$.

## Pitfalls

- **Reading updated values in the same level.** Line L5 must use the values of the previous level. A sequential loop that updates $G[i]$ in place, from high $i$ to low, is correct; from low to high it combines already updated values and computes wrong blocks.
- **Forgetting the carry in.** Without line L2, the network computes $a + b$ only; a carry in must be folded into position 0, or treated as an extra position $-1$ with $g = c_0$, $p = 0$.
- **Using $P$ from the wrong operator.** The propagate bit must be $a_i \oplus b_i$ for the sum, though $a_i \vee b_i$ also works inside the prefix network; mixing them in line L8 gives wrong sums.
- **Counting only gates.** The gate depth is minimal, but the wires of the last levels can dominate the delay; compare layouts, not gate counts.
- **Non-power-of-two widths.** The level count is $\lceil \log_2 n \rceil$; the levels with $d \ge n$ are not needed, and building them wastes cells.

## Implementations

## History

Kogge and Stone published recursive doubling in 1973 as a general method for first-order linear recurrences on parallel machines, and the carry recurrence $c_{i+1} = g_i \vee (p_i \wedge c_i)$ is the case that gave the adder its name. The idea of computing carries by blocks in a tree is older: Weinberger and Smith described carry lookahead in the late 1950s, and Sklansky's conditional-sum adder of 1960 has the divide-and-conquer prefix structure now named after him. Ladner and Fischer studied parallel prefix networks in general in 1980, and Brent and Kung gave their area-efficient layout in 1982. Knowles described the family of minimal-depth networks between Kogge-Stone and Sklansky in 1999, and Harris arranged the classical networks in a single taxonomy in 2003.

## References

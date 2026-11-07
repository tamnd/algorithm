---
tag: XD1FWT
kind: algorithm
slug: brent-kung-adder
name: Brent-Kung adder
aliases:
- Brent-Kung prefix adder
- BK adder
area: algebra/integer-arithmetic
level: advanced
summary: Parallel-prefix adder with fewer prefix cells and about twice the depth of Kogge-Stone.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Richard Brent and H. T. Kung gave the network and its regular VLSI layout in 1982.
prereqs: [carry-lookahead-adder, parallel-prefix, boolean-circuit]
see_also: [kogge-stone-adder, sklansky-adder, carry-lookahead-adder, ripple-carry-adder, carry-select-adder, parallel-prefix, carry-propagation, prefix-sums]
sources:
  - paper: doi:10.1109/TC.1982.1675982
    title: Richard P. Brent and H. T. Kung, A regular layout for parallel adders, IEEE Transactions on Computers C-31(3), 1982
    locator: pp. 260 to 264 (the carry network as a prefix computation with the operator o, and the tree layout)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 6, Carry-lookahead adders, Sections 6.4 and 6.5 (carry determination as prefix computation, and alternative parallel prefix networks)
  - paper: doi:10.1145/322217.322232
    title: Richard E. Ladner and Michael J. Fischer, Parallel prefix computation, Journal of the ACM 27(4), 1980
    locator: pp. 831 to 838 (prefix circuits with a tradeoff between size and depth)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (prefix adders and their networks)
---

The Brent-Kung adder computes the carries of an $n$-bit addition with a [parallel prefix](/parallel-prefix/) network shaped as a binary tree that is used twice: once going up, to combine the generate and propagate signals of blocks of size $2, 4, 8, \ldots$, and once going down, to hand the finished prefixes to the positions in between. For $n = 2^L$ it uses $2n - 2 - L$ two-input prefix cells in $2L - 1$ levels. That is about $2n$ cells against about $n \log_2 n$ for the [Kogge-Stone adder](/kogge-stone-adder/), at the price of about twice the number of levels. Brent and Kung gave it in 1982 together with a regular layout, and it is the standard example of a prefix adder of linear size and logarithmic depth. It is the radix-2 form of the hierarchical [carry-lookahead adder](/carry-lookahead-adder/).

## In plain words

Adding two binary numbers is slow because of the carries: each position needs to know whether a carry arrives from the right. For any block of positions you can ask two questions: does the block make a carry by itself, and does it pass on a carry that comes in? The answers for two neighbouring blocks combine into the answers for the joined block.

The Brent-Kung adder first joins blocks in pairs, like a knockout tournament: pairs of positions, then pairs of pairs, and so on, until the whole right half is one block. Along the way, the positions at the end of each block that touches the right end learn their carry. Then it runs the tournament backwards, and each of the other positions joins its small block to a finished block to its right. Few joins are needed, so the circuit is small.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$, with $n \ge 1$, and a carry-in bit $c_0$. The output is the $n + 1$ bits of $a + b + c_0$, the fixed-width [integer addition](/integer-addition/).

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates of fan-in 2 and unit delay. The size, given in the field `time`, is the number of gates; the depth is the number of gates on the longest path. The cell and level counts below are proved for every $n$; the exact depth $4L$ for $n = 2^L$ is observed by the test script for $L \le 10$, and the general depth bound is proved. Fan-out and wire length are not part of the model; the remarks on layout are observations about real circuits.

## The algorithm

For each position, $g_i = a_i \wedge b_i$ (generate) and $p_i = a_i \oplus b_i$ (propagate). A block $k..i$ has the pair $(G_{i:k}, P_{i:k})$, and adjacent blocks combine by the associative *carry operator*

$$(G, P) \circ (G', P') = (G \vee (P \wedge G'),\; P \wedge P') ,$$

with the high block on the left. One prefix cell evaluates $\circ$ with three gates, or two when $P$ is not needed. Once the carry-in is folded into position 0, the carry into position $i + 1$ is $c_{i+1} = G_{i:0}$.

```pseudo id=main
BRENT-KUNG-ADD(a, b, c_in)                         ▷ n bits each, low bit first
L1  for all i in parallel: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  g[0] ← g[0] ∨ (p[0] ∧ c_in)                     ▷ fold the carry in
L3  (G, P) ← (g, p);  d ← 1
L4  while d < n do                                  ▷ the up-sweep
L5      for all i ≡ 2d − 1 (mod 2d), i < n, in parallel: (G[i], P[i]) ← (G[i], P[i]) ∘ (G[i − d], P[i − d])
L6      d ← 2d
L7  d ← ⌊d / 4⌋
L8  while d ≥ 1 do                                  ▷ the down-sweep
L9      for all i ≡ d − 1 (mod 2d), 3d − 1 ≤ i < n, in parallel: (G[i], P[i]) ← (G[i], P[i]) ∘ (G[i − d], P[i − d])
L10     d ← ⌊d / 2⌋
L11 c[0] ← c_in;  for all i: c[i + 1] ← G[i]
L12 for all i in parallel: s[i] ← p[i] ⊕ c[i]
L13 return s[0 .. n − 1] and the carry out c[n]
```

In the up-sweep, the level with distance $d$ updates the positions $i$ with $2d \mid i + 1$, so position $2^k - 1$ ends with the whole prefix $0..2^k - 1$. In the down-sweep, the level with distance $d$ updates the positions $i$ whose $i + 1$ is an odd multiple of $d$ and at least $3d$: each joins its block of length $d$ to the finished prefix just below. A cell whose new block reaches position 0 computes only $G$.

## Example

Add $a = 182 = 10110110_2$ and $b = 91 = 01011011_2$ with $c_0 = 0$ and $n = 8$, the example of the [Kogge-Stone](/kogge-stone-adder/) page. The strings are written from position 7 down to position 0.

| step | $d$ | positions updated | $G$ after the step |
|---|---|---|---|
| L1 | | | $00010010$ |
| L5 | 1 | 1, 3, 5, 7 | $00110010$ |
| L5 | 2 | 3, 7 | $10111010$ |
| L5 | 4 | 7 | $10111010$ |
| L9 | 2 | 5 | $10111010$ |
| L9 | 1 | 2, 4, 6 | $11111110$ |

After the up-sweep, positions 0, 1, 3 and 7 hold $G_{i:0}$. At the down level $d = 2$, position 5 joins its block $4..5$ to the prefix $0..3$ held by position 3. At $d = 1$, positions 2, 4 and 6 join their own bit to the prefixes held by 1, 3 and 5. The carries $c_8 \cdots c_1$ are $11111110$, the sum bits are $p \oplus c = 11101101 \oplus 11111100 = 00010001$, and the result is $1\,0001\,0001_2 = 273$. The network has 11 cells in 5 levels and depth 12, where Kogge-Stone has 17 cells in 3 levels and depth 9.

## Correctness

Say that position $i$ *holds the block* $k..i$ when $(G[i], P[i]) = (G_{i:k}, P_{i:k})$; at the start, after line L2, position $i$ holds $i..i$, with position 0 including the carry-in. A cell is correct when position $i - d$ holds a block that ends right below the block of $i$, since $\circ$ then joins two adjacent blocks.

- **After the up-sweep**, by induction on $d$: if $2^t$ is the largest power of 2 that divides $i + 1$ and $2^t \le n$, position $i$ holds the block of length $2^t$ ending at $i$. In particular, position $2^k - 1$ holds $0..2^k - 1$.
- **In the down-sweep**, levels go from large $d$ to small. At level $d$, position $i$ has $i + 1 = (2m + 1) d$, so after the up-sweep it holds the block of length $d$ ending at $i$. Position $i - d$ has $i - d + 1 = 2md$, a multiple of $2d$; either it is a power of 2, so it was finished in the up-sweep, or its own down-sweep cell was at a level larger than $d$. Either way it holds $0..i - d$, and the cell gives position $i$ the block $0..i$.

Every position $i \ge 1$ with $i + 1$ not a power of 2 gets exactly one down-sweep cell, at $d$ equal to the largest power of 2 that divides $i + 1$. So in the end every position holds $0..i$, $c_{i+1} = G_{i:0}$, and $s_i = p_i \oplus c_i$ is the sum bit. The full proof is below.

## Complexity

**Cells, proved.** Position $i$ gets one up-sweep cell for each $d$ with $2d \mid i + 1$, which is $\nu_2(i + 1)$ cells, where $\nu_2$ is the exponent of 2. By Legendre's formula, $\sum_{m=1}^{n} \nu_2(m) = n - s_2(n)$, where $s_2(n)$ is the number of 1s in the binary form of $n$. The down-sweep has one cell for each position $i < n$ such that $i + 1$ is not a power of 2, which is $n - 1 - \lfloor \log_2 n \rfloor$ cells. So the network has

$$2n - 1 - s_2(n) - \lfloor \log_2 n \rfloor$$

cells, which is $2n - 2 - L$ for $n = 2^L$; for $n = 64$ it is 120 and for $n = 1024$ it is 2036. The test script checks the formula for every $n < 300$.

**Levels, proved.** The up-sweep level $d$ is not empty when $2d \le n$, and the down-sweep level $d$ when $3d \le n$, so there are $\lfloor \log_2 n \rfloor + \lfloor \log_2 (n/3) \rfloor + 1$ levels for $n \ge 3$, which is $2L - 1$ for $n = 2^L$.

**Size.** Each cell has at most 3 gates. Lines L1, L2 and L12 add $3n + 2$ gates. So the size is at most $3(2n) + 3n + 2 = O(n)$, and it is $\Theta(n)$ because each input enters a gate. For $n = 8$ there are 52 gates, for $n = 1024$ there are 8159.

**Depth.** Line L1 gives each signal at time 1 and line L2 gives $g_0$ at time 3. Each level of cells adds at most 2, so after $t$ levels every $G$ is ready by time $3 + 2t$, and the sum bits by time $2t + 4$. With the level count above, the depth is at most $2(2L - 1) + 4 = 4L + 2$ for $n = 2^L$, which is $\Theta(\log n)$. The test script observes depth exactly $4L$ for $4 \le n = 2^L \le 1024$, two less than the bound, because the cell chain that starts at $g_0$ is not the longest path. Kogge-Stone has depth $2L + 3$ on the same model.

**Simulation.** Evaluating the network sequentially costs time proportional to its size, $\Theta(n)$, which is the `time` entry of the front matter, and the extra space is the $\Theta(n)$ signals.

## Properties

- **Linear size.** About $2n$ cells, the fewest among the classical logarithmic-depth prefix networks. Snir's lower bound for prefix circuits says that size plus depth is at least about $2n - 2$, and Brent-Kung is close to it.
- **About twice the minimal depth.** $2\log_2 n - 1$ levels against $\log_2 n$ for [Kogge-Stone](/kogge-stone-adder/) and [Sklansky](/sklansky-adder/).
- **Low fan-out per level.** In each level, each cell output feeds at most one cell of that level besides its own position. A finished prefix such as position $2^k - 1$ is read at several levels, and layouts carry it down through buffers or wires.
- **Few wiring tracks.** At most one long wire crosses each place per level, and the layout is a binary tree, which gave the area $O(n \log n)$ in the original paper.
- **All prefixes.** Every carry is computed, so the network also gives comparison and increment.

## Variants and improvements

- **[Kogge-Stone](/kogge-stone-adder/).** Minimal depth with about $n \log_2 n$ cells and fan-out 2.
- **[Sklansky](/sklansky-adder/).** Minimal depth with $\frac{n}{2} \log_2 n$ cells and fan-out up to $n/2$.
- **Han-Carlson.** One Brent-Kung level before and after a Kogge-Stone network on the odd positions, a mix of the two.
- **Ladner-Fischer.** A family of prefix networks that trades depth for size, with Brent-Kung's shape at one end of the range (Ladner and Fischer, 1980).
- **Higher radix.** Joining $r$ blocks at a time instead of 2 gives the hierarchical [carry-lookahead adder](/carry-lookahead-adder/) with $r$-input lookahead units.
- **Prefix sums.** The same up-sweep and down-sweep compute the [prefix sums](/prefix-sums/) of any associative operator with $O(n)$ work and $O(\log n)$ span, as in Blelloch's scan.

## When to use it

Use a Brent-Kung adder when area, wiring or power matter more than the last few gate delays: wide adders off the critical path, low-power designs, and adders in FPGAs and small processors. It is also the textbook example of a work-efficient parallel prefix. When delay matters most, [Kogge-Stone](/kogge-stone-adder/) or a hybrid such as Han-Carlson is faster; for narrow adders a [ripple-carry adder](/ripple-carry-adder/) is smaller still.

## Pitfalls

- **Starting the down-sweep at the top.** After the up-sweep, $d$ is the first power of 2 that is at least $n$, and line L7 divides it by 4. Starting at $d/2$ is harmless, since that level is empty, but starting from 1 and going up, as in the up-sweep, makes a cell read a prefix that is not yet finished. The levels of line L9 must go from large $d$ to small.
- **Wrong positions in the down-sweep.** Line L9 updates $i$ with $i \equiv d - 1 \pmod{2d}$ and $i \ge 3d - 1$. Including $i = d - 1$ makes it read position $-1$, and using $i \equiv 2d - 1$, the up-sweep rule, combines blocks that are not adjacent.
- **Combining in the wrong order.** The operator $\circ$ is not commutative: the high block goes on the left. Writing $(G[i - d], P[i - d]) \circ (G[i], P[i])$ in lines L5 or L9 gives wrong carries when the low block generates and the high block kills.
- **Forgetting the carry in.** Without line L2 the network adds $a + b$ only. The carry-in must be folded into $g_0$ before the prefix network, or treated as an extra position.

## Implementations

## History

Prefix computation with a tree of linear size and logarithmic depth was studied by Ofman (1962) for addition and by Ladner and Fischer (1980) for general associative operators. Brent and Kung (1982) wrote the carry computation as a prefix problem with the operator $\circ$, gave the up-and-down tree network, and showed a regular layout with area $O(n \log n)$ and depth $O(\log n)$ in the VLSI model. The name Brent-Kung adder now refers to this network. Kogge and Stone's recursive doubling (1973) is the minimal-depth alternative, and later work by Han and Carlson (1987) and Knowles (1999) filled in the space between them.

## References

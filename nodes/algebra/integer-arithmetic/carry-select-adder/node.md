---
tag: 0D2Z2R
kind: algorithm
slug: carry-select-adder
name: Carry-select adder
aliases:
- conditional sum adder
- CSLA
area: algebra/integer-arithmetic
level: advanced
summary: Computes blocks of sums for both carry-in values and selects the correct one.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(n^(1/2))}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Bedrij described the carry-select adder in 1962; Sklansky's conditional-sum adder of 1960 applies the same selection recursively.
prereqs: [ripple-carry-adder, carry-propagation, boolean-circuit]
see_also: [carry-skip-adder, carry-lookahead-adder, ripple-carry-adder, kogge-stone-adder, sklansky-adder, brent-kung-adder, integer-addition]
sources:
  - paper: doi:10.1109/IRETELC.1962.5407919
    title: O. J. Bedrij, Carry-select adder, IRE Transactions on Electronic Computers EC-11(3), 1962
    locator: pp. 340 to 346
  - paper: doi:10.1109/TEC.1960.5219822
    title: J. Sklansky, Conditional-sum addition logic, IRE Transactions on Electronic Computers EC-9(2), 1960
    locator: pp. 226 to 231 (the recursive form of carry selection)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 7, Variations in fast adders, Sections 7.3 and 7.4 (carry-select adders, and the conditional-sum adder)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (carry-select and conditional-sum adders)
---

A carry-select adder splits an $n$-bit addition into blocks and adds each block twice at the same time, once as if the carry into the block were 0 and once as if it were 1. When the real carry into a block arrives, it only has to choose one of the two ready results, and the choice also gives the carry into the next block. So the carry crosses each block in two gate delays instead of two per bit. With blocks of about $\sqrt{n}$ bits the depth is about $4\sqrt{n}$; with blocks that grow by one bit each, it is about $2\sqrt{2n}$. The size stays linear, about twice that of a [ripple-carry adder](/ripple-carry-adder/). Bedrij described the scheme in 1962. Applied recursively, so that each half of each block is itself selected, it becomes Sklansky's conditional-sum adder, with logarithmic depth.

## In plain words

In a plain adder, each position waits for the carry from its right, so the carry crawls through all $n$ positions. A carry-select adder cuts the number into blocks and asks, for every block at once: what would the answer be if a carry came in, and what if none came in? Both answers are worked out in parallel, before anyone knows which one is needed.

The first block is added normally. Its carry out tells the second block which of its two answers is right; that answer comes with its own carry out, which tells the third block, and so on. Picking an answer is fast, so the carry moves quickly from block to block. The price is doing most of the work twice.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$, with $n \ge 1$, and a carry-in bit $c_0$. The output is the $n + 1$ bits of $a + b + c_0$, the fixed-width [integer addition](/integer-addition/). The adder is also given block sizes $k_0, k_1, \ldots, k_{t-1} \ge 1$ with sum $n$, low block first.

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates of fan-in 2 and unit delay; a NOT is an XOR with the constant 1. The size, given in the field `time`, is the number of gates; the depth is the number of gates on the longest path. The depth formulas below are proved and also checked exactly by the test script, and the size bound is proved. The front matter states the depth for block sizes of order $\sqrt{n}$.

## The algorithm

Each position has $g_i = a_i \wedge b_i$ and $p_i = a_i \oplus b_i$, and a ripple step is $s_i = p_i \oplus c_i$, $c_{i+1} = g_i \vee (p_i \wedge c_i)$. With a constant carry the first step of a block simplifies: with carry 0 it is $s = p$, $c = g$, and with carry 1 it is $s = \neg p$, $c = g \vee p$.

```pseudo id=main
CARRY-SELECT-ADD(a, b, c_in, k[0..t − 1])        ▷ n bits, low first; blocks of sizes k[j]
L1  for all i in parallel: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  ripple through block 0 with carry c_in, giving its sums and its carry out C
L3  for each block j ≥ 1, in parallel:
L4      ripple through block j twice, from carry 0 and from carry 1, giving sums s⁰, s¹ and carries out C⁰[j], C¹[j]
L5  for j ← 1 to t − 1 do                         ▷ the selection chain
L6      x ← C                                      ▷ the real carry into block j
L7      for each position i of block j: s[i] ← s⁰[i] ⊕ (x ∧ (s⁰[i] ⊕ s¹[i]))
L8      C ← C⁰[j] ∨ (C¹[j] ∧ x)
L9  return s[0 .. n − 1] and the carry out C
```

Line L7 is a multiplexer: it gives $s^0_i$ when $x = 0$ and $s^1_i$ when $x = 1$. Line L8 is a multiplexer for the carry out, simplified because $C^0[j] \le C^1[j]$: a block that sends a carry with carry-in 0 also sends one with carry-in 1. The differences $s^0_i \oplus s^1_i$ are computed in the parallel part, before the carry arrives.

## Example

Add $a = \texttt{B6D3}_{16}$ and $b = \texttt{69E5}_{16}$ with $c_0 = 0$, $n = 16$ and four blocks of 4 bits. The nibbles are written high bit first.

| block $j$ | $a$ nibble | $b$ nibble | $s^0$, $C^0$ (L4) | $s^1$, $C^1$ (L4) | carry in $x$ (L6) | chosen sum (L7) | carry out (L8) |
|---|---|---|---|---|---|---|---|
| 0 | 0011 | 0101 | | | $c_0 = 0$ | 1000 (L2) | 0 |
| 1 | 1101 | 1110 | 1011, 1 | 1100, 1 | 0 | 1011 | 1 |
| 2 | 0110 | 1001 | 1111, 0 | 0000, 1 | 1 | 0000 | 1 |
| 3 | 1011 | 0110 | 0001, 1 | 0010, 1 | 1 | 0010 | 1 |

The result is $1\,0010\,0000\,1011\,1000_2 = \texttt{120B8}_{16} = 73912 = 46803 + 27109$. Block 2 is the case where the choice matters: it is all propagate, so its two results differ in every bit and in the carry. Block 1 sends a carry whatever comes in, which is why its two carry outs are both 1. The circuit has 146 gates and depth 15; a 16-bit ripple-carry adder of the same gates has depth 33.

## Correctness

Fix a block $j \ge 1$ that covers positions $\ell..u$. Ripple addition is correct for each carry-in, so $(s^0, C^0[j])$ are the sum bits and carry out of $a_{u..\ell} + b_{u..\ell} + 0$, and $(s^1, C^1[j])$ those of $a_{u..\ell} + b_{u..\ell} + 1$. By induction on $j$, the value $x$ in line L6 is the true carry $c_\ell$ into the block: for $j = 1$ it is the carry out of block 0, computed by ripple from $c_0$; for larger $j$, line L8 of the previous step chose the carry out that belongs to the true carry into the previous block. Since $C^0[j] \le C^1[j]$, the formula $C^0[j] \vee (C^1[j] \wedge x)$ equals $C^x[j]$, and line L7 gives $s^x$. So every block outputs the bits of its sum with its true carry-in, which is the sum of the whole numbers. The full proof is below.

## Complexity

**Depth, proved.** Line L1 gives $g$ and $p$ at time 1, and each ripple step adds 2. So block 0 sends its carry at time $1 + 2k_0$. In block $j$, the carry out with carry-in 1 is ready at time $2k_j$ and the differences of line L7 by time $2k_j$. Write $T_j$ for the time at which the carry into block $j$ arrives. Then $T_1 = 1 + 2k_0$ and $T_{j+1} = \max(T_j, 2k_j) + 2$, and the sums of block $j$ are ready at $\max(T_j, 2k_j) + 2$.

- **Uniform blocks** of size $k$, with $t \ge 2$ blocks: $2k_j \le 2k < T_j$ for all $j$, so $T_j = 2k + 2j - 1$ and the depth is $2k + 2t - 1$. With $k = \sqrt{n}$, $t = \sqrt{n}$ and the depth is $4\sqrt{n} - 1$; for $n = 64$ and $k = 8$ it is 31, against $2n + 1 = 129$ for ripple.
- **Growing blocks** $k_0, k_0, k_0 + 1, k_0 + 2, \ldots$, the last block cut to fit: block $j \ge 1$ has $k_j = k_0 + j - 1$, so $2k_j \le T_j = 2k_0 + 2j - 1$ and every block is ready when its carry arrives. The depth is $2k_0 + 2(t - 1) + 1$. With $k_0 = 1$, $n \ge 1 + \sum_{j=1}^{t-2} j + 1 > (t - 1)(t - 2)/2$, so $(t - 2)^2 < 2n$, $t < \sqrt{2n} + 2$, and the depth $2t + 1$ is less than $2\sqrt{2n} + 5$. For $n = 64$ it is 25; for $n = 1024$ it is 93, against 127 for uniform blocks of 32.

The test script checks both formulas exactly for every $n < 70$ and every block size, and the bound for the squares $n \le 529$. The depth is $\Theta(\sqrt{n})$ for these schedules, and no choice of one-level block sizes does better than order $\sqrt{n}$, since a schedule with $t$ blocks pays 2 gate levels per block on the selection chain, and its largest block, of at least $n/t$ bits, needs about $2n/t$ levels for its ripple, and $\max(2t, 2n/t) \ge 2\sqrt{n}$.

**Size, proved.** Each position of block 0 costs at most 5 gates, and each position of a later block at most 11: 2 for $g$ and $p$, at most 3 in each of the two ripple copies, 1 for the difference and 2 for the selection. Each block adds 2 gates for line L8. So the size is at most $11n + 2t = \Theta(n)$, about twice the $5n$ of a ripple-carry adder. For $n = 1024$ with blocks of 32 it is 11010 gates.

**Simulation.** Evaluating the circuit sequentially takes time proportional to its size, $\Theta(n)$, the `time` entry of the front matter.

## Properties

- **Delay independent of the data.** Every block is added in both ways for every input, so the delay is the depth above for every input, unlike a [carry-skip adder](/carry-skip-adder/), whose worst path depends on the block structure in a similar way but saves the duplicated hardware.
- **Twice the adder hardware.** Each later block holds two adders, and a multiplexer per sum bit. This doubles area and power, which is the main cost of the scheme.
- **Composable.** The two copies inside each block can be any adder: ripple, [carry-lookahead](/carry-lookahead-adder/) or a prefix network. The selection chain can itself be replaced by a lookahead tree over the block carries.
- **Simple wiring.** The block carry chain runs in one direction, and each multiplexer reads one carry, so the layout is regular.

## Variants and improvements

- **Conditional-sum adder.** Sklansky (1960) applied the selection recursively: each half of a block is computed for both carry-ins, and the pair of results for the block is built from the pairs of its halves by selection. The depth is $O(\log n)$ and the size $O(n \log n)$, and the selection tree is the network of the [Sklansky adder](/sklansky-adder/).
- **Square-root block sizes.** The growing schedule above, with each block one bit longer than the previous, balances the two arrival times at each block; this is the usual textbook design.
- **Multilevel carry select.** Blocks of blocks, with selection at both levels, reduce the depth further at the cost of more hardware; carried to $\log_2 n$ levels this is the conditional-sum adder.
- **Add-one select.** Instead of a second adder, compute $s^1$ from $s^0$ by an incrementer, or by the observation that $s^1 = s^0 + 1$ flips the trailing run of 1s; this saves area.
- **Carry select on prefix networks.** Wide fast adders often compute sparse carries with a [Kogge-Stone](/kogge-stone-adder/) tree and fill the blocks between them by carry selection.

## When to use it

Use a carry-select adder when a ripple-carry adder is too slow but a full prefix network is too complex, typically for widths of 16 to 64 bits in area-tolerant designs, or as the block-level stage of a larger adder. It is also used in FPGAs, where the fast carry chains make the two block adders cheap. Avoid it when power and area are tight; the [carry-skip adder](/carry-skip-adder/) reaches the same order of depth with almost no extra hardware, and the [Brent-Kung](/brent-kung-adder/) adder reaches logarithmic depth with linear size.

## Pitfalls

- **Selecting the carry out with the sums.** Line L8 must choose between $C^0[j]$ and $C^1[j]$ by the carry into the block; using the carry out of block 0 for every block, as if it reached all blocks at once, is wrong. The right carry into block $j$ is the carry chosen at block $j - 1$ (line L6).
- **Equal blocks that are too small.** With $k = 1$ the selection chain has $n$ steps and the depth is $2n + 1$, the same as ripple; with $k = n$ there is no selection. The depth $2k + 2t - 1$ is minimized at $k = \sqrt{n}$, and growing blocks do better still.
- **A full multiplexer for the carry.** Writing the carry selection as $(C^0 \wedge \neg x) \vee (C^1 \wedge x)$ is correct but needs an inverter and an extra gate on the critical path. Line L8 uses $C^0 \le C^1$ to drop the inverted term.
- **Growing the first block.** The growing schedule must start with two blocks of the same size $k_0$, because block 0 has no head start: its carry out arrives at $1 + 2k_0$, and block 1 is ready at $2k_1$, so $k_1 = k_0$, not $k_0 + 1$.

## Implementations

## History

Sklansky described conditional-sum addition in 1960, the recursive form in which every block computes both results. Bedrij's paper of 1962 gave the one-level carry-select adder with blocks and multiplexers. Both came from the early search for fast adders for transistor computers, together with carry lookahead (Weinberger and Smith, 1958) and carry skip (Lehman and Burla, 1961). Carry selection remains a standard component of high-speed adder designs, usually combined with prefix networks.

## References

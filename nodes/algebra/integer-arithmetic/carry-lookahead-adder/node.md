---
tag: ZGRFB8
kind: algorithm
slug: carry-lookahead-adder
name: Carry-lookahead adder
aliases:
- CLA
- block carry-lookahead adder
- hierarchical carry-lookahead adder
area: algebra/integer-arithmetic
level: advanced
summary: Computes carries from generate and propagate signals in logarithmic depth.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Weinberger and Smith described carry lookahead in 1958 and MacSorley surveyed it in 1961; the 4-bit lookahead unit became a standard part in the 1970s.
prereqs: [ripple-carry-adder, carry-propagation, boolean-circuit]
see_also: [kogge-stone-adder, brent-kung-adder, sklansky-adder, carry-skip-adder, carry-select-adder, parallel-prefix, integer-addition]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 6, Carry-lookahead adders, Sections 6.1 and 6.2 (unrolling the carry recurrence and the design of multilevel lookahead adders)
  - paper: doi:10.1109/JRPROC.1961.287779
    title: O. L. MacSorley, High-speed arithmetic in binary computers, Proceedings of the IRE 49(1), 1961
    locator: pp. 67 to 91 (the section on carry lookahead adders)
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 29, Arithmetic circuits, Section 29.2, Addition circuits (carry-lookahead addition as a prefix computation on the kill, propagate and generate status)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 2, Two-operand addition (carry-lookahead adders and their multilevel form)
---

A carry-lookahead adder computes the carries of an $n$-bit addition from the *generate* and *propagate* signals of the bit positions, without waiting for each carry to move one place at a time as in a [ripple-carry adder](/ripple-carry-adder/). The positions are grouped into blocks of $r$, usually $r = 4$. A lookahead unit computes the generate and propagate signals of its block, and the units form a tree of height $h = \lceil \log_r n \rceil$. Signals go up the tree and carries come back down, so every carry is ready after at most $4h$ gate delays, while the size of the circuit stays linear in $n$. This hierarchical form, with 4-bit units, is the classic carry-lookahead adder of computer arithmetic. The same idea with two-input cells and a different tree shape gives the [parallel prefix](/parallel-prefix/) adders: [Brent-Kung](/brent-kung-adder/), [Kogge-Stone](/kogge-stone-adder/) and [Sklansky](/sklansky-adder/).

## In plain words

When you add two binary numbers, the slow part is the carry. In the plain method, each position waits for the carry from the position to its right, so a carry can take $n$ steps to cross the whole number.

A lookahead adder asks two questions about each position, and then about each block of positions. Does this block make a carry by itself? And would it pass on a carry that comes in from the right? Both answers can be found from the inputs, without knowing any carry. A small unit answers the questions for a block of four positions. A second layer of units answers them for blocks of sixteen, and so on. Once the top knows the answers for big blocks, the carries come back down the layers, and each position gets its carry after a few steps per layer.

## The problem

The input is two $n$-bit numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{n-1} \cdots b_0)_2$ and a carry-in bit $c_0$. The output is the $n + 1$ bits of $a + b + c_0$: the sum bits $s_0, \ldots, s_{n-1}$ and the carry out $c_n$. This is fixed-width [integer addition](/integer-addition/) in base 2.

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates, each with unit delay. The lookahead units have $r$ children, a constant, and their gates have fan-in at most $r + 1$. The size, given in the field `time`, is the number of gates; the depth is the number of gates on the longest path from an input to an output. The order bounds $\Theta(n)$ and $\Theta(\log n)$ below are proved for each fixed $r \ge 2$. The exact gate counts and depths are counted by the test script; the formula $4h$ is proved as an upper bound and observed to be exact for $r \ge 3$ when $n = r^h$.

## The algorithm

For each position, $g_i = a_i \wedge b_i$ says that position $i$ makes a carry, and $p_i = a_i \oplus b_i$ that it passes an incoming carry on. The carry recurrence is $c_{i+1} = g_i \vee (p_i \wedge c_i)$; unrolled over a block of $m$ consecutive positions or sub-blocks with signals $(g_0, p_0), \ldots, (g_{m-1}, p_{m-1})$, low first, it gives the *lookahead formula*

$$c_k = g_{k-1} \vee p_{k-1} g_{k-2} \vee p_{k-1} p_{k-2} g_{k-3} \vee \cdots \vee p_{k-1} \cdots p_1 g_0 \vee p_{k-1} \cdots p_0\, c ,$$

where $c$ is the carry into the block and $c_k$ the carry into its member $k$. The block's own signals are $G = $ the formula for $c_m$ without its last term, and $P = p_{m-1} \cdots p_0$, so that the carry out of the block is $G \vee P c$. Each formula is one level of AND gates and one OR gate.

```pseudo id=main
CLA-ADD(a, b, c0, r)                          ▷ n bits each, low first; units with r children
L1  for each i: g[i] ← a[i] ∧ b[i];  p[i] ← a[i] ⊕ b[i]
L2  level[0] ← the leaves (g[i], p[i]), i = 0..n − 1;  h ← 0
L3  repeat                                     ▷ the upward pass
L4      h ← h + 1;  cut level[h − 1] into groups of r consecutive nodes, low first
L5      for each group that is not the only one: G ← g[m−1] ∨ p[m−1] g[m−2] ∨ ⋯ ∨ p[m−1] ⋯ p[1] g[0];  P ← p[m−1] ⋯ p[0]
L6  until level[h] has one node, the root
L7  carry-in of the root ← c0                  ▷ the downward pass
L8  for each node, from the root down, with carry-in c and children 0..m − 1:
L9      carry-in of child 0 ← c;  carry-in of child k ← the lookahead formula c_k, for k = 1..m − 1
L10 c_n ← the lookahead formula c_m at the root
L11 for each i: s[i] ← p[i] ⊕ (carry-in of leaf i)
L12 return s[0..n − 1] and c_n
```

In line L5, $(g[j], p[j])$ are the signals of the $j$-th child of the group, and $m \le r$ is the number of children. A group with one child passes its child's signals on with no gates. The root's own $G$ and $P$ are not needed, since line L10 computes the carry out directly. With $r = 4$, each node of the tree is one 4-bit lookahead unit of the classic design, and an adder of 16 bits uses four units in the first level and one in the second.

## Example

Add $a = 1010\,0111_2 = 167$ and $b = 0101\,1001_2 = 89$ with $c_0 = 0$, $n = 8$ and $r = 4$. The bits are listed from position 0 up.

| position $i$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $a_i$ | 1 | 1 | 1 | 0 | 0 | 1 | 0 | 1 |
| $b_i$ | 1 | 0 | 0 | 1 | 1 | 0 | 1 | 0 |
| $g_i$ (L1) | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| $p_i$ (L1) | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| carry $c_i$ (L9) | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| $s_i$ (L11) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

The upward pass (L3 to L6) has two groups at level 1: the low block, positions 0 to 3, has $G_0 = g_3 \vee p_3 g_2 \vee p_3 p_2 g_1 \vee p_3 p_2 p_1 g_0 = 0 \vee 0 \vee 0 \vee 1 = 1$ and $P_0 = 0$; the high block, positions 4 to 7, has $G_1 = 0$ and $P_1 = 1$. Level 2 is the root, and $h = 2$. In the downward pass, the root gives the carry $c_0 = 0$ to the low block and $c_4 = G_0 \vee P_0 c_0 = 1$ to the high block (L9), and $c_8 = G_1 \vee P_1 G_0 \vee P_1 P_0 c_0 = 1$ (L10). Inside the low block, $c_1 = g_0 = 1$, $c_2 = g_1 \vee p_1 g_0 = 1$ and $c_3 = 1$; inside the high block, every carry is $1$ because every $p_i$ is $1$ and the carry-in is $1$. All sum bits are $p_i \oplus c_i = 0$, and the result is $1\,0000\,0000_2 = 256 = 167 + 89$.

The carry made at position 0 travels through all 8 positions. A ripple-carry adder needs 8 carry steps for it; here the longest path has 7 gates, and the bound $4h = 8$ holds.

## Correctness

For a node $v$ of the tree, let $[\ell_v, u_v]$ be the positions of the leaves below it. Call $c^{\ast}_i$ the true carry into position $i$, defined by $c^{\ast}_0 = c_0$ and $c^{\ast}_{i+1} = g_i \vee p_i c^{\ast}_i$. The proof has two invariants.

- **Upward.** For each node $v$ other than the root, $c^{\ast}_{u_v + 1} = G_v \vee P_v c^{\ast}_{\ell_v}$, and $P_v = 1$ exactly when all $p_i$ with $i \in [\ell_v, u_v]$ are $1$. For a leaf this is the carry recurrence. For a group, it follows by unrolling the children's relations, which is the lookahead formula.
- **Downward.** For each node $v$, the carry-in assigned to $v$ in line L7 or L9 equals $c^{\ast}_{\ell_v}$. It holds at the root, which receives $c_0 = c^{\ast}_0$, and line L9 keeps it, because the lookahead formula for child $k$ is the unrolled carry recurrence across children $0, \ldots, k-1$, by the upward invariant.

So each leaf $i$ gets $c^{\ast}_i$, and $s_i = a_i \oplus b_i \oplus c^{\ast}_i$, which is the sum bit of position $i$; line L10 gives $c^{\ast}_n$. The full proof is below.

## Complexity

**Height.** Each pass of the loop L3 to L6 divides the number of nodes by $r$, rounded up, so the tree has $h = \max(1, \lceil \log_r n \rceil)$ levels above the leaves. This is proved and also checked by the tests.

**Depth, proved.** Line L1 gives every $g_i$ and $p_i$ at time 1. By induction, a node at level $\ell \ge 1$ has its $G$ at time at most $2\ell + 1$ and its $P$ at time at most $\ell + 1$, since one lookahead formula adds an AND level and an OR level. In the downward pass, the carries into the children of the root are ready at time at most $2h + 1$, and each level down adds at most 2, so the carry into each leaf is ready at time at most $4h - 1$. Line L11 adds one XOR, and line L10 finishes at time at most $2h + 1$. The depth is at most $4h = 4\lceil \log_r n \rceil$ for $n \ge 2$, which is $\Theta(\log n)$ for fixed $r$; the lower bound $\Omega(\log n)$ holds for every circuit of bounded fan-in, since $c_n$ depends on all $2n + 1$ inputs.

**Depth, observed.** For $n = r^h$ the test script measures depth exactly $4h$ for $r = 4$ (8 for 16 bits, 16 for 256 bits, 20 for 1024 bits) and $4h - 1$ for $r = 2$ with $h \ge 2$, where the root's carries skip one AND level. A ripple-carry adder of the same gates has depth about $2n$.

**Size, proved.** A group with $m \le r$ children uses at most $m + 1$ gates for $G$ and $P$ and at most $\sum_{k=1}^{m} (k + 1) = O(r^2)$ gates for the carries of lines L9 and L10, and a group with one child uses none. A tree with $n$ leaves has at most $n - 1$ groups with two or more children. Lines L1 and L11 add $3n$ gates. So the size is $O(r^2 n)$, which is $\Theta(n)$ for fixed $r$.

**Size, observed.** The script counts exactly $8n - 5$ gates for $r = 2$ and $(23n - 14)/3$ for $r = 4$, at $n = 4, 16, \ldots, 1024$, and at most $8n$ for $r = 4$ and every $n < 130$. For example, 16 bits with $r = 4$ use 118 gates. The largest fan-in is $r + 1$, reached by the last term of a carry formula with $m = r$.

**Simulation.** Evaluating the circuit sequentially takes time proportional to its size, $\Theta(n)$, which is the `time` entry of the front matter. The extra space is the $\Theta(n)$ signals of the tree.

## Properties

- **Linear size and logarithmic depth together.** The carry-lookahead adder is optimal in both measures up to constant factors among bounded fan-in circuits: size $\Theta(n)$ is needed to read the inputs, and depth $\Omega(\log n)$ to combine them.
- **Every carry is computed.** Unlike a [carry-skip adder](/carry-skip-adder/), whose delay depends on block sizes and on the worst carry chain, the lookahead adder computes each carry by a fixed formula, so its delay is the same for all inputs.
- **Group signals are reusable.** The $(G, P)$ outputs of a unit let the units be cascaded into wider adders; the 16-bit adder of four 4-bit adders and one lookahead unit is the textbook case.
- **Bounded fan-in, with a large constant.** Gates with fan-in 5 are slower than two-input gates in real logic, which is one reason designs move to two-input [parallel prefix](/parallel-prefix/) cells.

## Variants and improvements

- **Single-level lookahead.** Computing every $c_k$ for $k \le n$ directly from the lookahead formula gives depth 3 for all carries and 4 for the sums, a constant, but with fan-in $n + 1$ and $\Theta(n^2)$ gates. This shows that addition is in the circuit class of constant depth with unbounded fan-in, and it is practical only for small blocks.
- **Ripple between blocks.** Using lookahead inside 4-bit blocks and a ripple of the block carries $c_{4j+4} = G_j \vee P_j c_{4j}$ gives depth about $n/2$ with small units, a common middle ground in older designs.
- **Parallel prefix adders.** Writing the block signals as a [parallel prefix](/parallel-prefix/) computation with the associative operator $(G, P) \circ (G', P') = (G \vee P G', P P')$ and two-input cells gives the [Brent-Kung adder](/brent-kung-adder/) (the radix-2 form of this tree, $2 \log_2 n - 1$ levels of cells), the [Kogge-Stone adder](/kogge-stone-adder/) ($\log_2 n$ levels, $\Theta(n \log n)$ cells) and the [Sklansky adder](/sklansky-adder/) ($\log_2 n$ levels with high fan-out).
- **Ling adder.** Ling's 1981 variant computes a pseudo-carry $h_{i+1} = g_i \vee c_i$ that has a simpler formula, and recovers the carries at the end, saving a gate level in each unit.
- **Combination with selection.** Large adders often compute block sums for both carry-in values, as in a [carry-select adder](/carry-select-adder/), and use the lookahead tree only to pick between them.

## When to use it

Use a carry-lookahead adder when an adder must be fast for every input and the width is in the tens of bits or more: the arithmetic units of processors, address adders, and the final adders of tree multipliers such as the [Wallace tree](/wallace-tree-multiplier/). For small widths a [ripple-carry adder](/ripple-carry-adder/) is smaller and fast enough. For the fastest wide adders, two-input prefix networks such as [Kogge-Stone](/kogge-stone-adder/) or hybrids with carry selection are the usual choice. In software on a word RAM, carries between machine words are handled by the processor's add-with-carry instruction, and lookahead is not used; the idea appears in software only in bit-sliced and SIMD code.

## Pitfalls

- **Carry formula in the wrong order.** The formula in line L9 starts from the member just below $k$: $c_k = g_{k-1} \vee p_{k-1} g_{k-2} \vee \cdots$. Writing it from the bottom, $g_0 \vee p_0 g_1 \vee \cdots$, multiplies the propagate signals of the wrong members and gives wrong carries whenever the block mixes generate and propagate positions. The right form multiplies $g_j$ by the $p$ of every member above $j$ and below $k$.
- **Using the root's signals for the carry out.** If line L10 is replaced by $G_{\text{root}}$, the carry out ignores $c_0$; the correct carry out is $G_{\text{root}} \vee P_{\text{root}} c_0$, which line L10 computes in one formula.
- **Propagate as OR in the sum.** Inside the tree, $p_i = a_i \vee b_i$ also works, since $g_i = 1$ covers the case $a_i = b_i = 1$. But line L11 needs $p_i = a_i \oplus b_i$ for the sum bit; using the OR form there gives $s_i = 0$ instead of $1$ when $a_i = b_i = 1$ and $c_i = 1$.
- **Mixing levels.** The carry into a child must come from its parent (line L9), not from the root's formula at the leaf level. Computing all leaf carries from the root's children with one huge formula is the single-level adder, with fan-in growing with $n$.

## Implementations

## History

The idea of anticipating carries is old; Babbage designed an "anticipating carriage" for his engines in the nineteenth century. For electronic computers, Weinberger and Smith described carry lookahead in "A logic for high-speed addition" (1958), and MacSorley's survey of 1961 explained lookahead adders with groups and multilevel units, which became the standard approach for fast adders. Ofman showed in 1962 that addition has circuits of depth $O(\log n)$ and size $O(n)$. In the 1970s, 4-bit adder and lookahead carry chips such as the 74181 4-bit ALU and the 74182 lookahead carry generator made the hierarchical scheme a common building block. Brent and Kung (1982) recast the lookahead tree as a parallel prefix network with a regular layout, and the later prefix adders grew from that view.

## References

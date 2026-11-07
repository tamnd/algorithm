---
tag: N0JM8H
kind: algorithm
slug: wallace-tree-multiplier
name: Wallace tree multiplier
aliases:
- Wallace tree
- Wallace multiplier
- carry-save adder tree multiplier
area: algebra/integer-arithmetic
level: advanced
summary: Hardware multiplier that sums partial products with a tree of carry-save adders.
solves: [integer-multiplication]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
prereqs: [carry-save-addition, multi-operand-addition, array-multiplier]
see_also: [dadda-multiplier, array-multiplier, booth-multiplication, carry-save-addition, multi-operand-addition, kogge-stone-adder, schoolbook-multiplication, integer-multiplication]
sources:
  - paper: C. S. Wallace, A suggestion for a fast multiplier, IEEE Transactions on Electronic Computers EC-13(1), 1964
    title: C. S. Wallace, A suggestion for a fast multiplier
    locator: pp. 14 to 17 (the tree of carry-save adders for the partial products, and a final fast adder)
  - paper: L. Dadda, Some schemes for parallel multipliers, Alta Frequenza 34, 1965
    title: Luigi Dadda, Some schemes for parallel multipliers
    locator: the column view of the reduction and the sequence of maximal heights 2, 3, 4, 6, 9, 13, 19
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 8, Multioperand addition (Wallace and Dadda trees), and Chapter 11, Tree and array multipliers
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 4, Multiplication (reduction of the partial product matrix by trees of counters)
---

A Wallace tree multiplier forms all $n^2$ partial product bits $a_i b_j$ of two $n$-bit numbers at once, with one AND gate each, and adds them with a tree of full adders that never propagates a carry. Each level of the tree takes the bits of every column in groups of three and replaces each group by a sum bit in the same column and a carry bit in the next, so a column of height $h$ shrinks to about $2h/3$. After about $\log_{3/2}(n/2)$ levels every column holds at most two bits, and one fast carry-propagate adder, such as a [Kogge-Stone adder](/kogge-stone-adder/), adds the two remaining rows. The circuit has $\Theta(n^2)$ gates and depth $\Theta(\log n)$, against depth $\Theta(n)$ for an [array multiplier](/array-multiplier/) of the same size. C. S. Wallace proposed it in 1964, and with Dadda's refinement of 1965 it is the standard structure of the multipliers in processors.

## In plain words

Multiplying two binary numbers on paper gives a stack of shifted copies of the first number, one for each 1 in the second, and the stack must be added up. Adding the rows one at a time is slow, because each addition waits for its carries.

A full adder takes three bits of the same column and gives two bits: a sum bit that stays in the column and a carry bit that moves one column left. The total value does not change, but three bits became two. A Wallace tree does this everywhere at once: in every column, every group of three bits goes through its own full adder. After one round each column has about two thirds of its bits. Round after round the stack gets lower, until only two rows are left, and these two are added by one ordinary fast adder.

## The problem

The input is two unsigned numbers $a = (a_{n-1} \cdots a_0)_2$ and $b = (b_{m-1} \cdots b_0)_2$, usually with $m = n$. The output is the $n + m$ bits of the product $ab$; see [integer multiplication](/integer-multiplication/). Since $ab = \sum_{i,j} a_i b_j 2^{i+j}$, the product is the sum of the $nm$ bits $a_i b_j$, where the bit $a_i b_j$ has weight $2^{i+j}$ and stands in column $i + j$. The column $k$ holds $\min(k, n - 1, m - 1, n + m - 2 - k) + 1$ bits, at most $\min(n, m)$.

**Cost model.** [Boolean circuit](/boolean-circuit/) with AND, OR and XOR gates of fan-in 2. The size, given in the field `time`, is the number of gates, and the depth is the number of gates on the longest path from an input to an output. A full adder is 5 gates of depth 3 for the carry and 2 for the sum, a half adder 2 gates of depth 1. The level counts and size bounds below are proved; the gate counts and depths for given $n$ were measured by the implementation. Wire length and layout are not counted by the model.

## The algorithm

```pseudo id=main
WALLACE-MULTIPLY(a[0 .. n − 1], b[0 .. m − 1])
L1  for all i, j in parallel: put a[i] ∧ b[j] into column i + j
L2  while some column holds more than two bits do      ▷ one level of the tree
L3      for every column k in parallel:
L4          split the bits of column k into groups of three, and a rest of 0, 1 or 2 bits
L5          each group of three → a full adder: its sum bit to column k, its carry bit to column k + 1
L6          a rest of two bits → a half adder, the same way; a rest of one bit stays in column k
L7  X, Y ← the two rows formed by the first and the second bit of every column (0 where missing)
L8  return X + Y, by one carry-propagate adder of width n + m
```

All the full adders of one level work at the same time on the bits that the previous level produced, so a level costs the delay of one full adder whatever the width. Line L6 is Wallace's original rule, which reduces as early as possible. Dadda's variant uses as few adders as possible in each level and leaves the rest of the work to later levels; see Variants.

## Example

Multiply $a = 182 = 10110110_2$ by $b = 91 = 01011011_2$, with $n = m = 8$. Line L1 puts 64 bits into 15 columns. The column heights, from column 0 to column 15, change level by level as follows; the table was produced by the implementation.

| level | column heights, columns 0 to 15 | highest |
|---|---|---|
| start | 1 2 3 4 5 6 7 8 7 6 5 4 3 2 1 0 | 8 |
| 1 | 1 1 2 3 3 4 5 5 6 4 4 4 2 2 2 0 | 6 |
| 2 | 1 1 1 2 2 3 3 4 4 4 3 3 2 2 2 1 | 4 |
| 3 | 1 1 1 1 2 2 2 3 3 3 2 2 2 2 2 2 | 3 |
| 4 | 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2 2 | 2 |

In level 1, column 7 holds 8 bits: two full adders take six of them and leave a sum bit each, and a half adder takes the last two, so 3 bits stay; column 8 receives those 3 carries and keeps 3 bits of its own 7, so it has 6. After four levels no column holds more than two bits, and the final adder gives $16562 = 182 \cdot 91$. The tree used 36 full adders and 25 half adders; the whole circuit, with the 64 AND gates and a 16-bit Kogge-Stone adder, has 489 gates and depth 22. The test of this page checks the product, the heights and these counts.

## Correctness

A full adder on bits $x, y, z$ of column $k$ outputs $s = x \oplus y \oplus z$ and $c = \mathrm{maj}(x, y, z)$ with $x + y + z = s + 2c$, so the weighted value $x 2^k + y 2^k + z 2^k$ equals $s 2^k + c 2^{k+1}$. A half adder satisfies $x + y = (x \oplus y) + 2(x \wedge y)$ in the same way. So the quantity $V = \sum_k 2^k \cdot (\text{sum of the bits in column } k)$ is the same after every level, and it starts as $\sum_{i,j} a_i b_j 2^{i+j} = ab$. When the loop stops every column has at most two bits, so $V = X + Y$, and line L8 returns $ab$. The loop stops because each full adder lowers the total number of bits by one, and a level in which some column holds three or more bits uses at least one full adder. The full proof, with the bound on the number of levels, is below.

## Complexity

**Levels.** Let $d_0 = 2$ and $d_{j+1} = \lfloor 3 d_j / 2 \rfloor$, the sequence 2, 3, 4, 6, 9, 13, 19, 28, 42, 63, 94 of Dadda. If every column has at most $d_{j+1}$ bits, then after one level every column has at most $d_j$: a column of height $h$ keeps $\lceil h / 3 \rceil$ bits or fewer of its own and receives at most $\lfloor (h' + 1) / 3 \rfloor$ carries from a column of height $h'$, and for $h, h' \le d_{j+1}$ the two together are at most $\lceil d_{j+1}/3 \rceil + \lfloor (d_{j+1} + 1)/3 \rfloor = \lceil 2 d_{j+1} / 3 \rceil \le d_j$. So the number of levels is at most the least $L$ with $d_L \ge \min(n, m)$, which is $\log_{3/2} n + O(1)$. For $n = 8, 16, 24, 32, 53, 64$ the tree has $4, 6, 7, 8, 9, 10$ levels. For $k$ rows of equal width this tree needs exactly that many levels; for the triangle of a multiplier, a column receives its carries from a shorter neighbour, and the measured count is one less for $n = 20$ and $n = 29$, the only such cases for $n < 90$.

**Depth.** The AND gates have depth 1, each level adds at most 3, and a Kogge-Stone adder of width $n + m$ adds at most $2\lceil \log_2 (n + m) \rceil + 2$. So the depth is at most $3L + 2\lceil \log_2(n + m) \rceil + 3 = \Theta(\log n)$ for $m = n$. Measured depths are 22, 30, 37 and 45 for $n = 8, 16, 32, 64$.

**Size.** There are $nm$ AND gates. Each full adder removes one bit, and the two final rows hold at most $2(n + m)$ bits, so there are fewer than $nm$ full adders; a half adder removes none, and a level has at most one half adder per column, so there are at most $(n + m + 1)L$ of them. With the final adder of $O((n + m) \log (n + m))$ gates, the size is $\Theta(n^2)$ for $m = n$. Measured: 489 gates for $n = 8$, 7111 for $n = 32$ and 27111 for $n = 64$, about $6.6 n^2$.

## Properties

- **No carry propagation in the tree.** Every full adder works on bits of its own level; the only carry chain is in the final adder.
- **Logarithmic depth.** $\log_{3/2} n + O(1)$ levels of full adders plus a logarithmic-depth adder, against $\Theta(n)$ for an array multiplier.
- **Quadratic size.** About $n^2$ full adders, the same order as the array multiplier, so the speed costs wiring, not gates.
- **Irregular wiring.** Carries leave each column for the next one at every level, and the number of bits per column changes from level to level, so the layout is less regular than an array.
- **Unsigned core.** The tree adds bits of positive weight; signed operands need recoding or correction terms, as below.

## Variants and improvements

- **[Dadda multiplier](/dadda-multiplier/).** Same levels, but in each level only as many adders as needed to bring every column down to the next Dadda number; it uses fewer half adders and a slightly smaller final adder. For $n = 8$ it uses 35 full adders and 7 half adders, against 36 and 25 here; both counts were checked by script.
- **Booth recoding.** Radix-4 [Booth recoding](/booth-multiplication/) of one operand gives about $n/2$ partial products in the digit set $\{-2, \ldots, 2\}$ instead of $n$, which removes about one level and a quarter of the adders.
- **Larger counters and compressors.** A 4:2 compressor takes four bits and a carry in and gives two bits and a carry out, with a regular binary tree structure and a depth of about 3 XOR delays; (7,3) counters reduce faster per level.
- **Signed operands.** The Baugh-Wooley method rewrites the two's complement product so that a few partial product bits are inverted and a constant is added, and the same tree then multiplies signed numbers. The implementation multiplies the magnitudes and fixes the sign instead.
- **Fused multiply-add.** An addend enters the tree as one more row, so $ab + c$ costs about the same as $ab$.
- **Multi-operand addition.** Without the AND gates the same tree adds $k$ numbers; see [multi-operand addition](/multi-operand-addition/).

## When to use it

Use a Wallace or Dadda tree for a fast single-cycle or pipelined multiplier, as in the integer and floating-point multipliers of processors, signal processors and cryptographic hardware, where latency matters and the area of about $n^2$ full adders is affordable. Use an [array multiplier](/array-multiplier/) when a regular layout matters more than delay, and a sequential shift-and-add multiplier when area is the limit. In software the tree is useful as a model only: a processor multiplies a word in a few cycles, and multiprecision products are built from word products by [schoolbook](/schoolbook-multiplication/) or [Karatsuba multiplication](/karatsuba-multiplication/).

## Pitfalls

- **Propagating carries inside a level.** The carry of a full adder in column $k$ belongs to the next level of column $k + 1$; feeding it into an adder of the same level makes a ripple chain and destroys the logarithmic depth.
- **Losing a carry at the top.** Carries can reach column $n + m$ at intermediate levels; they are always zero, because the product is less than $2^{n+m}$, but a circuit that drops a column too early drops real bits in a wider variant such as a fused multiply-add.
- **A slow final adder.** A ripple-carry adder of width $2n$ at the end adds depth $\Theta(n)$ and wastes the tree; use a parallel-prefix or carry-select adder.
- **Signed partial products.** Treating two's complement operands as unsigned gives a wrong high half; use Baugh-Wooley, Booth recoding, or sign handling as in the implementation.
- **Counting levels by $\log_2$.** Each level reduces a column by a factor of about $3/2$, not 2, so 64 rows need 10 levels, not 6.

## Implementations

## History

C. S. Wallace described the multiplier in 1964: form all partial products at once, reduce them with carry-save adders arranged as a tree, and finish with a fast carry-propagate adder. He observed that the delay grows with the logarithm of the operand length. Luigi Dadda in 1965 looked at the partial products column by column, introduced the sequence of maximal heights now named after him, and showed how to reach the same number of levels with fewer adders. Booth recoding (1951), the 4:2 compressor of the 1980s and Baugh and Wooley's signed array (1973) were combined with these trees in the multipliers of later processors.

## References

---
tag: KMMETW
kind: algorithm
slug: carry-save-addition
name: Carry-save addition
aliases:
- CSA
- carry-save adder
- 3-to-2 compressor
area: algebra/integer-arithmetic
level: advanced
summary: Adds three numbers into sum and carry vectors in constant time per digit, deferring carry propagation.
solves: [integer-addition]
model: boolean-circuit
complexity:
  vars: {n: the number of digits of each operand}
  time: {worst: Θ(n), average: Θ(n), best: Θ(n)}
  depth: {worst: Θ(1)}
  space: {extra: Θ(n)}
properties: {deterministic: true, recursive: false}
history:
  note: Keeping carries unresolved during repeated addition was used in the multipliers of the 1950s; Wallace arranged carry-save adders in a tree in 1964.
prereqs: [ripple-carry-adder, redundant-number-system, integer-addition]
see_also: [wallace-tree-multiplier, dadda-multiplier, array-multiplier, carry-propagation, redundant-number-system, ripple-carry-adder, carry-lookahead-adder, booth-multiplication]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Chapter 8, Multioperand addition, Sections 8.2 and 8.3 (carry-save adders, and Wallace and Dadda trees)
  - paper: doi:10.1109/PGEC.1964.263830
    title: C. S. Wallace, A suggestion for a fast multiplier, IEEE Transactions on Electronic Computers EC-13(1), 1964
    locator: pp. 14 to 17 (the tree of carry-save adders that reduces the partial products)
  - book: isbn:9780262031417
    title: Thomas H. Cormen, Charles E. Leiserson and Ronald L. Rivest, Introduction to Algorithms, first edition, MIT Press, 1990
    locator: Chapter 29, Arithmetic circuits, Section 29.2, Addition circuits (carry-save addition) and Section 29.3, Multiplication circuits
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 3, Multioperand addition (carry-save adders and reduction trees)
---

Carry-save addition reduces three numbers to two with the same sum, and it does so without moving any carry more than one position. Each position adds its three digits, keeps the low digit of the result as a *sum* digit, and hands the high digit to the next position as a *carry* digit, which it stores instead of adding. The two output numbers $s$ and $c$ satisfy $x + y + z = s + c$. Because no position waits for another, the step has constant depth for every width, where an ordinary addition must resolve carry chains of length up to $n$ (see [carry propagation](/carry-propagation/)). A sum of many numbers is kept as a pair $(S, C)$, the *carry-save form*, and one ordinary addition at the end turns it into a single number. This is how hardware multipliers add their partial products, in an [array](/array-multiplier/) or in a [Wallace tree](/wallace-tree-multiplier/).

## In plain words

When you add a long column of numbers by hand, the slow part is the carrying. Carry-save addition postpones it. Take three numbers. In each column, add the three digits. Write the last digit of that small sum in one row, and write its carry in a second row, shifted one column to the left. Do not add the carry in yet.

Now you have two rows instead of three, and their total is the same. No column had to wait for its neighbour, so all columns can work at once. If more numbers come, keep folding them in, three rows into two, again and again. Only at the very end do you do one real addition of the last two rows, with its carries.

## The problem

The input is three nonnegative integers $x$, $y$, $z$, each given by $n$ digits in base $\beta \ge 2$, least significant first, with zero top digits so that the sum fits: $x + y + z < \beta^n$. The output is two integers $s$ and $c$, again as $n$ digits, with $x + y + z = s + c$, every digit of $s$ in $[0, \beta)$ and every digit of $c$ in $\{0, 1, 2\}$. For $m$ operands, the problem is multi-operand [integer addition](/integer-addition/): return the single number $x_1 + \cdots + x_m$.

**Cost model.** For $\beta = 2$ the step is a [Boolean circuit](/boolean-circuit/): one full adder per position, so size $\Theta(n)$ and depth $O(1)$, which are the fields `time` and `depth`. For $\beta = 2^w$ on a word RAM, a step is $n$ independent word operations, so it also costs $\Theta(n)$ time but has no carry chain and vectorizes. The bounds on the step and on the number of tree levels are proved; the timing remarks about hardware are observations.

## The algorithm

```pseudo id=main
CSA(x, y, z, β)                                  ▷ three n-digit numbers in base β
L1  for all i in parallel: t ← x[i] + y[i] + z[i]          ▷ 0 ≤ t ≤ 3(β − 1)
L2      s[i] ← t mod β;  c[i + 1] ← ⌊t / β⌋              ▷ the carry goes one place, no further
L3  c[0] ← 0
L4  return (s, c)                                 ▷ x + y + z = s + c

CARRY-SAVE-SUM(x_1, …, x_m, β)                    ▷ m ≥ 2 numbers, padded so that the sum fits
L5  (S, C) ← (x_1, x_2)
L6  for j ← 3 to m do (S, C) ← CSA(S, C, x_j, β)
L7  return S + C                                  ▷ one carry-propagate addition
```

In base 2, line L2 is a full adder: $s_i = x_i \oplus y_i \oplus z_i$ and $c_{i+1} = \operatorname{maj}(x_i, y_i, z_i)$. In any base the carry digit is at most $\lfloor 3(\beta - 1)/\beta \rfloor \le 2 < \beta$ for $\beta \ge 3$, and at most 1 for $\beta = 2$, so the pair $(S, C)$ can be fed back into CSA as two ordinary operands. Line L7 can use any adder, for example a [carry-lookahead adder](/carry-lookahead-adder/). The tree form replaces the chain of line L6 by levels: each level splits the current numbers into groups of three and replaces every group by its two outputs.

## Example

Add $x = 487$, $y = 659$ and $z = 328$ in base 10 with $n = 4$ digits.

| position $i$ | $x_i$ | $y_i$ | $z_i$ | $t$ (L1) | $s_i$ (L2) | $c_{i+1}$ (L2) |
|---|---|---|---|---|---|---|
| 0 | 7 | 9 | 8 | 24 | 4 | 2 |
| 1 | 8 | 5 | 2 | 15 | 5 | 1 |
| 2 | 4 | 6 | 3 | 13 | 3 | 1 |
| 3 | 0 | 0 | 0 | 0 | 0 | |

So $s = 0354$ and $c = 1120$ (the carry of position $i$ is written at position $i + 1$, and $c_0 = 0$). Each row used only its own column. The single carry-propagate addition $354 + 1120 = 1474$ gives $487 + 659 + 328 = 1474$.

In base 2, $13 + 11 + 7$ with 6 bits: $x = 001101$, $y = 001011$, $z = 000111$. The column sums from position 0 up are $3, 2, 2, 2, 0, 0$, so $s = 000001$ and $c = 011110$, that is, $s = 1$ and $c = 30$, and $1 + 30 = 31$.

For many operands the tree is faster than the chain. With $m$ numbers, the chain uses $m - 2$ CSA steps in sequence; the tree uses the least $L$ with $d_L \ge m$, where $d_0 = 2$ and $d_{j+1} = \lfloor 3d_j/2 \rfloor$: the sequence $2, 3, 4, 6, 9, 13, 19, 28, 42, 63, \ldots$. So 9 operands need 4 levels and 63 operands need 9.

## Correctness

At each position, line L2 splits $t = x_i + y_i + z_i$ as $t = s_i + \beta \cdot c_{i+1}$ with $0 \le s_i < \beta$. Multiplying by $\beta^i$ and summing over the positions gives

$$x + y + z = \sum_i (s_i + \beta c_{i+1}) \beta^i = \sum_i s_i \beta^i + \sum_i c_{i+1} \beta^{i+1} = s + c ,$$

because $c_0 = 0$ (line L3). The carry out of the top position is 0, since $x + y + z < \beta^n$: otherwise $s + c$, which equals the sum, would be at least $\beta^n$. For CARRY-SAVE-SUM, the invariant $S + C = x_1 + \cdots + x_j$ holds after each step of line L6, so line L7 returns the total. The full proof is below.

## Complexity

**One step, proved.** Line L1 and line L2 do a constant amount of work per position, and no position reads another position's output, so the step has $n$ independent cells: size $\Theta(n)$ and depth $O(1)$. In base 2 each cell is one full adder, with depth 2 in the XOR-majority form; the test script checks the identity $x + y + z = s + c$ and the carry bound on 1500 random inputs in bases from 2 to $2^{16}$.

**Many operands, proved.** The chain of line L6 does $m - 2$ steps, each of depth $O(1)$ but in sequence, and the final addition costs one carry-propagate addition. In the tree, a level turns $k$ numbers into $2\lfloor k/3 \rfloor + (k \bmod 3)$ numbers; the largest $k$ that reaches 2 numbers in $L$ levels is $d_L$ above, which grows like $(3/2)^L$. So the tree has $\lceil \log_{3/2}(m/2) \rceil + O(1)$ levels, the total work is $m - 2$ steps of $n + O(\log m)$ digits each, and the depth is $O(\log m)$ steps plus one final addition. The level counts are checked by the test script for every $m < 200$.

**Comparison.** Adding $m$ numbers with ordinary adders of depth $\Theta(\log n)$ costs depth $\Theta(\log m \cdot \log n)$ in a tree; with carry-save it is $O(\log m + \log n)$, because only the final addition propagates carries.

## Properties

- **Redundant output.** The pair $(s, c)$ is a [redundant](/redundant-number-system/) representation: a value has many carry-save forms, and each digit position holds a digit from $\{0, \ldots, \beta + 1\}$ in effect. Addition is easy in this form; comparison, sign detection and division by a power of the base are not, because they need the resolved carries.
- **Width independence.** The delay of a step does not depend on $n$, which is what makes deep accumulations, such as $n$ partial products of a multiplier, fast.
- **A counter.** In base 2, a full adder counts the 1s among three bits and writes the count in binary; carry-save trees are trees of such counters. Larger counters, such as 4-to-2 compressors, are built from them.
- **Exact.** No precision is lost; the deferred carries are kept, not dropped.

## Variants and improvements

- **Wallace and Dadda trees.** The [Wallace tree](/wallace-tree-multiplier/) reduces as many groups of three as possible at each level; the [Dadda multiplier](/dadda-multiplier/) reduces only as much as needed to reach the next number of the sequence $d_j$, which saves adders.
- **4-to-2 compressors.** Two CSA levels merged into one cell with a lateral carry that does not propagate further; they give more regular trees in multipliers.
- **Signed and two's complement operands.** Sign extension of each operand, or the Baugh-Wooley constants in multipliers, let the same cells handle negative numbers.
- **Carry-save in iterative algorithms.** Hardware Montgomery multiplication, SRT division and square root keep their running remainder in carry-save form and inspect only a few top digits at each step, resolved by a short adder.
- **Delayed carries in software.** Big-number libraries that keep limbs below $2^{52}$ or $2^{51}$ in 64-bit words, or that use SIMD lanes, accumulate several products before normalizing the carries; this is the software form of the same idea.

## When to use it

Use carry-save addition whenever more than two numbers must be added, or when an addition is repeated many times before the result is needed: partial products in multipliers, multiply-accumulate units, dot products, and the iteration of division and modular multiplication circuits. For a single sum of two numbers it does not help, since the final carry-propagate addition is still needed. In software on a word RAM with an add-with-carry instruction, carries between words are cheap, and the technique pays mainly with SIMD or with limbs that have spare bits.

## Pitfalls

- **Shifting the carries twice or not at all.** Line L2 stores the carry of position $i$ at position $i + 1$, which already gives it the weight $\beta^{i+1}$. Shifting $c$ again before the final addition doubles every carry; storing it at position $i$ without shifting drops a factor of $\beta$. The right reading is $s + c$ with $c$ as stored.
- **No room at the top.** If the operands use all $n$ digits, the carry of position $n - 1$ has nowhere to go and is lost. Pad the operands with enough zero digits that $x_1 + \cdots + x_m < \beta^n$, about $\log_\beta m$ extra digits.
- **Reading the value from one vector.** Neither $s$ nor $c$ alone is the sum, and their top digits do not give its sign or size. Decisions on the value need a carry-propagate addition, or an estimate from a few top digits of both, as in SRT division.
- **Feeding the carry vector with large digits in base 2.** In base 2 a carry digit is at most 1, so $(S, C)$ is two ordinary binary numbers. In a base $\beta \ge 3$ a carry can be 2, which is still a valid digit; but if the inputs are themselves carry-save digits larger than $\beta - 1$, line L1 can exceed $3(\beta - 1)$ and the carry bound fails.

## Implementations

## History

Keeping the carries of a repeated addition in a separate register, and resolving them only at the end, was used in the fast multipliers of the 1950s. Wallace (1964) proposed reducing all the partial products of a multiplication at once with a tree of carry-save adders, which gave multiplication in depth $O(\log n)$, and Dadda (1965) refined the counting. Carry-save arithmetic became the standard internal representation of multipliers, multiply-accumulate units and iterative dividers, and it is the simplest example of the redundant number systems that Avizienis studied in 1961.

## References

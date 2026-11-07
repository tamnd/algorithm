---
tag: Q7R1ED
kind: algorithm
slug: dadda-multiplier
name: Dadda multiplier
aliases:
- Dadda tree
- Dadda reduction
area: algebra/integer-arithmetic
level: advanced
summary: Hardware multiplier that reduces partial products with a minimal number of adders.
solves: [integer-multiplication]
model: boolean-circuit
complexity:
  vars: {n: the number of binary digits of each operand}
  time: {worst: Θ(n^2), average: Θ(n^2), best: Θ(n^2)}
  depth: {worst: Θ(log n)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, recursive: false}
history:
  note: Luigi Dadda proposed the column-by-column reduction with the target heights 2, 3, 4, 6, 9, 13, ... in 1965, a year after Wallace's tree multiplier.
prereqs: [carry-save-addition, wallace-tree-multiplier, array-multiplier]
see_also: [wallace-tree-multiplier, array-multiplier, carry-save-addition, booth-multiplication, multi-operand-addition, kogge-stone-adder, integer-multiplication, schoolbook-multiplication]
sources:
  - paper: L. Dadda, Some schemes for parallel multipliers, Alta Frequenza 34, 1965
    title: Luigi Dadda, Some schemes for parallel multipliers
    locator: pp. 349 to 356 (the counter view of the columns and the reduction to the heights 2, 3, 4, 6, 9, 13, ...)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Section 11.1, Full-tree multipliers, and Section 8.3, Wallace and Dadda trees (dot diagrams of both reductions)
  - book: isbn:9781558607989
    title: Miloš D. Ercegovac and Tomás Lang, Digital Arithmetic, Morgan Kaufmann, 2004
    locator: Chapter 4, Multiplication (reduction by rows of full and half adders in Dadda's scheme)
  - paper: W. J. Townsend, E. E. Swartzlander and J. A. Abraham, A comparison of Dadda and Wallace multiplier delays, Proceedings of SPIE 5205, Advanced Signal Processing Algorithms, Architectures, and Implementations XIII, 2003
    title: A comparison of Dadda and Wallace multiplier delays
    locator: the counts of full and half adders of both schemes and their delays with a final adder
---

A Dadda multiplier is a combinational circuit that multiplies two $n$-bit numbers by summing their $n^2$ partial product bits in columns, with a tree of full and half adders that does only as much work at each level as the next level needs. Like a [Wallace tree](/wallace-tree-multiplier/), it reduces the bits in $O(\log n)$ levels of [carry-save](/carry-save-addition/) cells to two rows and adds them with one fast adder. Unlike Wallace, who reduces as much as possible at once, Dadda reduces each column to a fixed target height taken from the sequence $2, 3, 4, 6, 9, 13, 19, \ldots$, which uses the fewest adders of any scheme of this kind: $n^2 - 4n + 3$ full adders and $n - 1$ half adders for $n \ge 3$, with a final adder of width $2n - 2$.

## In plain words

Multiplying two binary numbers gives a grid of bits, one AND of an input bit pair for each grid cell, and the bits of equal weight form columns. The middle columns are tall and the edges are short. The job is to add up every column, with carries.

A full adder takes three bits from a column and puts back one bit there plus one carry bit in the next column, so the column shrinks by two. A half adder takes two and puts back one, plus a carry. Dadda's plan is to shrink the columns in rounds, to a height chosen in advance for each round, and to use no more adders than that target needs. The last round leaves two rows, and one ordinary adder finishes.

## The problem

The input is two unsigned integers $a$ and $b$ of $n$ bits each, $a = \sum_i a_i 2^i$ and $b = \sum_j b_j 2^j$. The output is the $2n$ bits of $ab$. The partial product bit $a_i \wedge b_j$ has weight $2^{i+j}$, so column $k$ starts with $h_k = \min(k + 1, 2n - 1 - k)$ bits for $0 \le k \le 2n - 2$, and the tallest column has $n$ bits.

**Cost model.** A [Boolean circuit](/boolean-circuit/) with unit-delay cells: an AND gate, a half adder and a full adder each count as one cell, and the delay of a path is the number of cells on it. The field `time` is the number of cells and `depth` is the delay. The bounds on the number of stages, the reduction delay and the number of full adders (given the final shape) are proved; the number of half adders and the final shape of the columns are observed for every $n$ from 3 to 40 and for 48 and 64 by the test script.

## The algorithm

Let $d_1 = 2$ and $d_{j+1} = \lfloor 3 d_j / 2 \rfloor$, which gives $2, 3, 4, 6, 9, 13, 19, 28, 42, 63, \ldots$, and let $d_t$ be the largest term below $n$.

```pseudo id=main
DADDA-MULTIPLY(a, b)                          ▷ a, b: n bits each, low bit first
L1  for i, j ← 0 to n − 1: put a_i ∧ b_j into column i + j
L2  d_1, …, d_t ← the terms 2, 3, 4, 6, 9, … that are less than n
L3  for d ← d_t, d_(t−1), …, d_1 do                ▷ one stage per target height
L4      for k ← 0 to 2n − 1 do e ← h_k + (carries into k from this stage) − d
L5          if e > 0: put ⌊e/2⌋ full adders on bits of column k
L6          if e > 0: put (e mod 2) half adders on bits of column k
L7          the other bits pass; sums stay in column k, carries go to column k + 1
L8  add the two rows with a carry-propagate adder
L9  return the 2n product bits
```

Here $h_k$ is the height of column $k$ before the stage. Each full adder lowers the height of its column by 2 and each half adder by 1, while every carry that arrives from column $k - 1$ adds 1, so after the stage column $k$ has exactly $\min(d, h_k + \text{carries})$ bits. The adders of a stage take their inputs only from the bits present before the stage, so a stage is one level of cells.

## Example

For $n = 4$ the target heights are $3$ and $2$. The table gives the column heights and the cells of each stage; the heights do not depend on the values of $a$ and $b$.

| column $k$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| after L1 | 1 | 2 | 3 | 4 | 3 | 2 | 1 |
| stage $d = 3$ (L5, L6) | | | | 1 HA | 1 HA | | |
| after stage 1 | 1 | 2 | 3 | 3 | 3 | 3 | 1 |
| stage $d = 2$ (L5, L6) | | | 1 HA | 1 FA | 1 FA | 1 FA | |
| after stage 2 | 1 | 2 | 2 | 2 | 2 | 2 | 2 |

In column 3 of stage 1 there are 4 bits, so $e = 4 - 3 = 1$ and one half adder suffices. Its carry raises column 4 to $3 + 1$, so column 4 also needs one half adder, and its carry raises column 5 to $2 + 1 = 3$, which is the target. In stage 2, column 2 has $e = 3 - 2 = 1$, and columns 3 to 5 each have $3 + 1 - 2 = 2$, one full adder each. In total there are 3 full adders and 3 half adders, $n^2 - 4n + 3 = 3$ and $n - 1 = 3$, and the final adder spans columns 1 to 6, width $2n - 2 = 6$. With $a = 13$ and $b = 11$ the two rows add to $143$.

## Correctness

The cells preserve the weighted sum: a full adder turns three bits $x, y, z$ of weight $2^k$ into $s + 2c$ with $x + y + z = s + 2c$, and a half adder does the same for two bits. So the sum of $\text{bit} \cdot 2^{\text{column}}$ over all bits is $ab$ after every stage. What needs a proof is that the rule is always possible: column $k$ has at least $3\lfloor e/2 \rfloor + 2(e \bmod 2)$ bits for its adders. Let $D$ be the target of the previous stage ($D = n$ for the first stage); then every $h_k \le D \le \lfloor 3d/2 \rfloor$, by the choice of $d_t$ and the recurrence. By induction on $k$, at most $D - d$ carries enter each column, and then $h_k + 3 \cdot \text{carries} \le 4D - 3d \le 3d$, which is the condition. After the last stage every column has at most 2 bits, and a carry-propagate adder of the two rows returns $ab$, which fits in $2n$ bits. The full proof is below.

## Complexity

**Stages and delay, proved.** There are $t$ stages, one per term $d_j < n$. Since $d_j$ grows like $(3/2)^j$, $t = \log_{3/2} n + O(1)$: for $n = 8, 16, 32, 64$ it is $4, 6, 8, 10$. Every bit after stage $s$ arrives at time at most $s + 1$, since the AND gates take one unit and each stage one more; so the reduction has delay exactly $t + 1$. A final adder of width $2n - 2$ with delay $O(\log n)$, such as a [Kogge-Stone adder](/kogge-stone-adder/), gives total delay $O(\log n)$. With a ripple-carry final adder the delay is $2n - 1$, measured by the test script, and the tree gains nothing.

**Size, proved given the shape.** A full adder turns 3 bits into 2 and a half adder turns 2 into 2, so the number of full adders equals the number of bits removed: $n^2$ minus the bits left at the end. The test script observes that the final shape is one bit in column 0 and two bits in each column $1, \ldots, 2n - 2$, that is $4n - 3$ bits, which gives $n^2 - 4n + 3$ full adders. It also observes $n - 1$ half adders. With $n^2$ AND gates the circuit has $\Theta(n^2)$ cells.

**Against Wallace, observed.** A greedy Wallace model that puts a full adder on every group of three bits of a column and a half adder on every leftover pair uses, for $n = 8$, 36 full adders and 25 half adders in 4 stages; Dadda uses 35 and 7, also in 4 stages. The number of stages of both trees is the same, $t$, since both reach height $d_j$ after the same number of levels.

## Properties

- **Fewest adders for the stage count.** Each stage uses only the adders needed to reach the next target, so no stage does work that the next one could have done.
- **Same depth as Wallace.** The number of reduction levels is $t$, the least possible for trees of 3-to-2 counters, since $d_j$ is the largest number of bits that $j$ levels can reduce to 2 in one column with carries.
- **Wider final adder.** Dadda leaves two full rows of width $2n - 2$, while Wallace finishes some low columns early and needs a slightly narrower final adder. This partly offsets the saving in half adders.
- **Irregular wiring.** Like every tree multiplier, the layout is less regular than an [array multiplier](/array-multiplier/), and the wire lengths are not reflected in the unit-delay model.

## Variants and improvements

- **Signed operands.** The Baugh-Wooley form or sign extension of the partial products, and [Booth recoding](/booth-multiplication/), which halves the number of rows before the reduction, are combined with Dadda trees in practice.
- **Larger counters.** Trees of 4-to-2 compressors or (7,3) counters reduce the number of levels, with the same idea of reducing each column only to a precomputed target.
- **Reduced-area variants.** Bickerstaff, Schulte and Swartzlander (1993) proposed a reduced-area tree that uses as many full adders as possible early and fewer half adders, at the cost of a slightly different final adder.
- **Delay-aware reduction.** With unequal delays from the inputs of a full adder to its outputs, assigning the late bits to the fast inputs, and the timing of the final adder to the arrival profile of the columns, improves the real delay.

## When to use it

Use a Dadda tree for a fast parallel multiplier when area matters, which is the usual case: it has the delay of a Wallace tree and fewer cells. Use an array multiplier when the layout must be regular or pipelined row by row, and a sequential shift-and-add multiplier when area matters far more than speed. In software, on a word RAM, none of this applies: the machine provides the word product and [schoolbook](/schoolbook-multiplication/) or Karatsuba multiplication works on limbs.

## Pitfalls

- **Forgetting the incoming carries.** Line L4 counts the carries that the stage sends into column $k$ from column $k - 1$. Computing $e = h_k - d$ instead leaves columns of height $d + 1$ or $d + 2$ after the stage, and the next stage starts above its assumed height. The right count is $e = h_k + \text{carries} - d$.
- **Reducing too early.** Using full adders wherever three bits are available, as in line L5 with $\lfloor h_k / 3 \rfloor$ in place of $\lfloor e/2 \rfloor$, gives a Wallace tree: correct, but with more half adders and no fewer stages.
- **Feeding new carries into the same stage.** If a stage's adders take carries produced in the same stage as inputs, the stage becomes two cell levels deep. Line L5 and line L6 take only bits that were present before the stage; the carries join the next stage.
- **A slow final adder.** Line L8 with a ripple-carry adder makes the delay $2n - 1$ and wastes the tree. The final adder must have delay $O(\log n)$ to keep the total logarithmic.

## Implementations

## History

Wallace (1964) showed that the partial products of a multiplication can be added in a tree of carry-save adders with $O(\log n)$ delay. Dadda (1965) viewed the reduction as one of columns of bits, with full and half adders as counters, and gave the schedule of target heights $2, 3, 4, 6, 9, 13, \ldots$, which reaches the same number of levels with fewer adders. Habibi and Wintz (1970) compared the two schemes, and later comparisons, such as the one of Townsend, Swartzlander and Abraham (2003), found that Dadda multipliers are slightly faster as well as smaller once the final adder is included.

## References

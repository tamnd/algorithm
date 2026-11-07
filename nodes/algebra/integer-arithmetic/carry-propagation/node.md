---
tag: F1QKKS
kind: concept
slug: carry-propagation
name: Carry propagation
aliases:
- carry chain
area: algebra/integer-arithmetic
level: intro
summary: The process by which a carry out of one digit position affects the positions above it.
prereqs: [integer-addition, positional-number-system]
see_also: [ripple-carry-adder, carry-lookahead-adder, carry-skip-adder, carry-select-adder, carry-save-addition, redundant-number-system, parallel-prefix, kogge-stone-adder]
sources:
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Section 5.3, Analysis of carry propagation, Section 5.4, Carry completion detection, Section 3.1, Coping with the carry problem, and Section 6.1, Unrolling the carry recurrence
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Algorithm A and the carries of addition)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.2, Addition and subtraction (the carry of Algorithm 1.1 and its cost in software)
---

Carry propagation is the way a carry out of one digit position of an addition changes the positions above it, and possibly all of them. In the sum of two $n$-digit numbers, the carry into position $i$ depends on all digits below $i$, so the last carry can depend on all $2n$ input digits. This dependence is the main cost of addition in hardware, where a chain of $n$ carry steps is slow. Fast adders ([carry-lookahead](/carry-lookahead-adder/), [parallel-prefix](/parallel-prefix/), [carry-skip](/carry-skip-adder/), [carry-select](/carry-select-adder/)) compute the carries in fewer steps, and [redundant number systems](/redundant-number-system/) avoid propagation altogether.

## In plain words

When you add 1 to 999, the first position makes a carry. That carry turns the next 9 into a 0 and makes a new carry, and so on, until the answer is 1000. One small change at the right end has changed every digit. This movement of carries from right to left is carry propagation.

A carry moves on only through a position whose two digits add up to exactly one less than the base, like 9 and 0, or 4 and 5, in base ten. Such positions pass the carry on unchanged. A position whose digits add up to the base or more makes a new carry, and a position whose digits add up to less stops it.

For random numbers, long chains of passing positions are rare. But a circuit must be fast in the worst case too, so fast adders find all carries at once.

## The idea

**The recurrence.** Add $A = \sum a_i \beta^i$ and $B = \sum b_i \beta^i$ in the base $\beta$, with a carry-in $c_0$. The carries are $c_{i+1} = \lfloor (a_i + b_i + c_i)/\beta \rfloor \in \{0, 1\}$, and the sum digits are $s_i = (a_i + b_i + c_i) \bmod \beta$ ([integer addition](/integer-addition/)).

**Generate, propagate, kill.** Each position is of exactly one of three types, which depend only on $a_i + b_i$:

| type | condition | effect on the carry |
|---|---|---|
| generate $g_i$ | $a_i + b_i \ge \beta$ | $c_{i+1} = 1$ |
| propagate $p_i$ | $a_i + b_i = \beta - 1$ | $c_{i+1} = c_i$ |
| kill $k_i$ | $a_i + b_i \le \beta - 2$ | $c_{i+1} = 0$ |

So $c_{i+1} = g_i \lor (p_i \land c_i)$. In base 2, $g_i = a_i \land b_i$ and $p_i = a_i \oplus b_i$. Some designs use $p_i = a_i \lor b_i$ instead, which also works in the formula for $c_{i+1}$ because $g_i$ already covers the case $a_i = b_i = 1$.

**Carry chains.** A *carry chain* of length $j$ starts at a generating position $i$ and continues through the propagating positions $i + 1, \ldots, i + j - 1$; the carry it starts reaches $c_{i+j}$. Unrolling the recurrence over a block of positions $i$ to $k$ gives a *group generate* and a *group propagate*:

$$G_{i:k} = g_k \lor p_k g_{k-1} \lor p_k p_{k-1} g_{k-2} \lor \cdots \lor p_k \cdots p_{i+1} g_i, \qquad P_{i:k} = p_k p_{k-1} \cdots p_i ,$$

with $c_{k+1} = G_{i:k} \lor (P_{i:k} \land c_i)$. The pairs combine by an associative operator, $(G, P) \circ (G', P') = (G \lor P G', P P')$ where $(G, P)$ is the upper block. So all carries are the prefixes of a sequence under an associative operation, which a [parallel prefix](/parallel-prefix/) circuit computes in $O(\log n)$ depth.

**The worst case.** The chain can be as long as $n$: $A = \beta^n - 1$ (all digits $\beta - 1$) and $B = 1$ give $c_1 = c_2 = \cdots = c_n = 1$. A [ripple-carry adder](/ripple-carry-adder/), which waits for each carry in turn, has delay $\Theta(n)$ on this input.

**The average case.** Take the bits $a_i$ and $b_i$ of a binary addition to be independent and uniform, with $c_0 = 0$. Let $L$ be the length of the longest carry chain. Then

$$\mathbb{E}[L] \le \log_2 n + \tfrac{3}{2} .$$

*Proof.* A chain of length at least $k$ starts at position $i$ when $g_i = 1$ (probability $1/4$) and $p_{i+1} = \cdots = p_{i+k-1} = 1$ (probability $2^{-(k-1)}$, independent of $g_i$). By the union bound over the $n$ start positions, $\Pr[L \ge k] \le n \cdot 2^{-k-1}$. Let $K = \lceil \log_2 n \rceil$. Then

$$\mathbb{E}[L] = \sum_{k \ge 1} \Pr[L \ge k] \le K + \sum_{k > K} n 2^{-k-1} = K + n 2^{-K-1} \le K + \tfrac12 \le \log_2 n + \tfrac32 . \qquad \blacksquare$$

So an adder that detects when all its carries have settled finishes in $O(\log n)$ expected time (Parhami, Section 5.4, carry completion detection). The bound is close to the truth: the average of $L$ over random pairs is a little below $\log_2 n$, for example about $9.4$ for $n = 1024$ and about $5.3$ for $n = 64$.

**How often a carry happens.** For uniform random digits in the base $\beta$, a position generates with probability $\frac{\beta(\beta-1)/2}{\beta^2} = \frac{\beta - 1}{2\beta}$ and propagates with probability $\frac{1}{\beta}$. If $p$ is the long-run probability of a carry, then $p = \frac{\beta - 1}{2\beta} + \frac{p}{\beta}$, which gives $p = \frac12$ for each base. So half of all positions produce a carry, but in a large base such as $\beta = 2^{64}$ a carry almost never travels more than one position, because a propagating position has probability $2^{-64}$.

**Avoiding propagation.** A *redundant* representation allows more than $\beta$ digit values, so that a sum can be written without waiting for carries. In [carry-save addition](/carry-save-addition/), a number is kept as two numbers whose sum it is, and three numbers become two in constant depth. In a signed-digit system each digit of a sum depends only on a few digits of the inputs. Software for elliptic curves often uses limbs of 51 bits in 64-bit words, so that many additions can be done before carries are resolved.

## Examples

**A full chain in base 10.** $999 + 1$: positions 0, 1 and 2 have $a_i + b_i = 10, 9, 9$, so position 0 generates and positions 1 and 2 propagate. The chain has length 3, and the sum is 1000.

**Binary chains.** For $A = 1011\,0110$ and $B = 0100\,1101$ (bits written high to low), the low four positions are $(0,1), (1,0), (1,1), (0,1)$ from position 0 up: propagate, propagate, generate, propagate. With $c_0 = 0$ the first two pass a 0, position 2 generates and position 3 passes the carry on. The high four positions are $(1,0), (1,0), (0,1), (1,0)$, all propagating, so the carry from position 2 travels to the top: the chain from position 2 has length 6, and $A + B = 182 + 77 = 259 = 1\,0000\,0011$.

**Limbs in base $2^8$.** $\text{0x5EA73C} + \text{0xA158D4}$: the limb sums are $\text{0x3C} + \text{0xD4} = 272 \ge 256$ (generate), then $\text{0xA7} + \text{0x58} = 255$ and $\text{0x5E} + \text{0xA1} = 255$ (both propagate). The sum is $\text{0x1000010}$, with a chain of length 3 into a new limb.

**No generate, no carry.** In $1000 + 0111$ in binary, every position propagates, since each has one 0 and one 1. With $c_0 = 0$ no carry ever starts, and the sum is $1111$. With $c_0 = 1$ the same inputs give a chain through all four positions and the sum $10000$.

**A kill.** In $1001 + 0011$, position 0 generates ($1 + 1$), position 1 propagates ($0 + 1$), and position 2 kills ($0 + 0$), so the carry stops there: $c_1 = c_2 = 1$, $c_3 = 0$, and the sum is $9 + 3 = 12 = 1100$.

## Where it is used

- The design of each hardware adder: [ripple-carry adder](/ripple-carry-adder/), [carry-skip adder](/carry-skip-adder/), [carry-select adder](/carry-select-adder/), [carry-lookahead adder](/carry-lookahead-adder/), [Kogge-Stone adder](/kogge-stone-adder/), [Brent-Kung adder](/brent-kung-adder/) and [Sklansky adder](/sklansky-adder/).
- Multipliers, which postpone all carries with [carry-save addition](/carry-save-addition/) in a tree and resolve them once at the end ([Wallace tree](/wallace-tree-multiplier/), [Dadda multiplier](/dadda-multiplier/)).
- Software bignum libraries, which use the add-with-carry instruction for the carry chain of [integer addition](/integer-addition/), and delayed carries when the limbs are smaller than the word.
- [Redundant number systems](/redundant-number-system/) and [signed-digit representations](/signed-digit-representation/), which exist to bound how far a carry can travel.

## References

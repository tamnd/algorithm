---
tag: RZA6ZT
kind: problem
slug: integer-addition
name: Integer addition
aliases:
- adding binary numbers
- multiprecision addition
area: algebra/integer-arithmetic
level: intro
summary: Add two n-digit integers in a given radix, producing an n+1 digit sum.
model: word-ram
complexity:
  vars: {n: the number of limbs of the longer operand}
  time: {worst: Θ(n)}
prereqs: [positional-number-system, radix, arbitrary-precision-arithmetic]
see_also: [carry-propagation, ripple-carry-adder, carry-lookahead-adder, carry-save-addition, multi-operand-addition, twos-complement, integer-overflow, integer-multiplication]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, third edition
    locator: Section 4.3.1, The classical algorithms (Algorithm A, addition of nonnegative integers, and Algorithm S, subtraction)
  - book: isbn:9780521194693
    title: Richard P. Brent and Paul Zimmermann, Modern Computer Arithmetic, Cambridge University Press, 2010
    locator: Section 1.2, Addition and subtraction (Algorithm 1.1, IntegerAddition)
  - book: isbn:9780195328486
    title: Behrooz Parhami, Computer Arithmetic, Algorithms and Hardware Designs, second edition, Oxford University Press, 2010
    locator: Part II, Addition/Subtraction (Chapter 5 basic addition and the analysis of carry propagation, Chapter 6 carry-lookahead adders and carry determination as a prefix computation, Chapter 7 carry-skip and carry-select adders)
  - paper: doi:10.1145/322217.322232
    title: Richard E. Ladner and Michael J. Fischer, Parallel prefix computation, Journal of the ACM 27(4), 1980
    locator: pp. 831 to 838 (prefix circuits of logarithmic depth and linear size, with the carry computation as the main application)
---

Integer addition is the problem of computing the sum of two integers given by their digits in a radix $\beta$. For two $n$-digit operands, the sum has $n$ digits and one carry digit, and the carry of each position depends on all positions below it ([carry propagation](/carry-propagation/)). On the [word RAM](/word-ram/) the school method takes $\Theta(n)$ limb operations, which is optimal. In hardware, where the question is the depth of a circuit, the [carry-lookahead adder](/carry-lookahead-adder/) and the parallel-prefix adders reach depth $O(\log n)$ with $O(n)$ gates, which is also optimal.

## In plain words

You add two long numbers the way you learned at school. You start at the right. You add the two digits and the carry. You write down the last digit of this sum, and you carry the rest to the next position on the left. At the end, a last carry can make the result one digit longer.

A computer does the same with large digits: one digit is one machine word. The work is one small step for each digit, so a number twice as long takes twice as long to add.

The hard part is the carry. A carry can move from the rightmost digit all the way to the leftmost digit, as when you add one to 999. A circuit that waits for each carry in turn is slow, so fast circuits find all the carries at the same time with a clever tree.

## Definition

Fix a radix $\beta \ge 2$. In software $\beta = 2^w$ for a word size $w$, and in hardware $\beta = 2$.

**Input.** Two integers given by $n$ digits each, $A = \sum_{i=0}^{n-1} a_i \beta^i$ and $B = \sum_{i=0}^{n-1} b_i \beta^i$ with $0 \le a_i, b_i < \beta$, and a carry-in $c_0 \in \{0, 1\}$. An operand with fewer digits is padded with zero digits.

**Output.** Digits $s_0, \ldots, s_{n-1}$ with $0 \le s_i < \beta$ and a carry-out $c_n \in \{0, 1\}$ such that

$$A + B + c_0 = c_n \beta^n + \sum_{i=0}^{n-1} s_i \beta^i .$$

The output is unique, because the representation of a number in $[0, \beta^{n+1})$ by $n$ digits and one top digit is unique.

**The carry recurrence.** For $i = 0, 1, \ldots, n - 1$,

$$s_i = (a_i + b_i + c_i) \bmod \beta, \qquad c_{i+1} = \left\lfloor \frac{a_i + b_i + c_i}{\beta} \right\rfloor .$$

Each carry is 0 or 1. By induction on $i$: $c_0 \le 1$, and if $c_i \le 1$ then $a_i + b_i + c_i \le 2(\beta - 1) + 1 = 2\beta - 1$, so $c_{i+1} \le 1$. Multiply $a_i + b_i + c_i = s_i + \beta c_{i+1}$ by $\beta^i$ and sum over $i$. The left side has the carry terms $\sum_{i=0}^{n-1} c_i \beta^i$ and the right side has $\sum_{i=1}^{n} c_i \beta^i$. All of them cancel except $c_0$ on the left and $c_n \beta^n$ on the right, which gives the defining equation. So the recurrence computes the unique output.

**Generate and propagate.** A position *generates* a carry when $a_i + b_i \ge \beta$: then $c_{i+1} = 1$ for each $c_i$. It *propagates* when $a_i + b_i = \beta - 1$: then $c_{i+1} = c_i$. Otherwise it *kills*: $c_{i+1} = 0$. With $g_i$ and $p_i$ for these two conditions, $c_{i+1} = g_i \lor (p_i \land c_i)$, and unrolled,

$$c_{i+1} = g_i \lor (p_i \land g_{i-1}) \lor (p_i \land p_{i-1} \land g_{i-2}) \lor \cdots \lor (p_i \land \cdots \land p_0 \land c_0).$$

This is the formula behind all fast adders.

## Variants

- **Subtraction.** $A - B$ for $A \ge B$ uses a borrow $b'_{i+1} = 1$ when $a_i - b_i - b'_i < 0$. Equivalently, $A - B = A + (\beta^n - 1 - B) + 1 - \beta^n$: complement each digit of $B$ to $\beta - 1 - b_i$, add with carry-in 1, and drop the carry-out, which is 1 exactly when $A \ge B$.
- **Unequal lengths.** For $m > n$ digits, the last $m - n$ positions only add the carry. The cost is $O(n)$ plus the length of the carry run, which is $O(m)$ in the worst case but $O(1)$ on average for random digits.
- **Signed operands.** In [two's complement](/twos-complement/) with $n$ bits, the same adder gives the sum modulo $2^n$. The result is wrong exactly when the two operands have the same sign and the sum has the other sign ([integer overflow](/integer-overflow/)). With sign and magnitude, an addition of operands of different signs becomes a subtraction of magnitudes.
- **Modular addition.** Add modulo $\beta^n$ by dropping $c_n$, or modulo $m$ by one conditional subtraction of $m$, as in [modular arithmetic](/modular-multiplication/).
- **Increment.** Adding the constant 1 is the counter problem. Its cost on the word RAM is $O(1)$ amortized over a sequence of increments from zero.
- **Many operands.** Adding $k$ numbers is [multi-operand addition](/multi-operand-addition/). [Carry-save addition](/carry-save-addition/) reduces three operands to two without any carry propagation.
- **Redundant output.** If the sum may stay in a [redundant number system](/redundant-number-system/), each digit of the result depends on $O(1)$ digits of the input, and addition takes constant depth.

## Examples

| radix | $A$ | $B$ | carries $c_1 \ldots c_n$ | sum |
|---|---|---|---|---|
| 10 | 987 | 45 | 1, 1, 1 | 1032 |
| $2^8$ | [255, 255, 255] | [1] | 1, 1, 1 | [0, 0, 0, 1] |
| $2^8$ | 0x5EA73C | 0xA158D4 | 1, 1, 1 | 0x1000010 |
| 2 | 1011 | 0101 | 1, 1, 1, 1 | 10000 |
| 2 | 1000 | 0111 | 0, 0, 0, 0 | 1111 |

Digit lists are least significant first. In the third row, the low limbs are $\text{0x3C} + \text{0xD4} = 272 = 256 + 16$, then $\text{0xA7} + \text{0x58} + 1 = 256$, then $\text{0x5E} + \text{0xA1} + 1 = 256$: one position generates, and the two above it propagate, so the sum $16777232$ needs a fourth limb. In the last row, no position generates, and every position above the lowest propagates, so a carry-in of 1 would ripple through all four positions and give 10000.

**Signed overflow.** In 8-bit two's complement, $100 + 100 = 200$, which the adder returns as the bit pattern of $200 - 256 = -56$. Both operands are positive and the result is negative, so the overflow flag is set.

## Known algorithms

- **The carry loop.** Knuth's Algorithm A, or Algorithm 1.1 of Brent and Zimmermann, runs the carry recurrence once per limb: $\Theta(n)$ limb operations, $O(1)$ extra space, and the operands can be read and written in the same pass. Processors have an add-with-carry instruction for this loop.
- **[Ripple-carry adder](/ripple-carry-adder/).** The same recurrence as a chain of $n$ full adders: size $\Theta(n)$ and depth $\Theta(n)$.
- **[Carry-skip adder](/carry-skip-adder/).** Blocks whose positions all propagate pass the carry in one step: depth $O(\sqrt{n})$ with blocks of size about $\sqrt{n}$.
- **[Carry-select adder](/carry-select-adder/).** Each block computes its sum for both carry-ins and a multiplexer picks one: depth $O(\sqrt{n})$, and $O(\log n)$ in the recursive conditional-sum form with $O(n \log n)$ gates.
- **[Carry-lookahead adder](/carry-lookahead-adder/).** Computes the carries from the generate and propagate signals by a tree: depth $O(\log n)$, size $O(n)$.
- **Parallel-prefix adders.** The carries are a prefix computation ([parallel prefix](/parallel-prefix/)). The [Kogge-Stone adder](/kogge-stone-adder/) has depth $\lceil \log_2 n \rceil$ prefix levels and about $n \log_2 n$ cells, the [Brent-Kung adder](/brent-kung-adder/) about $2 \log_2 n$ levels and fewer than $2n$ cells, and the [Sklansky adder](/sklansky-adder/) $\lceil \log_2 n \rceil$ levels and about $\tfrac12 n \log_2 n$ cells with high fan-out.

## Bounds

**Word RAM.** The carry loop uses $\Theta(n)$ limb operations. Each algorithm needs $\Omega(n)$: if it does not read some limb $a_i$, an adversary can change $a_i$ by one, which changes the output digit $s_i$ and the algorithm cannot see it. So $\Theta(n)$ is tight.

**Boolean circuits, depth.** In a circuit of gates with fan-in 2, each output of depth $d$ depends on at most $2^d$ inputs. The carry-out $c_n$ of an $n$-bit adder depends on all $2n$ inputs: set $a_j = 1$, $b_j = 0$ at each position $j \ne i$ so that every other position propagates, and $c_0 = 0$; then $c_n = a_i \land b_i$ for the position $i$ that is left free, so both $a_i$ and $b_i$ matter. Hence the depth is at least $\lceil \log_2 (2n) \rceil = 1 + \lceil \log_2 n \rceil$. The parallel-prefix adders reach $O(\log n)$, so the depth $\Theta(\log n)$ is tight.

**Boolean circuits, size.** The output $c_n$ depends on $2n$ inputs, so a fan-in 2 circuit for it alone has at least $2n - 1$ gates. The ripple-carry adder has $O(n)$ gates. Ladner and Fischer (1980) showed that depth $O(\log n)$ and size $O(n)$ are possible at the same time, with their prefix circuits.

**Unbounded fan-in.** The unrolled formula for $c_{i+1}$ is an OR of $i + 2$ ANDs, so with gates of unbounded fan-in, addition has circuits of constant depth and $O(n^2)$ gates. Addition is in the class $\mathrm{AC}^0$ ([circuit complexity](/circuit-complexity/)).

**Average carry length.** For random operands, the longest run of propagating positions is about $\log_2 n$, so an asynchronous adder that detects when its carries are done finishes in $O(\log n)$ expected time. The page [carry propagation](/carry-propagation/) proves the bound.

## Reductions

- **Subtraction and comparison reduce to addition.** By the complement rule of the variants, $A - B$ is one addition with carry-in 1 and $O(n)$ extra work, and the carry-out gives the sign of $A - B$, so it decides $A \ge B$.
- **Multiplication by shift and add.** A product $A \cdot B$ is a sum of shifted copies of $A$, one for each nonzero digit of $B$. [Schoolbook multiplication](/schoolbook-multiplication/) is $n$ additions, and the hardware multipliers ([array multiplier](/array-multiplier/), [Wallace tree](/wallace-tree-multiplier/), [Dadda multiplier](/dadda-multiplier/)) are trees of adders.
- **Carries as a prefix problem.** The pair $(g_i, p_i)$ acts on a carry as the function $c \mapsto g_i \lor (p_i \land c)$, and composition of such functions is associative. So the carries are the prefix compositions of these $n$ functions, and each [parallel prefix](/parallel-prefix/) circuit gives an adder.

## Applications

- Each larger operation of [arbitrary-precision arithmetic](/arbitrary-precision-arithmetic/): multiplication, division and radix conversion all run many additions.
- The arithmetic and logic unit of each processor, the address computation of each memory access, and program counters.
- The final step of each hardware multiplier, which adds the two numbers that a carry-save tree leaves.
- Checksums such as the Internet checksum, which use [ones' complement arithmetic](/ones-complement-arithmetic/), an addition with an end-around carry.

## References

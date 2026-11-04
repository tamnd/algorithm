---
tag: SS7E4E
kind: concept
slug: unit-cost-model
name: Unit-cost model
aliases:
- uniform cost criterion
area: foundations/models-of-computation
level: core
summary: Assumption that every RAM instruction costs one step regardless of operand size.
prereqs: [random-access-machine, asymptotic-notation]
see_also: [logarithmic-cost-model, word-ram, transdichotomous-model, ram-turing-equivalence, integer-multiplication, big-integer]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 1, uniform and logarithmic cost criteria for RAM programs
  - title: J. Hartmanis and J. Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory, 1974
    locator: pages 13 to 23
  - title: Stephen A. Cook and Robert A. Reckhow, Time-bounded random access machines, Journal of Computer and System Sciences 7(4), 1973
    locator: pages 354 to 375
---

The unit-cost model is the rule that every instruction of a [random access machine](/random-access-machine/) costs one step, whatever the size of its operands. The running time of a program is then the number of instructions that it executes. Most analyses of algorithms use this rule, and it is sound when the numbers that the program handles have $O(\log n)$ bits, where $n$ is the input size. It fails when a program can build numbers with many more bits, because one step then does the work of many bit operations.

## In plain words

A computer adds two numbers in one step if the numbers fit in a machine word. The unit-cost model says: count every such step as one unit, and never ask how big the numbers are.

This is a good rule when the numbers are small. A loop counter, an array index and a key that fits in a word are small. The rule is bad when a program makes very large numbers. A real machine needs many steps to add two numbers with a million digits. The unit-cost model still counts one step.

So the rule is a promise: the numbers stay small. When the promise holds, step counts predict real time well. When it does not, step counts can be wrong by an exponential factor, and you must count bit operations instead.

## The idea

### The rule

In the unit-cost model, each instruction of the RAM costs 1: a load, a store, an addition, a subtraction, a comparison, a jump, and (when the machine has it) a multiplication or a division. A register can hold an integer of any size. The cost of a program on an input is the number of instructions that it executes.

### When the rule is sound

Let a program run on an input of size $n$. Suppose that, in every step, each number stored in a register, and each address used, has absolute value less than $n^c$ for a constant $c$. Then each number has at most $c \lg n + 1$ bits, and a processor with words of $\Theta(\log n)$ bits holds it in $O(1)$ words. This is the assumption of the [word RAM](/word-ram/) and of the [transdichotomous model](/transdichotomous-model/): the word size grows with the input, so an index of the input fits in one word.

Under this assumption, the unit-cost time and the [logarithmic-cost](/logarithmic-cost-model/) time differ by at most a factor $O(\log n)$. Each instruction costs at least 1 in the logarithmic-cost model, because every operand has bit length at least 1. And it costs $O(c \log n)$ there, because it touches a constant number of values of at most $c \lg n + 1$ bits. So, for the same program,

$$T_{\text{unit}} \le T_{\log} \le O(c \log n) \cdot T_{\text{unit}}.$$

The factor $\log n$ is real. A loop that counts from 1 to $n$ has unit-cost time $n$ and logarithmic-cost time $\Theta(n \log n)$ (see the [logarithmic-cost model](/logarithmic-cost-model/)). So a bound that is exact up to $\log$ factors must name its cost model.

### Where the rule fails

With addition, subtraction and multiplication, one instruction can double the bit length of a number. If $x$ and $y$ have $a$ and $b$ bits, then $xy$ has at most $a + b$ bits. So after $t$ instructions the longest number has at most $2^t b_0$ bits, where $b_0$ is the longest bit length of an input or a constant. Repeated squaring comes within a factor 2 of this bound. With only addition and subtraction the growth is slow: each instruction adds at most one bit, since $|x \pm y| \le 2 \max(|x|, |y|)$. So after $t$ instructions every number has at most $b_0 + t$ bits, and the logarithmic cost of the run is $O(t (b_0 + t))$. This is a polynomial loss, and it is the reason why the unit-cost RAM without multiplication and the logarithmic-cost RAM are polynomially related (Cook and Reckhow 1973). Multiplication is what makes the gap exponential.

Take $x_0 = 2$ and $x_{k+1} = x_k \cdot x_k$. By induction, $x_k = 2^{2^k}$: the case $k = 0$ is $2 = 2^{2^0}$, and $x_{k+1} = (2^{2^k})^2 = 2^{2^{k+1}}$. The number $2^{2^k}$ has $2^k + 1$ bits.

| $k$ | $x_k$ | bits of $x_k$ |
|---|---|---|
| 0 | 2 | 2 |
| 1 | 4 | 3 |
| 2 | 16 | 5 |
| 3 | 256 | 9 |
| 4 | 65536 | 17 |

So $n$ multiplications build a number with $2^n + 1$ bits. Even to write this number down takes $2^n$ steps on a machine that writes one bit at a time. A model that charges 1 for each of these multiplications gives no information about real cost. With multiplication and bitwise Boolean instructions, the languages that the unit-cost RAM decides in polynomial time are exactly the languages in [PSPACE](/pspace/) (Hartmanis and Simon 1974). So unless $\mathsf{P} = \mathsf{PSPACE}$, this model is stronger than the Turing machine with a polynomial slowdown. The same kind of failure happens with any unit-cost instruction that creates long numbers from short ones, such as multiplication, or a left shift by an amount that is itself a large number. Division does not make numbers longer, but it adds power when it is combined with these instructions.

There are two usual repairs. One is to bound the numbers: the word RAM allows words of $w$ bits and does arithmetic modulo $2^w$. The other is to charge by length: the [logarithmic-cost model](/logarithmic-cost-model/).

## Examples

- **Sound.** [Binary search](/binary-search/) on an array of $n$ items. The registers hold indices from $0$ to $n$ and keys. If the keys have $O(\log n)$ bits, the unit-cost count of $\lceil \lg(n+1) \rceil$ probes is the right order of magnitude of the real time.
- **Sound.** [Merge sort](/merge-sort/) on $n$ keys that fit in a word. The unit-cost time $\Theta(n \log n)$ counts steps on words, and no number grows.
- **Not sound.** Computing the Fibonacci number $F_n$ with $n - 1$ additions. The unit-cost time is $n - 1$, but $F_n$ has about $0.694 n$ bits, because $\lg \varphi \approx 0.694$ where $\varphi = (1 + \sqrt 5)/2$. The $k$-th addition adds numbers of about $0.694 k$ bits, so in the logarithmic-cost model the total is $\Theta(n^2)$. For $n = 1000$, $F_n$ has 694 bits, and the lengths of $F_1, \dots, F_{999}$ add up to 346115 bits. See [Fibonacci numbers](/fibonacci-numbers/).
- **Not sound.** Repeated squaring, as above. The unit-cost time is $n$, and a real computation of $2^{2^n}$ needs at least $2^n$ bit operations just for the output.
- **Sound with a modulus.** [Binary exponentiation](/binary-exponentiation/) of $a^e \bmod m$ with $m$ less than $2^w$. Every number stays below $m^2$, which fits in two words. With $e$ also below $2^w$, the unit-cost time is $O(\log e)$ steps. If $m$ has $b$ bits and $b$ is not bounded by the word size, the cost must be counted in bit operations, with the cost of [integer multiplication](/integer-multiplication/).

## Where it is used

- The running times of most algorithms in textbooks, in particular the bounds on sorting, searching, graph algorithms and data structures, are unit-cost bounds on a RAM with words of $\Theta(\log n)$ bits. CLRS states this assumption in its description of the RAM model.
- The [word RAM](/word-ram/) makes the assumption explicit, and so makes the unit-cost bounds exact statements about a defined machine.
- Algorithms on [big integers](/big-integer/) and on [arbitrary precision arithmetic](/arbitrary-precision-arithmetic/) must not charge one step for each big-integer operation. They count bit operations, or word operations on a word RAM.
- The [comparison model](/comparison-model/) is a stricter model that counts only comparisons. A lower bound there holds for a unit-cost RAM program that uses its keys only in comparisons.

## References

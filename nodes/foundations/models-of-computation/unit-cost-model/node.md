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
see_also: [logarithmic-cost-model, word-ram, transdichotomous-model, ram-turing-equivalence, integer-multiplication, big-integer, pspace, integer-factorization]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, the RAM model and the assumption that a word has c lg n bits
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 1, the uniform and logarithmic cost criteria for RAM programs
  - paper: doi:10.1016/S0022-0000(73)80029-7
    title: Stephen A. Cook and Robert A. Reckhow, Time bounded random access machines, Journal of Computer and System Sciences 7(4) (1973)
    locator: pp. 354 to 375 (the cost function l(n), and the simulation by a Turing machine in time T(n)^3 when l(n) is constant)
  - paper: doi:10.1109/SWAT.1974.20
    title: Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974)
    locator: pp. 13 to 23 (polynomial time on the RAM with multiplication and Boolean operations equals PSPACE)
  - paper: doi:10.1016/0020-0190(79)90087-5
    title: Adi Shamir, Factoring numbers in O(log n) arithmetic steps, Information Processing Letters 8(1) (1979)
    locator: pp. 28 to 31
  - paper: "Vaughan R. Pratt, Michael O. Rabin and Larry J. Stockmeyer, A characterization of the power of vector machines, Proceedings of the 6th Annual ACM Symposium on Theory of Computing (STOC 1974)"
    locator: the main theorem (polynomial time on vector machines equals PSPACE)
  - paper: "Peter van Emde Boas, Machine models and simulations, in Handbook of Theoretical Computer Science, volume A, Elsevier and MIT Press (1990)"
    locator: Chapter 1, the invariance thesis and the first and second machine classes
---

The unit-cost model is the rule that every instruction of a [random access machine](/random-access-machine/) costs one step, whatever the size of its operands. The running time of a program is then the number of instructions that it executes. Most analyses of algorithms use this rule, and it is sound when every number that the program handles has $O(\log n)$ bits, where $n$ is the input size. It fails when a program can build much longer numbers, because one step then does the work of many bit operations, and the [logarithmic-cost model](/logarithmic-cost-model/) or the [word RAM](/word-ram/) is the correct model.

## In plain words

A computer adds two numbers in one step if each number fits in a machine word. The unit-cost model says: count every such step as one unit, and do not ask how big the numbers are.

This is a good rule when the numbers stay small. A loop counter, an array index and a key that fits in a word are small. The rule is bad when a program makes very large numbers. A real machine needs many steps to add two numbers with a million digits, but the unit-cost model still counts one step.

So the rule is a promise that the numbers stay small. When the promise holds, the step count predicts the real time well. When it does not hold, the step count can be wrong by an exponential factor, and you must count bit operations instead.

## The idea

### The rule

In the unit-cost model, each instruction of the RAM costs 1: a load, a store, an addition, a subtraction, a comparison, a jump, and (when the machine has them) a multiplication, a division, a shift and a bitwise operation. A register can hold an integer of any size. The time of a program on an input is the number of instructions that it executes, and the space is the number of registers that it uses. Aho, Hopcroft and Ullman call this the *uniform cost criterion*. Cook and Reckhow (1973) write it as the cost function $l(n) = 1$.

### When the rule is sound

Let a program run on an input of size $n$. Suppose that, at each step, each number in a register and each address in use has absolute value less than $n^c$, for a constant $c \ge 1$ and $n \ge 2$. Then each number has at most $c \lg n + 1$ bits. A processor with words of $\Theta(\log n)$ bits holds each number in $O(1)$ words, and does each instruction in $O(1)$ word operations. This is the assumption of the [word RAM](/word-ram/) and of the [transdichotomous model](/transdichotomous-model/).

Under this assumption the unit-cost time $T_{\text{unit}}$ and the [logarithmic-cost](/logarithmic-cost-model/) time $T_{\log}$ of the same run satisfy

$$T_{\text{unit}} \le T_{\log} \le (k c \lg n + k) \cdot T_{\text{unit}},$$

where $k$ is the largest number of values (operands, results and addresses) that one instruction touches. Proof: under the logarithmic rule each instruction costs the sum of the bit lengths of the values that it touches. Each bit length is at least 1, so each instruction costs at least 1. There are at most $k$ values, each of at most $c \lg n + 1$ bits, so each instruction costs at most $k(c \lg n + 1)$. Sum over the $T_{\text{unit}}$ instructions of the run.

Both bounds can be tight. A loop that counts from 1 to $n$ has unit-cost time $\Theta(n)$ and logarithmic-cost time $\Theta(n \log n)$ (see the [logarithmic-cost model](/logarithmic-cost-model/)). So a bound that is exact to within a $\log n$ factor must name its cost model.

### How fast numbers grow

Let $b_0 \ge 1$ be the largest bit length of an input number or a constant of the program, and let $L_t$ be the largest bit length of a number in a register after $t$ instructions.

- **Addition and subtraction only.** For integers $x, y$ we have $|x \pm y| \le 2 \max(|x|, |y|)$, so a result has at most one bit more than its longer operand. By induction on $t$, $L_t \le b_0 + t$. The logarithmic cost of a run of $t$ instructions is then at most $k t (b_0 + t)$, a polynomial in $t$ and $b_0$.
- **With multiplication.** If $x$ and $y$ have $a$ and $b$ bits, then $|xy| < 2^{a+b}$, so $xy$ has at most $a + b$ bits. By induction, $L_t \le 2^t b_0$.

Repeated squaring comes close to the second bound. Take $x_0 = 2$ and $x_{k+1} = x_k^2$. By induction $x_k = 2^{2^k}$, because $x_0 = 2 = 2^{2^0}$ and $(2^{2^k})^2 = 2^{2^{k+1}}$. The number $2^{2^k}$ has $2^k + 1$ bits, against the bound $2^k \cdot 2$ with $b_0 = 2$.

| $k$ | $x_k$ | bits of $x_k$ |
|---|---|---|
| 0 | 2 | 2 |
| 1 | 4 | 3 |
| 2 | 16 | 5 |
| 3 | 256 | 9 |
| 4 | 65536 | 17 |
| 5 | $2^{32}$ | 33 |

So $n$ unit-cost multiplications build a number of $2^n + 1$ bits, and a machine that writes one bit in each step needs at least $2^n + 1$ steps to write it down.

### What the extra power buys

The growth of numbers is not only a matter of cost. Long numbers act as a large parallel memory, and a unit-cost RAM can use them to solve hard problems in few steps.

- **Without multiplication.** Cook and Reckhow (1973) proved that a multitape Turing machine simulates their RAM with $l(n) = 1$, which has addition and subtraction but no multiplication, in time $O(T(n)^3)$. So this unit-cost RAM decides the same languages in polynomial time as the [Turing machine](/turing-machine/).
- **With multiplication and Boolean operations.** Hartmanis and Simon (1974) proved that a unit-cost RAM with multiplication and bitwise Boolean operations on integers of unbounded size decides in polynomial time exactly the languages in [PSPACE](/pspace/). Nondeterminism adds nothing there: nondeterministic polynomial time on this machine is also PSPACE. So, unless $\mathsf{P} = \mathsf{PSPACE}$, this model is stronger than any machine that the Turing machine simulates with a polynomial loss of time.
- **With shifts and Boolean operations.** Pratt, Rabin and Stockmeyer (1974) proved the same equality with PSPACE for *vector machines*, which do bitwise operations and shifts on bit vectors of unbounded length at unit cost. A left shift by an amount that is itself a large number makes a long number in one step, as a multiplication does.
- **With division.** Shamir (1979) showed that a unit-cost RAM with addition, subtraction, multiplication and integer division finds a nontrivial factor of a composite number $N$ in $O(\log N)$ steps. A simpler form of the idea uses this fact: for $N \ge 2$, the smallest prime factor of $N$ is the smallest $k$ with $\gcd(N, k!) > 1$. For $N = 91$ we have $\gcd(91, 6!) = 1$ and $\gcd(91, 7!) = 7$. The numbers $k!$ have about $k \lg k$ bits, so the step count says nothing about the real cost of [integer factorization](/integer-factorization/).

Van Emde Boas (1990) uses this split to define two classes of machines. The *first machine class* holds the models that simulate the Turing machine, and are simulated by it, with a polynomial loss of time and a constant-factor loss of space: the Turing machine itself, and the RAM under the logarithmic rule. The *second machine class* holds the models whose polynomial time is PSPACE, such as the unit-cost RAM with multiplication and Boolean operations.

There are two usual repairs. One is to bound the numbers: the [word RAM](/word-ram/) has words of $w$ bits and does arithmetic modulo $2^w$, at unit cost. The other is to charge by length: the [logarithmic-cost model](/logarithmic-cost-model/).

## Examples

- **Sound.** [Binary search](/binary-search/) on a sorted array of $n$ items. The registers hold indices from $0$ to $n$ and keys. If each key has $O(\log n)$ bits, the unit-cost count of at most $\lceil \lg(n+1) \rceil$ probes (20 probes for $n = 10^6$) is the right order of the real time.
- **Sound.** [Merge sort](/merge-sort/) on $n$ keys that each fit in a word. The unit-cost time $\Theta(n \log n)$ counts word operations, and no number is longer than a key or an index.
- **Not sound.** Computing the Fibonacci number $F_n$ with $n - 1$ additions. The unit-cost time is $n - 1$. But $F_k$ has $k \lg \varphi + O(1)$ bits, where $\varphi = (1 + \sqrt 5)/2$ and $\lg \varphi \approx 0.694$, so the additions together touch $\Theta(n^2)$ bits. For $n = 1000$, $F_{1000}$ has 694 bits, and the bit lengths of $F_1, \dots, F_{999}$ add up to 346115. See [Fibonacci numbers](/fibonacci-numbers/).
- **Not sound.** Repeated squaring, as in the table above. The unit-cost time is $n$, and the output $2^{2^n}$ alone has $2^n + 1$ bits.
- **Sound with a modulus.** [Binary exponentiation](/binary-exponentiation/) of $a^e \bmod m$ with $a, m < 2^w$ and $e < 2^w$. Each product is less than $m^2 < 2^{2w}$, so it fits in two words, and the unit-cost time is $O(\log e)$. If $m$ has $b$ bits and $b$ is not bounded by the word size, each product is a [big integer](/big-integer/) product, and the cost must include the cost of [integer multiplication](/integer-multiplication/) of $b$-bit numbers.

## Where it is used

- Most running times in algorithm textbooks, for sorting, searching, graphs and data structures, are unit-cost bounds on a RAM whose words have $\Theta(\log n)$ bits. CLRS states this assumption in Section 2.2: a word has $c \lg n$ bits for a constant $c \ge 1$.
- The [word RAM](/word-ram/) builds the assumption into the model, so that a unit-cost bound becomes an exact statement about a defined machine.
- The [comparison model](/comparison-model/) counts only comparisons. Its lower bounds hold for every unit-cost RAM program that uses the keys only in comparisons.
- Algorithms on [big integers](/big-integer/) and on [arbitrary precision arithmetic](/arbitrary-precision-arithmetic/) do not charge one step for an operation on a long number. They count bit operations, or word operations on a word RAM.

### Pitfalls

- **Unit cost with no bound on the numbers.** A bound such as "factoring in $O(\log N)$ steps" or "PSPACE in polynomial time" is true on the unit-cost RAM with multiplication, and says nothing about real machines. Check that each number stays polynomial in the input size before you trust a unit-cost bound.
- **Counting the input in items, not bits.** An input of $m$ integers of $b$ bits each has $m b$ bits. A unit-cost bound in $m$ hides the factor $b$ when $b$ is large, as in algorithms on big integers.
- **Pseudo-polynomial time.** An algorithm with $O(nW)$ unit-cost steps, such as the dynamic program for the [subset sum problem](/subset-sum-problem/) with target $W$, is not polynomial in the input size, because $W$ has only $\lg W$ bits in the input.
- **Shifts and divisions are not harmless.** A left shift by a large amount builds a long number as a multiplication does, and division with multiplication gives fast factoring. A model with these instructions must bound the word size.
- **Comparing bounds across models.** A $\Theta(n)$ bound in the unit-cost model and a $\Theta(n \log n)$ bound in the logarithmic-cost model can describe the same program. Say which model a bound uses.

## References

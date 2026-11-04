---
tag: MJAXQZ
kind: concept
slug: logarithmic-cost-model
name: Logarithmic-cost model
aliases:
- logarithmic cost criterion
- bit-cost model
area: foundations/models-of-computation
level: core
summary: RAM cost measure where an operation costs time proportional to the bit length of its operands.
prereqs: [random-access-machine, unit-cost-model, logarithms]
see_also: [turing-machine, ram-turing-equivalence, word-ram, integer-multiplication, big-integer, multitape-turing-machine]
sources:
  - paper: "Cornelis Slot and Peter van Emde Boas, The problem of space invariance for sequential machines, Information and Computation 77(2) (1988)"
    locator: pages 93 to 122
  - paper: "David Harvey and Joris van der Hoeven, Integer multiplication in time O(n log n), Annals of Mathematics 193(2) (2021)"
    locator: pages 563 to 617
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms
    locator: Chapter 1, uniform and logarithmic cost criteria for RAM programs, and the simulation of a RAM by a Turing machine
  - paper: "Stephen A. Cook and Robert A. Reckhow, Time-bounded random access machines, Journal of Computer and System Sciences 7(4) (1973)"
    locator: pages 354 to 375
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, the RAM model and the word size limit
---

The logarithmic-cost model is a cost rule for a [random access machine](/random-access-machine/) in which an instruction costs the bit length of the numbers that it uses. Adding two numbers of $b$ bits costs about $b$, not 1. The rule is faithful to the cost on a machine that works bit by bit, and it makes the RAM and the [Turing machine](/turing-machine/) agree up to a polynomial factor. It is the correct rule when a program handles numbers of unbounded size, where the [unit-cost model](/unit-cost-model/) is not sound.

## In plain words

On paper, you add two numbers digit by digit. A number with twice as many digits takes about twice as long. The logarithmic-cost model copies this. It charges for an instruction by the number of digits (in base two) of the numbers that the instruction touches.

A number with a million digits is a long number, and an instruction on it is a long job. A counter that reaches a million has only about 20 binary digits, because the number of digits grows like the logarithm of the number. This is why the model has this name.

The price is that analysis is harder, because each step needs a bit length. The gain is that the answer no longer hides work in huge numbers. You use this model when the numbers can be large, as in number theory, exact arithmetic and cryptography.

## The idea

### The cost of a number

For an integer $m$, let $l(m)$ be its bit length, as AHU define it:

$$l(m) = \begin{cases} \lfloor \lg |m| \rfloor + 1 & m \ne 0, \\ 1 & m = 0. \end{cases}$$

So $l(1) = 1$, $l(2) = l(3) = 2$, $l(4) = \dots = l(7) = 3$, and $l(m) = \Theta(\log |m|)$ for $|m| \ge 2$. Here $\lg = \log_2$, see [logarithms](/logarithms/).

### The cost of an instruction

Under the logarithmic-cost rule, the cost of an instruction is the sum of $l(\cdot)$ over the addresses that it uses and the values that it reads or writes. For example, "add the content of register $a$ to the [accumulator](/random-access-machine/)" costs $l(a) + l(c(a)) + l(\text{accumulator})$, where $c(a)$ is the content of register $a$. An access through a pointer pays for the pointer value and for the content that it reaches. The exact list differs between texts. They agree up to a constant factor, and a constant factor does not change an asymptotic bound. In a direct access the address $a$ is a constant of the program, so $l(a)$ is a constant. In an indirect access, the bit length $l(c(a))$ of the pointer is what matters: charging it stops a program from reaching huge addresses for free.

The cost of a program is the sum of the costs of the instructions that it executes. The space of a program is the sum, over all registers that it uses (including the accumulator), of $l(x_i)$, where $x_i$ is the number of largest magnitude ever stored in register $i$ (this is the definition of AHU). Slot and van Emde Boas (1988) study how this space compares with the space of a Turing machine. Polynomial relation of the two measures is enough to keep the class $\mathsf{PSPACE}$ the same. A class such as $\mathsf{L}$ needs a relation within a constant factor, and this needs a more careful measure of space than the one above.

### The charge for multiplication

The rule above charges a multiplication of numbers with $a$ and $b$ bits a cost of order $a + b$. No multitape Turing machine is known to multiply two $n$-bit numbers in $O(n)$ time, and no Boolean circuit of size $O(n)$ is known. The best Turing machine bound is $O(n \log n)$ (Harvey and van der Hoeven, 2021; see [integer multiplication](/integer-multiplication/)). So a model with multiplication must state its charge. A common choice is the cost of the best known multiplication algorithm, and a simple choice is $\Theta(ab)$ for the schoolbook method. The simulation theorem below is stated for programs without multiplication and division. The size of the input is the sum of $l(x_i)$ over the input numbers $x_i$. If a multiplication or division of numbers with $a$ and $b$ bits is charged at least $a + b$, the simulation still runs in $O(T(n)^2)$ steps. Each register still holds $O(T(n))$ bits, the Turing machine multiplies by the schoolbook method in $O(c_i^2)$ steps, where $c_i$ is the charge of the instruction, and the sum of the squares of the charges is at most $T(n)^2$.

### Relation to the Turing machine

Assume $T(n) \ge n$, so that the program can read its input. AHU prove that a RAM program, with the instructions load, store, add, subtract, read, write, an unconditional jump, the conditional jumps JGTZ (jump if the accumulator is positive) and JZERO (jump if the accumulator is zero), and halt, but no multiplication or division, that runs in logarithmic-cost time $T(n)$ can be simulated by a multitape [Turing machine](/multitape-turing-machine/) in $O(T(n)^2)$ steps. The square comes from this: the program makes at most $T(n)$ accesses, and the Turing machine simulates each one by a scan of a tape of length $O(T(n))$. The other direction, the simulation of a Turing machine by a RAM, also has a polynomial overhead. So the two models define the same class of polynomial-time computations. Cook and Reckhow (1973) define RAMs with a general cost function $l(n)$, study the logarithmic case $l(n) = \log n$, and prove that such RAMs and multitape Turing machines simulate each other with polynomial overhead. This is the reason why logarithmic cost is the standard rule in complexity theory. See [the equivalence of the RAM and the Turing machine](/ram-turing-equivalence/).

The unit-cost model with multiplication does not have this property. Start with $x = 2$ and square it $n$ times. Then $n$ unit-cost instructions produce $2^{2^n}$, a number with $2^n + 1$ bits, and a Turing machine needs at least $2^n + 1$ steps to write it. Under the logarithmic-cost rule, the same program costs at least $2^n + n - 1$, because for $k = 0, \dots, n-1$ the squaring number $k+1$ has the operand $2^{2^k}$ with $2^k + 1$ bits, and $\sum_{k=0}^{n-1} (2^k + 1) = 2^n + n - 1$.

The rule also bounds the growth of numbers. A multiplication of numbers of $a$ and $b$ bits gives a result of at most $a + b$ bits, and the instruction costs at least $a + b$ under the rule above. An addition gives a result of at most $\max(a, b) + 1$ bits. So the result of an instruction is never much longer than the cost of that instruction. A number is never much longer than the total cost so far, plus the length of the input and of the constants of the program.

## Examples

- **A counter.** The loop that adds 1 to a register $n$ times, starting at 0, costs $\sum_{i=1}^{n} l(i)$ in the register part alone. This sum is at most $n (\lfloor \lg n \rfloor + 1)$. It is at least $(n/2) \lfloor \lg n \rfloor$, because at least $n/2$ of the values $i$ satisfy $i > n/2$, and for these $l(i) \ge \lfloor \lg n \rfloor$. So the sum is $\Theta(n \log n)$. For $n = 1000$ the sum is exactly 8987. The unit-cost time of the same loop is $n$.
- **Adding $n$ numbers of $b$ bits.** Each partial sum is less than $n \cdot 2^b$, so it has at most $b + \lceil \lg n \rceil$ bits. The cost is $O(n (b + \log n))$.
- **Fibonacci numbers by addition.** The number $F_k$ has about $0.694 k$ bits, so the $n - 1$ additions cost $\Theta(n^2)$ in total, against $n - 1$ in the unit-cost model. See [Fibonacci numbers](/fibonacci-numbers/).
- **Repeated squaring.** The program that squares $x = 2$ a total of $n$ times costs $\Theta(2^n)$ when a multiplication of $b$-bit numbers is charged $\Theta(b)$, as in the rule above. It costs $\Omega(2^n)$ under any charge of at least $b$, for example $\Theta(4^n)$ under the schoolbook charge $\Theta(b^2)$. In the unit-cost model it costs $n$.
- **Bounded numbers.** If every value and every address that a program uses during its run is less than $n^c$, its logarithmic cost is at most $O(c \log n)$ times its unit cost, and at least its unit cost. For such a program the two rules give the same bound up to a logarithmic factor. See the [unit-cost model](/unit-cost-model/).

## Where it is used

- Complexity theory, to link the RAM to the [Turing machine](/turing-machine/) and to define polynomial time on both.
- Algorithms on big numbers: [integer multiplication](/integer-multiplication/), division, greatest common divisor, primality tests and [big integer](/big-integer/) libraries. Their bounds count bit operations.
- Any algorithm in which a number can grow with the running time, such as an exact computation with rationals, or a computation of $a^b$ without a modulus.
- Textbooks state the unit-cost bound for an algorithm and then check that the numbers stay small. A [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits builds this check into the model.

## References

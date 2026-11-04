---
tag: 8HFM94
kind: model
slug: random-access-machine
name: Random access machine
aliases:
- RAM
area: foundations/models-of-computation
level: intro
summary: Idealized sequential machine with a random-access memory of registers, the standard model for algorithm analysis.
prereqs: [asymptotic-notation]
see_also: [word-ram, unit-cost-model, logarithmic-cost-model, real-ram, turing-machine, ram-turing-equivalence, comparison-model, cell-probe-model]
sources:
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2, the RAM model of computation
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 8.2, counting sort
  - title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 1, the sections on random access machines and on their cost
  - title: Stephen A. Cook and Robert A. Reckhow, Time-bounded random access machines, Journal of Computer and System Sciences 7(4), 1973
    locator: pp. 354 to 375
  - title: J. Hartmanis and J. Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory, 1974
    locator: the theorem that polynomial time with multiplication and Boolean instructions equals PSPACE
  - title: J. C. Shepherdson and H. E. Sturgis, Computability of recursive functions, Journal of the ACM 10(2), 1963
    locator: pp. 217 to 255
  - title: C. C. Elgot and A. Robinson, Random-access stored-program machines, an approach to programming languages, Journal of the ACM 11(4), 1964
    locator: pp. 365 to 399
---

The random access machine (RAM) is a model of a sequential computer with an unbounded sequence of numbered registers, each of which holds one integer. A program is a finite list of instructions, and an instruction can read or write the register whose number is held in another register. The time of a run is the cost of the instructions it executes. The model has two cost rules: under the [unit-cost](/unit-cost-model/) rule each instruction costs 1, and under the [logarithmic-cost](/logarithmic-cost-model/) rule an instruction costs the number of bits of the numbers it touches. Most algorithm texts use the RAM with a unit-cost rule for numbers of $O(\log n)$ bits, and this page names the rule each time.

## The machine

The memory is a sequence of registers $R_0, R_1, R_2, \ldots$. Each holds a non-negative integer, and all registers hold $0$ at the start. The register $R_0$ is the *accumulator*. The register numbers in the text of a program are at least $1$. An indirect operand whose register holds $0$ names the accumulator. A program is a finite numbered list of instructions, and the machine starts at instruction 1. After an instruction it goes to the next one, unless the instruction is a jump or a halt. The input is a finite sequence of non-negative integers $x_1, \ldots, x_m$, and the machine reads them in order. The machine used here is the accumulator machine of Aho, Hopcroft and Ullman, with the sequential input and a few changes. An operand $X$ is one of three forms: a constant $=c$, a register $i$ (the value $R_i$), or an indirect register $*i$ (the value $R_{R_i}$). The instructions are these.

- `LOAD X` sets $R_0$ to the value of $X$.
- `STORE i` sets $R_i$ to $R_0$. `STORE *i` sets $R_{R_i}$ to $R_0$.
- `ADD X` sets $R_0$ to $R_0 + v$, where $v$ is the value of $X$. `SUB X` sets $R_0$ to $\max(R_0 - v, 0)$.
- `READ` sets $R_0$ to the next input integer, or to $0$ if no input integer is left.
- `JUMP k` goes to instruction $k$. `JZERO k` goes to $k$ if $R_0 = 0$. `JEOF k` goes to $k$ if all input integers are read.
- `HALT` stops the run. The output of a decision is the value of $R_0$ at the stop: $0$ rejects and any other value accepts. The programs on this page halt with $R_0 \in \{0, 1\}$.

The indirect operand makes the model *random access*: a program can compute an address and then read or write that register in one instruction, so every register is as near as every other. Texts differ in the details. Some use three-address instructions such as $R_i \leftarrow R_j + R_k$, some add multiplication and division, and some put the input in the first registers. Multiplication changes the cost analysis (see below). An input in registers that the program can index changes what a [Turing machine](/turing-machine/) can simulate (see [RAM and Turing machine equivalence](/ram-turing-equivalence/)).

Shepherdson and Sturgis (1963) defined the unlimited register machine, a register machine with no indirect operand. Elgot and Robinson (1964) studied the RASP, a RAM whose program is stored in the registers, so that a run can change its own instructions. Cook and Reckhow (1973) gave the standard time-bounded RAM with both cost rules. Aho, Hopcroft and Ullman (1974, Chapter 1) show that the RAM and the RASP simulate each other with a constant-factor loss of time.

## What it counts

Under the **unit-cost rule**, each executed instruction costs 1, so the time is the number of instructions executed. The space is the number of distinct registers that the run writes.

Under the **logarithmic-cost rule**, the length of a non-negative integer $x$ is $\ell(x) = \lfloor \lg x \rfloor + 1$ for $x \ge 1$ and $\ell(0) = 1$. An instruction costs the sum of the lengths of the numbers it reads, writes or uses as an address. With $c(i)$ for the value of $R_i$, the costs are:

| Instruction | Cost |
|---|---|
| `LOAD =c` | $\ell(c)$ |
| `LOAD i` | $\ell(i) + \ell(c(i))$ |
| `LOAD *i` | $\ell(i) + \ell(c(i)) + \ell(c(c(i)))$ |
| `STORE i` | $\ell(c(0)) + \ell(i)$ |
| `STORE *i` | $\ell(c(0)) + \ell(i) + \ell(c(i))$ |
| `ADD X`, `SUB X` | $\ell(c(0))$ plus the cost of `LOAD X` |
| `READ` | $\ell(x)$ for the integer $x$ read |
| `JZERO` | $\ell(c(0))$ |
| `JUMP`, `JEOF`, `HALT` | $1$ |

The time is the sum of the costs of the executed instructions. The space is the largest total of $\ell(c(i))$ over the registers at one moment of the run. The size $n$ of an input is the sum of $\ell(x_j) + 1$ over the input integers, which is the length of the input as a string. A time bound $t(n)$ is the worst case over the inputs of size $n$.

**Example.** The program below adds the $m$ input integers and halts with the sum in $R_0$. The register $R_1$ holds the sum.

```text
1  LOAD =0
2  STORE 1
3  JEOF 8
4  READ
5  ADD 1
6  STORE 1
7  JUMP 3
8  LOAD 1
9  HALT
```

Instructions 1 and 2 run once. Instructions 3 to 7 run once for each input integer. Instructions 3, 8 and 9 run once more at the end. So the unit-cost time is $5m + 5$: for the input $5, 3, 8$ it is $20$ and the output is $16$.

For the logarithmic cost, write $s_i$ for the sum of the first $i$ integers and $x_i$ for the $i$-th one. The $i$-th round costs $1 + \ell(x_i) + (\ell(x_i) + 1 + \ell(s_{i-1})) + (\ell(s_i) + 1) + 1 = 2\ell(x_i) + \ell(s_{i-1}) + \ell(s_i) + 4$. The set-up costs $1 + 2 = 3$ and the end costs $1 + (1 + \ell(s_m)) + 1$. So the total is

$$
6 + \ell(s_m) + \sum_{i=1}^{m} \bigl( 2\ell(x_i) + \ell(s_{i-1}) + \ell(s_i) + 4 \bigr).
$$

For $5, 3, 8$ this is $61$. Suppose that each $x_i$ has exactly $b$ bits. Then $i\,2^{b-1} \le s_i < i\,2^b$, so $b + \lfloor \lg i \rfloor \le \ell(s_i) \le b + \lfloor \lg i \rfloor + 1$. The sum of $\lfloor \lg i \rfloor$ for $i \le m$ is $m \lg m - O(m)$, so the logarithmic-cost time is $\Theta(m b + m \lg m)$. The input size is $n = m(b+1)$, so the time is $\Theta(n + m \lg m)$, which is more than linear in $n$ when $b = o(\lg m)$, for example when every $x_i = 1$. The unit-cost time $\Theta(m)$ hides the cost of the large numbers.

## Relation to other models

The unit-cost rule does not match real computers when numbers can grow without bound. If the instruction set has multiplication (`MULT X` sets $R_0$ to $R_0 \cdot v$), the three instructions `LOAD 1`, `MULT 1`, `STORE 1` square $R_1$. Start with $R_1 = 2$. After $k$ rounds, $R_1 = 2^{2^k}$, a number of $2^k + 1$ bits, and the unit-cost time is $3k + O(1)$. Time polynomial in $k$ produces a number with exponentially many bits. With addition and subtraction only, a value at most doubles in each instruction, so after $t$ instructions every value has at most $t + b$ bits, where $b$ bounds the length of the program constants and of the input integers. Then each instruction costs $O(t + b)$ in the logarithmic-cost rule, and the logarithmic-cost time is $O(t(t+b))$ for a unit-cost time $t$.

The RAM with logarithmic cost and the [Turing machine](/turing-machine/) simulate each other with a polynomial loss of time. [RAM and Turing machine equivalence](/ram-turing-equivalence/) states and proves the bounds: $O(t^2)$ steps of a multitape machine for a RAM of logarithmic-cost time $t$, and $O(T \log T)$ logarithmic-cost time of a RAM for a multitape machine of time $T$. So the class of polynomial-time languages is the same on both models. See [unit-cost model](/unit-cost-model/) and [logarithmic-cost model](/logarithmic-cost-model/) for the two rules.

The [word RAM](/word-ram/) limits each register to $w$ bits, with $w \ge \lg n$, and it counts each instruction as 1. This is the model of CLRS Section 2.2: a word has $c \lg n$ bits for a constant $c \ge 1$. The limit keeps the unit-cost rule realistic. The [real RAM](/real-ram/) lets each register hold a real number with exact arithmetic at unit cost. Real computers do not do this, so its bounds do not carry over to them directly.

A RAM can use a key as an address, so on integer keys it can beat the lower bounds of the [comparison model](/comparison-model/). The [cell-probe model](/cell-probe-model/) counts only the reads and writes of memory cells. A cell-probe lower bound for cells of $w$ bits is also a lower bound for the word RAM with $w$-bit words, because each instruction reads or writes $O(1)$ cells.

## Known results in the model

- **Counting sort.** Sorting $n$ integers in the range $0$ to $k - 1$ takes $O(n + k)$ time on the unit-cost RAM with $O(n + k)$ extra space (CLRS Section 8.2). This is $o(n \lg n)$ when $k = o(n \lg n)$, and linear when $k = O(n)$. See [counting sort](/counting-sort/) and the [sorting problem](/sorting-problem/).
- **Polynomial equivalence with the Turing machine.** The two models decide the same languages in polynomial time when the RAM has logarithmic cost, or has unit cost without multiplication. See [RAM and Turing machine equivalence](/ram-turing-equivalence/).
- **Exponential gap with multiplication.** With unit-cost multiplication, the RAM builds a number of $2^k$ bits in $O(k)$ steps, as shown above. A machine that writes this number out needs at least $2^k$ steps, so a step-by-step simulation that stores the register contents is not polynomial. This does not by itself separate the languages decided. Hartmanis and Simon (1974) showed that polynomial time on a unit-cost RAM with multiplication and bitwise Boolean instructions equals [PSPACE](/pspace/).

## References

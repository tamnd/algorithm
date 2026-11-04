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
see_also: [word-ram, unit-cost-model, logarithmic-cost-model, real-ram, turing-machine, ram-turing-equivalence, register-machine, pointer-machine]
sources:
  - book: isbn:9780201000290
    title: Alfred V. Aho, John E. Hopcroft and Jeffrey D. Ullman, The Design and Analysis of Computer Algorithms, Addison-Wesley, 1974
    locator: Chapter 1, the sections on random access machines, on the cost of RAM programs, on the stored-program model (RASP) and on the relation to Turing machines
  - paper: doi:10.1016/S0022-0000(73)80029-7
    title: Stephen A. Cook and Robert A. Reckhow, Time bounded random access machines, Journal of Computer and System Sciences 7(4) (1973)
    locator: pp. 354 to 375 (the cost function l(n), the simulations with Turing machines and with the stored-program model, and the time hierarchy)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Section 2.2 (the RAM model of computation) and Section 8.2 (counting sort)
  - paper: doi:10.1109/SWAT.1974.20
    title: Juris Hartmanis and Janos Simon, On the power of multiplication in random access machines, 15th Annual Symposium on Switching and Automata Theory (1974)
    locator: pp. 13 to 23 (polynomial time with multiplication and Boolean instructions equals PSPACE)
  - paper: doi:10.1145/321160.321170
    title: John C. Shepherdson and Howard E. Sturgis, Computability of recursive functions, Journal of the ACM 10(2) (1963)
    locator: pp. 217 to 255
  - paper: doi:10.1145/321239.321240
    title: Calvin C. Elgot and Abraham Robinson, Random-access stored-program machines, an approach to programming languages, Journal of the ACM 11(4) (1964)
    locator: pp. 365 to 399
  - paper: "Peter van Emde Boas, Machine models and simulations, in Handbook of Theoretical Computer Science, volume A, Elsevier and MIT Press (1990)"
    locator: Chapter 1, the RAM variants, the invariance thesis and the first and second machine classes
---

The random access machine (RAM) is a model of a sequential computer with an unbounded sequence of numbered registers, each of which holds one integer. A program is a finite list of instructions, and an instruction can read or write the register whose number is held in another register. The time of a run is the total cost of the instructions it executes. The model has two cost rules: under the [unit-cost](/unit-cost-model/) rule each instruction costs 1, and under the [logarithmic-cost](/logarithmic-cost-model/) rule an instruction costs the number of bits of the numbers it touches. Algorithm texts use the unit-cost RAM with numbers of $O(\log n)$ bits, which is the [word RAM](/word-ram/), and complexity theory uses the logarithmic-cost RAM.

## The machine

The memory is a sequence of registers $R_0, R_1, R_2, \ldots$. Each holds a non-negative integer of any size, and all registers hold $0$ at the start. The register $R_0$ is the *accumulator*. A program is a finite numbered list of instructions, and the machine starts at instruction 1. After an instruction it goes to the next one, unless the instruction is a jump or a halt. The input is a finite sequence of non-negative integers $x_1, \ldots, x_m$, and the machine reads them in order.

An operand $X$ has one of three forms: a constant $=c$, a register $i$ (the value $R_i$), or an indirect register $*i$ (the value $R_{R_i}$). The instructions are these.

- `LOAD X` sets $R_0$ to the value of $X$.
- `STORE i` sets $R_i$ to $R_0$. `STORE *i` sets $R_{R_i}$ to $R_0$.
- `ADD X` sets $R_0$ to $R_0 + v$, where $v$ is the value of $X$. `SUB X` sets $R_0$ to $\max(R_0 - v, 0)$.
- `READ` sets $R_0$ to the next input integer, or to $0$ if no input integer is left.
- `JUMP k` goes to instruction $k$. `JZERO k` goes to $k$ if $R_0 = 0$. `JEOF k` goes to $k$ if all input integers are read.
- `HALT` stops the run. The output of a decision is the value of $R_0$ at the stop: $0$ rejects and any other value accepts.

The indirect operand makes the model *random access*: a program computes an address and then reads or writes that register in one instruction, so every register is as near as every other. An array $A[0 \ldots n-1]$ stored from register $B$ on is read with `LOAD =B`, `ADD j`, `STORE t`, `LOAD *t`, which loads $A[R_j]$ in four instructions whatever $R_j$ is.

This machine is the accumulator machine of Aho, Hopcroft and Ullman (AHU) with three changes. AHU allow negative integers, so their `SUB` does not stop at $0$, and they have `JGTZ` (jump if $R_0 > 0$) in place of `JEOF`. They also have `MULT`, `DIV` and an output tape with `WRITE`. Other texts use three-address instructions such as $R_i \leftarrow R_j + R_k$, or put the input in the first registers. These choices change running times by at most a constant factor, with two exceptions: multiplication and division under the unit-cost rule (see [Known results in the model](#known-results-in-the-model)), and an input in registers that the program can index, which matters for sublinear time and for simulation by a [Turing machine](/turing-machine/) (see [RAM and Turing machine equivalence](/ram-turing-equivalence/)).

Shepherdson and Sturgis (1963) defined the unlimited register machine, a [register machine](/register-machine/) whose instructions name their registers in the program text. Elgot and Robinson (1964) studied the RASP (random access stored program machine), whose program is stored in the registers, so that a run can change its own instructions. Cook and Reckhow (1973) defined the time-bounded RAM with a general cost function $l(n)$ for an operand $n$, which covers both cost rules.

## What it counts

Under the **unit-cost rule**, each executed instruction costs 1, so the time is the number of instructions executed. The space is the number of registers that the run uses.

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

The time is the sum of the costs of the executed instructions. The space is the sum, over the registers that the run uses, of $\ell$ of the largest number that the register ever holds (the AHU definition). The size $n$ of an input is the sum of $\ell(x_j) + 1$ over the input integers, which is the length of the input as a string with a separator after each integer. A time bound $t(n)$ is the worst case over the inputs of size $n$.

**Example.** The program below adds the $m$ input integers and halts with the sum in $R_0$. The register $R_1$ holds the running sum.

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

Instructions 1 and 2 run once. Instructions 3 to 7 run once for each input integer. Instructions 3, 8 and 9 run once more at the end. So the unit-cost time is $5m + 5$. For the input $5, 3, 8$ it is $20$, and the output is $16$.

For the logarithmic cost, write $x_i$ for the $i$-th input integer and $s_i = x_1 + \cdots + x_i$, with $s_0 = 0$. The $i$-th round costs $1$ for `JEOF`, $\ell(x_i)$ for `READ`, $\ell(x_i) + \ell(1) + \ell(s_{i-1})$ for `ADD 1`, $\ell(s_i) + \ell(1)$ for `STORE 1` and $1$ for `JUMP`, so it costs $2\ell(x_i) + \ell(s_{i-1}) + \ell(s_i) + 4$. The set-up costs $\ell(0) + (\ell(0) + \ell(1)) = 3$, and the end costs $1 + (\ell(1) + \ell(s_m)) + 1 = 3 + \ell(s_m)$. So the total is

$$
6 + \ell(s_m) + \sum_{i=1}^{m} \bigl( 2\ell(x_i) + \ell(s_{i-1}) + \ell(s_i) + 4 \bigr).
$$

For $5, 3, 8$ the partial sums are $0, 5, 8, 16$ with lengths $1, 3, 4, 5$. The three rounds cost $14$, $15$ and $21$, and the total is $6 + 5 + 50 = 61$.

Suppose now that each $x_i$ has exactly $b$ bits. Then $i\,2^{b-1} \le s_i < i\,2^b$, so $b + \lfloor \lg i \rfloor \le \ell(s_i) \le b + \lfloor \lg i \rfloor + 1$. The sum of $\lfloor \lg i \rfloor$ for $1 \le i \le m$ is $m \lg m - O(m)$, so the logarithmic-cost time is $\Theta(m b + m \log m)$. The input size is $n = m(b+1)$, so the time is $\Theta(n + m \log m)$. This is more than linear in $n$ when $b = o(\log m)$, for example when every $x_i = 1$: the sum then grows to $m$, and each update of it costs $\Theta(\log m)$. The unit-cost time $\Theta(m)$ hides this cost.

## Relation to other models

- **Turing machine.** The RAM with logarithmic cost and the multitape [Turing machine](/turing-machine/) simulate each other with a polynomial loss of time. Cook and Reckhow (1973) proved that a Turing machine of time $T(n)$ runs on a RAM in time $O(T(n)\,l(T(n)))$, which is $O(T(n) \log T(n))$ under the logarithmic rule, and that a RAM of time $T(n)$ runs on a Turing machine in time $O(T(n)^2)$ under the logarithmic rule, and $O(T(n)^3)$ under the unit-cost rule. Their RAM has addition and subtraction but no multiplication. So polynomial time, the class [P](/p/), is the same on both models. [RAM and Turing machine equivalence](/ram-turing-equivalence/) gives the proofs.
- **Stored-program machine.** A RASP keeps its program in its registers. Cook and Reckhow (1973) and AHU show that a RAM and a RASP simulate each other with a constant-factor loss of time, under both cost rules. So the fixed program of the RAM is not a restriction.
- **Register machine.** A [register machine](/register-machine/) has a fixed finite set of registers and no indirect operand. It computes the same functions, but with an exponential loss of time when it has only increment and decrement.
- **Word RAM.** The [word RAM](/word-ram/) limits each register to $w$ bits, with $w \ge \lg n$, and counts each instruction as 1. CLRS Section 2.2 uses this model with $w = c \lg n$ for a constant $c \ge 1$. The limit keeps the unit-cost rule realistic.
- **Real RAM.** The [real RAM](/real-ram/) lets each register hold a real number, with exact arithmetic at unit cost. Real computers do not do this, so its bounds do not carry over to them directly.
- **Pointer machine.** A [pointer machine](/pointer-machine/) can follow pointers but cannot compute an address. The RAM can, so it can index an array in one step.
- **Comparison and cell-probe models.** A RAM can use a key as an address, so on integer keys it can beat the lower bounds of the [comparison model](/comparison-model/). The [cell-probe model](/cell-probe-model/) counts only the reads and writes of memory cells. A cell-probe lower bound for cells of $w$ bits is a lower bound for the word RAM with $w$-bit words, because each instruction reads or writes $O(1)$ cells.
- **Parallel RAM.** The [PRAM](/pram-model/) has many RAM processors that share one memory and work in lockstep.

## Known results in the model

- **Counting sort.** Sorting $n$ integers in the range $0$ to $k - 1$ takes $O(n + k)$ time on the unit-cost RAM with $O(n + k)$ extra space (CLRS Section 8.2). This is $O(n)$ when $k = O(n)$, below the $\Omega(n \log n)$ [comparison sort lower bound](/comparison-sort-lower-bound/). The algorithm uses each key as an address. See [counting sort](/counting-sort/).
- **Polynomial equivalence with the Turing machine.** The RAM decides the same languages in polynomial time as the Turing machine, under the logarithmic rule, and under the unit-cost rule without multiplication (Cook and Reckhow 1973). Van Emde Boas (1990) calls the models with this property, and with a constant-factor loss of space, the *first machine class*.
- **A time hierarchy with a constant factor.** Cook and Reckhow (1973) proved this. Let $T_2(n)$ be computable by a RAM in time $O(T_2(n))$, and let $T_1(n)$ satisfy $\liminf_{n \to \infty} T_1(n)/T_2(n) = 0$. Then some set is recognized by a RAM in time $O(T_2(n))$ and by no RAM in time $O(T_1(n))$. The gap is finer than in the [time hierarchy theorem](/time-hierarchy-theorem/) for multitape Turing machines, which needs a factor $\log T_1(n)$.
- **Exponential growth with multiplication.** With a unit-cost `MULT X` that sets $R_0$ to $R_0 \cdot v$, the three instructions `LOAD 1`, `MULT 1`, `STORE 1` square $R_1$. Start with $R_1 = 2$. After $k$ rounds, $R_1 = 2^{2^k}$, a number of $2^k + 1$ bits, and the unit-cost time is $3k + O(1)$. With addition and subtraction only, a value at most doubles in each instruction, so after $t$ instructions every value has at most $t + b$ bits, where $b$ bounds the length of the program constants and of the input integers. See the [unit-cost model](/unit-cost-model/).
- **PSPACE in polynomial time.** Hartmanis and Simon (1974) proved that polynomial time on a unit-cost RAM with multiplication and bitwise Boolean instructions equals [PSPACE](/pspace/), for deterministic and for nondeterministic machines. Van Emde Boas (1990) puts such machines in the *second machine class*.

### Pitfalls

- **A unit-cost bound with growing numbers.** The unit-cost time of the summing program above is $\Theta(m)$, but its logarithmic-cost time is $\Theta(m b + m \log m)$. A unit-cost bound is meaningful only when every number stays polynomial in the input size, as on the word RAM.
- **Unit-cost multiplication.** Allowing `MULT` at unit cost with no bound on the numbers moves the model into the second machine class. Do not mix bounds proved on such a machine with bounds on real computers.
- **Space with sparse addresses.** Under the AHU definition, a run that writes to register $2^{100}$ uses only one register, but the address itself has 101 bits. Hashing or a bound on the addresses is needed before a RAM space bound becomes a bound on real memory.
- **The input as items.** An input of $m$ integers has size $\sum (\ell(x_j) + 1)$, not $m$. A bound in $m$ is a statement about the unit-cost RAM only.
- **Different instruction sets.** Texts differ in the instruction set and in where the input sits. Each change is harmless up to a constant factor, except unit-cost multiplication or division and an indexable input, so state the model when you quote a bound.

## References

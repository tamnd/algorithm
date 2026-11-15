---
tag: JYEF5C
kind: algorithm
slug: stochastic-superoptimization
name: Stochastic superoptimization
aliases:
- STOKE
area: compilers-and-program-analysis/optimizations
level: research
summary: Searches the space of instruction sequences by Markov chain Monte Carlo with a cost of correctness on tests plus speed.
model: word-ram
complexity:
  vars: {L: the number of instruction slots of a program, s: the number of steps of the chain, n: the number of initial tests, I: the number of possible inputs of the program}
  time: {worst: O(s L (n + I) + (L + I) L I)}
  space: {extra: O(L + n + I)}
properties: {deterministic: false, recursive: false, online: false, exact: false}
prereqs: [superoptimization, metropolis-hastings, three-address-code]
see_also: [cegis, translation-validation, equality-saturation, peephole-optimization, simulated-annealing, detailed-balance, program-synthesis, hamming-distance]
sources:
  - paper: doi:10.1145/2451116.2451150
    title: Eric Schkufza, Rahul Sharma and Alex Aiken, Stochastic superoptimization, Proceedings of the 18th International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2013), 305-316
    locator: the cost function with the Hamming-distance correctness term and the performance term, the four moves (opcode, operand, swap, instruction), the Metropolis acceptance rule, the synthesis and optimization phases, and the validation with counterexamples
  - paper: doi:10.1063/1.1699114
    title: Nicholas Metropolis, Arianna W. Rosenbluth, Marshall N. Rosenbluth, Augusta H. Teller and Edward Teller, Equation of state calculations by fast computing machines, The Journal of Chemical Physics 21(6), 1953, 1087-1092
    locator: the acceptance rule min(1, exp(-ΔE/kT)) for symmetric moves
  - paper: doi:10.1093/biomet/57.1.97
    title: W. K. Hastings, Monte Carlo sampling methods using Markov chains and their applications, Biometrika 57(1), 1970, 97-109
    locator: the acceptance rule for proposals that are not symmetric, and the proof that it keeps the target distribution
  - paper: doi:10.1145/36206.36194
    title: Henry Massalin, Superoptimizer, a look at the smallest program, Proceedings of the Second International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS II), 1987, 122-126
    locator: the exhaustive search by length that stochastic search replaces for long programs
  - paper: doi:10.1145/2872362.2872387
    title: Phitchaya Mangpo Phothilimthana, Aditya Thakur, Rastislav Bodik and Dinakar Dhurjati, Scaling up superoptimization, Proceedings of the 21st International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS 2016), 297-310
    locator: the comparison and combination of stochastic, enumerative and symbolic search
---

Stochastic superoptimization, as in the STOKE tool of Schkufza, Sharma and Aiken, looks for a faster loop-free program that is equivalent to a given one by a random walk over programs. The walk is a [Metropolis-Hastings](/metropolis-hastings/) chain. Its cost function adds two terms: how many output bits are wrong on a set of test inputs, and how slow the program is. Each step changes one random part of the current program and keeps the change with a probability that depends on how much the cost goes up. The chain can pass through wrong programs on its way to a right one, which lets it reach rewrites far from the start. A candidate that is right on all tests is not yet known to be right, so it must pass an equivalence check before it is accepted. When the check fails, the input it finds becomes a new test.

## In plain words

We want a shorter piece of code that does exactly what a given piece does. There are far too many pieces of code to try them all, so we take a random walk. At each step we make one small random edit: change an operation, change a register, swap two lines, or replace or delete a line. We score each piece of code by how wrong it is on some sample inputs and by how long it is. A better score is always kept. A worse score is kept only sometimes, and less often the worse it is. This lets the walk climb out of dead ends. When we find code that is right on every sample and shorter than our best, we check it on every possible input. If it fails, the failing input joins the samples. Only checked code is ever returned.

## The problem

**Machine.** A toy machine has registers `r0` to `r3` of $w$ bits. All arithmetic is modulo $2^w$. The inputs start in `r0` and `r1`, the other registers start at 0, and the output is `r0` at the end. An instruction in [toy IR](/three-address-code/) form is `rd = ra op rb` with `op` one of `+ - & | ^ << >>`, or a copy `rd = ra`. An operand is a register or the constant 1. A shift by $w$ or more gives 0. With $w = 4$ there are 716 instructions and $I = 2^{8} = 256$ inputs.

**Programs.** A program has $L$ slots. Each slot holds an instruction or is *unused*. The length $\mathrm{perf}(R)$ of a program $R$ is its number of used slots; here every instruction costs one cycle.

**Task.** Given a target program $T$, find a program $R$ that gives the same output as $T$ on every input, with $\mathrm{perf}(R)$ as small as possible. The target is loop-free, as in STOKE.

**Cost.** For a list of tests $\tau$, each an input with the output of $T$ on it,

$$\mathrm{eq}(R; \tau) = \sum_{t \in \tau} \mathrm{popcount}(R(t) \oplus T(t)), \qquad c(R) = \mathrm{eq}(R; \tau) + \mathrm{perf}(R).$$

$\mathrm{eq}$ counts the wrong output bits, the [Hamming distance](/hamming-distance/) to the right outputs. It is 0 exactly when $R$ is right on all tests. Counting bits, and not just right or wrong tests, gives the walk a slope to follow towards right programs.

**Target distribution.** For an inverse temperature $\beta > 0$, the chain is built to sample from

$$\pi(R) = \frac{e^{-\beta c(R)}}{Z}, \qquad Z = \sum_{R'} e^{-\beta c(R')},$$

over all programs with $L$ slots. Cheap programs are likely, and a program with one more wrong bit or one more instruction is $e^{\beta}$ times less likely.

**Moves.** Each step picks one of four moves with probability $\tfrac14$ each and a slot $i$ uniformly:

- *opcode*: if slot $i$ holds an operator instruction, replace the operator by another one, chosen uniformly;
- *operand*: pick an operand place of slot $i$ (the destination or a source) and replace it by another value, chosen uniformly;
- *swap*: pick a second slot $j$ uniformly and swap slots $i$ and $j$;
- *instruction*: make slot $i$ unused with probability $p_u$, or else fill it with an instruction chosen uniformly from all $N$ instructions.

A move that does not apply leaves the program as it is. The first three moves are symmetric: the chance to propose $R^*$ from $R$ equals the chance to propose $R$ from $R^*$. The instruction move is not, unless $p_u = 1/(N + 1)$. With $q(s) = p_u$ for an unused slot and $q(s) = (1 - p_u)/N$ for an instruction, its *Hastings factor* is

$$h(R, R^*) = \frac{q(R_i)}{q(R^*_i)},$$

where $R_i$ and $R^*_i$ are the old and new contents of slot $i$. For the three symmetric moves $h = 1$.

**Acceptance.** A proposal $R^*$ is accepted with probability

$$\alpha(R, R^*) = \min\left(1,\; h(R, R^*)\, e^{-\beta (c(R^*) - c(R))}\right).$$

With symmetric proposals this is the Metropolis rule $\min(1, e^{-\beta \Delta c})$, which the STOKE paper uses. Hastings added the factor $h$ for proposals that are not symmetric. Without it, the chain does not sample from $\pi$.

## The algorithm

```pseudo id=main
STOKE(T, tests, L, beta, steps)
L1  R <- T with unused slots added up to L slots; c <- cost(R)
L2  best <- T
L3  repeat steps times
L4      pick a move and propose R* from R; h <- its Hastings factor
L5      c* <- cost(R*)
L6      with probability min(1, h * exp(-beta (c* - c))) set R <- R* and c <- c*
L7      if eq(R; tests) = 0 and perf(R) < perf(best) then
L8          if R and T agree on every input then best <- R without its unused slots
L9          else add an input where R and T differ to tests; c <- cost(R)
L10 return best
```

L1 starts from the target, as in the optimization phase of STOKE. The synthesis phase starts from a random or empty program instead, and drops the performance term until it finds a right program. L8 is the equivalence check. Here it runs the two programs on all $I$ inputs. STOKE proves equivalence with an SMT solver over bit vectors, which also gives a counterexample when it fails. L9 is the same loop as [counterexample-guided inductive synthesis](/cegis/): every wrong candidate that passed the tests makes the tests stronger.

## Example

**Target.** `x + y` written with the identity $x + y = (x \oplus y) + 2(x \wedge y)$, in four instructions:

```
r2 = r0 ^ r1
r3 = r0 & r1
r3 = r3 << 1
r0 = r2 + r3
```

The tests are the inputs $(0, 0)$, $(1, 2)$, $(3, 5)$ and $(7, 9)$, with $w = 4$, $L = 4$, $\beta = 4$, $p_u = 0.2$, and random seed 1. In 50000 steps the run does this:

| step | event | program |
|---|---|---|
| 1120 | right on the 4 tests, refuted at input $(0, 1)$: it gives 2, the target gives 1 | `r3 = 1 ^ r0; r2 = r0 ^ r1; r0 = r2 << r3` |
| 1535 | checked, accepted, 3 instructions | `r0 = r1 + r0; r2 = r0 - 1; r2 = 1 - 1` |
| 2563 | checked, accepted, 2 instructions | `r0 = r1 + r0; r3 = r2 - r3` |
| 30250 | checked, accepted, 1 instruction | `r0 = r1 + r0` |

The refuted program is a good case of why the check is needed. It computes $(x \oplus y) \ll (x \oplus 1)$. On the four tests this happens to equal $x + y$ modulo 16: for $(7, 9)$ the shift is by 6, which gives 0, and $7 + 9 = 16$ is also 0. It is wrong on 233 of the 256 inputs. After the check, $(0, 1)$ is a fifth test, and the chain moves on. The two accepted programs of length 3 and 2 hold dead instructions, which the chain removes later. Massalin's search over all programs of length 0 and 1 confirms that one instruction is the least possible. With seeds 0 to 5, all six runs reach the one-instruction program within 50000 steps.

**A second target.** `2x + 2y` as `r2 = r0 + r0; r3 = r1 + r1; r0 = r2 + r3`. Exhaustive search finds that the shortest equivalent program has 2 instructions, for example `r0 = r0 + r1; r0 = r0 + r0`. With $L = 3$, all six seeds 0 to 5 reach length 2 within 50000 steps, in forms like `r0 = r0 + r1; r0 = r0 << 1`. Three of the six runs first meet a candidate that is right on the tests but wrong at $(0, 1)$.

**Tests are not proof.** With only the tests $(0, 0)$ and $(1, 2)$, the program `r0 = r0 | r1` has $\mathrm{eq} = 0$, since $0 \mid 0 = 0$ and $1 \mid 2 = 3$. The check finds $(1, 1)$, where it gives 1 and the target gives 2. It is wrong on 175 of the 256 inputs.

**The temperature.** There are 716 instructions and one unused value per slot. A move that deletes an instruction has Hastings factor $\frac{0.8/716}{0.2} \approx 0.0056$, and it lowers the cost by 1. At $\beta = 4$ it is accepted with probability $0.0056 \cdot e^4 \approx 0.31$; at $\beta = 2$ only with $0.041$. In 50000 steps with $\beta = 2$, only one of six seeds reaches one instruction, against all six with $\beta = 4$.

**The chain samples $\pi$.** On a machine with 1-bit registers, two registers, the operators `^` and `&`, and $L = 2$, there are $19^2 = 361$ programs, and $\pi$ can be computed exactly. With $\beta = 1$, $p_u = 0.5$ and 200000 steps, the visit frequencies are at total variation distance 0.027 from $\pi$. With the Hastings factor left out, the distance is 0.68: the chain spends most of its time on the empty program, because the unused slot is proposed half of the time.

## Correctness

The full proofs are in [proofs/correctness.md](proofs/correctness.md).

1. **Soundness.** The returned program agrees with $T$ on every input. `best` starts as $T$ and changes only in L8, after the check on all inputs. Being right on all tests does not suffice, as the examples show.
2. **The chain samples $\pi$.** With the tests fixed, each move with its acceptance rule satisfies detailed balance with respect to $\pi$: for $R \ne R^*$, $\pi(R)\, q(R \to R^*)\, \alpha(R, R^*) = \pi(R^*)\, q(R^* \to R)\, \alpha(R^*, R)$. A mix of such moves, chosen independently of the state, keeps $\pi$ too. The chain is irreducible, since $L$ instruction moves turn any program into any other, and aperiodic, since a move can leave the program as it is. So it converges to $\pi$ from any start.
3. **Complete in the limit.** L9 adds a new input each time, so the tests change at most $I$ times. After the last change the chain is a fixed irreducible chain on a finite set, so with probability 1 it visits a shortest equivalent program, which then passes L7 and L8. So with probability 1, `best` reaches the least length among programs of $L$ slots, but there is no bound on the time.

## Complexity

The model is the word RAM with words of at least $w$ bits. A step costs $O(L)$ for the move and $O(L \cdot |\tau|)$ for the cost, and $|\tau| \le n + I$ since each new test is a new input. A check in L8 costs $O(L \cdot I)$. A failed check adds a test, which happens at most $I$ times, and a passed check makes `best` shorter, which happens at most $L$ times. So $s$ steps take $O(s L (n + I) + (L + I) L I)$ time and $O(L + n + I)$ space. In practice $|\tau|$ stays close to $n$: the example adds one test in 50000 steps. The number of steps needed to find a short program has no useful bound. On real x86-64 code, STOKE evaluates many millions of proposals.

## Properties

- **Sound.** Only checked programs are returned. The soundness rests on the check, not on the search.
- **Randomized and incomplete.** A run of fixed length may miss the shortest program. Different seeds find different programs.
- **Works on long programs.** Exhaustive search by length tries $N^k$ programs of length $k$, which is already $716^3 \approx 3.7 \times 10^8$ at length 3 here. The chain only ever looks at one program and its neighbours, so it scales to targets of tens of instructions.
- **Loop-free targets.** The cost and the check are for straight-line code, as in STOKE.

## Variants and improvements

- **Better correctness terms.** STOKE also counts a right value in the wrong register at a small extra cost, so that the chain can find it and move it. It adds penalties for faults and undefined behaviour.
- **Real performance models.** STOKE sums the latencies of the instructions as a fast estimate of the run time, in place of the instruction count used here, and measures the final candidates by running them.
- **Floating point with tunable precision.** Schkufza, Sharma and Aiken (PLDI 2014) allow a bounded error in floating-point results, which makes faster rewrites legal.
- **Conditional correctness.** Sharma, Schkufza, Churchill and Aiken (OOPSLA 2015) optimize code under conditions that hold where it is used.
- **Mixed search.** Phothilimthana and others split the program into windows and combine stochastic, enumerative and symbolic search, which finds better code than any one of them.
- **Simulated annealing.** Lowering $\beta$ over time, as in [simulated annealing](/simulated-annealing/), trades sampling of $\pi$ for a faster descent.

## When to use it

Use it to optimize a hot, loop-free kernel of tens of instructions where a few cycles matter, such as a cryptographic or numeric inner block, and where an equivalence checker for the instruction set exists. For very short sequences, an exhaustive [superoptimizer](/superoptimization/) is complete and fast enough. For whole programs, [equality saturation](/equality-saturation/) or a [peephole optimizer](/peephole-optimization/) with known rules scales better.

## Pitfalls

- **Returning a program that only passed the tests.** A rewrite found by testing needs a proof. The example finds a program that is right on the four tests and wrong on 233 of the 256 inputs. Always check, and keep the counterexample as a test.
- **Leaving out the Hastings factor.** With a fixed $p_u$ for unused slots, the plain Metropolis rule samples a different distribution. Either include $h$ or choose the proposals so that they are symmetric.
- **A temperature that is too high.** For small $\beta$, the many long programs with dead code outweigh the few short ones, and the chain seldom shortens the program.
- **A temperature that is too low.** For large $\beta$, the chain rarely accepts a worse program, and it gets stuck near the start like a local search.
- **Checks for a model that is too small.** A check over a toy machine, or over some inputs, says nothing about the real instruction set. STOKE checks with a bit-vector model of each x86-64 instruction, and the check is only as good as that model.
- **Equivalence on outputs only.** Here only `r0` is compared. A real rewrite must also keep memory, flags and every other live register, or the check must state which of them are dead.

## Implementations

## History

Massalin's 1987 superoptimizer searched all programs by length and only scaled to a handful of instructions. Bansal and Aiken (2006) built a superoptimizer from a database of short rewrites. Schkufza, Sharma and Aiken presented STOKE at ASPLOS 2013. They replaced enumeration by a Metropolis chain over loop-free x86-64 programs, and their rewrites matched or beat the code of gcc and icc at `-O3`, and in some cases expert hand-written assembly. Later work extended STOKE to floating point with bounded error (2014) and to conditional correctness (2015), and Phothilimthana and others combined it with other searches (2016).

## References

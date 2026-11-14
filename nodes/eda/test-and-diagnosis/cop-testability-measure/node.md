---
tag: ZPFC9R
kind: algorithm
slug: cop-testability-measure
name: COP testability measure
aliases:
- controllability-observability program
- probabilistic testability
area: eda/test-and-diagnosis
level: core
summary: Brglez's probabilistic measures of the chance that a line is 1 and that it is observed under random patterns, used to predict random pattern testability.
model: word-ram
complexity:
  vars: {L: the number of lines, P: the number of gate input pins}
  time: {worst: "O(L + P)"}
  space: {extra: O(L)}
properties: {deterministic: true, exact: false, recursive: false, online: false}
history:
  year: 1984
  people: [Franc Brglez]
  note: Brglez defined the COP measures in 1984, after the signal probabilities of Parker and McCluskey (1975), to find the faults that random patterns are unlikely to detect.
prereqs: [signal-probability-propagation, stuck-at-fault-model]
see_also: [scoap, test-point-insertion, built-in-self-test, weighted-random-pattern-testing, fault-coverage, redundant-fault, model-counting, fault-simulation]
sources:
  - paper: "Franc Brglez, On testability analysis of combinational networks, Proceedings of the IEEE International Symposium on Circuits and Systems (ISCAS), vol. 1, 221 to 225, 1984"
    title: F. Brglez, On testability analysis of combinational networks, Proc. ISCAS 1984, vol. 1, 221 to 225
    locator: the definitions of the probabilistic controllability and observability, the gate rules and the detection probability
  - paper: "Kenneth P. Parker and Edward J. McCluskey, Probabilistic treatment of general combinational networks, IEEE Transactions on Computers C-24(6), 668 to 670, 1975"
    title: K. P. Parker and E. J. McCluskey, Probabilistic treatment of general combinational networks, IEEE Transactions on Computers C-24(6), 668 to 670, June 1975
    locator: signal probability, the independence assumption and the exact method for reconvergent fanout
  - paper: doi:10.1109/TC.1984.5009315
    title: Jacob Savir, Gary S. Ditlow and Paul H. Bardell, Random pattern testability, IEEE Transactions on Computers C-33(1), 79 to 90, 1984
    locator: detection probabilities under random patterns and the cutting algorithm that bounds them under reconvergence
  - book: isbn:9780792379911
    title: Michael L. Bushnell and Vishwani D. Agrawal, Essentials of Electronic Testing for Digital, Memory and Mixed-Signal VLSI Circuits, Kluwer, 2000
    locator: the chapter on testability measures
---

COP is a testability measure for combinational circuits by Brglez (1984). For every line it computes two numbers under random input vectors: the controllability $C$, which is the probability that the line is 1, and the observability $O$, which is the probability that a change of the line reaches a primary output. The product of the two numbers estimates the probability that one random vector detects a [stuck-at fault](/stuck-at-fault-model/) on the line. COP takes one forward and one backward pass, each with one rule per gate. It treats all signals as independent. The numbers are exact when the circuit has no fanout, and they can be wrong in either direction when a signal fans out and the branches meet again. Test engineers use COP to find the faults that random patterns will rarely detect, and to place test points for [built-in self-test](/built-in-self-test/).

## In plain words

Feed a circuit random inputs, each a fair coin. Some faults are found almost at once. Others need millions of vectors, because they need one rare input pattern to show up and another rare pattern to reach an output. COP estimates both chances for every wire.

It walks forward from the inputs and gives each wire the chance that it is 1. Then it walks back from the outputs and gives each wire the chance that a change on it gets through. Multiply the two and you get the chance that one random vector finds the fault. A small chance flags a hard fault. The method is fast because it never looks at more than one gate at a time, and that is also why it can be wrong when one signal reaches a gate along two paths.

## The problem

The input is a combinational circuit with $L$ lines in topological order (the stems of the inputs and gates and the fanout branches, as on the [PODEM](/podem/) page) and a probability $p_i$ for each primary input, usually $1/2$. The inputs are independent. For each line $k$ with good value $v_k$, the target values are

- $\Pr[v_k = 1]$, the exact controllability;
- $\Pr[E_k]$, where $E_k$ is the event that forcing $k$ to $\lnot v_k$ changes some primary output. This is the probability that the [Boolean difference](/transition-density/) of the outputs with respect to $k$ is 1;
- the detection probability of $k$ stuck at $s$, the probability that a random vector detects it.

All three are #P-hard to compute exactly on general circuits (see [signal probability propagation](/signal-probability-propagation/)). COP gives estimates $C[k]$, $O[k]$ and $d(k/s)$ in linear time.

## The algorithm

```pseudo id=main
COP(C, p)
L1  for each line k in topological order
L2      if k is a primary input then C[k] ← p_k
L3      else if k is a fanout branch of the stem t then C[k] ← C[t]
L4      else if k is AND or NAND then c ← ∏ C[j] over the inputs j of k
L5      else if k is OR or NOR then c ← 1 − ∏ (1 − C[j])
L6      else if k is XOR or XNOR then c ← 0, and for each input j, c ← c (1 − C[j]) + (1 − c) C[j]; for NOT and BUF, c ← C[j]
L7      C[k] ← 1 − c if k inverts, else c
L8  for each line k in reverse topological order
L9      if k is a primary output then O[k] ← 1
L10     else if k is a stem with branches b_1, …, b_m then O[k] ← 1 − ∏ (1 − O[b_i])
L11     else if k feeds one gate g then O[k] ← O[g] times
L12         ∏ S_g(j) over the other inputs j of g
L13 d(k/0) ← C[k] O[k]; d(k/1) ← (1 − C[k]) O[k]
```

$S_g(j)$ is the probability that the side input $j$ is non-controlling, so that a change of $k$ passes the gate: $C[j]$ for AND and NAND, $1 - C[j]$ for OR and NOR, and 1 for XOR, XNOR, NOT and BUF. A line with no fanout that is not an output keeps $O[k] = 0$. Line L10 combines the branches as if they reached the outputs independently.

## Example

**A tree.** Take $g = ab$, $h = c + d$ and $z = \overline{g h}$, with every $p_i = 1/2$. No net fans out.

| line | $C$ | $O$ | $d(\cdot/0)$ | $d(\cdot/1)$ |
|---|---|---|---|---|
| $a$, $b$ | 1/2 | $3/4 \cdot 1/2 = 3/8$ | 3/16 | 3/16 |
| $c$, $d$ | 1/2 | $1/4 \cdot 1/2 = 1/8$ | 1/16 | 1/16 |
| $g$ | 1/4 | $C[h] = 3/4$ | 3/16 | 9/16 |
| $h$ | 3/4 | $C[g] = 1/4$ | 3/16 | 1/16 |
| $z$ | $1 - 3/16 = 13/16$ | 1 | 13/16 | 3/16 |

The observability of $a$ is $O[g] \cdot C[b]$, since $b$ must be 1 for a change of $a$ to pass the AND. The observability of $c$ is $O[h] \cdot (1 - C[d])$, since $d$ must be 0 to let it pass the OR. Every number in the table equals the value found by enumerating the 16 vectors. If one random vector detects a fault with probability $d$, then $N$ vectors all miss it with probability $(1 - d)^N$. To detect $c$ stuck at 0 with probability 0.95, the circuit needs $N \ge \ln 20 / \ln(16/15)$, which is 47 vectors. For $a$ stuck at 0 it needs 15.

**Reconvergence.** Take $x = ab$, $y = ac$ and $z = xy$, so $a$ fans out and its branches meet at $z$.

| quantity | COP | exact |
|---|---|---|
| $C[z]$ | $1/4 \cdot 1/4 = 1/16$ | 1/8 |
| $O[a]$ | $1 - (7/8)^2 = 15/64$ | 1/4 |
| $d(a/0)$ | 15/128 | 1/8 |
| $d$ of the branch of $a$ into $x$ stuck at 1 | 1/16 | 0 |

The function is $z = abc$, but COP multiplies $C[x]$ and $C[y]$ as if they were independent. The last fault is [redundant](/redundant-fault/): with the branch at 1, $z = b \cdot ac = abc$ still. COP still predicts that one vector in 16 finds it. In the consensus circuit $p = ab$, $q = \overline{a} c$, $r = bc$, $z = p + q + r$, the redundant fault $r$ stuck at 0 gets $9/64$.

## Correctness

The [full proof](proofs/correctness.md) shows that COP is exact on fanout-free circuits. In such a circuit, the inputs of one gate read disjoint sets of primary inputs, so their values are independent, and the gate rules of lines L4 to L7 are the exact formulas for independent events. For observability, a change of line $k$ with the single fanout gate $g$ reaches the output exactly when every side input of $g$ is non-controlling and a change of $g$ reaches the output. The side inputs depend on disjoint parts of the inputs, and the second event depends only on the inputs outside the tree of $g$, so the probabilities multiply as in lines L11 and L12. A fault is detected when $k$ has the opposite value and a change of $k$ is observed, two events on disjoint inputs, which gives line L13.

With reconvergent fanout, the proof also shows by example that COP can be wrong. The stem rule of line L10 is neither an upper nor a lower bound: it is too low on the example above, and for $z = a \oplus a$, which is always 0, it gives $O[a] = 1$ where the exact value is 0.

## Complexity

Each line is visited once in each pass, and each gate input pin is read a constant number of times, so COP takes $O(L + P)$ arithmetic operations and $O(L)$ extra space, where $P$ is the number of gate input pins. With floating point numbers that is $O(L + P)$ time on a word RAM. The code of this page uses exact fractions so that the tests can compare with enumeration, and then the numbers can grow.

The exact probabilities cost much more. Enumeration takes $O(2^n (L + P))$ time for $n$ inputs, and the exact signal probability is #P-hard on general circuits. COP gives up exactness for linear time.

## Properties

- **Exact on fanout-free circuits.** This is proved. With fanout, a line whose fanin cone has no line that reaches it along two paths still gets an exact $C$, and the tests check that on random circuits.
- **No error bound.** Under reconvergence the error has no bound and no sign. It can reach almost 1, and a redundant fault can get a positive estimate.
- **Measured error.** On 500 random circuits with 4 to 6 inputs and 6 to 10 gates, drawn by `random.Random(2024)` with the generator of the tests (27 720 faults), the COP detection estimate differed from the exact value on 18 810 faults, was too high on 11 066 and too low on 7 744, with a mean absolute error of 0.036 and a largest error of 0.93. All 6 166 redundant faults got a positive estimate. This is a measurement on small random circuits, not a property of real designs.
- **Probabilities, not costs.** [SCOAP](/scoap/) counts how many lines a deterministic test must set. COP gives probabilities, which fit random-pattern test.
- **Inputs need not be fair.** Any $p_i$ in $[0, 1]$ works, which is what weighted random patterns use.

## Variants and improvements

- **Exact methods.** Parker and McCluskey (1975) keep each probability as a polynomial in the $p_i$ and replace $p_i^k$ by $p_i$. The result is exact, but the polynomials can grow to $2^n$ terms. Exact counting with BDDs or [model counting](/model-counting/) is also exact and can also blow up.
- **Bounds.** The cutting algorithm of Savir, Ditlow and Bardell (1984) cuts fanout branches, gives them the interval $[0, 1]$, and propagates intervals that are guaranteed to contain the exact values.
- **Correlation corrections.** Later methods carry pairwise correlations of the signals that meet at a gate, which removes much of the error at a quadratic cost.
- **Sampling.** Fault simulation of a few thousand random vectors, as in [fault coverage](/fault-coverage/) estimation, measures the detection probabilities directly with a statistical error. STAFAN by Jain and Agrawal (1985) collects such counts from one good-circuit simulation.
- **Test points.** [Test point insertion](/test-point-insertion/) uses COP to find lines with low $C$, $1 - C$ or $O$ and to choose where a control or observation point helps most.

## When to use it

Use COP early, to screen a design for faults that resist random patterns before you commit to [built-in self-test](/built-in-self-test/) or [weighted random patterns](/weighted-random-pattern-testing/), and inside test point insertion, where it must be recomputed after each candidate point. Its estimates rank lines well enough for these uses on many circuits. When you need the real coverage of a given number of vectors, run a [fault simulator](/fault-simulation/) instead.

## Pitfalls

- **Trusting the numbers under reconvergence.** COP can call a redundant fault easy and an easy fault hard. Treat it as a ranking heuristic, and confirm the hardest faults by simulation.
- **The stem rule.** Combining the branches by $1 - \prod (1 - O[b_i])$ is a guess. Two branches can cancel each other, as in $a \oplus a$, or always act together.
- **Fanout branches and stems are different faults.** A fault on one branch is observed only through that branch. Give the branches their own lines, as the page does.
- **Unused lines.** A line that reaches no output has $O = 0$. Do not treat such lines as hard to test; their faults are redundant.
- **Rounding.** With floating point numbers, very small probabilities in deep circuits underflow to 0. Use logarithms or a floor when you rank hard faults.

## Implementations

## History

Parker and McCluskey defined signal probabilities in 1975 and showed how reconvergent fanout breaks the gate formulas. In 1984 Franc Brglez added the observability side and the detection estimate in his paper on the testability analysis of combinational networks, and the method became known as COP. The same year, Savir, Ditlow and Bardell studied random pattern testability and gave the cutting algorithm with guaranteed bounds. COP then became a standard input to random-pattern test tools, to weighted random pattern generation and to test point insertion.

## References

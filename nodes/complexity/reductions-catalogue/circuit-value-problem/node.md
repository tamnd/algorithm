---
tag: 5N85WQ
kind: problem
slug: circuit-value-problem
name: Circuit value problem
aliases:
- Circuit evaluation
area: complexity/reductions-catalogue
level: core
summary: Given a Boolean circuit and its input values, decide whether the output is 1. In P by evaluation, and P-complete under logspace reductions, also for monotone circuits.
prereqs: [boolean-circuit, p, logspace]
see_also: [circuit-sat, nc, circuit-complexity, multitape-turing-machine, cook-levin-theorem, horn-sat, parallel-prefix, max-flow-problem]
sources:
  - paper: doi:10.1145/990518.990519
    title: Richard E. Ladner, The circuit value problem is log space complete for P, SIGACT News 7(1), 1975, pages 18 to 20
    locator: the main theorem
  - paper: doi:10.1145/1008354.1008356
    title: Leslie M. Goldschlager, The monotone and planar circuit value problems are log space complete for P, SIGACT News 9(2), 1977, pages 25 to 29
    locator: the main theorems (monotone circuits, and planar circuits)
  - book: isbn:9780195085914
    title: Raymond Greenlaw, H. James Hoover and Walter L. Ruzzo, Limits to Parallel Computation, P-Completeness Theory, Oxford University Press, 1995
    locator: the chapters on P-completeness and the circuit value problem, and the list of P-complete problems in Part II (circuit value and its variants)
---

The circuit value problem, CVP, gives a [Boolean circuit](/boolean-circuit/) together with the values of its inputs, and asks whether the output is 1. Evaluating the gates one by one solves it in linear time, so it is in [P](/p/). Ladner (1975) proved that it is P-complete under [logspace](/logspace/) reductions: every problem in P reduces to it. Goldschlager (1977) proved the same for monotone circuits and for planar circuits. So CVP plays for P the role that [circuit satisfiability](/circuit-sat/) plays for NP. It is the standard example of a problem that is believed to be *inherently sequential*: a fast parallel algorithm for it, in the class [NC](/nc/), would put all of P in NC.

## In plain words

A circuit is a network of AND, OR and NOT parts with input switches and one output light. Here the switches are already set, and the question is only whether the light is on.

This is easy: compute each part after the parts that feed it. A computer does it in one pass.

The interesting question is whether many processors working together can do it much faster. Every efficient computation can be written as such a circuit, with one layer of parts per step of the computation. If many processors could evaluate any circuit in a very short time, then every efficient computation could be sped up in the same way. Most researchers believe that this is not possible, and the circuit value problem is the standard example of a task that seems to need its steps one after another.

## Definition

**Instance.** A Boolean circuit $C$ with gates of type AND and OR with fan-in 2 and NOT with fan-in 1, listed in an order where each gate comes after its inputs, and a value $x \in \{0, 1\}^n$ for its inputs. Equivalently, the inputs are constant gates.

**Question.** Is $C(x) = 1$?

**Encoding.** Each gate is written as its type and the indices of its inputs, and the input values as bits. A circuit with $s$ gates has length $O(s \log s)$.

**Complexity.** In P: evaluation in the given order takes $O(s)$ time on a [word RAM](/word-ram/), and polynomial time on the [multitape Turing machine](/multitape-turing-machine/). P-complete under logspace (many-one) reductions (Ladner 1975). Since logspace reductions compose and $\mathsf{L} \subseteq \mathsf{NC} \subseteq \mathsf{P}$, CVP is in L if and only if P = L, and in NC if and only if P = NC.

## Variants

- **Monotone CVP.** No NOT gates. It is still P-complete (Goldschlager 1977), by the dual-rail reduction below.
- **Planar CVP.** The circuit is drawn in the plane without crossings. It is still P-complete (Goldschlager 1977), using a planar crossover gadget in place of each crossing of two wires.
- **Formula value.** If every gate has fan-out 1, the circuit is a formula, and evaluating a Boolean formula is much easier: it is in NC1. The sharing of gate outputs is what makes CVP hard to parallelize.
- **Bounded depth.** A circuit of depth $d$ can be evaluated in $O(d)$ parallel steps, one layer at a time, so CVP restricted to polylogarithmic depth is in NC.
- **Circuit satisfiability.** With free inputs and the question "is the output 1 for some input?", the problem becomes [CIRCUIT-SAT](/circuit-sat/), which is NP-complete.

## Examples

**Evaluation.** Take the inputs $x_1, x_2, x_3$ and the gates
$$g_1 = x_1 \lor x_2,\quad g_2 = x_1 \land x_2,\quad g_3 = \lnot g_2,\quad g_4 = g_1 \land g_3,\quad g_5 = g_4 \land x_3,$$
with output $g_5$, at the input $x = (1, 0, 1)$. A script evaluated the gates in order: $g_1 = 1$, $g_2 = 0$, $g_3 = 1$, $g_4 = 1$, $g_5 = 1$. So this is a yes-instance. The circuit computes $(x_1 \oplus x_2) \land x_3$, so at $x = (1, 1, 1)$ it is a no-instance.

**Dual rail.** The reduction to monotone CVP below makes two wires $g^+$ and $g^-$ for each gate, meant to carry $g$ and $\lnot g$, and removes all NOT gates. The script built the monotone circuit for $x = (1, 0, 1)$ and evaluated it: $g_1^+ = 1$, $g_2^+ = 0$, $g_3^+ = 1$, $g_4^+ = 1$, $g_5^+ = 1$, and each $g_i^-$ was the complement of $g_i^+$. So the output wire $g_5^+$ has the value 1, as in the original circuit. On 300 random circuits with random inputs, every wire $g^+$ had the value of $g$ and every wire $g^-$ its complement.

## Known algorithms

- **Sequential evaluation.** Compute the gates in topological order, in $O(s)$ time. If the order is not given, a [depth-first search](/depth-first-search/) finds one in linear time.
- **Parallel evaluation by layers.** With one processor per gate, a circuit of depth $d$ is evaluated in $O(d)$ parallel steps. This is fast only for shallow circuits.
- **Special circuits.** Formulas, and circuits with special structure such as those of [parallel prefix](/parallel-prefix/) computations, can be evaluated in polylogarithmic parallel time.

## Bounds

- **P-completeness.** CVP is not in NC unless P = NC, and not in L unless P = L. Both inclusions are believed to fail, but neither is proved.
- **Sequential time.** The linear-time algorithm is optimal up to constant factors, since every gate must be read.
- **Consequences.** Many other problems are P-complete through reductions from CVP, such as Horn satisfiability ([Horn-SAT](/horn-sat/)), linear programming and maximum flow with values in binary ([max flow](/max-flow-problem/)), and the depth-first search order of a graph; see Greenlaw, Hoover and Ruzzo.

## Reductions

All reductions here are logspace many-one reductions, because polynomial-time reductions would make every nontrivial problem in P complete.

**From every problem in P (Ladner 1975).** Let $L \in \mathsf{P}$ be decided by a single-tape Turing machine $M$ in time $T(n) = p(n)$, where $p$ is a polynomial, and assume $M$ stays in its final state once it halts.

- *Map.* For input $x$ with $\lvert x \rvert = n$, build the circuit $C_x$ that computes the table of the computation: $T + 1$ rows of $T + 1$ cells, where each cell holds a tape symbol and, at the head, the state, in a constant number of bits. Row 0 is the start configuration on $x$, given by constant gates. Each cell of row $t + 1$ is computed from cells $j - 1, j, j + 1$ of row $t$ by a fixed constant-size circuit. The output is an OR over the last row of the bit "this cell holds the accepting state".
- *Cost.* $C_x$ has $O(T^2)$ gates. A logspace machine writes it gate by gate with counters for $t$ and $j$, which take $O(\log T) = O(\log n)$ bits. So the map is computable in logarithmic space.
- *If $x \in L$, then $C_x$ outputs 1.* By induction on $t$, row $t$ of the circuit holds the configuration of $M$ after $t$ steps. $M$ accepts $x$ within $T$ steps and stays in the accepting state, so the last row holds it and the output is 1.
- *If $C_x$ outputs 1, then $x \in L$.* By the same induction, the last row is the configuration of $M$ on $x$ after $T$ steps. The output is 1, so this configuration is accepting, and $x \in L$.

This is the construction of the [Cook-Levin theorem](/cook-levin-theorem/) and of [CIRCUIT-SAT](/circuit-sat/), with the certificate removed. Machines with several tapes are first simulated on one tape, with a quadratic slowdown.

**To monotone CVP (dual rail, Goldschlager 1977).** Let $C$ be a circuit with input $x$.

- *Map.* For each input $x_i$ make two constant gates $x_i^+ = x_i$ and $x_i^- = 1 - x_i$. For each gate $g$ make two gates: if $g = a \land b$, then $g^+ = a^+ \land b^+$ and $g^- = a^- \lor b^-$; if $g = a \lor b$, then $g^+ = a^+ \lor b^+$ and $g^- = a^- \land b^-$; if $g = \lnot a$, then $g^+$ is the wire $a^-$ and $g^-$ is the wire $a^+$. The output is $g_s^+$.
- *Cost.* The new circuit has at most twice as many gates as $C$ plus $2n$ constants, and each new gate depends only on one old gate. So the map is computable in logarithmic space.
- *Invariant.* For every gate $g$, the value of $g^+$ is the value of $g$ in $C$, and the value of $g^-$ is its complement. This holds at the inputs, and it is kept at each gate by De Morgan's laws, for example $\lnot(a \land b) = \lnot a \lor \lnot b$. The NOT gate swaps the two wires.
- *Both directions.* By the invariant, the output $g_s^+$ is 1 if and only if $C(x) = 1$.

## Applications

- **Limits to parallel speedup.** A problem shown P-complete by a reduction from CVP is unlikely to have an NC algorithm. This guides the search for parallel algorithms toward special cases; see [NC](/nc/).
- **Hardness inside P.** Logspace reductions from CVP prove P-completeness of Horn-SAT, linear programming, maximum flow and many simulation problems.
- **Circuit complexity.** CVP links uniform computation with [circuit complexity](/circuit-complexity/): every polynomial-time computation is a polynomial-size circuit, and evaluating such circuits is exactly as hard as all of P.

## References

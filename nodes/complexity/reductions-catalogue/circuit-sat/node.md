---
tag: Z77TSA
kind: problem
slug: circuit-sat
name: Circuit satisfiability
aliases:
- CIRCUIT-SAT
area: complexity/reductions-catalogue
level: core
summary: Decide whether some input makes a Boolean circuit output 1. NP-complete straight from the definition of NP, and the Tseitin transformation reduces it to SAT.
prereqs: [boolean-circuit, np-complete, polynomial-time-verifier]
see_also: [circuit-value-problem, sat, tseitin-transformation, cook-levin-theorem, p-poly, strong-exponential-time-hypothesis, parsimonious-reduction, karp-21-np-complete]
sources:
  - book: isbn:9780521424264
    title: Sanjeev Arora and Boaz Barak, Computational Complexity, A Modern Approach, Cambridge University Press, 2009
    locator: Section 6.1.2 (CKT-SAT and its NP-completeness, by the circuit for a polynomial-time machine)
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition, MIT Press, 2022
    locator: Chapter 34, the circuit-satisfiability problem, its NP-completeness and the reduction to formula satisfiability
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability, A Guide to the Theory of NP-Completeness, W. H. Freeman, 1979
    locator: Chapter 2 (Cook's theorem, by a tableau of the computation) and Appendix A9.1, problem LO1 (Satisfiability)
---

Circuit satisfiability asks whether a [Boolean circuit](/boolean-circuit/) has an input that makes its output 1. It is the most direct [NP-complete](/np-complete/) problem: a polynomial-time verifier, unrolled over its running time, is a circuit of polynomial size whose free inputs are the certificate. So every problem in NP reduces to it with almost no encoding work. The [Tseitin transformation](/tseitin-transformation/) then reduces it to [SAT](/sat/) in linear time, which is one standard way to prove the [Cook-Levin theorem](/cook-levin-theorem/). Its counterpart with a fixed input, the [circuit value problem](/circuit-value-problem/), is P-complete.

## In plain words

A circuit is a network of small logic parts, such as AND, OR and NOT, wired together, with some input switches and one output light. The question is whether some setting of the switches turns the light on.

Checking one setting is easy: follow the wires and compute each part. Finding a setting may need many tries, because the number of settings doubles with each switch.

The problem is central because any checking program can be built as such a circuit. If a program checks proposed answers to some puzzle, wire up its steps as logic parts and leave the proposed answer as the switches. A setting that lights the output is an answer the program accepts.

## Definition

**Instance.** A Boolean circuit $C$ with input gates $x_1, \ldots, x_n$, gates of type AND and OR with fan-in 2 and NOT with fan-in 1, any fan-out, and one output gate. The circuit is a directed acyclic graph, given as a list of gates in an order where each gate comes after its inputs.

**Question.** Is there $x \in \{0, 1\}^n$ with $C(x) = 1$?

**Encoding.** Each gate is written as its type and the indices of its inputs, so a circuit with $s$ gates has length $O(s \log s)$. The certificate is the input $x$. The verifier computes the gates in the given order, in time $O(s)$ on a [word RAM](/word-ram/), and in polynomial time on the [multitape Turing machine](/multitape-turing-machine/). So the problem is in NP.

**Complexity.** NP-complete under Karp (polynomial-time many-one) reductions, and even under logspace reductions. The hardness proof below uses only the definition of NP.

## Variants

- **Formula satisfiability.** A circuit in which every gate has fan-out 1 is a formula; this is [SAT](/sat/) in its general form. Every formula is a circuit, and the Tseitin transformation goes the other way.
- **Monotone circuits.** Without NOT gates the problem is in P: a monotone circuit outputs 1 on some input if and only if it outputs 1 on the all-ones input.
- **Circuit value.** With the input fixed, the question is only to evaluate the circuit; this is the [circuit value problem](/circuit-value-problem/), which is in P and P-complete.
- **Counting.** Counting the satisfying inputs is #P-complete, and the Tseitin transformation preserves the count, since it is a [parsimonious reduction](/parsimonious-reduction/).
- **Restricted classes.** Satisfiability of CNF formulas of bounded width ([k-SAT](/k-sat/)) or of shallow circuit classes such as [AC0](/ac0/) is still NP-complete for $k \ge 3$ and for depth 2.

## Examples

**A small circuit.** Take the inputs $x_1, x_2, x_3$ and the gates
$$g_1 = x_1 \lor x_2,\quad g_2 = x_1 \land x_2,\quad g_3 = \lnot g_2,\quad g_4 = g_1 \land g_3,\quad g_5 = g_4 \land x_3,$$
with output $g_5$. It computes $(x_1 \oplus x_2) \land x_3$. A script evaluated it on all 8 inputs: the satisfying inputs are $(0, 1, 1)$ and $(1, 0, 1)$. At $(1, 0, 1)$ the gate values are $g_1 = 1, g_2 = 0, g_3 = 1, g_4 = 1, g_5 = 1$, and this list of values is what the verifier computes.

**The Tseitin transformation of this circuit.** Give each gate a new variable and write clauses that say "the variable equals the gate's value". For $g = a \land b$ the clauses are $(g \lor \lnot a \lor \lnot b)$, $(\lnot g \lor a)$ and $(\lnot g \lor b)$; for $g = a \lor b$ they are $(\lnot g \lor a \lor b)$, $(g \lor \lnot a)$ and $(g \lor \lnot b)$; for $g = \lnot a$ they are $(g \lor a)$ and $(\lnot g \lor \lnot a)$. Add the unit clause $(g_5)$. The script built the formula, with 8 variables and $4 \cdot 3 + 2 + 1 = 15$ clauses, and checked all 256 assignments.

- **Forward.** The satisfying input $(1, 0, 1)$ with the gate values above satisfies all 15 clauses.
- **Backward.** The formula has exactly 2 satisfying assignments, and their first three bits are the 2 satisfying inputs of the circuit. So here the counts agree, and the script found the same on 300 random circuits.

## Known algorithms

- **Brute force.** Try all $2^n$ inputs, each in $O(s)$ time, for $O(2^n s)$ time.
- **Through SAT solvers.** The Tseitin transformation gives a CNF formula with $n + s$ variables and $O(s)$ clauses, and a [CDCL](/cdcl/) solver handles it; this is how equivalence of two circuits is checked in practice, through a [miter circuit](/miter-circuit/).
- **Restricted classes.** For some circuit classes, algorithms slightly faster than $2^n$ are known, and such algorithms imply lower bounds in [circuit complexity](/circuit-complexity/).

## Bounds

- **NP-completeness.** No polynomial-time algorithm exists unless P = NP.
- **Exponential time.** CNF-SAT is a special case, so under the [strong exponential time hypothesis](/strong-exponential-time-hypothesis/) there is no algorithm with time $O(2^{(1-\varepsilon) n})$ for any constant $\varepsilon > 0$.
- **Size of the reduction.** A verifier that runs in time $T$ on a single-tape machine gives a circuit of size $O(T^2)$. For [multitape machines](/multitape-turing-machine/), simulating them first on one tape costs a quadratic factor; see [multitape simulation](/multitape-simulation-theorem/).

## Reductions

**From every problem in NP (Karp reduction).** Let $L \in \mathsf{NP}$. By the definition of NP with [verifiers](/polynomial-time-verifier/), there are a polynomial $p$ and a single-tape Turing machine $M$ that runs in time $T(n) = p(n)$ such that $x \in L$ if and only if $M(x, y) = 1$ for some certificate $y$ of length $p(\lvert x \rvert)$. We may assume that $M$ stays in its accepting or rejecting state once it reaches it.

- *Map.* For input $x$ with $\lvert x \rvert = n$ and $T = T(n)$, write the computation of $M$ as a table of $T + 1$ rows and $T + 1$ cells per row: row $t$ is the tape after $t$ steps, and each cell holds a tape symbol and, at the head position, the state. Encode each cell with a constant number of bits. The content of cell $j$ in row $t + 1$ is a fixed function of cells $j - 1$, $j$ and $j + 1$ in row $t$, which a constant-size circuit computes. The circuit $C_x$ has the bits of $x$ as constants in row 0, the bits of $y$ as its free inputs, $T \cdot (T + 1)$ copies of the cell circuit, and as output an OR over the last row of the bit "this cell holds the accepting state".
- *Cost.* $C_x$ has $O(T^2)$ gates, and the gates follow a regular pattern, so $C_x$ is written in time polynomial in $n$ (in fact in logarithmic space).
- *If $x \in L$, then $C_x$ is satisfiable.* Take a certificate $y$ with $M(x, y) = 1$ and use it as the input. By induction on $t$, row $t$ of the circuit holds the configuration of $M$ after $t$ steps, so the last row has the accepting state and the output is 1.
- *If $C_x$ is satisfiable, then $x \in L$.* Take any input $y$ with $C_x(y) = 1$. By the same induction, row $T$ is the configuration of $M$ on $(x, y)$ after $T$ steps. The output is 1, so this configuration is accepting, $M(x, y) = 1$, and $x \in L$.

Together with membership, this proves that CIRCUIT-SAT is NP-complete. Arora and Barak (Section 6.1.2) give this proof with circuits; the [Cook-Levin theorem](/cook-levin-theorem/) gives the same argument with clauses.

**To SAT (Tseitin transformation).** Let $C$ have inputs $x_1, \ldots, x_n$ and gates $g_1, \ldots, g_s$ with output $g_s$.

- *Map.* One variable per input and per gate, the clauses for each gate shown under Examples, and the unit clause $(g_s)$.
- *Cost.* At most $3s + 1$ clauses of at most three literals each, in linear time. So the result is even a 3-CNF formula.
- *If $C(x) = 1$, then the formula is satisfiable.* Give each gate variable the value of its gate on input $x$. Each group of clauses holds because the gate variable equals the gate's value, and $(g_s)$ holds because $C(x) = 1$.
- *If the formula is satisfiable, then $C$ is.* Take any satisfying assignment, and let $x$ be its input part. The clauses of a gate force its variable to equal the gate function of its inputs' variables. By induction in the gate order, every gate variable equals the gate's value on $x$, and $(g_s)$ says that $C(x) = 1$.

The gate variables are determined by $x$, so the reduction is parsimonious. See [Tseitin transformation](/tseitin-transformation/). Composing the two reductions proves that SAT, and even 3-SAT, is NP-complete.

## Applications

- **Hardware verification.** Two circuits are equivalent if and only if the circuit that XORs their outputs is unsatisfiable. This is the [miter circuit](/miter-circuit/) method, and it is solved with SAT solvers after the Tseitin transformation.
- **A start for reductions.** CIRCUIT-SAT is the natural first NP-complete problem in courses that start from circuits, and the source of the reduction to SAT and on to [Karp's reduction tree](/karp-21-np-complete/).
- **Circuit lower bounds.** If NP problems had polynomial-size circuits, CIRCUIT-SAT would too; the class of such problems is [P/poly](/p-poly/).

## References

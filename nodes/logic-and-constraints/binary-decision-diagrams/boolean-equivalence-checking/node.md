---
tag: BW9Q92
kind: problem
slug: boolean-equivalence-checking
name: Boolean equivalence checking
aliases:
- combinational equivalence checking
- functional equivalence
- CEC
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Decide whether two boolean functions or circuits compute the same function.
prereqs: [boolean-function, sat]
see_also: [bdd-canonicity, reduced-ordered-bdd, sat, circuit-sat, co-np-complete, polynomial-identity-testing, free-binary-decision-diagram, equivalence-checking]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 1 (equivalence as a test whether two reduced graphs match exactly), Section 2 (Theorem 1, reduced function graphs are canonical) and the appendix (the multiplier lower bound)
  - paper: doi:10.1016/S0020-0190(80)90078-2
    title: Manuel Blum, Ashok K. Chandra and Mark N. Wegman, Equivalence of free Boolean graphs can be decided probabilistically in polynomial time, Information Processing Letters 10(2), 1980, pages 80 to 82
    locator: the whole note (the polynomial of a free graph and the test at a random point)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (a BDD base with one node for each distinct function)
---

Boolean equivalence checking asks whether two descriptions of Boolean functions, such as two circuits or two formulas over the same inputs $x_1, \ldots, x_n$, give the same output for all $2^n$ inputs. For circuits and formulas the problem is [coNP-complete](/co-np-complete/), because two descriptions differ exactly when their XOR is satisfiable. For [reduced ordered BDDs](/reduced-ordered-bdd/) with one variable order in one shared store, it is a single pointer comparison, because the representation is [canonical](/bdd-canonicity/). This page is about combinational functions; for the equivalence of systems with state, such as bisimulation, see [equivalence checking](/equivalence-checking/).

## In plain words

You have two machines that each take the same switches as input and turn on one lamp. You want to know whether the two lamps always agree. You could try every setting of the switches, but with many switches there are far too many settings. To show that the machines differ, one setting where the lamps disagree is enough. To show that they agree, you need an argument that covers all settings at once. A good way is to turn both machines into the same standard drawing. Two machines agree exactly when their standard drawings are the same.

## Definition

**Input.** Two descriptions $F$ and $G$ of Boolean functions $f, g : \{0,1\}^n \to \{0,1\}$ over the same variables $x_1, \ldots, x_n$. The usual descriptions are Boolean circuits, formulas, and binary decision diagrams.

**Output.** *Yes* if $f(a) = g(a)$ for all $a \in \{0,1\}^n$, and *no* otherwise. A useful checker also returns a *counterexample* when the answer is no: an input $a$ with $f(a) \neq g(a)$.

Equivalence is the same as the statement that $f \oplus g$ is the constant $0$, and the same as the statement that $f \leftrightarrow g$ is a tautology. For circuits with $m$ outputs, the two circuits are equivalent when each pair of matching outputs is equivalent.

## Variants

- **By representation.** The inputs can be CNF or DNF formulas, circuits, [ordered BDDs](/ordered-binary-decision-diagram/) with one order, ordered BDDs with two different orders, or [free BDDs](/free-binary-decision-diagram/). The complexity depends strongly on the representation; see Bounds.
- **Equivalence under a care set.** Decide whether $f(a) = g(a)$ for all $a$ with $c(a) = 1$, where $c$ is a care set. This is the equivalence of $c \wedge f$ and $c \wedge g$. It occurs when part of the input space cannot happen; see [don't-care minimization](/dont-care-minimization/).
- **Implication.** Decide whether $f \leq g$, that is $f(a) = 1$ implies $g(a) = 1$. It is the same as the statement that $f \wedge \neg g$ is $0$, and equivalence is implication both ways.
- **Unknown input correspondence.** Decide whether $f$ and $g$ are equivalent after some permutation of the inputs, or some negation of inputs and outputs. This problem is called Boolean matching, and it needs a search over the correspondences on top of the equivalence test.
- **Sequential equivalence.** Circuits with registers are equivalent when they give the same output sequences from their initial states. This needs a search of the reachable states, as in [symbolic reachability](/symbolic-reachability/), and is not a combinational problem.

## Examples

**Equivalent.** $F = x_1 \wedge (x_2 \vee x_3)$ and $G = (x_1 \wedge x_2) \vee (x_1 \wedge x_3)$ are equal by the distributive law. Built in one BDD store with the order $x_1 < x_2 < x_3$, both give the same root node: $(x_1, 0, u)$ with $u = (x_2, (x_3, 0, 1), 1)$.

**Equivalent, with different shapes.** $F = x_1 \oplus x_2$ and $G = (x_1 \vee x_2) \wedge \neg(x_1 \wedge x_2)$. The circuits have different gates, but the BDDs are the same three inner nodes.

**Not equivalent.** $F = x_1 \wedge x_2$ and $G = x_1 \vee x_2$. The miter $F \oplus G$ is $1$ at $a = (1, 0)$, which is a counterexample: $F(a) = 0$ and $G(a) = 1$.

**A miter.** To compare two circuits with one output each, join their inputs and add one XOR gate on the two outputs. The new circuit has output $1$ on an input exactly when the two circuits differ on it. For $m$ outputs, add $m$ XOR gates and one OR gate on them. The circuits are equivalent if and only if the miter is unsatisfiable.

## Known algorithms

| method | answer | cost |
|---|---|---|
| truth tables | exact | $O(2^n)$ evaluations of each description |
| [ROBDDs](/reduced-ordered-bdd/) in one store | exact, with a counterexample from the BDD of $f \oplus g$ | the cost to build the two BDDs, then $O(1)$ |
| [SAT](/sat/) on the miter | exact, with a counterexample from the model | one SAT call on a formula of linear size |
| random simulation | finds differences, cannot prove equivalence | $O(\text{size})$ for each input tried |
| Blum, Chandra and Wegman | for free BDDs, one-sided error | polynomial |

- **Truth tables.** Evaluate both descriptions on all $2^n$ inputs. This is practical only for small $n$, about $30$ at most.
- **ROBDDs.** Build the BDDs of $f$ and $g$ in one shared store with one variable order, gate by gate with [APPLY](/bdd-apply/) or [ITE](/ite-operator/). By the [canonicity theorem](/bdd-canonicity/), $f = g$ if and only if the two root pointers are equal. If they differ, any path to the terminal $1$ in the BDD of $f \oplus g$ is a counterexample. For two BDDs in separate stores with the same order, a parallel walk that compares the two reduced graphs takes $O(|f| + |g|)$ time. All the cost is in building the BDDs, which can be exponential: Bryant (1986) proved that for every order some output bit of an integer multiplier has a BDD of exponential size; see the [multiplier lower bound](/multiplier-bdd-lower-bound/).
- **SAT on the miter.** Convert the miter to CNF with the [Tseitin transformation](/tseitin-transformation/), with $O(\text{size})$ clauses, and run a SAT solver. A model is a counterexample, and *unsatisfiable* proves equivalence.
- **Random simulation.** Evaluate both descriptions on random inputs, many at a time with bit-parallel words. A difference gives a counterexample. If none is found, the descriptions may still differ on a few inputs, so simulation alone never proves equivalence.
- **Combined checkers.** Two circuits from a synthesis flow usually share much of their structure. Practical checkers use structural hashing to merge identical gates, simulation to find candidate pairs of internal signals that seem equal, and SAT or BDDs to prove each candidate, and they merge the proven pairs before the next step.
- **Free BDDs.** Blum, Chandra and Wegman (1980) give each node $v = (x_i, l, h)$ of a free BDD the polynomial $p_v = (1 - x_i) p_l + x_i p_h$ over a finite field, with $p = 0$ and $p = 1$ at the terminals. Since no path tests a variable twice, $p_v$ is multilinear and agrees with $f_v$ on $\{0,1\}^n$. Two Boolean functions are equal exactly when their multilinear polynomials are equal, so the test evaluates both polynomials at one random point. By the [Schwartz-Zippel lemma](/schwartz-zippel-lemma/), a field with at least $2n$ elements gives error at most $1/2$ when the functions differ, and no error when they are equal. See [polynomial identity testing](/polynomial-identity-testing/).

## Bounds

- **Formulas and circuits: coNP-complete.** The problem is in coNP, because a counterexample is a short certificate for *no* that can be checked in polynomial time. It is coNP-hard, because a CNF formula $\varphi$ is unsatisfiable if and only if $\varphi$ is equivalent to the constant $0$. The same holds for DNF formulas, since a DNF $\psi$ is a tautology if and only if $\psi$ is equivalent to $1$. So a polynomial-time algorithm for equivalence of formulas exists if and only if P = NP.
- **ROBDDs with one order: linear time.** Reduced ordered BDDs are canonical (Bryant 1986, Theorem 1), so equal functions have isomorphic graphs. In a shared store with a unique table the test is $O(1)$, and for separate stores it is $O(|f| + |g|)$.
- **Ordered BDDs that are not reduced.** Reduce both in linear time with the [reduction rules](/bdd-reduction-rules/), then compare.
- **Ordered BDDs with different orders.** Rebuilding one diagram in the order of the other can make it exponentially larger, so the canonical test does not apply directly.
- **Free BDDs: randomized polynomial time.** The test of Blum, Chandra and Wegman puts the problem in coRP. No deterministic polynomial-time algorithm is known.
- **General branching programs.** A CNF formula has a branching program of linear size, so equivalence of branching programs is coNP-complete.

## Reductions

- **To SAT.** $F$ and $G$ are not equivalent if and only if the miter $F \oplus G$ is satisfiable. With the Tseitin transformation the miter becomes a CNF of linear size, so non-equivalence reduces to [SAT](/sat/) and to [circuit SAT](/circuit-sat/).
- **From SAT.** A CNF $\varphi$ is satisfiable if and only if it is not equivalent to the constant $0$, so the complement of SAT reduces to equivalence.
- **To tautology.** $F$ and $G$ are equivalent if and only if $F \leftrightarrow G$ is a tautology.
- **To one node.** In a BDD store, satisfiability of $f$ is the test $f \neq 0$, and tautology is the test $f = 1$. Both are special cases of the pointer comparison.

## Applications

- **Logic synthesis and chip design.** After a tool optimizes a circuit or maps it to a cell library, a combinational equivalence check confirms that the new netlist computes the same functions as the old one.
- **Fixpoint tests in model checking.** In [symbolic reachability](/symbolic-reachability/) the loop stops when the set of reached states does not change. With BDDs this test is one pointer comparison per step.
- **Specification against implementation.** A designer compares a circuit with a reference model, such as a formula or a simpler circuit, and a counterexample shows an input that exposes the bug.
- **Program verification.** Equivalence of two loop-free code fragments over bit vectors reduces to equivalence of the circuits that compute their outputs.

## References

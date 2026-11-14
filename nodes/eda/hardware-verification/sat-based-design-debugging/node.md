---
tag: 1D5R8Y
kind: algorithm
slug: sat-based-design-debugging
name: SAT-based design debugging
aliases:
- Smith-Veneris debugging
- SAT-based error localization
area: eda/hardware-verification
level: research
summary: Smith, Veneris and coauthors' method that adds a multiplexer at each suspect gate and asks a SAT solver which few gates can be changed to fix all failing traces.
model: word-ram
complexity:
  vars: {G: the number of suspect gates, k: the size of the corrections found, V: the number of variables and literals of the debug instance}
  time: {worst: "O(G^k 2^V V)"}
  space: {extra: O(V)}
properties: {deterministic: true, exact: true, complete: true, recursive: false}
history:
  year: 2005
  people: [Alexander Smith, Andreas Veneris, Moayad Fahim Ali, Anastasios Viglas]
  note: Smith, Veneris, Ali and Viglas wrote design debugging and fault diagnosis as one SAT problem with a multiplexer at each suspect line and a bound on the number of selected lines.
prereqs: [tseitin-transformation, sequential-counter-encoding, dpll]
see_also: [max-sat, minimal-correction-subset, minimal-unsatisfiable-subset, sat-based-atpg, effect-cause-diagnosis, time-frame-expansion, miter-circuit, incremental-sat]
sources:
  - paper: doi:10.1109/TCAD.2005.852031
    title: A. Smith, A. Veneris, M. F. Ali and A. Viglas, Fault diagnosis and logic debugging using Boolean satisfiability, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 24(10), 1606 to 1621, 2005
    locator: the copies of the circuit per test vector, the multiplexer with a select line and a free value at each suspect, the bound on the number of active selects, and the enumeration of all solutions with blocking clauses
  - paper: doi:10.1109/ICCAD.2004.1382572
    title: M. F. Ali, A. Veneris, A. Smith, S. Safarpour, R. Drechsler and M. Abadir, Debugging sequential circuits using Boolean satisfiability, IEEE/ACM International Conference on Computer-Aided Design (ICCAD 2004), 204 to 209, 2004
    locator: the extension to sequential circuits by unrolling the circuit over the clock cycles of each failing trace, with one select per suspect shared by all cycles
  - paper: doi:10.1109/TCAD.2010.2061270
    title: Y. Chen, S. Safarpour, J. Marques-Silva and A. Veneris, Automated design debugging with maximum satisfiability, IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems 29(11), 1804 to 1817, 2010
    locator: debugging as maximum satisfiability, in which the correction sets are the minimal correction subsets of soft constraints on the suspects
---

SAT-based design debugging finds where a circuit that fails a set of tests can be changed so that it passes them. Smith, Veneris, Ali and Viglas (2005) build one formula. It holds a copy of the circuit for each test, with the inputs fixed to the test vector and the outputs fixed to the expected values. At each suspect gate a multiplexer chooses between the gate's own value and a free value. The select line of the multiplexer is one variable shared by all copies, and a cardinality constraint allows at most $k$ selects to be true. A model of the formula names $k$ gates and gives new values for them in each test that make every test pass. The gates are the places to look for the bug. Blocking each answer and solving again lists all sets of $k$ gates, and raising $k$ from 0 finds the least number of changes that explains the failures. The proof on this page shows that a select set makes the formula satisfiable exactly when those gates have new values that fix all tests.

## In plain words

A circuit gives the wrong answer on some tests. You want to know which gates to look at.

Put a switch at every gate. When a switch is on, the gate's output is cut and replaced by any value you like. When it is off, the gate works as normal. Now ask a SAT solver: with at most one switch on, is there a choice of replacement values that makes every test give the right answer? Each switch is the same in all tests, but the replacement value may differ from test to test.

If the answer is yes, the switch that is on names a gate that can explain all the failures. Forbid that answer and ask again to find the others. If no single gate works, allow two switches, and so on.

## The problem

Given a combinational circuit $C$ with gates in topological order, a set $\Sigma$ of suspect gates, tests $(v_j, y_j)$ for $j = 1, \ldots, T$, each an input vector and the expected outputs, and a bound $k_{\max}$. A set $S \subseteq \Sigma$ has *correction values* if there are values $\omega(g, j) \in \{0, 1\}$ for $g \in S$ such that, for every test $j$, simulating $C$ on $v_j$ with each $g \in S$ forced to $\omega(g, j)$ gives $y_j$. Find the least $k \le k_{\max}$ for which a set of $k$ suspects has correction values, and all such sets of size $k$. When the test inputs are pairwise distinct, $S$ has correction values exactly when the gates of $S$ can be replaced by new logic of the primary inputs that passes all tests. Usually the tests are the failing vectors that verification found, often with some passing vectors added so that the fix does not break them.

## The algorithm

```pseudo id=main
SAT-DEBUG(C, Σ, tests, k_max)
L1  for each test (v_j, y_j) do make a copy C_j of the circuit, with units for the inputs v_j and the expected outputs y_j
L2      for each suspect g in Σ do replace g in C_j by MUX(s_g, w_{g,j}, op_g(fanins in C_j)), with s_g shared and w_{g,j} free
L3      write every other gate of C_j with its Tseitin clauses; F ← the conjunction of all copies
L4  for k ← 0 to k_max do
L5      F_k ← F ∧ (at most k of the selects s_g are true), by a sequential counter
L6      while F_k has a model M do
L7          S ← {g in Σ : s_g is true in M}
L8          report S; add the clause ∨_{g in S} ¬s_g to F_k        ▷ block S and its supersets
L9      if some S was reported then return k and the reported sets
L10 return no set of at most k_max suspects explains the tests
```

The multiplexer of line L2 is four clauses: $s_g \Rightarrow (g_j \Leftrightarrow w_{g,j})$ and $\neg s_g \Rightarrow (g_j \Leftrightarrow o_{g,j})$, where $o_{g,j}$ is the gate's own value in copy $j$. Line L5 uses the [sequential counter](/sequential-counter-encoding/) of Sinz. The code of this page calls a small [DPLL](/dpll/) solver that decides the selects first, false before true.

## Example

The intended circuit has inputs $a, b, c$ and gates $g_1 = a \vee b$, $g_2 = b \wedge c$, $g_3 = g_1 \oplus c$ and $g_4 = g_1 \vee g_2$, with outputs $g_3$ and $g_4$. The implementation has the bug $g_1 = a \wedge b$. It fails on the four vectors with $a \ne b$. Take the two failing tests $abc = 010$ and $011$.

| test | expected $(g_3, g_4)$ | circuit $(g_3, g_4)$ |
|---|---|---|
| $010$ | $(1, 1)$ | $(0, 0)$ |
| $011$ | $(0, 1)$ | $(1, 1)$ |

With all four gates suspect, the instance has 36 variables and 72 clauses. For $k = 0$ the units propagate through both copies, and the outputs contradict the expected values, so line L6 finds no model. For $k = 1$:

- **$g_1$.** With $w_{g_1, 1} = w_{g_1, 2} = 1$, both copies compute the intended values. This is the model that line L6 finds, and line L8 blocks $\{g_1\}$.
- **$g_3$ alone.** It can fix $g_3$ in both tests, but $g_4 = 0$ in the first test stays wrong.
- **$g_4$ alone.** It fixes $g_4$, but $g_3$ stays wrong in both tests.
- **$g_2$ alone.** Setting $g_2 = 1$ in the first test fixes $g_4$, but $g_3 = g_1 \oplus c = 0$ stays wrong.

After the blocking clause the formula is unsatisfiable, so the answer is $k = 1$ and the one set $\{g_1\}$, with the correction value 1 in both tests. If $k = 2$ were asked, the sets $\{g_2, g_3\}$ and $\{g_3, g_4\}$ would also explain the tests, besides the supersets of $\{g_1\}$.

## Correctness

Two facts carry the proof. First, for a fixed select set $S$, a model of the formula is the same thing as a set of correction values for $S$: by induction over the topological order, each variable of copy $j$ equals the value of its signal in the simulation of test $j$ with the gates of $S$ forced to $w_{g,j}$, and the output units say that this simulation passes. Second, correction values are monotone: a set that works stays working when gates are added, by forcing each added gate to the value it has anyway. So at the first $k$ with a model, every model has exactly $k$ selects true, the blocking clause of line L8 removes exactly one set, and each set of size $k$ that works is a model of all the other blocking clauses. The loop therefore lists exactly the sets of size $k$ with correction values. When the test inputs are distinct, these are exactly the sets of $k$ gates that new logic can fix for the tests. The full proof, with the Tseitin clauses and the counter, is in [the proof file](proofs/correctness.md).

The tests compare the result with brute force on 120 random circuits of 4 inputs and 10 gates, each with one gate of the wrong type and up to 3 failing tests. The brute force tries every single gate with every vector of values over the tests. The sets agree, the real error site is in a reported set, and the correction values of each set pass the tests in simulation. On 40 circuits with two wrong gates, the least $k$ and the sets of size $k$ agree with brute force over all pairs. The Tseitin clauses of every gate type and the counter for up to 5 variables are checked against their truth tables.

## Complexity

Let $L$ be the number of gates and pins of $C$. The instance has $V = O(T L + \lvert \Sigma \rvert k)$ variables and literals: one copy of the circuit per test, two extra variables and four clauses per suspect and test, and $O(\lvert \Sigma \rvert k)$ for the counter. Building it is linear in $V$. Each call of the solver at line L6 takes $O(2^V V)$ time in the worst case. The number of calls is at most $k_{\max} + 1$ plus the number of reported sets, which is at most $\binom{G}{k}$ for $G = \lvert \Sigma \rvert$. Space is $O(V)$.

The worst case cannot be avoided in general. Deciding whether a set of at most $k$ suspects has correction values is NP-complete. It is in NP, since $S$ and $\omega$ can be checked by simulation. It is NP-hard by a reduction from circuit satisfiability: put a buffer with constant input 0 in front of each input $x_i$ of a circuit $D$, make the buffers the suspects, and use one test with output 1 and $k$ equal to the number of inputs. Correction values are then exactly a satisfying assignment of $D$. In practice the inputs of each copy are fixed, so unit propagation decides most of the formula once the selects are chosen.

## Properties

- **Deterministic.** The solver decides the variables in a fixed order, so the reported sets come in a fixed order.
- **Exact and complete for the tests.** The reported sets are exactly the minimum-size sets of suspects with correction values. They say nothing about inputs outside the tests.
- **Not a repair.** The result names locations and per-test values, not new gate functions. Finding the new logic is a separate step.

## Variants and improvements

- **Sequential circuits.** Ali, Veneris, Smith, Safarpour, Drechsler and Abadir (2004) unroll the circuit over the cycles of each failing trace, as in [time-frame expansion](/time-frame-expansion/). The select of a gate is shared by all cycles, and the free value is per cycle.
- **Maximum satisfiability.** Chen, Safarpour, Marques-Silva and Veneris (2010) make the hard part the test copies and each $\neg s_g$ a soft clause. A correction set is then a [minimal correction subset](/minimal-correction-subset/), and the least $k$ is the [MaxSAT](/max-sat/) optimum. This drops the counter and allows core-guided solvers.
- **Unsatisfiable cores.** Without multiplexers, the gates whose clauses appear in a [minimal unsatisfiable subset](/minimal-unsatisfiable-subset/) of the test copies are candidates, which is cheaper but coarser.
- **Incremental solving.** The copies do not change with $k$. An [incremental SAT](/incremental-sat/) solver keeps learned clauses and adds the counter and the blocking clauses with assumptions.
- **Fault diagnosis.** With the tests of a failing chip in place of a specification, the same formula locates defects, as in [effect-cause diagnosis](/effect-cause-diagnosis/). Smith and coauthors treat both uses.

## When to use it

Use it after verification has found failing traces and the design has a reference: a golden model, a specification, or the expected values of a regression. It is the step between the [miter](/miter-circuit/) or simulation that says "wrong" and the engineer who has to change the RTL. It fits when the bug is in few places. Many simultaneous errors need large $k$, and the number of candidate sets grows like $\binom{G}{k}$. For a first ranking, cheaper path-tracing or simulation-based methods find a superset of the candidates quickly, and the SAT step then prunes them.

## Pitfalls

- **Too few tests.** With one failing test, many gates can explain it, often every gate on the paths to the wrong outputs. Add more failing vectors, and passing vectors to keep the fix from breaking working behavior.
- **Equal inputs, different outputs.** The free values are per test, so two tests with the same input vector and conflicting expected outputs still give a model. No circuit passes such tests. Remove duplicates before encoding.
- **Equivalent locations.** A gate and a buffer chain or a gate with one fanout in front of it give the same corrections. The reported sets are candidates, not one true site.
- **Per-test values may not be a gate.** The new values may not be a function of the gate's own fanins, so a reported set does not mean that a change of gate type fixes the bug.
- **A fix for the tests only.** The reported sets pass the given tests. Check the repaired design against the full specification, for example with an equivalence check.

## Implementations

## History

Smith, Veneris, Ali and Viglas presented the SAT formulation of logic debugging and fault diagnosis with correction multiplexers and published the journal version in 2005. Ali and coauthors extended it to sequential circuits at ICCAD 2004. Safarpour, Chen, Marques-Silva and Veneris then recast it as maximum satisfiability, with the journal paper in 2010. Later work added abstraction and refinement, hierarchical debugging, and unsatisfiable cores to handle large designs.

## References

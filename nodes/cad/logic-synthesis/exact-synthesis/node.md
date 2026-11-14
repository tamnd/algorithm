---
tag: EFS5EC
kind: problem
slug: exact-synthesis
name: Exact synthesis
aliases:
- SAT-based exact synthesis
- optimum circuit synthesis
area: cad/logic-synthesis
level: research
summary: Find a circuit with the fewest gates or least depth for a small Boolean function, today by encoding the circuit structure as a SAT problem.
prereqs: [boolean-circuit, circuit-complexity, sat]
see_also: [aig-rewriting, majority-inverter-graph, multi-level-logic-synthesis, boolean-matching, cegis, superoptimization, symmetry-breaking, syntax-guided-synthesis]
sources:
  - paper: doi:10.1007/978-3-642-02777-2_5
    title: Arist Kojevnikov, Alexander S. Kulikov and Grigory Yaroslavtsev, Finding efficient circuits using SAT-solvers, Theory and Applications of Satisfiability Testing (SAT 2009), LNCS 5584, 32 to 44, 2009
    locator: the SAT encoding of "f has a circuit of r gates" with selection, gate function and simulation variables
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.1.2, Boolean Evaluation (Boolean chains, the cost of small functions found by exhaustive search, and the exercises on SAT encodings)
  - paper: doi:10.4230/LIPIcs.CCC.2020.22
    title: Rahul Ilango, Bruno Loff and Igor C. Oliveira, NP-hardness of circuit minimization for multi-output functions, Computational Complexity Conference (CCC 2020), LIPIcs 169, 22:1 to 22:36, 2020
    locator: the NP-hardness of the minimum circuit size problem for functions with many outputs given by truth tables
  - paper: "Valentine Kabanets and Jin-Yi Cai, Circuit minimization problem, Proceedings of the 32nd ACM Symposium on Theory of Computing (STOC), 2000, pages 73 to 79"
    title: Circuit minimization problem
    locator: the minimum circuit size problem for a function given by its truth table, and why its NP-hardness is hard to prove (general locator)
  - paper: "Claude E. Shannon, The synthesis of two-terminal switching circuits, Bell System Technical Journal 28(1), 1949, pages 59 to 98"
    title: The synthesis of two-terminal switching circuits
    locator: the counting argument that most functions of n variables need large circuits
  - paper: "O. B. Lupanov, A method of circuit synthesis, Izvestiya VUZ Radiofizika 1 (1958)"
    title: A method of circuit synthesis
    locator: the upper bound of about 2^n / n gates for every function of n variables (general locator)
---

Exact synthesis asks for a [Boolean circuit](/boolean-circuit/) with the fewest gates, or the least depth, that computes a given Boolean function over a given set of gate types. The function is small, often 4 to 8 inputs, and is given by its truth table. Unlike the heuristics of [multi-level logic synthesis](/multi-level-logic-synthesis/), an exact method must prove that no smaller circuit exists. The decision version, "is there a circuit with at most $r$ gates", is in NP for a truth table input, and since 2009 the usual method encodes it as a [SAT](/sat/) instance and asks a solver for $r = 1, 2, 3, \dots$. The cost grows very fast with $r$, so exact synthesis is used for small cuts of large circuits, for libraries of optimal subcircuits, and for questions in [circuit complexity](/circuit-complexity/).

## In plain words

You have a small logic function, for example "the output is 1 when at least two of the three inputs are 1". You also have a set of allowed gates, for example all gates with two inputs. You want a circuit that uses as few gates as possible, and you want to be sure that nothing smaller exists. Trying all circuits by hand is slow, because their number grows very fast with the number of gates. The modern way is to write the question "is there a circuit with exactly this many gates" as a large logic puzzle and give it to a SAT solver. If the solver says no for 3 gates and finds a circuit for 4, then 4 is the optimum.

## Definition

**Input.** A function $f : \{0,1\}^n \to \{0,1\}^m$ given by its truth table, a basis $\mathcal{B}$ of gate types, and a cost, the number of gates or the depth.

**Feasible solutions.** A circuit over $\mathcal{B}$: a sequence of gates $g_{n+1}, \dots, g_{n+r}$, where $g_1, \dots, g_n$ are the inputs, each gate applies a function of $\mathcal{B}$ to earlier signals, and $m$ chosen signals (with their complements, if the basis allows free inverters) compute $f$ on all $2^n$ inputs. Knuth calls such a sequence a Boolean chain.

**Objective.** Minimize $r$, the gate count $C_{\mathcal{B}}(f)$, or the depth $D_{\mathcal{B}}(f)$, the largest number of gates on a path from an input to an output.

**Decision version.** Given the truth table of $f$ and $r$, does $f$ have a circuit over $\mathcal{B}$ with at most $r$ gates? For $\mathcal{B} = B_2$, all 16 functions of two inputs, this is the minimum circuit size problem (MCSP) of complexity theory.

## Variants

- **By the basis.** $B_2$, all two-input gates. $U_2$, the two-input gates without XOR and XNOR. AND with free inverters, the base of an [and-inverter graph](/and-inverter-graph/). Majority of three with free inverters, the base of a [majority-inverter graph](/majority-inverter-graph/). All functions of $k$ inputs, for [LUT mapping](/lut-mapping/).
- **By the cost.** Fewest gates; least depth; fewest gates under a depth bound; or the number of AND gates only (the multiplicative complexity), which matters for cryptography.
- **Multiple outputs.** One circuit that computes $m$ functions, where shared gates count once.
- **Don't-cares.** The function is fixed only on a care set. This is the form that appears when a cut of a larger circuit is rewritten.
- **Fixed topology.** The shape of the circuit is given, and only the gate functions and fanins are unknown. Topology enumeration solves the problem by many such smaller instances.
- **Formulas.** Each gate may feed only one other gate, so the circuit is a tree.

## Examples

All examples use the basis $B_2$ with 3 inputs $x, y, z$. The minima below were checked by an exhaustive search over all circuits of each size.

- **Three-input XOR.** $x \oplus y \oplus z$ needs 2 gates, since one gate sees at most two inputs.
- **Majority.** $\mathrm{MAJ}(x, y, z)$ needs exactly 4 gates. No circuit of 3 gates computes it. A circuit of 4 gates is $t_1 = x \oplus y$, $t_2 = y \oplus z$, $t_3 = t_1 \wedge t_2$, and the output $t_3 \oplus y$. When $x = z \ne y$, both XORs are 1 and the output is $\bar{y} = x$. In every other case, $t_3 = 0$ and the output is $y$, which is then the majority.
- **Full adder.** The two outputs sum $= x \oplus y \oplus z$ and carry $= \mathrm{MAJ}(x, y, z)$ need 5 gates together, and 4 do not suffice. A circuit of 5 gates is $t_1 = x \oplus y$, sum $= t_1 \oplus z$, $a = x \wedge y$, $b = z \wedge t_1$ and carry $= a \vee b$. The sharing of $t_1$ saves one gate against 2 plus 4 gates for the two outputs on their own. This circuit is the cell of a [ripple carry adder](/ripple-carry-adder/).

## Known algorithms

- **Exhaustive enumeration.** List all circuits of $1, 2, 3, \dots$ gates and keep the first one that computes $f$, or, for all functions of $n$ inputs at once, grow the set of functions with known cost one gate at a time. Knuth (TAOCP 7.1.2) computes the cost of every function of 4 inputs this way, with the functions grouped into classes under permutation and complementation of inputs, the classes of [Boolean matching](/boolean-matching/).
- **SAT encoding.** Kojevnikov, Kulikov and Yaroslavtsev (2009). For a fixed $r$, there are variables for the two fanins of each gate, for the truth table of each gate's function, and for the value of each gate on each of the $2^n$ input rows. Clauses tie the value of a gate on a row to its fanins and its function, and fix the outputs to $f$. The instance is satisfiable exactly when a circuit with $r$ gates exists. A solver such as [CDCL](/cdcl/) is called for $r = 1, 2, \dots$ until the answer is yes.
- **Symmetry breaking.** Many circuits are the same up to the order of the gates. Clauses that force a normal form, for example that each gate is used, that the gates are in a fixed order, or that each gate function maps $(0,0)$ to 0 (the normal chains of Knuth), cut the search without losing an optimum. See [symmetry breaking](/symmetry-breaking/).
- **Counterexample-guided encoding.** Encode only some rows of the truth table, solve, check the circuit on all rows, and add a row where it fails. This is [CEGIS](/cegis/) applied to circuits, and it keeps the SAT instances small.
- **Topology enumeration.** List the possible shapes of a circuit with $r$ gates, and solve a small SAT instance for each shape.

## Bounds

**Upper bounds (proved).**

- For a truth table input, the decision version is in NP: a circuit of at most $r$ gates is a certificate, and it can be checked on all $2^n$ rows in time polynomial in the table size.
- Every function of $n$ inputs has a circuit over $B_2$ with $(1 + o(1))\, 2^n / n$ gates (Lupanov 1958).
- The SAT encoding with $r$ gates of two inputs, with one variable for each gate and each pair of earlier signals, has $O(r (n + r)^2)$ fanin variables, $3r$ or $4r$ function variables and $r \cdot 2^n$ value variables, and $O(r (n + r)^2\, 2^n)$ clauses. Each call of the solver can take time exponential in this size.

**Lower bounds (proved).**

- Most functions are hard: by Shannon's counting argument (1949), the number of circuits with $r$ gates is far less than $2^{2^n}$ when $r$ is a bit less than $2^n / n$, so almost every function of $n$ inputs needs about $2^n / n$ gates. The argument does not name a hard function.
- For functions with many outputs given by truth tables, the minimum circuit size problem is NP-hard (Ilango, Loff and Oliveira 2020).
- For a function with one output, it is not known whether MCSP is NP-hard. Kabanets and Cai (2000) showed that certain natural reductions cannot prove it without proving new circuit lower bounds. So exact synthesis has no proof of NP-hardness in its most common form, and no polynomial-time algorithm either.

**Measured.** The SAT method and its variants find optimum circuits for small functions, and published runs report that the solver time grows very fast with the number of gates $r$. This is an observation from runs on small benchmark functions, not a proved bound. Exact synthesis tools in practice are used on cuts with few inputs for this reason.

## Reductions

- **To SAT.** For each $r$, "is there a circuit of $r$ gates for $f$" reduces to a SAT instance of size $O(r (n + r)^2\, 2^n)$, as above. The optimum is found with at most $C(f)$ such calls, or with $O(\log C(f))$ calls by binary search.
- **To QBF.** When $f$ is given by a specification and not by a table, the question is "there exists a circuit such that for all inputs it agrees with $f$", an $\exists\forall$ formula, that is a [QBF](/qbf/) with two quantifier blocks. CEGIS solves it by a loop of SAT calls.
- **Inside synthesis.** Exact synthesis is the Boolean case of [superoptimization](/superoptimization/) and of [syntax-guided synthesis](/syntax-guided-synthesis/), where the grammar is a set of gate types.
- **From MCSP.** The decision version over $B_2$ with a truth table input and one output is exactly MCSP, so any hardness result for MCSP holds for it.

## Applications

- **Rewriting libraries.** [AIG rewriting](/aig-rewriting/) replaces a small cut of a large circuit by a precomputed optimum circuit for the cut's function. The library is built by exact synthesis, one entry per class of functions of 4 inputs.
- **Resynthesis of cuts.** For cuts with 5 to 8 inputs, exact synthesis is run on the fly, with the don't-cares of the cut, to find a smaller replacement.
- **Majority logic.** Libraries and rewriting for [majority-inverter graphs](/majority-inverter-graph/) use exact MIG synthesis.
- **Cryptography.** Small circuits with few gates or few AND gates for S-boxes, for fast software and for masking against side channels.
- **Circuit complexity.** Exact values of $C(f)$ for small functions test conjectures and give upper bounds that hold for all $n$ when a small circuit is used as a block.

## References

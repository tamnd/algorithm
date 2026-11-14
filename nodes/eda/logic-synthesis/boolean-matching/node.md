---
tag: 5HJMPV
kind: problem
slug: boolean-matching
name: Boolean matching
aliases:
- Boolean match problem
- NPN matching
area: eda/logic-synthesis
level: advanced
summary: Decide whether a library cell implements a given function under a permutation and negation of its inputs, as in technology mapping.
prereqs: [boolean-function, boolean-equivalence-checking]
see_also: [technology-mapping, aig-rewriting, canonical-labeling, graph-isomorphism-problem, polynomial-hierarchy, co-np-complete, exact-synthesis, tree-covering-technology-mapping]
sources:
  - paper: doi:10.1109/43.277607
    title: "Frederic Mailhot and Giovanni De Micheli, Algorithms for technology mapping based on binary decision diagrams and on Boolean operations, IEEE Transactions on Computer-Aided Design 12(5), 1993"
    locator: pages 599 to 620; Boolean matching of cluster functions against library cells in technology mapping, with BDDs and don't-cares
  - paper: "Manindra Agrawal and Thomas Thierauf, The formula isomorphism problem, SIAM Journal on Computing 30(3), 2000"
    title: The formula isomorphism problem
    locator: pages 990 to 1009; formula isomorphism is in Sigma_2^p and is not Sigma_2^p-complete unless the polynomial hierarchy collapses (general locator for the exact statements)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: chapter 10, Boolean matching in library binding (general locator, not checked)
---

Boolean matching asks whether two Boolean functions are the same up to a renaming of the inputs, a negation of some inputs and, in the common NPN form, a negation of the output. In [technology mapping](/technology-mapping/), one function is the function of a small part of the circuit and the other is the function of a library cell, and a match means that the cell can replace that part, with the inputs wired in the found order and with inverters where the found negations are. Unlike structural matching, which compares the shape of a pattern with the circuit, Boolean matching compares functions, so it finds a cell however the part is built. The NPN equivalence classes of functions of $n$ inputs number 1, 2, 4, 14, 222 and 616126 for $n = 0$ to $5$, so matching reduces a library and the set of functions that a mapper meets to a small number of classes. For functions given as truth tables of a few inputs the problem is easy in practice. For functions given as formulas or circuits it is co-NP-hard and lies in $\Sigma_2^p$.

## In plain words

A library cell computes a fixed rule of its inputs. A part of a circuit also computes a rule of its inputs. The question is whether the cell can do the part's job if you are free to choose which wire goes to which input of the cell, to put an inverter on some of the wires, and to put an inverter on the cell's output.

If the answer is yes, the cell can replace the part. Many rules look different but become the same after such changes, so a short list of cells can cover many parts.

## Definition

Write $x = (x_1, \ldots, x_n)$, a permutation $\pi$ of $\{1, \ldots, n\}$, a vector $c \in \{0,1\}^n$ and a bit $c_0$. The NPN transform $T = (\pi, c, c_0)$ maps a function $g$ of $n$ inputs to
$$(T g)(x) = c_0 \oplus g\big(x_{\pi(1)} \oplus c_1, \ldots, x_{\pi(n)} \oplus c_n\big).$$

**Input.** Two functions $f$ and $g$ of $n$ inputs, given as truth tables, as [BDDs](/reduced-ordered-bdd/), or as formulas or circuits.

**Feasible solutions.** The transforms $T = (\pi, c, c_0)$ such that $f = T g$. There are $n! \, 2^{n+1}$ transforms.

**Objective.** None: the problem is a decision problem, and a transform with $f = T g$ is the answer when one exists.

**Decision version.** Is there a transform $T$ with $f = T g$? Then $f$ and $g$ are *NPN-equivalent*.

The transforms form a group under composition, so NPN-equivalence is an equivalence relation, and its classes are the NPN classes. The P, NP and PN forms allow only the permutation, the permutation and the input negations, or the permutation and the output negation.

## Variants

- **By the transforms.** P-matching (permutations only), NP-matching, NPN-matching. The number of classes for $n = 0, \ldots, 5$ is:

  | $n$ | P classes | NP classes | NPN classes |
  |---|---|---|---|
  | 0 | 2 | 2 | 1 |
  | 1 | 4 | 3 | 2 |
  | 2 | 12 | 6 | 4 |
  | 3 | 80 | 22 | 14 |
  | 4 | 3984 | 402 | 222 |
  | 5 | 37333248 | 1228158 | 616126 |

  These values were computed for this page by Burnside's lemma over the $n! \, 2^{n+1}$ transforms, and checked against an exhaustive count of the classes for $n \le 4$.
- **Different numbers of inputs.** A function $f$ of $m < n$ inputs matches a cell of $n$ inputs when the cell, with $n - m$ inputs tied to constants or to other inputs, computes $f$ up to a transform.
- **With don't-cares.** $f$ is given with a set of input values where its value does not matter, and $T g$ must agree with $f$ only on the care set. The don't-cares come from the rest of the circuit, as in [observability don't-cares](/observability-dont-care/).
- **Library matching.** Given $f$ and a library, find every cell that matches $f$, or the cheapest one. With a canonical form for each class, this becomes a lookup in a table indexed by the form.
- **Canonical form.** Given $f$, compute a fixed member of its class, for example the smallest truth table in the class, so that two functions are equivalent exactly when their forms are equal. This is a form of [canonical labeling](/canonical-labeling/).
- **Multiple outputs.** Match several functions at once, with one transform of the shared inputs.

## Examples

Truth tables below use the convention of the [AIG pages](/and-inverter-graph/): $x_1$ is the high bit of the row index.

- **AND with a negated input.** $f = a \land \neg b$ and $g = $ AND2. The transform $\pi = $ identity, $c = (0, 1)$, $c_0 = 0$ gives $f = T g$. In a mapping, this is AND2 with an inverter on $b$.
- **OR from NAND.** $f = a \lor b$ and $g = $ NAND2: $a \lor b = \mathrm{NAND}(\neg a, \neg b)$, so $c = (1, 1)$, $c_0 = 0$. They are NP-equivalent.
- **XOR and XNOR.** XOR2 has the table $0110$ and XNOR2 has $1001$. They are equivalent by $c_0 = 1$, and also by $c = (1, 0)$, $c_0 = 0$.
- **Multiplexer.** $f(a, b, c) = a b \lor \neg a c$ and $g(s, x_0, x_1) = \neg s x_0 \lor s x_1$ are P-equivalent, with $s = a$, $x_1 = b$ and $x_0 = c$.
- **A non-example.** AND3 and the majority function MAJ3 do not match. A change of inputs keeps the number of rows where the function is 1, and a negation of the output turns $k$ such rows into $2^n - k$. AND3 has 1 such row, so every function in its class has 1 or 7, and MAJ3 has 4.
- **The two-input classes.** The 16 functions of two inputs fall into 4 NPN classes: the constants, the single variables, the AND-type functions (8 of them, such as AND, OR, NAND and $a \land \neg b$) and the XOR-type functions (XOR and XNOR).

## Known algorithms

- Exhaustive search over the $n! \, 2^{n+1}$ transforms, practical for small $n$.
- Pruning with invariants, values that every transform keeps, such as the number of 1 rows and the numbers of 1 rows of the cofactors of each input, before the search.
- Canonical forms computed for both functions and compared, with precomputed tables of the classes for $n \le 4$, as in [AIG rewriting](/aig-rewriting/).
- BDD-based matching, as in Mailhot and De Micheli (1993).
- SAT or QBF solvers on the formula "there is a transform such that for all inputs the two functions agree".

## Bounds

**Upper bounds (proved).**

- Truth table input of $n$ inputs. Each transform is checked in $O(n 2^n)$ steps, so the exhaustive search takes $O(n! \, 2^{2n+1} n)$ steps. With $N = 2^n$ the size of a table, this is $N^{O(\log \log N)}$, at most quasi-polynomial in the input size.
- Formula or circuit input. The decision version is in $\Sigma_2^p$, the second level of the [polynomial hierarchy](/polynomial-hierarchy/): guess $T$, then check for all $x$ that $f(x) = (T g)(x)$, a co-NP check.
- For formulas under a permutation of the variables, Agrawal and Thierauf (2000) showed that the problem is not $\Sigma_2^p$-complete unless the polynomial hierarchy collapses. See their paper for the exact class.

**Lower bounds (proved, as hardness).**

- Formula or circuit input: the decision version is co-NP-hard, in all of the P, NP and NPN forms. Proof: a formula $F$ of $n$ variables is a tautology exactly when $F \lor y$, with a new variable $y$, is equivalent to the constant 1 of $n + 1$ inputs. A transform of a constant is a constant, so a function matches the constant 1 exactly when it is constant. If $F$ is a tautology, $F \lor y = 1$. If not, $F(a) = 0$ for some $a$, and $F \lor y$ is 0 at $(a, 0)$ and 1 at $(a, 1)$, so it is not constant. The map from $F$ to $F \lor y$ takes polynomial time, and tautology is [co-NP-complete](/co-np-complete/).
- Formula input: [graph isomorphism](/graph-isomorphism-problem/) reduces to P-matching. A graph with edge set $E$ gives the monotone formula $\bigwedge_{uv \in E} (x_u \lor x_v)$. The clauses are the prime implicates of this monotone function, so the function determines $E$, and two such formulas match under a permutation exactly when the graphs are isomorphic.

**Measured.** Nothing on this page. Mappers report the time spent in matching on their benchmark sets.

## Reductions

- **From equivalence checking.** [Boolean equivalence checking](/boolean-equivalence-checking/) is Boolean matching with $T$ fixed to the identity, so every hardness result for equivalence checking of circuits carries over, as the proof above shows.
- **To canonical forms.** A canonical form for NPN classes reduces matching to two form computations and a comparison, and library matching to one form computation and a table lookup.
- **From graph isomorphism.** As above, for formula input.
- **To QBF with two levels.** "There is $T$ such that for all $x$, $f(x) = (T g)(x)$" is a $\exists\forall$ formula once $T$ is encoded in bits, which shows membership in $\Sigma_2^p$.

## Applications

- **Technology mapping into cells.** Cut-based mappers compute the truth table of each cut and look up the cells that match it.
- **AIG rewriting.** Rewriting looks up the best known AIG for the NPN class of each 4-input cut, from a table of the 222 classes.
- **LUT-based structures.** Matching cuts against configurable cells or LUT structures with a fixed internal wiring.
- **Verification with unknown input order.** Checking two blocks for equality when the correspondence of their inputs is not known.
- **Exact synthesis databases.** Tables of the smallest circuits of all functions of up to 4 or 5 inputs are stored per NPN class, as in [exact synthesis](/exact-synthesis/).

## References

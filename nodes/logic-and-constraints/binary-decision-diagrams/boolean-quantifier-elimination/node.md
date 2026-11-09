---
tag: 1MAMN0
kind: problem
slug: boolean-quantifier-elimination
name: Boolean quantifier elimination
aliases:
- existential quantifier elimination
- projection of boolean functions
- Boolean projection
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Remove quantified variables from a boolean formula to obtain an equivalent quantifier-free function.
prereqs: [boolean-function, cofactor, shannon-expansion]
see_also: [bdd-quantification, davis-putnam-elimination, bounded-variable-elimination, qbf, tseitin-transformation, quantifier-elimination, fourier-motzkin-elimination, symbolic-reachability]
sources:
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the quantifiers on BDDs)
  - paper: doi:10.1145/321033.321034
    title: Martin Davis and Hilary Putnam, A computing procedure for quantification theory, Journal of the ACM 7(3), 1960, pages 201 to 215
    locator: the rule for the elimination of atomic formulas (all resolvents on one variable replace the clauses that contain it)
  - paper: doi:10.1016/0890-5401(92)90017-A
    title: J. R. Burch, E. M. Clarke, K. L. McMillan, D. L. Dill and L. J. Hwang, Symbolic model checking, 10^20 states and beyond, Information and Computation 98(2), 1992, pages 142 to 170
    locator: the image of a set of states as an existential quantification of a conjunction of BDDs (the relational product)
  - paper: doi:10.1145/800125.804029
    title: L. J. Stockmeyer and A. R. Meyer, Word problems requiring exponential time, Proceedings of the 5th ACM Symposium on Theory of Computing, 1973, pages 1 to 9
    locator: the completeness results for quantified Boolean formulas (all quantifiers, polynomial space)
---

Boolean quantifier elimination takes a Boolean function $f$ over two sets of variables $X$ and $Y$ and computes a quantifier-free description of $\exists X\, f$ or $\forall X\, f$, a function of $Y$ alone. The semantics is simple: $\exists x\, f = f|_{x=0} \vee f|_{x=1}$ and $\forall x\, f = f|_{x=0} \wedge f|_{x=1}$, so the whole difficulty is the size of the result in the chosen representation. On BDDs the operation is [BDD quantification](/bdd-quantification/), on CNF it is [Davis-Putnam elimination](/davis-putnam-elimination/), and with all variables quantified under alternating quantifiers it decides [QBF](/qbf/), which is PSPACE-complete.

## In plain words

A rule talks about some things you care about and some helper things you do not care about. You want a new rule that talks only about the things you care about, and says "there is some way to set the helpers so that the old rule holds". For one helper this is easy: write the rule once with the helper off and once with it on, and join the two with "or". Each helper doubles the work if you do it this way, and the new rule can be much longer than the old one. The art is to find a short form of the new rule.

## Definition

**Input.** A description $F$ of a Boolean function $f(X, Y)$, where $X = \{x_1, \ldots, x_k\}$ and $Y = \{y_1, \ldots, y_m\}$ are disjoint sets of variables, and a quantifier $\exists$ or $\forall$.

**Output.** A description $G$, with no variable of $X$, of the function $g(Y) = \exists X\, f$ or $g(Y) = \forall X\, f$. Here $(\exists X\, f)(b) = 1$ if $f(a, b) = 1$ for some $a \in \{0,1\}^k$, and $(\forall X\, f)(b) = 1$ if $f(a, b) = 1$ for all $a$.

Seen as sets, $\exists X\, f$ is the projection of the set of models of $f$ onto the $Y$ coordinates, and $\forall X\, f$ is the set of $b$ whose whole fiber $\{0,1\}^k \times \{b\}$ lies inside the set of models. The two are dual: $\forall X\, f = \neg \exists X\, \neg f$. Quantifiers of the same kind commute, so the order of the variables in $X$ does not change the result. It changes only the cost of the steps.

## Variants

- **By representation.** The description can be a [reduced ordered BDD](/reduced-ordered-bdd/), a CNF, a DNF, or a circuit. The result is usually wanted in the same representation, and the cost depends strongly on the pair of representation and quantifier.
- **Relational product.** Compute $\exists X\, (f \wedge g)$ without building $f \wedge g$ first. Model checkers use it for the image of a set of states under a transition relation; on BDDs it is the AND-EXISTS operation of [BDD quantification](/bdd-quantification/).
- **Alternating prefix.** Eliminate $Q_1 x_1\, Q_2 x_2 \cdots Q_k x_k\, f$ with mixed quantifiers, from the innermost one outward. When $Y$ is empty the result is a constant, and the problem is to evaluate a closed [QBF](/qbf/).
- **Other theories.** The same question over linear inequalities on the reals is solved by [Fourier-Motzkin elimination](/fourier-motzkin-elimination/), over the integers with addition and order it is the decision procedure of [Presburger arithmetic](/presburger-arithmetic/), and over real closed fields by [quantifier elimination](/quantifier-elimination/) for the reals. The Boolean case is the finite one, where the expansion over the two values of a variable is always exact.

## Examples

**One variable.** $\exists x\, \big((x \wedge y) \vee (\neg x \wedge z)\big) = y \vee z$, and $\forall x\, \big((x \wedge y) \vee (\neg x \wedge z)\big) = y \wedge z$.

**One resolution step.** In CNF, $\exists x\, \big((x \vee a) \wedge (\neg x \vee b)\big) = (a \vee b)$. Davis-Putnam elimination replaces the clauses that contain $x$ by all their resolvents on $x$.

**Easy cases.** In a DNF, $\exists x$ just deletes the literals $x$ and $\neg x$ from every term, because $\exists$ distributes over $\vee$ and $\exists x$ of a term drops its literal of $x$. In a CNF, $\forall x$ deletes the literals of $x$ from every clause, by the dual argument. Both take linear time and never grow the description. The hard cases are $\exists$ on CNF and $\forall$ on DNF.

**Exponential CNF from a linear CNF.** Let $f$ be the [Tseitin](/tseitin-transformation/) CNF of the parity $x_1 \oplus \cdots \oplus x_n$, built as a chain: $t_1 = x_1$, the four clauses of $t_i \leftrightarrow (t_{i-1} \oplus x_i)$ for $i = 2, \ldots, n$, and the unit clause $(t_n)$. It has $4n - 3$ clauses. Each $x$ has exactly one value of the helpers $t_2, \ldots, t_n$ that satisfies the definitions, so $\exists t_2 \cdots t_n\, f$ is the parity of $x$. Every CNF of the parity of $n$ variables has at least $2^{n-1}$ clauses (see Bounds). So elimination turns $4n - 3$ clauses into at least $2^{n-1}$ clauses, and Davis-Putnam elimination gives exactly $2^{n-1}$:

| $n$ | clauses of $f$ | clauses after elimination |
|---|---|---|
| 3 | 9 | 4 |
| 5 | 17 | 16 |
| 7 | 25 | 64 |
| 10 | 37 | 512 |

On BDDs the same parity has only $2n + 1$ nodes, so this example is hard for CNF but easy for BDDs. The [BDD quantification](/bdd-quantification/) page has the reverse kind of example: functions whose BDD grows from $3L + 1$ nodes to about $\tfrac{3}{2}L^2$ nodes after one quantified variable, and exponentially after several.

## Known algorithms

- **Expansion.** For any representation with restriction and OR, $\exists x\, f = f|_{x=0} \vee f|_{x=1}$. On a circuit this doubles the size for each variable, so $k$ variables can give a factor $2^k$.
- **BDDs.** [BDD quantification](/bdd-quantification/) eliminates a set $X$ in one recursion over the BDD of $f$, with a [computed table](/computed-table/). One variable costs $O(|f|^2)$ and the result has at most $|f|^2$ nodes. The relational product does the AND and the quantification in one pass.
- **CNF, by resolution.** [Davis-Putnam elimination](/davis-putnam-elimination/) removes one variable $x$ by replacing the $p$ clauses with $x$ and the $q$ clauses with $\neg x$ by their $p \cdot q$ resolvents, without the tautologies. SAT preprocessors use [bounded variable elimination](/bounded-variable-elimination/), which removes a variable only when the number of clauses does not grow.
- **CNF, by SAT calls.** Find a model of $f$, keep only its values on $Y$ as a cube, and add the negation of the cube to $f$ as a blocking clause. Repeat until no model is left. Practical versions make each cube larger before they block it, as long as the cube stays inside $\exists X\, f$. The cubes form a DNF of $\exists X\, f$, so the negated cubes form a CNF of $\forall X\, \neg f$.
- **Alternating prefixes.** QBF solvers expand or eliminate the innermost block of quantifiers, or search over the outer variables with clause and cube learning; see [QBF](/qbf/).

## Bounds

- **One variable.** On BDDs, $|\exists x\, f| \leq |f|^2$, and the square can be reached up to a constant factor. In CNF with $p$ clauses on $x$, $q$ clauses on $\neg x$ and $r$ other clauses, the result has at most $r + p \cdot q$ clauses.
- **Many variables: exponential output.** Every CNF of the parity of $n$ variables has at least $2^{n-1}$ clauses. *Proof.* Drop tautological clauses. A clause $C$ of the CNF must be false only on inputs with even parity. If $C$ missed a variable $x_j$, take an input that makes $C$ false and flip $x_j$: $C$ stays false, but the parity changes, so $C$ would be false on an input with odd parity. So every clause has all $n$ variables and is false on exactly one input. The $2^{n-1}$ inputs with even parity each need their own clause. $\square$ With the Tseitin example above, no algorithm can output a CNF of polynomial size for $\exists X\, f$ in general.
- **Decision problems.** Deciding whether $\exists X\, f$ is satisfiable is plain [SAT](/sat/). Deciding whether $\exists X\, f$ is a tautology, for $f$ in CNF, asks whether $\forall Y\, \exists X\, f$ holds, which is complete for the second level $\Pi_2^p$ of the [polynomial hierarchy](/polynomial-hierarchy/) (Stockmeyer and Wrathall, 1976). With an unbounded number of alternations the problem is QBF, which is complete for [PSPACE](/pspace/) (Stockmeyer and Meyer, 1973).

## Reductions

- **SAT is total elimination.** $f$ is satisfiable if and only if $\exists X\, f = 1$ with $X$ all the variables. Davis-Putnam elimination of all variables is a complete SAT procedure, and its cost on the parity example shows why modern solvers do not eliminate every variable.
- **QBF is alternating elimination.** A closed QBF is true if and only if eliminating its quantifiers from the inside out gives the constant $1$.
- **Image computation.** In [symbolic reachability](/symbolic-reachability/), the successors of a set $S(x)$ under a transition relation $T(x, x')$ are $\exists x\, (S(x) \wedge T(x, x'))$, an existential elimination after a conjunction.
- **Equivalence and implication.** $\forall X\, (f \leftrightarrow g)$ is the set of values of $Y$ for which $f$ and $g$ agree on all $X$. With $Y$ empty it is [Boolean equivalence checking](/boolean-equivalence-checking/).

## Applications

- **Symbolic model checking.** Image and pre-image computations are relational products, and the fixpoints of temporal logic use both quantifiers; see [symbolic model checking](/symbolic-model-checking/).
- **SAT preprocessing.** Bounded variable elimination removes many helper variables, for example the Tseitin variables of gates with few uses, before the search starts.
- **Projection of models.** Hiding internal signals of a circuit, or the helper variables of an encoding, gives the relation between the inputs and outputs that are of interest. Projected model counting counts the models of $\exists X\, f$; see [model counting](/model-counting/).
- **Synthesis.** Controller synthesis and games over finite state spaces compute fixpoints with alternating $\forall$ and $\exists$ over the moves of the two players.

## References

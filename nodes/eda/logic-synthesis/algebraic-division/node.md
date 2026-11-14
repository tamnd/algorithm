---
tag: NKSP1R
kind: algorithm
slug: algebraic-division
name: Algebraic division
aliases:
- weak division
area: eda/logic-synthesis
level: core
summary: Divides one sum of products by another, treating both as polynomials over literals, to get the unique largest quotient and a remainder in time polynomial in the number of cubes.
model: word-ram
complexity:
  vars: {m: the number of cubes of F, k: the number of cubes of D, n: the number of variables}
  time: {worst: O(k m n)}
  space: {extra: O(m n)}
properties: {deterministic: true, exact: true, online: false, recursive: false}
history:
  year: 1982
  people: [Robert K. Brayton, Curtis T. McMullen]
  note: Brayton and McMullen defined algebraic division and the weak division algorithm together with kernels, and the MIS system of Brayton, Rudell, Sangiovanni-Vincentelli and Wang made them the core of multi-level logic synthesis.
prereqs: [sum-of-products, polynomial-division]
see_also: [algebraic-kernel, kernel-extraction, multi-level-logic-synthesis, boolean-network, cofactor, dont-care-condition, hash-table, observability-dont-care]
sources:
  - paper: "Robert K. Brayton and Curtis T. McMullen, The decomposition and factorization of Boolean expressions, Proceedings of the International Symposium on Circuits and Systems (ISCAS), 1982, pages 49 to 54"
    locator: the algebraic product, the quotient and remainder of algebraic division, and the weak division algorithm
  - paper: doi:10.1109/TCAD.1987.1270347
    title: Robert K. Brayton, Richard Rudell, Alberto Sangiovanni-Vincentelli and Albert R. Wang, MIS, a multiple-level logic optimization system, IEEE Transactions on Computer-Aided Design 6(6), 1987, pages 1062 to 1081
    locator: the use of weak division in the factoring, substitution and extraction commands of MIS
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 8, Multiple-Level Combinational Logic Optimization, the section on the algebraic model and algebraic division
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: the chapters on multi-level logic synthesis (a general locator)
---

Algebraic division, also called weak division, divides a [sum of products](/sum-of-products/) $F$ by another sum of products $D$ and returns a quotient $Q$ and a remainder $R$ with $F = Q D + R$. It treats the two expressions as polynomials whose variables are the literals, as in [polynomial division](/polynomial-division/), and does not use Boolean rules such as $x x = x$ or $x + \bar{x} = 1$. The quotient is the largest set of cubes $Q$ over variables outside $D$ such that every product of a cube of $Q$ and a cube of $D$ is a cube of $F$, and it is unique. The algorithm takes time polynomial in the number of cubes, and it is the inner step of factoring, substitution and [kernel extraction](/kernel-extraction/) in [multi-level logic synthesis](/multi-level-logic-synthesis/).

## In plain words

Write a logic expression as a sum of terms, like a polynomial. To divide it by a smaller expression, ask which terms you can multiply by the divisor and get only terms that are already in the expression. Those terms form the quotient. The terms that are left over form the remainder.

For each term of the divisor, collect what remains of each big term after you strike out that divisor term. A quotient term must appear in every one of these lists, so keep the terms that all lists share.

This division follows only the rules of ordinary algebra. It misses some divisions that need the special rules of logic, but it is fast, its answer is unique, and it is easy to reason about.

## The problem

Cubes are sets of literals with at most one literal of each variable, and an SOP is a set of cubes, as on the [sum of products](/sum-of-products/) page. The support $\mathrm{sup}(G)$ of an SOP $G$ is the set of variables that occur in it. For SOPs $A$ and $B$ with $\mathrm{sup}(A) \cap \mathrm{sup}(B) = \emptyset$, the *algebraic product* is the set of cubes $A B = \{a \cup b : a \in A, b \in B\}$. It has $|A| \cdot |B|$ cubes, since disjoint supports make the map $(a, b) \mapsto a \cup b$ one to one.

**Input.** SOPs $F$ and $D$, with $D \neq \emptyset$.

**Output.** SOPs $Q$ and $R$ such that
$$F = Q D \cup R, \qquad Q D \cap R = \emptyset, \qquad \mathrm{sup}(Q) \cap \mathrm{sup}(D) = \emptyset,$$
and $Q$ is as large as possible: every cube $q$ with $\mathrm{sup}(q) \cap \mathrm{sup}(D) = \emptyset$ and $\{q\} D \subseteq F$ is in $Q$. Then $Q$ is written $F / D$, and $D$ is an *algebraic divisor* of $F$ when $Q \neq \emptyset$. If $R = \emptyset$ as well, $D$ is an algebraic factor of $F$.

The equality $F = Q D \cup R$ is an equality of sets of cubes, so it also holds as an equality of [Boolean functions](/boolean-function/).

## The algorithm

```pseudo id=main
WEAK-DIVIDE(F, D)
L1  for each cube d_i of D:
L2      V_i ← { c \ d_i : c ∈ F and d_i ⊆ c }   ▷ strike d_i out of each cube that contains it
L3      Q ← V_i if i = 1, else Q ∩ V_i          ▷ stop early if Q = ∅
L4  P ← { q ∪ d : q ∈ Q, d ∈ D }                ▷ the algebraic product Q D
L5  R ← F \ P; return (Q, R)
```

Line L2 lists, for one cube $d_i$ of the divisor, every cube $q$ such that $q \cup d_i$ is a cube of $F$ and $q$ has no literal of $d_i$. A cube of the quotient must be in every list, so line L3 intersects them. The intersection also removes every cube with a variable of $D$: such a variable occurs in some $d_i$, and $c \setminus d_i$ never holds a literal of it. Line L4 multiplies back, and line L5 keeps the rest of $F$ as the remainder.

With $F = ac + ad + bc + bd + e$ and $D = a + b$, line L2 gives $V_1 = \{c, d\}$ from the cubes $ac$ and $ad$, and $V_2 = \{c, d\}$ from $bc$ and $bd$. So $Q = c + d$, the product is $ac + ad + bc + bd$, and $R = e$. The expression of 9 literals becomes $(a + b)(c + d) + e$ with 5 literals.

## Example

Divide $F = ac + ad + bc + be$ by $D = a + b$.

| step | divisor cube | cubes of F that contain it | list | Q so far |
|---|---|---|---|---|
| L2, L3 | $a$ | $ac$, $ad$ | $V_1 = \{c, d\}$ | $\{c, d\}$ |
| L2, L3 | $b$ | $bc$, $be$ | $V_2 = \{c, e\}$ | $\{c\}$ |
| L4 | | | $P = \{ac, bc\}$ | $\{c\}$ |
| L5 | | | $R = \{ad, be\}$ | $\{c\}$ |

So $F = (a + b) c + ad + be$. The cube $d$ is in $V_1$ but not in $V_2$, because $F$ has $ad$ but no $bd$, so $d$ cannot be in the quotient.

Algebraic division can miss a divisor that Boolean rules find. $F = a + bc$ equals $(a + b)(a + c)$ as a function, since $(a + b)(a + c) = a + ac + ab + bc$ and the Boolean rule $a + ab = a$ removes two cubes. Weak division of $F$ by $a + b$ gives $V_1 = \{\emptyset\}$ from the cube $a$, which is the constant 1, and $V_2 = \{c\}$ from $bc$, so $Q = \emptyset$ and $R = F$. The product $(a + b)(a + c)$ is not algebraic, because both factors use $a$.

## Correctness

The [full proof](proofs/correctness.md) shows that the cube set $Q$ of line L3 is exactly the set $\mathcal{Q}$ of all cubes $q$ with $\mathrm{sup}(q) \cap \mathrm{sup}(D) = \emptyset$ and $q \cup d \in F$ for every $d \in D$. A cube of $\mathcal{Q}$ is in every $V_i$, since $(q \cup d_i) \setminus d_i = q$. A cube $q$ in every $V_i$ has no variable of $D$, by the argument after the pseudocode, and $q \cup d_i \in F$ for each $i$. So $Q = \mathcal{Q}$, which is the largest set of cubes allowed in a quotient. Any union of allowed cubes is allowed, so this largest set is unique, and with it $R = F \setminus Q D$ is unique too.

## Complexity

Let $F$ have $m$ cubes, $D$ have $k$ cubes, and let there be $n$ variables. Line L2 tests $m$ cubes for containment and removes $d_i$ from those that contain it, $O(m n)$ steps, or $O(m n / w)$ word operations with cubes as bit vectors. It runs $k$ times. The intersections of line L3 take $O(m n)$ expected time each with a [hash table](/hash-table/) of cubes, since each list has at most $m$ cubes. The product of line L4 has $|Q| k \le m$ cubes, because $Q D \subseteq F$ and the map is one to one. So the time is $O(k m n)$ and the extra space is $O(m n)$. This is polynomial in the sizes of $F$ and $D$, in contrast to Boolean division, which needs a two-level minimization.

## Properties

- **Exact for its model.** The quotient is the unique largest algebraic quotient, not an approximation.
- **Division by a cube.** If $D$ is one cube $d$, then $F / d$ is the set of cubes of $F$ that contain $d$, with $d$ removed. This is not the [cofactor](/cofactor/) $F_d$, which also keeps the cubes of $F$ that have no literal of $d$.
- **Units.** $F / 1 = F$ with remainder 0, and $F / F = 1$ with remainder 0.
- **Literal count.** If $Q \neq \emptyset$, then writing $F$ as $Q D + R$ uses $\ell(Q) + \ell(D) + \ell(R)$ literals in place of $\ell(F)$, and the saving is $\ell(Q D) - \ell(Q) - \ell(D)$, where $\ell$ counts literals.
- **Function preserved.** $F = Q D + R$ holds as cube sets, so the rewrite never changes the function and needs no check by simulation.

## Variants and improvements

- **Boolean division.** One adds a new variable $y$ for $D$ and minimizes $F$ with the don't-care set $y \oplus D$, so that rules such as $a + ab = a$ can be used. It finds more divisors, but it costs a two-level minimization, see [don't-care condition](/dont-care-condition/) and [observability don't-care](/observability-dont-care/).
- **Division by kernels.** Kernel extraction divides $F$ only by its [kernels](/algebraic-kernel/) and those of other nodes, since a multi-cube divisor shared by two expressions exists only if they share a kernel.
- **Bit vectors and sorting.** An implementation can store each cube as a bit vector of $2n$ bits and sort the lists, so that the intersections of line L3 are merges of sorted lists.
- **Substitution.** In a [Boolean network](/boolean-network/), each node is divided by each other node, and a node with a nonempty quotient is rewritten to use the other node as an input.

## When to use it

Use weak division inside factoring, substitution and common divisor extraction, where it is called many times on small SOPs and must be fast. Use Boolean division with don't-cares on the few candidates where the algebraic model gives no saving, or in a final pass. Do not use it on expressions where the complement of a variable must be treated as related to the variable, since the algebraic model treats $a$ and $\bar{a}$ as two unrelated letters.

## Pitfalls

- **Shared variables.** The quotient must not use a variable of the divisor. Code that intersects the lists without the support argument, or that multiplies back with Boolean rules, can produce a product that is not algebraic.
- **Redundant cubes in F.** If $F$ has two cubes with one inside the other, such as $a$ and $ab$, the algebraic model keeps both, and the quotient depends on that form. Make $F$ free of single-cube containment first.
- **Division by the constant 0.** The empty divisor has no quotient. Line L1 then has nothing to intersect, and code must reject it.
- **Mixing up quotient and cofactor.** Dividing by a single literal is not the cofactor, as the Properties list shows.

## Implementations

## History

Brayton and McMullen (ISCAS 1982) set up the algebraic model of multi-level logic, with expressions as polynomials over literals, defined the algebraic product and quotient, gave the weak division algorithm, and defined kernels as the divisors to try. The MIS system of Brayton, Rudell, Sangiovanni-Vincentelli and Wang (1987) used weak division in its factoring, substitution and extraction commands, and SIS (Sentovich et al. 1992) kept it. The textbooks of De Micheli (1994) and Hachtel and Somenzi (1996) present it as the basic step of algebraic synthesis.

## References

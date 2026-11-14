---
tag: YJP3VG
kind: definition
slug: implicant
name: Implicant
aliases:
- cube of a Boolean function
area: cad/logic-synthesis
level: intro
summary: A product term that implies a Boolean function, so the function is 1 wherever the term is 1, with don't-care points allowed.
prereqs: [sum-of-products, boolean-function]
see_also: [prime-implicant, dont-care-condition, two-level-logic-minimization, cofactor, quine-mccluskey, espresso, conjunctive-normal-form]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 2, Basic Definitions (implicants, covers and the on-set, off-set and don't-care set)
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization
  - paper: doi:10.1080/00029890.1952.11988183
    title: W. V. Quine, The problem of simplifying truth functions, American Mathematical Monthly 59(8), 521 to 531, 1952
    locator: the implicants and prime implicants of a truth function written in normal form
---

An implicant of a Boolean function $f$ is a product term $c$ such that $f$ is 1 at each input where $c$ is 1. In logic words, the term implies the function: $c \Rightarrow f$. Each term of a [sum of products](/sum-of-products/) of $f$ is an implicant of $f$, and a set of implicants whose union contains all the 1 points of $f$ is an SOP of $f$. When some inputs are [don't-care conditions](/dont-care-condition/), the term may also be 1 on those inputs, but never on an input where $f$ must be 0. The implicants that no larger implicant contains are the [prime implicants](/prime-implicant/), and these are the candidates that [two-level minimization](/two-level-logic-minimization/) chooses from.

## Definition

An incompletely specified function $f$ of $n$ variables is a partition of $\{0,1\}^n$ into three sets: the on-set $F$, where $f = 1$; the off-set $R$, where $f = 0$; and the don't-care set $D$, where the value is free. A completely specified function has $D = \emptyset$.

**Implicant.** A cube $c \subseteq \{0,1\}^n$ is an implicant of $f$ if
$$c \subseteq F \cup D, \quad \text{or, the same,} \quad c \cap R = \emptyset.$$
For a completely specified $f$ this says $c(x) \le f(x)$ for all $x$, that is, $c \Rightarrow f$.

**Cover.** A set $C$ of cubes is a cover of $f$ if each cube of $C$ is an implicant and
$$F \subseteq \bigcup_{c \in C} c \subseteq F \cup D.$$
The second inclusion holds because each cube is an implicant. A cover is a sum of products that agrees with $f$ on $F \cup R$, the care set.

Not every cube over the variables of $f$ is an implicant. A cube is one only if it misses the off-set. Some authors also ask that an implicant meets the on-set, so that a cube inside $D$ alone is not an implicant. Such a cube is never needed in a cover, so the two readings give the same minimum covers.

**Basic facts.**

1. A subcube of an implicant is an implicant. So the implicants form a down-set in the order of containment, and each minterm of $F$ is an implicant.
2. If $R$ is given as a cover $\{r_1, \ldots, r_k\}$, then $c$ is an implicant exactly when $c \cap r_i = \emptyset$ for each $i$. Two cubes are disjoint exactly when some variable has the literal $x$ in one and $\bar{x}$ in the other. This test takes $O(nk)$ time.
3. If $F \cup D$ is given as a cover $G$, then $c$ is an implicant exactly when the [cofactor](/cofactor/) $G_c$ is a tautology. This is the test that [Espresso](/espresso/) uses, with the [unate recursive paradigm](/unate-recursive-paradigm/) for the tautology check.
4. There are $3^n$ cubes, so $f$ has at most $3^n$ implicants. The constant 1 has all $3^n$ cubes as implicants.

The dual notion is the implicate: a clause $d$ (an OR of literals) with $f \Rightarrow d$. The clauses of a [conjunctive normal form](/conjunctive-normal-form/) of $f$ are implicates.

## Examples and non-examples

Take $f = x_1 x_2 + \bar{x}_1 x_3 = \sum m(1, 3, 6, 7)$ over $x_1, x_2, x_3$.

- **Implicants.** $f$ has 7 implicants: the four minterms $001, 011, 110, 111$ and the three cubes $0{-}1 = \bar{x}_1 x_3$, $11{-} = x_1 x_2$ and ${-}11 = x_2 x_3$. The cube $x_2 x_3$ is not a term of the given SOP, but it is an implicant: it is the points $011$ and $111$, and $f$ is 1 at both.
- **Non-example.** The cube $1{-}{-} = x_1$ is not an implicant: it contains $100$, where $f = 0$. The cube ${-}{-}1 = x_3$ is not one either, because it contains $101$.
- **With a don't-care.** Make minterm 5 ($101$) a don't-care. Then $f$ has 11 implicants. The new ones are $101$, $1{-}1$, ${-}01$ and ${-}{-}1 = x_3$. Now $x_3 + x_1 x_2$ is a cover with 2 cubes and 3 literals, against 2 cubes and 4 literals without the don't-care. The cover is 1 at the point 101, which is allowed.
- **Non-example of a cover.** $\{x_2 x_3, x_1 x_2\}$ is a set of implicants, but it is not a cover: it misses minterm 1.
- **Majority.** The majority function $\sum m(3, 5, 6, 7)$ has the implicants $x_1 x_2$, $x_1 x_3$, $x_2 x_3$ and its four minterms, 7 in all. No cube with one literal is an implicant, since $x_i = 1$ alone does not make a majority.

## Related definitions

- **[Sum of products](/sum-of-products/).** A cover is an SOP whose cubes are implicants.
- **[Prime implicant](/prime-implicant/).** An implicant that is not contained in any other implicant. In the example, $x_1 x_2$, $\bar{x}_1 x_3$ and $x_2 x_3$ are the primes.
- **[Don't-care condition](/dont-care-condition/).** The points of $D$, which make more cubes implicants.
- **[Cofactor](/cofactor/).** The test of fact 3 uses the cofactor of a cover by a cube.
- **[Two-level logic minimization](/two-level-logic-minimization/).** The choice of a cheapest cover from the implicants.
- **[Quine-McCluskey](/quine-mccluskey/).** Finds all prime implicants by merging pairs of implicants that differ in one variable.

## References

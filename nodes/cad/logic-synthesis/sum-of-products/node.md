---
tag: M58QRA
kind: definition
slug: sum-of-products
name: Sum of products
aliases:
- SOP form
- two-level AND-OR form
area: cad/logic-synthesis
level: intro
summary: A Boolean formula that is an OR of product terms, each an AND of literals, the form of two-level logic and of programmable logic arrays.
prereqs: [boolean-function]
see_also: [implicant, prime-implicant, two-level-logic-minimization, conjunctive-normal-form, shannon-expansion, karnaugh-map, boolean-network, circuit-complexity]
sources:
  - book: isbn:9780898381641
    title: Robert K. Brayton, Gary D. Hachtel, Curtis T. McMullen and Alberto L. Sangiovanni-Vincentelli, Logic Minimization Algorithms for VLSI Synthesis, Kluwer, 1984
    locator: Chapter 2, Basic Definitions, Section 2.3, Cubes and Covers
  - book: isbn:9780070163331
    title: Giovanni De Micheli, Synthesis and Optimization of Digital Circuits, McGraw-Hill, 1994
    locator: Chapter 7, Two-Level Combinational Logic Optimization
  - book: isbn:9780792397465
    title: Gary D. Hachtel and Fabio Somenzi, Logic Synthesis and Verification Algorithms, Kluwer, 1996
    locator: Chapter 4, Synthesis of Two-Level Circuits
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms, Part 1, Addison-Wesley, 2011
    locator: Section 7.1.1, Boolean basics (disjunctive normal forms)
---

A sum of products (SOP) is a Boolean formula that is an OR of product terms, where each product term is an AND of literals. A literal is a variable $x_i$ or its complement $\bar{x}_i$. An example is $x_1 x_2 + \bar{x}_1 x_3$. Each product term is true on a subcube of $\{0,1\}^n$, so an SOP is also a set of cubes, called a cover. Every [Boolean function](/boolean-function/) has an SOP: take one term for each input where the function is 1. In logic the same form is the disjunctive normal form (DNF). In hardware it is two-level logic: one AND gate for each term and one OR gate, or one row of a programmable logic array (PLA) for each term. The number of terms and the number of literals are the usual costs, and making them small is [two-level logic minimization](/two-level-logic-minimization/).

## Definition

Let $x_1, \ldots, x_n$ be Boolean variables. A **literal** is $x_i$ or $\bar{x}_i$. In a product, $x_i$ is true when $x_i = 1$ and $\bar{x}_i$ is true when $x_i = 0$.

**Product term, or cube.** A product term is an AND of literals in which no variable occurs twice. The term with no literal is the constant 1. A term $t$ with $k$ literals is true on a set of $2^{n-k}$ points of $\{0,1\}^n$. This set is a subcube of dimension $n - k$, and we use the same word, cube, for the term and for its set of points. A cube has a positional notation: a string $c \in \{0, 1, -\}^n$, where $c_i = 1$ means the literal $x_i$, $c_i = 0$ means $\bar{x}_i$, and $c_i = -$ means that $x_i$ does not occur. So $x_1 \bar{x}_3$ over three variables is $1{-}0$. There are $3^n$ cubes. A **minterm** is a cube with all $n$ literals, that is, one point of $\{0,1\}^n$. We number the minterms by the binary number $x_1 x_2 \cdots x_n$, with $x_1$ as the high bit.

**Sum of products.** A sum of products is a finite set $C = \{c_1, \ldots, c_m\}$ of cubes, read as the formula
$$f_C(x) = \bigvee_{j=1}^{m} c_j(x).$$
The empty set is the constant 0. The set of points where $f_C$ is 1 is the union of the cubes of $C$. If $f_C = f$, then $C$ is an SOP of $f$, or a **cover** of $f$.

**Cost.** The cost of $C$ is the pair (number of cubes $m$, number of literals $\sum_j |c_j|$), where $|c|$ is the number of literals of $c$. Two-level tools compare the number of cubes first and the literals second. The number of cubes is the number of AND gates, or of PLA rows. The number of literals is the number of AND inputs.

**Canonical SOP.** The canonical SOP, or sum of minterms, of $f$ has one minterm for each point $a$ with $f(a) = 1$. It is unique, and it is the only SOP of $f$ that has only minterms. One writes $f = \sum m(\ldots)$ with the list of minterm numbers.

## Examples and non-examples

**Sums of products.**

- $f = x_1 x_2 + \bar{x}_1 x_3$ is the cover $\{11{-},\ 0{-}1\}$. It is 1 on the minterms $\{6, 7\} \cup \{1, 3\}$, so $f = \sum m(1, 3, 6, 7)$. Its cost is 2 cubes and 4 literals.
- The majority of three inputs is $x_1 x_2 + x_1 x_3 + x_2 x_3$, 3 cubes and 6 literals. Its canonical SOP $\sum m(3, 5, 6, 7)$ has 4 cubes and 12 literals.
- One function has many SOPs. The cover $x_1 + \bar{x}_1 x_2$ and the cover $x_1 + x_2$ both give the OR of $x_1$ and $x_2$. The second one has fewer literals because $x_2$ is a larger cube than $\bar{x}_1 x_2$.
- The constant 1 is the cover $\{{-}{-}\cdots{-}\}$ with one cube and no literal. The constant 0 is the empty cover.
- Parity $x_1 \oplus \cdots \oplus x_n$ needs $2^{n-1}$ cubes in every SOP. A cube that misses a variable $x_j$ contains two points that differ only in $x_j$, and parity is 0 at one of them. So every cube of a parity SOP is a minterm, and parity has $2^{n-1}$ minterms. The [Shannon expansion](/shannon-expansion/) page gives the same proof and compares it with the BDD of parity, which has $2n + 1$ nodes.

**Non-examples.**

- $x_1 (x_2 + x_3)$ is an AND of sums, not an SOP. Multiplied out it is the SOP $x_1 x_2 + x_1 x_3$. An AND of sums of literals is the [conjunctive normal form](/conjunctive-normal-form/), the dual form.
- $\overline{x_1 x_2}$ is not an SOP, because the complement covers a product, not a literal. By De Morgan's law it is the SOP $\bar{x}_1 + \bar{x}_2$.
- $x_1 \bar{x}_1 x_2$ is not a product term in the sense above, because $x_1$ occurs twice. It is the constant 0, the empty set of points, and covers write it as no cube at all.
- $x_1 \oplus x_2$ is not an SOP as written. Its SOP is $x_1 \bar{x}_2 + \bar{x}_1 x_2$.

**SOP and CNF sizes.** The two forms can differ by an exponential factor. The SOP $f = x_1 y_1 + x_2 y_2 + \cdots + x_k y_k$ has $k$ cubes. Let $D$ be a clause of a CNF of $f$. Set each variable that is a positive literal of $D$ to 0 and each other variable to 1. Then $D$ is false, so $f$ must be 0, so for each $i$ the clause $D$ has the positive literal $x_i$ or $y_i$. Now pick one variable $z_i$ from each pair, and let $a$ be the point with all $z_i = 0$ and all other variables 1. Then $f(a) = 0$, so some clause is false at $a$. Its positive literals hit every pair and are all 0 at $a$, so they are exactly $z_1, \ldots, z_k$. The $2^k$ choices give $2^k$ different clauses, so every CNF of $f$ has at least $2^k$ clauses. Parity has $2^{n-1}$ clauses in every CNF too, by the same argument as for its SOP.

## Related definitions

- **[Boolean function](/boolean-function/).** The object an SOP describes. A function has one truth table and many SOPs.
- **[Implicant](/implicant/)** and **[prime implicant](/prime-implicant/).** A cube that can be part of an SOP of $f$, and such a cube that no larger cube can replace. Some minimum SOP of each function uses only prime implicants.
- **[Don't-care condition](/dont-care-condition/).** Inputs where the value of $f$ is free. An SOP then has to match $f$ only on the other inputs.
- **[Two-level logic minimization](/two-level-logic-minimization/).** The problem of finding an SOP of least cost. The [Karnaugh map](/karnaugh-map/), [Quine-McCluskey](/quine-mccluskey/) and [Espresso](/espresso/) solve it by hand, exactly and heuristically.
- **[Conjunctive normal form](/conjunctive-normal-form/).** The dual two-level form, an AND of OR clauses. The SOP of $\bar{f}$, with De Morgan's law, gives a CNF of $f$.
- **[Unate function](/unate-function/).** A function with an SOP in which each variable appears in one polarity only.
- **[Boolean network](/boolean-network/).** A circuit of many levels, where each node holds a small SOP. This is the object of [multi-level logic synthesis](/multi-level-logic-synthesis/).
- **[Circuit complexity](/circuit-complexity/).** An SOP is a circuit of depth 2 with unbounded fan-in, and the parity bound above is the base case of the lower bounds for constant-depth circuits.

## References

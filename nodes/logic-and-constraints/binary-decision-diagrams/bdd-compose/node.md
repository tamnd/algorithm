---
tag: SRJKH7
kind: algorithm
slug: bdd-compose
name: BDD functional composition
aliases:
- compose operation
- BDD substitution
- functional composition on BDDs
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Substitutes one function for a variable inside a BDD.
solves: [boolean-function-composition]
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f, g: the number of nodes of the BDD of g}
  time: {worst: O(f^2·g) expected}
  space: {extra: O(f^2·g)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant computed composition as g AND f|x=1 OR NOT g AND f|x=0 with a three-argument Apply, in time quadratic in the size of f and linear in the size of g.
prereqs: [ite-operator, cofactor, reduced-ordered-bdd]
see_also: [boolean-function-composition, ite-operator, bdd-apply, bdd-quantification, generalized-cofactor, cofactor, computed-table, symbolic-reachability]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.4 (Restriction) and Section 4.5 (Composition, the identity with two restrictions, and the bound O(|G1|^2 |G2|) in Table 1)
  - paper: doi:10.1109/DAC.1990.114826
    title: Karl S. Brace, Richard L. Rudell and Randal E. Bryant, Efficient implementation of a BDD package, Proceedings of the 27th ACM/IEEE Design Automation Conference, 1990, pages 40 to 45
    locator: Section 4.2 (ITE as the core operation from which the other operations are built)
---

Functional composition computes the [reduced ordered BDD](/reduced-ordered-bdd/) of $f[x_i := g]$, the function $f$ with the function $g$ put in place of the variable $x_i$. It uses the identity $f[x_i := g] = \mathrm{ite}(g, f|_{x_i=1}, f|_{x_i=0})$: two restrictions of $f$, each in linear time, and one call of the [ITE operator](/ite-operator/). The time is $O(|f|^2 \cdot |g|)$ expected, the bound of Bryant (1986), and the result can be quadratic in $|f|$ even when $g$ is a single variable.

## In plain words

A diagram answers a question about some inputs, and one of those inputs is now the answer to another question. Composition builds the diagram for the whole thing. First make two copies of the diagram: one where that input is fixed to yes, one where it is fixed to no. Each copy is quick to make and is no larger than the original. Then build a switch: ask the other question, and if its answer is yes, follow the first copy, otherwise the second. The switch is the usual three-way operation on diagrams, and it can make the result much larger than the original.

## The problem

**Input:** a store of reduced ordered BDDs with the order $x_1 < \cdots < x_n$, two nodes $f$ and $g$, and an index $i$.

**Output:** the node of $f[x_i := g]$, where $f[x_i := g](a) = f(a[x_i := g(a)])$ and $a[x_i := c]$ is the input $a$ with $x_i$ set to $c$. The function $g$ may depend on any variables, including $x_i$ and variables before or after $x_i$ in the order. For the general problem, with formulas and circuits as inputs, see [Boolean function composition](/boolean-function-composition/).

## The algorithm

```pseudo id=main
COMPOSE(f, i, g)
L1  f0 ← RESTRICT(f, i, 0)
L2  f1 ← RESTRICT(f, i, 1)
L3  return ITE(g, f1, f0)

RESTRICT(u, i, b)        ▷ with a memo table for one top-level call
L4  if the top variable of u comes after x_i then return u
L5  if the memo holds u then return it
L6  if u tests x_i then r ← high(u) if b = 1, else low(u)
L7  else r ← MK(var(u), RESTRICT(low(u), i, b), RESTRICT(high(u), i, b))
L8  store r in the memo, and return r
```

RESTRICT replaces each node that tests $x_i$ by one of its children, and MK rebuilds the nodes above them, so the result stays reduced. A terminal comes after every variable, so line L4 returns it. ITE is the operator of Brace, Rudell and Bryant, with its [computed table](/computed-table/).

## Example

Let $f = x_1 \wedge x_3$ and $g = x_2 \vee x_4$, and compute $f[x_3 := g]$.

- RESTRICT$(f, 3, 0)$ replaces the node of $x_3$ by its low child $0$. The node of $x_1$ becomes MK$(1, 0, 0) = 0$, so $f_0 = 0$.
- RESTRICT$(f, 3, 1)$ replaces it by the high child $1$, and the node of $x_1$ becomes MK$(1, 0, 1) = x_1$, so $f_1 = x_1$.
- ITE$(g, x_1, 0) = g \wedge x_1 = (x_1 \wedge x_2) \vee (x_1 \wedge x_4)$.

The result has the nodes $(x_1, 0, \cdot)$, then $(x_2, \cdot, 1)$, then $(x_4, 0, 1)$, and two terminals: 5 nodes.

**Quadratic growth.** Let $L = 2^k$, and take a variable $x$, two blocks $a$ and $b$ of $k$ address variables, $L$ data variables $d_0, \ldots, d_{L-1}$ and a variable $z$, in this order. Let $c_a = d_{\mathrm{val}(a)}$ and $c_b = d_{\mathrm{val}(b)}$ be the data variables that the addresses select, and $f = \mathrm{ite}(x, c_a, c_b)$, with $3L + 1$ nodes. Composition with $g = z$, a BDD of 3 nodes, moves the test of $x$ to the bottom of the order: $f[x := z] = \mathrm{ite}(z, c_a, c_b)$. Its BDD must remember both addresses until it reads $z$, and it has $2L^2 + 4L - 1$ nodes.

| $L$ | $\lvert f \rvert$ | $\lvert f[x := z] \rvert$ |
|---|---|---|
| 2 | 7 | 15 |
| 4 | 13 | 47 |
| 8 | 25 | 159 |
| 16 | 49 | 575 |
| 32 | 97 | 2175 |

So the size of the result can be $\Theta(|f|^2)$ with $|g| = 3$. The tests check these sizes.

## Correctness

At an input $a$, let $c = g(a)$. Then $f[x_i := g](a) = f(a[x_i := c]) = f|_{x_i=c}(a)$, which is $\mathrm{ite}(g, f|_{x_i=1}, f|_{x_i=0})$ at $a$. RESTRICT computes the cofactors: a node below $x_i$ does not depend on $x_i$, a node that tests $x_i$ is replaced by the child for $b$, and a node above commutes with the cofactor, so MK rebuilds it from the restricted children. ITE is correct and canonical, so the result is the unique node of $f[x_i := g]$. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

**Theorem (Bryant 1986).** COMPOSE takes $O(|f|^2 \cdot |g|)$ expected time, and $|f[x_i := g]| \leq |f|^2 \cdot |g|$.

*Proof.* Each RESTRICT visits each node of $f$ at most once, thanks to its memo, and returns a BDD with at most $|f|$ nodes: the nodes of $f$ below $x_i$ and one new node for each node of $f$ above $x_i$. ITE on three BDDs takes $O(|g| \cdot |f_1| \cdot |f_0|)$ expected time and makes at most that many nodes. $\square$

In Bryant's Table 1 the bound is $O(|G_1|^2 |G_2|)$. The quadratic example above shows that the factor $|f|^2$ cannot drop to $|f|$, even for $|g| = 3$.

## Properties

- **Exact and canonical.** The result is the unique node of $f[x_i := g]$.
- **Special cases.** With $g$ a constant $c$, composition is the restriction $f|_{x_i=c}$. With $g = x_i$ the result is $f$, and with $f = x_i$ it is $g$.
- **Quantification.** $\exists x_i\, f = f[x_i := 0] \vee f[x_i := 1]$, so [quantification](/bdd-quantification/) is the OR of two compositions with constants.
- **Persistent.** The algorithm only adds nodes.

## Variants and improvements

- **One pass.** A recursive version walks $f$ from the root. At a node below $x_i$ it returns the node, at a node that tests $x_i$ it returns ITE$(g, \mathrm{high}, \mathrm{low})$, and at a node above it returns ITE$(x_j, \text{the composed high child}, \text{the composed low child})$ for its variable $x_j$. It needs ITE and not MK above $x_i$, because $g$ may depend on variables before $x_j$. It avoids building the two restrictions.
- **Vector composition.** Substituting $g_1, \ldots, g_k$ for $x_1, \ldots, x_k$ at the same time is not the same as $k$ single substitutions in a row when some $g_j$ depends on a substituted variable. A simultaneous substitution walks $f$ once and replaces each node of $x_j$ by an ITE on $g_j$.
- **Renaming.** If $g = x_j$, and $f$ does not depend on $x_j$ or on any variable between $x_i$ and $x_j$ in the order, the composition relabels the nodes of $x_i$ as $x_j$ in linear time. Model checkers use renaming to move between current-state and next-state variables.
- **Generalized cofactors.** The [generalized cofactor](/generalized-cofactor/) operations generalize restriction from one variable to a care set.

## When to use it

Use composition to build the BDD of a circuit or a formula by substitution: start from the output function and substitute the function of each internal signal, or substitute a new value of a state variable in symbolic simulation. Use RESTRICT alone when $g$ is a constant, since it is linear and never grows the BDD. When many variables are replaced at once, use vector composition, not a chain of single compositions.

## Pitfalls

- **Substituting with MK.** Above $x_i$ the result cannot be built with MK on the composed children when $g$ depends on earlier variables, because the result would not be ordered. The two-restriction method and the one-pass method with ITE both avoid this error.
- **A chain of single substitutions in place of a simultaneous one.** $f[x_1 := g_1][x_2 := g_2]$ substitutes $g_2$ also inside $g_1$ when $g_1$ depends on $x_2$.
- **A memo shared between calls.** The memo of RESTRICT is valid only for one pair $(i, b)$. A memo that is shared between calls must include $i$ and $b$ in its key.
- **Size growth.** The result can be quadratic in $|f|$ even for a single-variable $g$, as in the example, because the test of $x_i$ moves to the position of the variables of $g$ in the order.

## Implementations

## History

Bryant (1986) gave composition as $f_1|_{x_i = f_2} = f_2 \cdot f_1|_{x_i=1} + \neg f_2 \cdot f_1|_{x_i=0}$, computed with restrictions and a three-argument form of Apply, and listed its cost as $O(|G_1|^2 |G_2|)$. Brace, Rudell and Bryant (1990) made ITE the core operation of their package, so composition became two restrictions and one ITE call. Composition is a basic step of symbolic simulation and of building the BDDs of circuits signal by signal.

## References

---
tag: 8DCSXX
kind: algorithm
slug: bdd-quantification
name: BDD quantification
aliases:
- existential quantification on BDDs
- universal quantification on BDDs
- BDD exists
- BDD forall
- smoothing
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Computes exists x. f and forall x. f as f|x=0 OR f|x=1 and AND.
solves: [boolean-quantifier-elimination]
model: word-ram
complexity:
  vars: {f: the number of nodes of the BDD of f, r: the largest number of nodes of a recursive result}
  time: {worst: O(f·r^2) expected}
  space: {extra: O(f·r^2)}
properties: {deterministic: true, exact: true, online: false, recursive: true, in_place: false}
history:
  year: 1986
  people: [Randal E. Bryant]
  note: Bryant's restriction and Apply give the quantifiers through the expansion f|x=0 OR f|x=1, an identity that goes back to Boole.
prereqs: [reduced-ordered-bdd, bdd-apply, cofactor, shannon-expansion]
see_also: [boolean-quantifier-elimination, bdd-apply, computed-table, symbolic-model-checking, symbolic-reachability, qbf, davis-putnam-elimination, bdd-compose]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4.3 (Apply) and Section 4.4 (Restriction), the two steps of quantification by the expansion f|x=0 OR f|x=1
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (the quantifiers on BDDs)
---

BDD quantification computes the [reduced ordered BDD](/reduced-ordered-bdd/) of $\exists X\, f$ or $\forall X\, f$ from the BDD of $f$ and a set $X$ of variables. For one variable it uses $\exists x\, f = f|_{x=0} \vee f|_{x=1}$ and $\forall x\, f = f|_{x=0} \wedge f|_{x=1}$: two linear-time restrictions and one [APPLY](/bdd-apply/), in $O(|f|^2)$ time. For a set $X$, one recursion over the nodes of $f$ replaces every node that tests a variable of $X$ by the OR (or AND) of its two quantified children. The result can be much larger than $f$: one quantified variable can square the size up to a constant factor, and a few can make it exponential.

## In plain words

A diagram answers a yes or no question about some inputs. Quantifying an input means asking a new question without that input: "is there a way to set this input so that the answer is yes?" or "is the answer yes for both ways?". To answer, walk through the diagram. Where a box asks about a removed input, there is no choice to follow, so combine the two sides: "either side says yes" for the first question, "both sides say yes" for the second. Boxes about other inputs stay as they are. A table of solved boxes makes each box cost one visit, but combining two sides can make the diagram much bigger.

## The problem

**Input:** a store of reduced ordered BDDs with the order $x_1 < \cdots < x_n$, a node $f$, a set $X$ of variables, and a quantifier, $\exists$ or $\forall$.

**Output:** the node of $\exists X\, f$ or $\forall X\, f$, where
$$(\exists X\, f)(a) = \bigvee_{b \in \{0,1\}^X} f(a[X := b]), \qquad (\forall X\, f)(a) = \bigwedge_{b \in \{0,1\}^X} f(a[X := b]),$$
and $a[X := b]$ is the input $a$ with the variables of $X$ set to $b$. The result does not depend on the variables of $X$. This is the BDD method for the problem of [Boolean quantifier elimination](/boolean-quantifier-elimination/), which also has methods on formulas and clauses.

## The algorithm

Let op be $\vee$ for $\exists$ and $\wedge$ for $\forall$.

```pseudo id=main
QUANT(op, f, X)
L1  if f is a terminal then return f
L2  if every variable of X comes before the top variable of f then return f
L3  if the computed table holds (op, f, X) then return it
L4  (x_i, l0, h0) ← the top variable and the two children of f
L5  l ← QUANT(op, l0, X)
L6  h ← QUANT(op, h0, X)
L7  if x_i ∈ X then r ← APPLY(op, l, h)
L8  else r ← MK(i, l, h)
L9  store r in the computed table under (op, f, X)
L10 return r
```

Line L2 stops the recursion below the last variable of $X$, where nothing is left to quantify. The key of the [computed table](/computed-table/) must include $X$, or an id of it, and op. For one variable, QUANT does the same work as RESTRICT twice and one APPLY, but in one pass. A common early stop for $\exists$: if $l = 1$ at a node of $X$, the result is $1$ without computing $h$.

## Example

**A multiplexer.** Let $f = (x_1 \wedge x_2) \vee (\neg x_1 \wedge x_3)$, "if $x_1$ then $x_2$ else $x_3$". Its root tests $x_1 \in X = \{x_1\}$, with children $x_3$ and $x_2$. Both are below the last variable of $X$, so line L2 returns them, and line L7 gives $\exists x_1\, f = x_3 \vee x_2$. In the same way $\forall x_1\, f = x_2 \wedge x_3$.

**Squaring the size.** Let $L = 2^k$. Take a variable $x$, two blocks of $k$ address variables $a$ and $b$, and $L$ data variables $d_0, \ldots, d_{L-1}$, in this order. Let $c_a = d_{\mathrm{val}(a)}$ be the data variable that $a$ selects, and $c_b = d_{\mathrm{val}(b)}$, and let
$$f = (x \wedge c_a) \vee (\neg x \wedge c_b), \qquad \exists x\, f = c_a \vee c_b.$$
The BDD of $c_a$ has $L - 1$ address nodes, $L$ data nodes and two terminals, $2L + 1$ in all, and the BDD of $f$ has $3L + 1$ nodes. The BDD of $c_a \vee c_b$ must remember $\mathrm{val}(a)$ while it reads $b$, so it has $L - 1$ nodes for $a$, $L(L - 1)$ for $b$, $L(L-1)/2$ nodes for the functions $d_i \vee d_j$ with $i < j$, $L$ nodes for single data variables, and two terminals:
$$|\exists x\, f| = (L - 1) + L(L - 1) + \frac{L(L - 1)}{2} + L + 2 = \frac{3L^2 + L + 2}{2} \approx \frac{|f|^2}{6}.$$

| $L$ | $\lvert f \rvert$ | $\lvert \exists x\, f \rvert$ |
|---|---|---|
| 2 | 7 | 8 |
| 4 | 13 | 27 |
| 8 | 25 | 101 |
| 16 | 49 | 393 |
| 32 | 97 | 1553 |

So the quadratic bound for one variable is tight up to a constant factor. The tests check these sizes.

**Exponential growth with a few variables.** Let $m = 2^s$, and order $s$ selector variables first, then $x_1, \ldots, x_m$, then $y_1, \ldots, y_m$. Let $f$ say "the selectors spell $i$, and $x_i \wedge y_i$". Its BDD has $3m + 1$ nodes. Quantifying the $s = \log_2 m$ selectors gives $\exists S\, f = x_1 y_1 \vee \cdots \vee x_m y_m$, which in this order has $2^{m+1}$ nodes, as in Bryant's example for [APPLY](/bdd-apply/). For $m = 2, 4, 8$ the sizes go from $7, 13, 25$ to $8, 32, 512$.

## Correctness

Three identities give the proof. If $f$ does not depend on any variable of $X$, then $\exists X\, f = f$ (line L2). If $x_i \in X$, then $\exists X\, f = \exists X'\, f|_{x_i=0} \vee \exists X'\, f|_{x_i=1}$ with $X' = X \setminus \{x_i\}$ (line L7). If $x_i \notin X$, quantification commutes with the cofactor by $x_i$, so the two cofactors of the result are the quantified children (line L8). The children of a node at level $i$ do not depend on $x_i$, so quantifying them over $X$ or $X'$ gives the same function. The induction is on the number of nodes below $f$, and the same proof works for $\forall$ with $\wedge$. The full proof is in [the proof file](proofs/correctness.md).

## Complexity

**One variable.** With $X = \{x_i\}$, line L2 stops at the first node below level $i$, and all APPLY calls at line L7 are on nodes of the BDD of $f$. They share one computed table, so there are at most $|f|^2$ pairs with real work, and the time is $O(|f|^2)$ expected. The result is $f|_{x_i=0} \vee f|_{x_i=1}$, each restriction has at most $|f|$ nodes, and so by the bound of APPLY, $|\exists x_i\, f| \leq |f|^2$. The squaring example shows that a result of size $\Theta(|f|^2)$ is possible.

**A set of variables.** Each node of $f$ does real work once for a given op and $X$. If $r$ bounds the size of the results $l$ and $h$, each APPLY at line L7 takes $O(r^2)$ expected time, so the total is $O(|f| \cdot r^2)$. Since quantifying one variable at most squares the size, $r \leq |f|^{2^{|X|}}$. The result is also a function of the $n - |X|$ other variables, so it has at most $2^{n - |X|} + 1$ nodes. The selector example shows that about $\log_2 |f|$ quantified variables can already give a result of size exponential in $|f|$, so no bound polynomial in $|f|$ holds for general $X$.

| selectors $s$ | address bits $k$ | $\lvert f \rvert$ | $\lvert \exists S\, f \rvert$ |
|---|---|---|---|
| 1 | 2 | 13 | 27 |
| 2 | 2 | 21 | 96 |
| 2 | 3 | 41 | 1091 |
| 3 | 3 | 73 | 6544 |

In this table $s$ selector variables choose one of $2^s$ blocks of $k$ address variables, and each block selects one of the $2^k$ shared data variables, as in the squaring example. All $s$ selectors are quantified.

## Properties

- **Exact and canonical.** The result is the unique node of the quantified function.
- **Duality.** $\forall X\, f = \neg \exists X\, \neg f$. With [complemented edges](/complemented-edges/), one procedure serves both quantifiers.
- **Order of the quantified variables.** Quantifiers of the same kind commute, so $\exists x\, \exists y\, f = \exists y\, \exists x\, f$, and one call can take the whole set $X$. Mixed quantifiers, such as $\forall x\, \exists y$, must be done from the inside out.
- **Persistent.** The algorithm only adds nodes.

## Variants and improvements

- **Relational product.** In [symbolic model checking](/symbolic-model-checking/) the image of a set of states is $\exists X\,(S(X) \wedge T(X, X'))$. The relational product, or AND-EXISTS, computes it in one recursion over pairs of nodes. It splits on the top variable of $f$ and $g$, recurses on the cofactor pairs, and at a variable of $X$ returns the OR of the two results, or $1$ at once if the first result is $1$. It never builds $f \wedge g$, which can be much larger than the result. Its result has at most $(|f| \cdot |g|)^{2^{|X|}}$ nodes, from the bounds for AND and for each quantified variable, and at most $2^{n - |X|} + 1$ nodes as a function of the other variables. The tests check it against $\exists X$ applied to the BDD of $f \wedge g$.
- **Early quantification.** When $T$ is a conjunction of parts, a variable can be quantified as soon as no later part depends on it. This keeps intermediate results small in [symbolic reachability](/symbolic-reachability/).
- **Unique quantification.** XOR at line L7 gives $f|_{x=0} \oplus f|_{x=1}$ for one variable, the Boolean difference of $f$ by $x$, which is 1 where the value of $f$ depends on $x$.
- **Generalized cofactors.** The [generalized cofactor](/generalized-cofactor/) operations constrain and restrict simplify a function under a care set; they are related to quantification but keep all variables.

## When to use it

Use BDD quantification when the function is already a BDD of moderate size and the result must be a BDD again: image computation and [symbolic reachability](/symbolic-reachability/), projection of a set of solutions onto some variables, and evaluation of [QBF](/qbf/) formulas with few variables. When the input is a CNF formula, the clause-based methods of [Boolean quantifier elimination](/boolean-quantifier-elimination/), such as [Davis-Putnam elimination](/davis-putnam-elimination/), avoid building a BDD at all.

## Pitfalls

- **A cache key without $X$.** A result for one set of variables can be returned for another.
- **Quantifying in a loop of single variables.** It works, but each step makes a full pass and an intermediate BDD. One call with the whole set is faster.
- **Size blow-up.** One variable can square the size, and a few variables can make it exponential. In model checking, quantify early and keep the quantified variables near the bottom of the [variable ordering](/variable-ordering/) when possible.
- **The relational product without the early stop.** At a variable of $X$, if the first result is $1$, the second need not be computed. Without this test the relational product does much useless work.
- **Mixed quantifiers in one call.** $\exists x\, \forall y\, f$ is not $\forall y\, \exists x\, f$ in general, so the quantifiers must be applied in their order, innermost first.

## Implementations

## History

The identity $\exists x\, f = f|_{x=0} \vee f|_{x=1}$ goes back to the elimination of variables in Boole's algebra of logic. Bryant (1986) gave RESTRICT and APPLY, with APPLY in time $O(|G_1| \cdot |G_2|)$, which together give quantification of one variable in quadratic time. Symbolic model checking in the early 1990s, by Burch, Clarke, McMillan, Dill and Hwang, made quantification and the relational product central BDD operations, since every image computation needs them. Knuth (2011, Section 7.1.4) treats the quantifiers on BDDs.

## References

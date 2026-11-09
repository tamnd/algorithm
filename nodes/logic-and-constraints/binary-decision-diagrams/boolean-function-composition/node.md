---
tag: TY2RZS
kind: problem
slug: boolean-function-composition
name: Boolean function composition
aliases:
- functional composition
- substitution of a function for a variable
- vector composition
area: logic-and-constraints/binary-decision-diagrams
level: intro
summary: Given BDDs for f and g, build the BDD of f with g put in place of a variable, or of f with a list of functions put in place of all its variables.
prereqs: [boolean-function, cofactor, shannon-expansion, ite-operator]
see_also: [bdd-compose, ite-operator, bdd-apply, bdd-quantification, cofactor, generalized-cofactor, variable-ordering, symbolic-reachability]
sources:
  - paper: doi:10.1109/TC.1986.1676819
    title: Randal E. Bryant, Graph-based algorithms for Boolean function manipulation, IEEE Transactions on Computers C-35(8), 1986, pages 677 to 691
    locator: Section 4, Compose, with the time bound O(|G1|^2 |G2|)
  - book: isbn:9780898714586
    title: Ingo Wegener, Branching Programs and Binary Decision Diagrams, Theory and Applications, SIAM, 2000
    locator: Chapter 3, OBDDs (the operations on OBDDs, replacement of a variable by a function)
  - book: isbn:9780201038040
    title: Donald E. Knuth, The Art of Computer Programming, Volume 4A, Combinatorial Algorithms Part 1, 2011
    locator: Section 7.1.4, Binary decision diagrams (composition and the ITE operation)
---

Boolean function composition puts a function in place of a variable. Given $f$ and $g$ over the variables $x_1, \ldots, x_n$ and an index $i$, the result is $f[x_i := g]$: evaluate $g$ first and give its value to $x_i$. In BDD work the inputs and the output are reduced ordered BDDs with one order, and the question is the cost and the size of the result. A single substitution is one call of [ITE](/ite-operator/): $f[x_i := g] = \mathrm{ITE}(g, f|_{x_i=1}, f|_{x_i=0})$, with $O(|f|^2 |g|)$ time (Bryant 1986). The algorithm is on the page [BDD compose](/bdd-compose/). This page is the problem: its forms, its size bounds, and what it reduces to.

## In plain words

A function is a box with input wires and one output wire. Composition connects the output of a second box to one input of the first box. The new box has the inputs of both boxes, with the connected input removed.

With BDDs, there is a simple rule. The first diagram asks about the connected input at some point. Instead of reading that input, the new diagram asks the second box for its answer, and goes on with that answer. The work is to merge the two diagrams into one diagram that keeps the fixed order of questions. This can make the result larger than both inputs together. If many inputs are connected at once, the result can be very large.

## Definition

The variables are $x_1, \ldots, x_n$, and all diagrams are reduced ordered BDDs with the same order $\pi$. The size $|f|$ counts the nodes of the diagram of $f$, with the sinks.

**Problem (single substitution).** The input is a BDD of $f$, a BDD of $g$, and an index $i$. The output is the BDD of

$$f[x_i := g](x) = f(x_1, \ldots, x_{i-1}, g(x), x_{i+1}, \ldots, x_n).$$

By the [Shannon expansion](/shannon-expansion/) of $f$ by $x_i$, this is

$$f[x_i := g] = (g \wedge f|_{x_i=1}) \vee (\neg g \wedge f|_{x_i=0}) = \mathrm{ITE}(g, f|_{x_i=1}, f|_{x_i=0}).$$

**Problem (vector composition).** The input is a BDD of $f$ and BDDs of $g_1, \ldots, g_n$. The output is the BDD of $f(g_1(x), \ldots, g_n(x))$. All the substitutions happen at the same time: the $g_j$ see the old variables, not the results of other substitutions.

## Variants

- **Substitution of a constant.** $f[x_i := c]$ for $c \in \{0, 1\}$ is the [cofactor](/cofactor/) $f|_{x_i=c}$. It takes $O(|f|)$ time, and the result is never larger than $f$.
- **Renaming.** $f[x_i := x_j]$. If the renaming keeps the relative order of the variables that $f$ uses, the result is $f$ with new labels, in $O(|f|)$ time. Otherwise it is a general composition.
- **Sequential substitution.** $f[x_1 := g_1][x_2 := g_2]$ is not the same as the vector composition if $g_1$ contains $x_2$, because the second step also changes the copy of $x_2$ inside $g_1$. See the second example.
- **Composition into new variables.** Write $f$ over new variables $y_1, \ldots, y_m$ and the $g_j$ over $x$. Then the result has no $y$ variables. This is how a circuit is built gate by gate, and how a function vector is applied to a state set in model checking.
- **Composition with a Boolean operator.** For an operator $\circ$, $f \circ g$ is $(y_1 \circ y_2)[y_1 := f, y_2 := g]$. So [APPLY](/bdd-apply/) is the special case where the outer function has two variables.

## Examples

The numbers below were checked with a script. The order is $x_1, x_2, x_3$, and sizes include the sinks.

**One substitution.** Let $f = x_1 \oplus x_3$ (5 nodes) and $g = x_2 \wedge x_3$ (4 nodes). The cofactors are $f|_{x_1=1} = \neg x_3$ and $f|_{x_1=0} = x_3$. So

$$f[x_1 := g] = \mathrm{ITE}(x_2 \wedge x_3, \neg x_3, x_3) = x_3 \wedge \neg x_2.$$

If $x_3 = 0$, both branches give 0. If $x_3 = 1$, the result is $\neg x_2$. The result has 4 nodes.

**Simultaneous against sequential.** Let $f = x_1 \wedge x_2$, $g_1 = x_2 \oplus x_3$ and $g_2 = x_1 \vee x_3$.

| method | result | value at $x = (1, 0, 0)$ |
|---|---|---|
| vector composition $f(g_1, g_2, x_3)$ | $(x_2 \oplus x_3) \wedge (x_1 \vee x_3)$ | 0 |
| $f[x_1 := g_1]$, then $[x_2 := g_2]$ | $(x_2 \wedge \neg x_3)[x_2 := x_1 \vee x_3] = x_1 \wedge \neg x_3$ | 1 |

The first step of the sequential method gives $(x_2 \oplus x_3) \wedge x_2 = x_2 \wedge \neg x_3$. The second step then replaces the $x_2$ that came from $g_1$, which the vector composition does not do.

**A large result from small inputs.** Let $f = y_1 \vee \cdots \vee y_k$ ($k + 2$ nodes), and $g_j = x_{2j-1} \wedge x_{2j}$ (4 nodes each). The composition is $x_1 x_2 + x_3 x_4 + \cdots + x_{2k-1} x_{2k}$. With the order $x_1, x_3, \ldots, x_{2k-1}, x_2, x_4, \ldots, x_{2k}$ its BDD has $2^{k+1}$ nodes: 4, 8, 16, 32 and 64 nodes for $k = 1, \ldots, 5$. The total input size is only $5k + 2$. With the order $x_1, x_2, x_3, \ldots$ the same result has $2k + 2$ nodes; see [variable ordering](/variable-ordering/).

## Known algorithms

- **By ITE.** Compute the two cofactors of $f$ in $O(|f|)$ time, then one ITE call. ITE with a [computed table](/computed-table/) visits at most one triple of nodes per call, so it takes $O(|g| \cdot |f|^2)$ time and the result has at most that many nodes.
- **Bryant's compose (1986).** One recursive pass that walks $f$ and $g$ together and uses the restriction of $f$ at $x_i$ on the way. Bryant gives the bound $O(|f|^2 |g|)$. The details are on the page [BDD compose](/bdd-compose/).
- **Vector composition by recursion on $f$.** For a node $u$ of $f$ with variable $x_j$ and children $u_0, u_1$, the result is $\mathrm{ITE}(g_j, R(u_1), R(u_0))$, where $R$ is the result for a child. Memoize $R$ on the nodes of $f$. This makes $|f|$ calls of ITE, but each call can be large, because the intermediate results are compositions too.
- **By quantification.** $f(g_1, \ldots, g_n) = \exists y \, \big(f(y) \wedge \bigwedge_j (y_j \leftrightarrow g_j(x))\big)$. This uses the relational product of [BDD quantification](/bdd-quantification/). It is how symbolic model checkers compute images, since the conjunction and the quantification run in one pass.

## Bounds

- **One substitution.** At most $O(|f|^2 |g|)$ nodes and time, from the ITE construction.
- **Constant substitution.** At most $|f|$ nodes and $O(|f|)$ time.
- **Vector composition.** No polynomial bound in the input sizes. The third example gives a result with $2^{k+1}$ nodes from inputs with $5k + 2$ nodes in total.
- **The order still counts.** The result is a function like any other, and its size depends on the order. If the result has an exponential lower bound for every order, as the middle bit of a product does ([multiplier lower bound](/multiplier-bdd-lower-bound/)), every composition method that builds it needs exponential time.

## Reductions

- **APPLY reduces to composition** with an outer function of two variables, as above.
- **Quantification reduces to substitution of constants:** $\exists x_i f = f[x_i := 0] \vee f[x_i := 1]$.
- **Composition reduces to ITE:** one substitution is one ITE call with two cofactors.
- **Composition reduces to a relational product**, a conjunction followed by an existential quantification over new variables.

## Applications

- **Building BDDs of circuits.** Each gate is a composition of a small function with the BDDs of its inputs. The BDD of a sub-circuit can be put in place of a cut variable.
- **Symbolic simulation.** Each register gets the BDD of its next-state function, composed over the steps of the simulation.
- **[Symbolic reachability](/symbolic-reachability/).** The preimage of a state set $S(x)$ under the next-state functions $\delta$ is $S(\delta_1(x), \ldots, \delta_n(x))$, a vector composition. The image needs a range computation, for example with the constrain operator of the [generalized cofactor](/generalized-cofactor/).
- **Equivalence checking.** Two circuits that share a sub-circuit can be compared by putting the same BDD in place of both cut points.

## References

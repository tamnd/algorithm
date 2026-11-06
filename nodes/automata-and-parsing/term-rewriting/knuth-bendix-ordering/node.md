---
tag: 5X50GY
kind: definition
slug: knuth-bendix-ordering
name: Knuth-Bendix ordering
aliases:
- KBO
area: automata-and-parsing/term-rewriting
level: advanced
summary: A reduction ordering comparing weights of terms, then symbols by precedence.
prereqs: [well-founded-reduction-ordering, lexicographic-order, termination]
see_also: [lexicographic-path-ordering, recursive-path-ordering, knuth-bendix-completion, polynomial-interpretation, multiset-ordering, word-problem, linearity, termination]
sources:
  - paper: doi:10.1016/B978-0-08-012975-4.50028-X
    title: Donald E. Knuth and Peter B. Bendix, Simple word problems in universal algebras, in J. Leech (editor), Computational Problems in Abstract Algebra, Pergamon Press, 1970
    locator: pp. 263 to 297 (the weight ordering on terms used to orient equations, and the completion procedure)
  - book: isbn:9780521779203
    title: Franz Baader and Tobias Nipkow, Term Rewriting and All That, Cambridge University Press, 1998
    locator: Chapter 5, Termination (Section 5.4, simplification orders, including the Knuth-Bendix order)
  - paper: doi:10.1016/S0890-5401(03)00021-X
    title: Konstantin Korovin and Andrei Voronkov, Orienting rewrite rules with the Knuth-Bendix order, Information and Computation 183(2) (2003)
    locator: pp. 165 to 186 (orientability by some KBO is decidable in polynomial time)
  - paper: doi:10.1007/s10817-006-9031-4
    title: Bernd Löchner, Things to know when implementing KBO, Journal of Automated Reasoning 36(4) (2006)
    locator: pp. 289 to 310 (a linear time algorithm for comparing two terms)
---

The **Knuth-Bendix ordering** (KBO) compares two terms first by their weight, the sum of the weights of their symbols, and only when the weights are equal by the precedence of the root symbols and then by the arguments from left to right. Knuth and Bendix introduced it in 1970 to orient equations into rules in their [completion procedure](/knuth-bendix-completion/). It is a [well-founded reduction ordering](/well-founded-reduction-ordering/), so a [term rewriting system](/term-rewriting-system/) terminates if each rule decreases. Because it counts symbols, it never orients a rule that copies a variable, and it suits systems that simplify terms, and many equational theorem provers use it as their default order.

## Definition

We use the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, positions as sequences of positive integers, $t|_p$ and $t[s]_p$, substitutions $\sigma$, rules $l \to r$, and $\to_R^*$. Let $|t|_x$ be the number of occurrences of the variable $x$ in $t$.

Fix a finite signature $\Sigma$, a strict partial order $>$ on $\Sigma$ (the **precedence**), a weight $w(f) \in \mathbb{N}$ for each $f \in \Sigma$ and a weight $w_0 > 0$ for variables. The weight of a term is

$$w(x) = w_0 \text{ for } x \in V, \qquad w(f(t_1, \ldots, t_n)) = w(f) + w(t_1) + \cdots + w(t_n).$$

The weights are **admissible** if $w(c) \ge w_0$ for each constant $c$, and if a unary symbol $f$ has $w(f) = 0$, then $f > g$ for every other symbol $g$. So at most one unary symbol has weight $0$.

For admissible weights, $s >_{\mathrm{kbo}} t$ iff $|s|_x \ge |t|_x$ for every variable $x$, and one of these holds.

1. $w(s) > w(t)$.
2. $w(s) = w(t)$, $t$ is a variable $x$, and $s = f^n(x)$ for some $n \ge 1$, where $f$ is the unary symbol of weight $0$.
3. $w(s) = w(t)$, $s = f(s_1, \ldots, s_n)$, $t = g(t_1, \ldots, t_m)$, and $f > g$.
4. $w(s) = w(t)$, $s = f(s_1, \ldots, s_n)$, $t = f(t_1, \ldots, t_n)$, and there is a $k$ with $s_i = t_i$ for $i < k$ and $s_k >_{\mathrm{kbo}} t_k$.

Case 4 is the [lexicographic](/lexicographic-order/) comparison of the arguments. The variable condition $|s|_x \ge |t|_x$ is what keeps the order stable under substitution: if $t$ had more copies of $x$, a large enough term put for $x$ would make $t\sigma$ heavier than $s\sigma$.

**Theorem.** For admissible weights:

- $>_{\mathrm{kbo}}$ is a strict partial order, closed under contexts and substitutions, with the subterm property. So it is a simplification ordering.
- It is well-founded, so it is a reduction ordering.
- If the precedence is total, $>_{\mathrm{kbo}}$ is total on ground terms.

The first item is proved by induction on terms; closure under substitution uses $w(t\sigma) = w(t) + \sum_x |t|_x (w(x\sigma) - w_0)$ and the variable condition. Admissibility is needed for the subterm property: if a unary $h$ had weight $0$ and some $g > h$, then $w(h(g(c))) = w(g(c))$ and $g > h$ would give $g(c) >_{\mathrm{kbo}} h(g(c))$.

*Proof of well-foundedness.* A chain $s_0 >_{\mathrm{kbo}} s_1 >_{\mathrm{kbo}} \cdots$ uses only the variables of $s_0$. Replace each of them by a new constant of weight $w_0$, below the unary symbol of weight $0$ if there is one and incomparable to every other symbol; the weights stay admissible, and by closure under substitution (with case 2 becoming case 3) the chain stays a chain. So it is enough to show that there is no infinite chain of ground terms. Every ground term has weight at least $w_0 > 0$. Call a term **accessible** if no infinite chain starts at it; a term below an accessible term is accessible.

We show by induction on $W$ that every ground term of weight $W$ is accessible. Assume this for all weights below $W$.

*Claim:* if $s = g(s_1, \ldots, s_n)$ has weight $W$ and every $s_i$ is accessible, then $s$ is accessible. Proceed by induction on $(g, (s_1, \ldots, s_n))$, first by the precedence, which is well-founded since $\Sigma$ is finite, then by the lexicographic extension of $>_{\mathrm{kbo}}$ on accessible tuples, which is well-founded. Let $s >_{\mathrm{kbo}} t$. If $w(t) < W$, then $t$ is accessible by the induction on $W$. Otherwise $w(t) = W$ and $t = h(t_1, \ldots, t_m)$ by case 3 or 4. An argument $t_j$ has weight $W$ only if $h$ is unary of weight $0$, because the other arguments have positive weight; otherwise $w(t_j) < W$ and $t_j$ is accessible.

- Case 3, $g > h$: $h$ is not the unary symbol of weight $0$, which is above all others. So all $t_j$ are accessible, and $t$ is accessible by the induction on the root, as $h$ is below $g$.
- Case 4, $h = g$: if $g$ is the unary symbol of weight $0$, then $s_1 >_{\mathrm{kbo}} t_1$, so $t_1$ is accessible because $s_1$ is. Otherwise all $t_j$ have smaller weight. In both cases $t$ is accessible by the induction on the tuple, which is lexicographically smaller.

Now let $s = g(s_1, \ldots, s_n)$ be any ground term of weight $W$, and use induction on its size. Each $s_i$ either has weight below $W$, and is accessible, or has weight $W$ and is smaller, and is accessible by the induction on size. The claim gives that $s$ is accessible. $\blacksquare$

**Computing the order.** For fixed weights and precedence, $s >_{\mathrm{kbo}} t$ can be decided in time $O(|s| + |t|)$ (Löchner, 2006); the direct recursion recomputes weights and variable counts and is quadratic. Deciding whether some admissible weights and precedence orient all rules of a finite system is solvable in polynomial time, by linear programming over the weights (Korovin and Voronkov, 2003). For the [lexicographic path ordering](/lexicographic-path-ordering/) the same question is NP-complete.

## Examples and non-examples

**Groups.** With $w(e) = 1$, $w(\cdot) = w(i) = 0$, $w_0 = 1$ and $i > \cdot > e$, which is admissible because $i$ is the greatest symbol, all ten rules of the convergent group system decrease. Some cases:

- $e \cdot x \to x$ has weights $2 > 1$, case 1.
- $(x \cdot y) \cdot z \to x \cdot (y \cdot z)$ has weights $3 = 3$, the same root and, in the first argument, $w(x \cdot y) = 2 > 1 = w(x)$: case 4.
- $i(x \cdot y) \to i(y) \cdot i(x)$ has weights $2 = 2$ and $i > \cdot$: case 3.
- $i(i(x)) \to x$ has weights $1 = 1$ and is $f^2(x) \to x$ with $f = i$: case 2.

This is the order Knuth and Bendix used to complete the group axioms.

**Addition.** With $w(+) = 0$, $w(s) = w(0) = 1$ and $+ > s$, the rule $s(x) + y \to s(x + y)$ has equal weights and is oriented by case 3.

**Moving a symbol out.** With $w(f) = 0$, $w(g) = 1$ and $f > g$, $f(g(x)) >_{\mathrm{kbo}} g(f(f(x)))$, by case 3. No [lexicographic path ordering](/lexicographic-path-ordering/) orients this rule.

**Non-example: duplication.** $d(x) \to p(x, x)$ violates the variable condition, so no KBO orients it, though it terminates. Likewise the third Ackermann rule $A(s(x), s(y)) \to A(x, A(s(x), y))$ has two copies of $x$ on the right, so the Ackermann system, which the LPO orients, is not oriented by any KBO.

**Non-example: inadmissible weights.** Let $w(h) = 0$ for a unary $h$, and let $g > h$ for a unary $g$. The definition then gives $g(x) >_{\mathrm{kbo}} h(g(x))$ by case 3, since both sides have weight $w(g) + w_0$. But the rule $g(x) \to h(g(x))$ does not terminate, and $g(c) >_{\mathrm{kbo}} h(g(c)) >_{\mathrm{kbo}} h(h(g(c))) >_{\mathrm{kbo}} \cdots$ is an infinite chain, by case 4. This is why the weight $0$ symbol must be the greatest.

**Non-example: commutativity.** $x + y$ and $y + x$ have the same weight and the same root, and neither $x >_{\mathrm{kbo}} y$ nor $y >_{\mathrm{kbo}} x$, so they are incomparable. No reduction ordering orients commutativity.

## Related definitions

- The [lexicographic path ordering](/lexicographic-path-ordering/) and the [recursive path ordering](/recursive-path-ordering/) use the precedence first and need no weights. They orient duplicating rules, such as distributivity, which KBO cannot; KBO orients some rules that they cannot, such as $f(g(x)) \to g(f(f(x)))$.
- A [polynomial interpretation](/polynomial-interpretation/) with linear polynomials generalizes the weight part of KBO; KBO adds the precedence as a tie breaker.
- [Knuth-Bendix completion](/knuth-bendix-completion/) needs a reduction ordering that is total on ground terms; KBO with a total precedence is one, and it is the usual choice in provers based on [unfailing completion](/unfailing-completion/).
- The variable condition is the same as asking the rules to be non-duplicating in the sense of [linearity](/linearity/), together with not introducing new variables.

## References

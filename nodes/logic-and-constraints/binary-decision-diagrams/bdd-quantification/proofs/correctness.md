---
title: QUANT returns the reduced ordered BDD of the quantified function
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order, and $X$ is a set of variables. For a function $f$ and an input $a$, let $a[Y := b]$ be $a$ with the variables of $Y$ set to the values $b$. Then
$$(\exists X\, f)(a) = \bigvee_{b \in \{0,1\}^X} f(a[X := b]), \qquad (\forall X\, f)(a) = \bigwedge_{b \in \{0,1\}^X} f(a[X := b]).$$
We treat both at once: $Q$ is $\exists$ when op is $\vee$, and $\forall$ when op is $\wedge$, and $Q_X f$ is the op of $f(a[X := b])$ over all $b$. The store is a [reduced ordered BDD](/reduced-ordered-bdd/) store, and $f_u$ is the function of node $u$. MK and APPLY are correct: MK$(i, l, h)$ returns the node of $(\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$ when $l$ and $h$ are below level $i$, and APPLY$(\mathrm{op}, l, h)$ returns the node of $f_l \;\mathrm{op}\; f_h$ (see [BDD apply](/bdd-apply/)).

**Lemma 1.** If $f$ does not depend on any variable of $X$, then $Q_X f = f$.

*Proof.* Every term $f(a[X := b])$ equals $f(a)$, and op is idempotent. $\square$

**Lemma 2.** Let $x_i \in X$ and $Y = X \setminus \{x_i\}$. Then $Q_X f = Q_Y (f|_{x_i=0}) \;\mathrm{op}\; Q_Y (f|_{x_i=1})$.

*Proof.* Split the terms by the value $c$ of $x_i$ in $b$. The terms with $c = 0$ are $f|_{x_i=0}(a[Y := b'])$ for all $b'$, and their op is $Q_Y (f|_{x_i=0})(a)$. The same holds for $c = 1$. op is associative and commutative, so the op of all terms is the op of the two parts. $\square$

**Lemma 3.** Let $x_i \notin X$. Then $(Q_X f)|_{x_i = c} = Q_X (f|_{x_i = c})$ for $c \in \{0, 1\}$.

*Proof.* Setting $x_i = c$ in the input $a$ does not touch the variables of $X$, so both sides are the op of $f(a[x_i := c][X := b])$ over all $b$. $\square$

**Theorem.** QUANT$(\mathrm{op}, u, X)$ returns the node of $Q_X f_u$. The result does not depend on $x_1, \ldots, x_{j}$ for $j$ smaller than the level of $u$.

*Proof.* By induction on the number of nodes reachable from $u$. Line L1: a terminal is a constant, and $Q_X$ of a constant is the constant. Line L2: $f_u$ depends only on variables of index at least the level of $u$, which are not in $X$, so the result is $f_u$ by Lemma 1. Line L3 returns a result that line L9 stored for the same key, which was correct when stored, and the store never changes a node.

Otherwise $u = (i, l_0, h_0)$. The functions $f_{l_0}$ and $f_{h_0}$ are the cofactors of $f_u$ by $x_i = 0$ and $x_i = 1$, and they do not depend on $x_i$ or on any earlier variable. By induction, $l$ and $h$ at lines L5 and L6 are the nodes of $Q_X f_{l_0}$ and $Q_X f_{h_0}$, and they do not depend on $x_1, \ldots, x_i$.

If $x_i \in X$, let $Y = X \setminus \{x_i\}$. Since $f_{l_0}$ does not depend on $x_i$, Lemma 2 applied to it gives $Q_X f_{l_0} = Q_Y f_{l_0}$; the same holds for $h_0$. So by Lemma 2 for $f_u$, $Q_X f_u = Q_Y f_{l_0} \;\mathrm{op}\; Q_Y f_{h_0} = f_l \;\mathrm{op}\; f_h$, which APPLY computes at line L7. Neither argument depends on $x_1, \ldots, x_i$, so the result does not either.

If $x_i \notin X$, then by Lemma 3 the cofactors of $Q_X f_u$ by $x_i = 0$ and $x_i = 1$ are $f_l$ and $f_h$. By the [Shannon expansion](/shannon-expansion/), MK$(i, l, h)$ at line L8 returns the node of $Q_X f_u$, and $l$ and $h$ are below level $i$ as MK requires. The result depends on no variable before $x_i$. $\blacksquare$

**Cost.** For a fixed op and $X$, each node $u$ reachable from the argument passes line L3 without a hit at most once, since line L9 stores its key before the call returns, and a call on $u$ only calls itself on nodes below $u$. So there are at most $|f|$ such calls, each with $O(1)$ work besides its recursive calls and one call of MK or APPLY.

For one variable, $X = \{x_i\}$, line L2 stops every path at the first node below level $i$. All calls of APPLY at line L7 are on pairs $(l, h)$ of nodes of the BDD of $f$ below level $i$, and the recursive calls of APPLY stay among such pairs. They share one computed table, so APPLY does real work for at most $|f|^2$ pairs in total. The time is $O(|f|^2)$ expected. The result is the function $f|_{x_i=0} \vee f|_{x_i=1}$, whose two restrictions have at most $|f|$ nodes each, so by the size bound of APPLY it has at most $|f|^2$ nodes.

In general, let $r$ be the largest number of nodes of a result $l$ or $h$ at lines L5 and L6. Each APPLY call at line L7 does real work for at most $r^2$ pairs, and there are at most $|f|$ such calls, so the time is $O(|f| \cdot r^2)$ expected.

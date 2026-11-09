---
title: ITE returns the reduced ordered BDD of if f then g else h
proves: [correctness]
status: full
---

We write $\mathrm{ite}(f, g, h) = (f \wedge g) \vee (\neg f \wedge h)$ for functions in $B_n$, and use the same name for the procedure ITE on node ids. The variables are $x_1, \ldots, x_n$ in this order. The store satisfies the invariant of the [reduced ordered BDD](/reduced-ordered-bdd/): no node has equal children, each edge goes down in the order, and the unique table holds one node per triple. MK keeps this invariant and returns a node for $(\neg x_i \wedge l) \vee (x_i \wedge h)$ when $l$ and $h$ are below level $i$.

**Lemma 1 (identities).** For all $f, g, h \in B_n$:

1. $\mathrm{ite}(1, g, h) = g$, $\mathrm{ite}(0, g, h) = h$, $\mathrm{ite}(f, g, g) = g$ and $\mathrm{ite}(f, 1, 0) = f$.
2. $\mathrm{ite}(f, f, h) = \mathrm{ite}(f, 1, h)$ and $\mathrm{ite}(f, g, f) = \mathrm{ite}(f, g, 0)$.
3. $\mathrm{ite}(f, g, 0) = \mathrm{ite}(g, f, 0)$ and $\mathrm{ite}(f, 1, h) = \mathrm{ite}(h, 1, f)$.
4. $\mathrm{ite}(f, g, h)|_{x_i=b} = \mathrm{ite}(f|_{x_i=b}, g|_{x_i=b}, h|_{x_i=b})$.

*Proof.* Parts 1 to 3 hold at each input $x$: check the two values of $f(x)$. For part 2, where $f(x) = 1$ the left side is $f(x) = 1$, and where $f(x) = 0$ both sides give $h(x)$; the second identity is the same with the roles of the values swapped. Part 3 says $f \wedge g = g \wedge f$ and $f \vee h = h \vee f$. Part 4 holds because a cofactor commutes with $\wedge$, $\vee$ and $\neg$ (see the [cofactor](/cofactor/) page). $\square$

**Theorem.** ITE$(f, g, h)$ returns the node of $\mathrm{ite}(f_f, f_g, f_h)$, and the store stays reduced.

*Proof.* Let $\lambda(f, g, h)$ be the sum of the levels of the three arguments, with $n + 1$ for a terminal. We use induction on $(n + 1) \cdot 3 - \lambda$, so a call may assume the theorem for any call whose arguments have a larger sum of levels, or the same sum and fewer normalization steps.

Lines L1 to L4 return the right node by part 1 of Lemma 1. Lines L5 to L7 replace the triple by another one with the same value of $\mathrm{ite}$, by parts 2 and 3. Replacing $g$ or $h$ by a terminal does not lower any level. A swap changes the order of the arguments but not the multiset of levels, so $\lambda$ does not change. A swap is done only when it puts the smaller id first, so it is not undone by the same rule, and the normalized triple is a fixed point of lines L5 to L7. If the triple now meets a terminal case, ITE calls itself on the same triple, and lines L1 to L4 return at once.

A cache hit at line L8 returns the node that was stored by line L13 for the same normalized triple, which is correct by the induction at the time of storing. Otherwise, line L9 takes the top variable $x_i$, the smallest index among the three arguments. For each argument, the two cofactors by $x_i$ are its children if it tests $x_i$, and the argument itself if it is below level $i$, because then it does not depend on $x_i$. Each cofactor has a level larger than $i$, and at least one argument tests $x_i$, so the sum of levels of each recursive call at lines L10 and L11 is larger. By the induction hypothesis and part 4 of Lemma 1, $t$ is the node of $\mathrm{ite}(f_f, f_g, f_h)|_{x_i=1}$ and $e$ is the node of the cofactor by $x_i = 0$. Both have levels larger than $i$. By the [Shannon expansion](/shannon-expansion/), MK$(i, e, t)$ at line L12 is the node of $\mathrm{ite}(f_f, f_g, f_h)$. $\blacksquare$

**Cost.** Each call that passes line L8 without a hit runs lines L9 to L13 once and stores its triple, so the number of such calls is the number of distinct triples stored. We claim that each stored triple is obtained from $(f_\alpha, g_\alpha, h_\alpha)$ by a permutation of the three entries and by replacing some entries with terminals, for some partial assignment $\alpha$ of a prefix $x_1, \ldots, x_{i-1}$, where $f_\alpha$ is the node of $f_f|_\alpha$ and so on. This holds for the top call with the empty $\alpha$. The cofactors at line L9 extend $\alpha$ by $x_i = b$, and the cofactor of a terminal is the terminal, so the arguments of a child call again have this form, and normalization keeps the form. Each node $f_\alpha$ is a node of the BDD of $f$, so there are at most $|f| \cdot |g| \cdot |h|$ triples $(f_\alpha, g_\alpha, h_\alpha)$. Each of them gives at most $3! \cdot 3^3$ stored triples, a constant. With $O(1)$ expected time for each hash lookup, ITE takes $O(|f| \cdot |g| \cdot |h|)$ expected time.

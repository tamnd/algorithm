---
title: APPLY returns the reduced ordered BDD of f op g in O(|f| |g|) calls
proves: [correctness]
status: full
---

The variables are $x_1, \ldots, x_n$ in this order. A node $u$ of the store has a level $\mathrm{lev}(u)$, the index of the variable it tests, and a terminal has level $n + 1$. We write $f_u$ for the function of node $u$. The store satisfies the invariant of the [reduced ordered BDD](/reduced-ordered-bdd/): no node has equal children, each child has a larger level than its parent, and the unique table holds at most one node per triple $(i, l, h)$. MK$(i, l, h)$ keeps this invariant. When $l$ and $h$ have levels larger than $i$, it returns a node $w$ with $f_w = (\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$ and $\mathrm{lev}(w) \geq i$. Let $\circ$ be a binary operator, given by its four values.

**Lemma 1 (cofactors of an operator).** For all functions $f$, $g$, all $i$ and $b \in \{0, 1\}$, $(f \circ g)|_{x_i = b} = f|_{x_i = b} \circ g|_{x_i = b}$.

*Proof.* At each input $x$ both sides are $f(x') \circ g(x')$, where $x'$ is $x$ with $x_i$ set to $b$. $\square$

**Lemma 2 (cofactors of a node).** Let $i \leq \mathrm{lev}(u)$. If $\mathrm{lev}(u) = i$, then the cofactors of $f_u$ by $x_i = 0$ and $x_i = 1$ are the functions of the low and the high child of $u$. If $\mathrm{lev}(u) > i$, both cofactors are $f_u$.

*Proof.* If $u$ tests $x_i$, then $f_u = (\neg x_i \wedge f_l) \vee (x_i \wedge f_h)$, and $f_l$ and $f_h$ do not depend on $x_i$, since their nodes only test variables of index larger than $i$. Setting $x_i = b$ gives $f_l$ or $f_h$. If $u$ is below level $i$, then $f_u$ does not depend on $x_i$. $\square$

**Lemma 3 (early stop).** If $u$ is a terminal with value $a$, the function $b \mapsto a \circ b$ is one of $0$, $1$, the identity or the negation. In the first two cases $f_u \circ f_v$ is that constant, and in the third case it is $f_v$. The same holds with the roles of $u$ and $v$ swapped.

*Proof.* There are only four functions of one bit, and $f_u \circ f_v = a \circ f_v$ is that function applied to $f_v$. $\square$

**Theorem 1.** APPLY$(\circ, u, v)$ returns the node $w$ with $f_w = f_u \circ f_v$, and $\mathrm{lev}(w) \geq \min(\mathrm{lev}(u), \mathrm{lev}(v))$.

*Proof.* Induction on $2(n + 1) - \mathrm{lev}(u) - \mathrm{lev}(v)$. Line L1 handles two terminals by the table of $\circ$. Line L2 is correct by Lemma 3, and the node it returns is $u$, $v$ or a terminal, which have levels at least the minimum. A hit at line L3 returns the result that line L8 stored for the same key, which was correct by the induction at that time; the store only grows, so the node is still valid. Otherwise let $i = \min(\mathrm{lev}(u), \mathrm{lev}(v)) \leq n$, since not both are terminals. By Lemma 2, lines L5 and L6 give the nodes of the four cofactors of $f_u$ and $f_v$ by $x_i$. Each of them has level larger than $i$ or is the argument itself at a level larger than $i$, and at least one argument is at level $i$ and is replaced by a child. So each recursive call at line L7 has a larger sum of levels, and by induction it returns the node of $f_u|_{x_i = b} \circ f_v|_{x_i = b}$, which is $(f_u \circ f_v)|_{x_i = b}$ by Lemma 1, with level larger than $i$. By the [Shannon expansion](/shannon-expansion/), MK$(i, \cdot, \cdot)$ returns the node of $f_u \circ f_v$, at level $i$ or larger. $\blacksquare$

**Theorem 2 (the result is canonical).** If the store holds a node $w'$ with $f_{w'} = f_u \circ f_v$, then APPLY returns $w'$.

*Proof.* All nodes, including the new ones, are made by MK, so the store stays reduced and ordered with one node per triple. By the [canonicity theorem](/bdd-canonicity/), a reduced ordered store has at most one node per function, so $w = w'$. $\square$

**Theorem 3 (cost).** With the computed table, APPLY$(\circ, u, v)$ passes line L3 without a hit at most $|u| \cdot |v|$ times, where $|u|$ is the number of nodes reachable from $u$, and makes at most $2|u| \cdot |v| + 1$ calls in all.

*Proof.* Call a pair $(u', v')$ *reached* if some call has these arguments. We show that both entries of a reached pair are reachable from $u$ and $v$. This holds for the top call. At line L5 the new first argument is $u'$ itself or a child of $u'$, so it is reachable from $u$; the same holds for $v'$. A call that passes line L3 without a hit stores its key at line L8 before it returns, and a later call with the same key hits. Every call that runs to line L8 returns and stores its key before a later call with the same key starts, because the recursion is depth first and the two calls cannot be on the stack at once: a call on $(u', v')$ only makes calls with a larger sum of levels. So each pair misses at most once, and there are at most $|u| \cdot |v|$ pairs. Each miss makes two calls, and every call except the top one is made by a miss, so the number of calls is at most $1 + 2|u| \cdot |v|$. $\square$

Each call does $O(1)$ work besides its two calls, when the unique table and the computed table are hash tables with $O(1)$ expected time per operation. So APPLY takes $O(|u| \cdot |v|)$ expected time.

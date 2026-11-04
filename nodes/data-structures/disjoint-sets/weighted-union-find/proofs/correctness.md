---
title: Weighted union-find keeps potentials that satisfy exactly the implied facts
proves: [correctness, termination]
status: full
---

Fix an abelian group $(G, +, 0)$. Let $F$ be the set of facts $\mathrm{val}(x) - \mathrm{val}(y) = d$ accepted so far, that is, added by a union that returned true. Say that $F$ *implies* $\mathrm{val}(x) - \mathrm{val}(y) = e$ when every assignment $\mathrm{val} : E \to G$ that satisfies all facts of $F$ also satisfies this one. For each element $x$ with root $r$, $\mathrm{pot}(x)$ is the sum of $w$ along the path from $x$ to $r$, excluding $r$, and $\mathrm{pot}(r) = 0$.

We prove that after each operation:

> **(T)** The parent pointers form a forest with union by size, as in the [disjoint-set forest](/disjoint-set-forest/), and $r.w = 0$ at each root $r$.
>
> **(P)** Each fact of $F$ relates two elements of one tree and is satisfied by $\mathrm{pot}$.
>
> **(I)** For $x$ and $y$ in one tree, $F$ implies $\mathrm{val}(x) - \mathrm{val}(y) = \mathrm{pot}(x) - \mathrm{pot}(y)$. For $x$ and $y$ in different trees, $F$ implies no fact about $\mathrm{val}(x) - \mathrm{val}(y)$.

The forest part of (T) is proved on the [disjoint-set forest](/disjoint-set-forest/) page, because the parent pointers and sizes change exactly as there; the values do not affect them. In particular every find stops.

**Initialization and MAKE-SET.** A new element is a root with $w = 0$ and no facts. Each tree of one element satisfies (P) and (I) trivially, and $\mathrm{pot}$ of every other element is unchanged.

**Lemma 1 (FIND).** FIND$(x)$ changes no potential, keeps (T), (P) and (I), and afterwards $x.w = \mathrm{pot}(x)$ if $x$ is not a root.

*Proof.* By induction on the depth $k$ of $x$. If $k = 0$, line L3 returns, nothing changes, and $x$ is the root. Let $k \ge 1$, with parent $q = x.p$. By the induction hypothesis, FIND$(q)$ changes no potential and leaves $q.w = \mathrm{pot}(q)$ if $q$ is not a root; if $q$ is the root, $q.w = 0 = \mathrm{pot}(q)$ by (T). So before line L5, $\mathrm{pot}(x) = x.w + \mathrm{pot}(q) = x.w + q.w$, because $x$ still points to $q$. Line L5 sets $x.w$ to this value and line L6 points $x$ to the root, so the new potential of $x$ is $x.w + 0 = $ the old $\mathrm{pot}(x)$. The nodes of the subtree of $x$ reach the root through $x$, and their sums up to $x$ do not change, so their potentials do not change either. No tree changes its node set, $F$ does not change, so (P) and (I) still hold. The Python form computes the same values with two loops: it collects the path, and from the node nearest the root down, it sets each value to its own value plus the new value of its parent, which is the parent's potential. $\square$

**DIFF$(x, y)$.** By Lemma 1, after line L8 both finds leave $x.w = \mathrm{pot}(x)$ and $y.w = \mathrm{pot}(y)$ (a root has $w = 0 = \mathrm{pot}$). If the roots differ, (I) says $F$ fixes no difference, and NONE is right. Otherwise line L9 returns $\mathrm{pot}(x) - \mathrm{pot}(y)$, which by (I) is the difference that $F$ implies.

**UNION$(x, y, d)$, same tree.** After line L10, $x.w = \mathrm{pot}(x)$ and $y.w = \mathrm{pot}(y)$. Let $e = \mathrm{pot}(x) - \mathrm{pot}(y)$. By (I), $F$ implies $\mathrm{val}(x) - \mathrm{val}(y) = e$, and by (P) $\mathrm{pot}$ satisfies $F$. If $d = e$, the new fact is implied by $F$; adding it changes no set of solutions, and $\mathrm{pot}$ satisfies it, so (P) and (I) hold. If $d \ne e$, the new fact contradicts $F$, because every solution of $F$ has the difference $e$, and $\mathrm{pot}$ is a solution. Line L11 returns false and the fact is not added. Either way the answer is right.

**UNION$(x, y, d)$, different trees.** The fact $\mathrm{val}(x) - \mathrm{val}(y) = d$ is the same as $\mathrm{val}(y) - \mathrm{val}(x) = -d$, so after the swap of line L12 we may assume that $x$ is in the tree $X$ with root $rx$ and $y$ in the tree $Y$ with root $ry$, with $|X| \le |Y|$. Write $\mathrm{pot}$ for the potentials before line L13 and $\mathrm{pot}'$ after.

*Potentials after the link.* Line L13 sets $rx.p = ry$ and $rx.w = c$, where $c = d + \mathrm{pot}(y) - \mathrm{pot}(x)$. For $z \in X$, the path from $z$ now goes to $rx$ and then to $ry$, so $\mathrm{pot}'(z) = \mathrm{pot}(z) + c$. For $z \in Y$ and for the other trees, nothing changes. The root $ry$ keeps $w = 0$, so (T) holds.

*(P).* Old facts relate two elements of one old tree. Inside $X$ all potentials shift by the same $c$, so differences are kept; the others do not change. For the new fact, $\mathrm{pot}'(x) - \mathrm{pot}'(y) = \mathrm{pot}(x) + c - \mathrm{pot}(y) = d$.

*(I), the new tree.* Let $F' = F \cup \{\mathrm{val}(x) - \mathrm{val}(y) = d\}$. Take $u, v \in X \cup Y$. If both are in $X$, then $F$ implies $\mathrm{val}(u) - \mathrm{val}(v) = \mathrm{pot}(u) - \mathrm{pot}(v) = \mathrm{pot}'(u) - \mathrm{pot}'(v)$, and so does $F' \supseteq F$; the same holds in $Y$. If $u \in X$ and $v \in Y$, then every solution of $F'$ has
$$\mathrm{val}(u) - \mathrm{val}(v) = (\mathrm{val}(u) - \mathrm{val}(x)) + (\mathrm{val}(x) - \mathrm{val}(y)) + (\mathrm{val}(y) - \mathrm{val}(v)) = (\mathrm{pot}(u) - \mathrm{pot}(x)) + d + (\mathrm{pot}(y) - \mathrm{pot}(v)),$$
which equals $\mathrm{pot}(u) + c - \mathrm{pot}(v) = \mathrm{pot}'(u) - \mathrm{pot}'(v)$.

*(I), different trees.* Let $u$ and $v$ be in different trees after the union. We show that $F'$ fixes no value of $\mathrm{val}(u) - \mathrm{val}(v)$. Let the tree of $u$ be $U$. For each $g \in G$, define $\mathrm{val}_g(z) = \mathrm{pot}'(z) + g$ for $z \in U$ and $\mathrm{val}_g(z) = \mathrm{pot}'(z)$ otherwise. Each fact of $F'$ relates two elements of one tree, by (P), so it is satisfied by $\mathrm{val}_g$, which shifts each tree by a constant. Then $\mathrm{val}_g(u) - \mathrm{val}_g(v) = \mathrm{pot}'(u) - \mathrm{pot}'(v) + g$ takes every value of $G$ as $g$ varies. So no fact about this difference is implied. The same argument, applied before the union, shows that the new fact relating $X$ and $Y$ never contradicts $F$, so returning true is right.

Line L14 updates the size of the new root, which is part of (T).

**Conclusion.** By induction on the operations, (T), (P) and (I) hold after each operation. So each union returns false exactly when its fact contradicts the accepted facts, and each DIFF returns the difference that the facts imply, or NONE when they imply none. $\blacksquare$

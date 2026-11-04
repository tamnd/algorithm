---
title: The operations of a disjoint-set forest keep the forest and rank invariants and implement the disjoint-set type
proves: [correctness, termination]
status: full
---

We write $E$ for the set of elements made so far, and $T(r)$ for the set of nodes whose path of parent pointers ends at the root $r$. The *sets* of the structure are the sets $T(r)$ over all roots $r$. We prove that the two invariants of the page hold after each operation:

> **(F)** For each $x \in E$, the sequence $x, x.p, x.p.p, \ldots$ reaches a root, an element $r$ with $r.p = r$, after at most $|E|$ steps.
>
> **(R)** For each non-root $x$, $x.rank < x.p.rank$. Each root $r$ has $|T(r)| \ge 2^{r.rank}$.

Under (F), the sets $T(r)$ are pairwise disjoint and cover $E$, because each element reaches exactly one root. So the structure represents a collection of disjoint sets, each with its root as representative.

**Lemma 1 (FIND).** Assume (F) and (R). Then FIND$(x)$ stops, returns the root $r$ of $x$, and after it (F) and (R) hold, each set $T(\cdot)$ is the same as before, and no rank has changed.

*Proof.* Let $x = x_0, x_1, \ldots, x_k = r$ be the path from $x$ to its root, with $x_{i+1} = x_i.p$ and $k \ge 0$. By (R), $x_0.rank < x_1.rank < \cdots < x_k.rank$.

*Termination and result.* By induction on $k$. If $k = 0$, then $x.p = x$, line L3 fails, and line L5 returns $x = r$. If $k \ge 1$, line L4 calls FIND$(x_1)$, whose path $x_1, \ldots, x_k$ is shorter. By the induction hypothesis it stops and returns $r$, and its only changes are to set $x_i.p \leftarrow r$ for $1 \le i < k$. Line L4 sets $x_0.p \leftarrow r$, and line L5 returns $r$.

*Invariants.* So the only changes of the whole call are $x_i.p \leftarrow r$ for $0 \le i < k$, made in the order $i = k - 1, \ldots, 0$. Take one such change. Before it, $x_i$ reaches $r$; after it, $x_i$ reaches $r$ in one step. Each other node $y$ whose path passes through $x_i$ reached $r$ through $x_i$ before, and still reaches $r$ through $x_i$ after, by a path that is not longer. No other path changes. So (F) holds and each $T(\cdot)$ keeps its members. For (R): $x_i.rank < x_{i+1}.rank \le r.rank$, by the chain of ranks above, so $x_i.rank < r.rank$ after the change. No rank changes, so the root part of (R) is untouched, and the sets $T(r)$ do not change, so their sizes do not change. $\square$

**Lemma 2 (MAKE-SET).** If (F) and (R) hold and $x \notin E$, then after MAKE-SET$(x)$ they hold for $E \cup \{x\}$, and the sets are the old sets and $\{x\}$, with representative $x$.

*Proof.* Lines L1 and L2 make $x$ a root of rank 0 with $T(x) = \{x\}$, and $|T(x)| = 1 = 2^0$. No other field changes, so each other path and each other set is as before. $\square$

**Lemma 3 (UNION).** Assume (F) and (R), and let $x, y \in E$ with sets $A = T(\mathrm{FIND}(x))$ and $B = T(\mathrm{FIND}(y))$. After UNION$(x, y)$, (F) and (R) hold. If $A = B$, the sets are unchanged. Else the sets are the old sets with $A$ and $B$ replaced by $A \cup B$, and the representative of each other set is unchanged.

*Proof.* By Lemma 1, line L6 sets $x$ and $y$ to the roots of $A$ and $B$, and keeps the invariants and the sets. If $x = y$, line L7 returns, and $A = B$. Else $x \ne y$ are two roots, so $A \cap B = \emptyset$. Write $a = x.rank$ and $b = y.rank$.

*Case $a > b$ (line L8).* The only change is $y.p \leftarrow x$. Each node of $B$ now reaches $y$ and then $x$, and each node of $A$ reaches $x$ as before, so $T(x) = A \cup B$ and the other sets do not change. A path in $A \cup B$ is at most $|A| + |B|$ nodes long, so (F) holds. For (R), the new non-root $y$ has $y.rank = b < a = x.rank$. The root $x$ has $|T(x)| = |A| + |B| > |A| \ge 2^{a}$, and its rank is still $a$.

*Case $a \le b$ (lines L9 and L10).* The change $x.p \leftarrow y$ makes $T(y) = A \cup B$, and (F) holds as in the first case. If $a < b$, the new non-root $x$ has $x.rank = a < b$, and $|T(y)| > |B| \ge 2^b$. If $a = b$, line L10 sets $y.rank = b + 1$. Then $x.rank = b < b + 1$, so the edge from $x$ is fine. Each other child $z$ of $y$ had $z.rank < b$, which is still less than $b + 1$. And $|T(y)| = |A| + |B| \ge 2^a + 2^b = 2^{b+1}$, by (R) for the two old roots.

In all cases only $x$ or $y$ stopped being a root, and the representative of each set other than $A$ and $B$ is its old root. $\square$

**Theorem.** Starting from the empty structure, after any sequence of MAKE-SET, FIND and UNION operations with valid arguments, (F) and (R) hold, each operation stops, and the sets $T(r)$ with representatives $r$ are exactly the sets of the [disjoint-set](/disjoint-set/) type after the same sequence. In particular, FIND$(x) = $ FIND$(y)$ if and only if $x$ and $y$ are in the same set, which is law (D3).

*Proof.* The empty structure has no elements, so (F) and (R) hold. By induction on the number of operations, using Lemma 2 for MAKE-SET, Lemma 1 for FIND and Lemma 3 for UNION, the invariants hold after each operation, and each operation changes the represented sets exactly as the type says. FIND returns the root of the tree of $x$, which is the representative of its set. Two elements have the same root exactly when they are in the same tree, by (F). $\blacksquare$

**Corollary (height).** Under (R), each tree has height at most $\lfloor \lg |E| \rfloor$.

*Proof.* On a path $x_0, \ldots, x_k$ to a root $r$, the ranks strictly increase from $x_0.rank \ge 0$, so $k \le r.rank$. By (R), $2^{r.rank} \le |T(r)| \le |E|$, so $r.rank \le \lg |E|$, and $k$ is an integer. $\square$

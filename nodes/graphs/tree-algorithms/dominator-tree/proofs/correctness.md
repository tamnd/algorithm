---
title: The dominators of a vertex are its ancestors in the dominator tree
proves: [correctness, termination]
status: full
---

Let $G$ be a directed graph with vertices $0, \ldots, n - 1$ and start vertex $r$, and let $R$ be the set of vertices reachable from $r$. For $a, b \in R$, $a$ *dominates* $b$ if every path from $r$ to $b$ contains $a$. All paths below start at $r$. We assume that line L1 returns the correct immediate dominators; that is proved on the page of the [Lengauer-Tarjan algorithm](/lengauer-tarjan-algorithm/).

**Lemma 1 (partial order).** Dominance on $R$ is reflexive, transitive and antisymmetric.

*Proof.* Reflexive: every path to $b$ ends at $b$. Transitive: let $a$ dominate $b$ and $b$ dominate $c$. A path $P$ to $c$ contains $b$; its prefix up to the first occurrence of $b$ is a path to $b$, so it contains $a$, and so does $P$. Antisymmetric: let $a \ne b$ and suppose both dominate each other. Take a simple path $P$ to $a$ (one exists since $a \in R$). It contains $b$, so $b$ occurs on $P$ before its last vertex $a$. The prefix of $P$ up to $b$ is a path to $b$; it must contain $a$, but $a$ occurs on the simple path $P$ only at the end, after $b$. Contradiction. $\square$

**Lemma 2 (chain).** Let $v \in R$, $v \ne r$, and let $D$ be the set of strict dominators of $v$. Then $D$ is not empty, any two elements of $D$ are comparable under dominance, and $D$ has a unique element $\mathrm{idom}(v)$ that is dominated by every element of $D$.

*Proof.* $r \in D$. Fix a simple path $P$ from $r$ to $v$. Every element of $D$ occurs on $P$, exactly once. Let $a, b \in D$ with $a$ before $b$ on $P$. Suppose $a$ does not dominate $b$: there is a path $Q$ to $b$ avoiding $a$. Then $Q$ followed by the part of $P$ after $b$ is a path to $v$; that part of $P$ does not contain $a$, since $a$ occurs on $P$ only before $b$. So we have a path to $v$ avoiding $a$, a contradiction with $a \in D$. Hence $a$ dominates $b$. So the elements of $D$ are totally ordered by dominance, in the order in which they occur on $P$, and the last of them on $P$ is dominated by all others; by antisymmetry it is unique. $\square$

**Lemma 3 (recursive form).** For $v \in R \setminus \{r\}$, the set of dominators of $v$ is $\{v\} \cup \mathrm{Dom}(\mathrm{idom}(v))$, where $\mathrm{Dom}(x)$ is the set of dominators of $x$, and $v \notin \mathrm{Dom}(\mathrm{idom}(v))$.

*Proof.* If $d$ dominates $\mathrm{idom}(v)$, then $d$ dominates $v$ by transitivity, since $\mathrm{idom}(v)$ dominates $v$. Conversely, a dominator $d \ne v$ of $v$ is in $D$ and, by Lemma 2, dominates $\mathrm{idom}(v)$. Finally $v$ does not dominate $\mathrm{idom}(v)$, by antisymmetry, since $\mathrm{idom}(v) \ne v$ dominates $v$. $\square$

**Lemma 4 (the tree).** The edges $v \to \mathrm{idom}(v)$ for $v \in R \setminus \{r\}$ form a tree on $R$ rooted at $r$, and for every $v \in R$, $\mathrm{Dom}(v)$ is the set of ancestors of $v$ in that tree.

*Proof.* By Lemma 3, $|\mathrm{Dom}(\mathrm{idom}(v))| = |\mathrm{Dom}(v)| - 1$. So following idom from $v$ strictly decreases the size of the dominator set, which is at least 1, and the walk ends after finitely many steps at the only vertex without an idom, $r$. There is no cycle, every vertex other than $r$ has one parent, so the edges form a tree rooted at $r$. By induction on $|\mathrm{Dom}(v)|$: $\mathrm{Dom}(r) = \{r\}$ (if $d$ dominates $r$, the path consisting of $r$ alone contains $d$), which is the set of ancestors of $r$; and for $v \ne r$, Lemma 3 gives $\mathrm{Dom}(v) = \{v\} \cup$ the ancestors of $\mathrm{idom}(v)$, which are the ancestors of $v$. $\square$

**Lemma 5 (the walk).** Lines L3 to L7 terminate, and afterwards, for $a, b \in R$, $a$ is an ancestor of $b$ in the tree if and only if $tin[a] \le tin[b]$ and $tout[b] \le tout[a]$.

*Proof.* Each tree vertex is pushed with phase enter once, by its parent (or initially, for $r$), and once with phase exit, so the loop runs $2|R|$ times. The stack discipline makes this a preorder walk: when $(v, \text{enter})$ is popped, the entries for the subtree of $v$ are pushed above $(v, \text{exit})$, so all of them are popped before it. So the vertices of the subtree of $v$ get the consecutive entry times $tin[v], \ldots, tin[v] + s(v) - 1$, where $s(v)$ is the subtree size, and $tout[v] = tin[v] + s(v)$. If $a$ is an ancestor of $b$, $b$'s entry time lies in $a$'s range and $b$'s range is inside $a$'s, which gives both inequalities. If not, the subtrees of $a$ and $b$ are disjoint or $b$ is a proper ancestor of $a$; in the first case their ranges are disjoint, so the two inequalities cannot both hold, and in the second $tin[b] < tin[a]$. $\square$

**Theorem.** DOMINATES$(a, b)$ returns true exactly when $a$ dominates $b$, DOMINATORS$(v)$ returns exactly the dominators of $v$, and all operations terminate.

*Proof.* If $a$ or $b$ is not in $R$, $a$ does not dominate $b$ under our convention, and line L8 returns false. Otherwise, by Lemma 4, $a$ dominates $b$ exactly when $a$ is an ancestor of $b$, and by Lemma 5 that is the test of line L9. Line L10 follows idom from $v$ to $r$, which terminates by Lemma 4 and lists the ancestors of $v$, that is, $\mathrm{Dom}(v)$. For $v \notin R$ the implementation returns the empty list. $\blacksquare$

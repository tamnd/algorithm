---
title: The double-array trie build establishes the invariant and lookups follow the trie
proves: [correctness]
status: full
---

We use the pseudocode, the codes $0, \ldots, R$ and the invariant (D1) to (D3) of the page. Let $T$ be the ordinary trie of the key set $K$ built at line L7, with an extra child on code 0 at each node whose path is a key. Write $cell(u)$ for the cell given to a node $u$ of $T$.

**Lemma 1 (the build gives each node of $T$ one cell, and no cell to two nodes).** When the queue empties, each node of $T$ has a cell, the cells of distinct nodes are distinct, $check[cell(u)] = cell(parent(u))$ for each non-root $u$, and $cell(u) = base[cell(parent(u))] + a$ where $a$ is the code of the edge into $u$.

*Proof.* The root gets cell 0, with a reserved check. A node $u$ is dequeued once, because it is enqueued once, by its parent. When $u$ is dequeued at line L9, its children have no cells yet, and line L10 picks a base $b$ for which every cell $b + a$, for $a$ in the codes of the children, is free. Line L11 marks these cells with the check $cell(u)$, so they are no longer free, and line L12 gives the cell $b + a$ to the child on $a$. Cells that are taken are never freed, so no later node gets one of them. Each node of $T$ other than the root is the child of exactly one node, so it gets exactly one cell, at the offset of its code from the base of its parent. Such a base exists: the arrays grow, and a base past the last used cell has all its cells free. Each node's base is set once, when it is dequeued, before any of its children's cells are read. $\square$

**Lemma 2 (D1).** For each node $u$ of $T$ and each code $a$, DA-NEXT$(cell(u), a)$ returns $cell(w)$ if $u$ has a child $w$ on $a$, and NIL otherwise.

*Proof.* If $w$ exists, by Lemma 1 the cell $t = base[cell(u)] + a$ is $cell(w)$ and its check is $cell(u)$, so lines L1 and L2 return $t$. If $w$ does not exist and $t$ is in range, the cell $t$ is free (check $-1$), or the cell of a node $w'$ whose parent $u'$ is not $u$, or the root. In the first case the check is $-1 \ne cell(u)$. In the second, $check[t] = cell(u')$, and $cell(u') \ne cell(u)$ by Lemma 1. The root cannot be $t$, since bases are at least 1 and codes are nonnegative. So line L2 fails and line L3 returns NIL. If $t$ is out of range, line L3 returns NIL too. $\square$

Lemma 1 also gives (D2): each cell other than the root is free or the cell of exactly one node, the one whose parent's cell is named by the check.

**Lemma 3 (D3 and DA-GET).** DA-GET$(k)$ returns the value of $k$ if $k \in K$ and NIL otherwise.

*Proof.* By Lemma 2 and induction on the symbols of $k$, after line L4 has read $j$ symbols, $s$ is the cell of the node of $T$ whose path is the first $j$ symbols of $k$, or the walk has returned NIL because no such node exists. In the second case $k$ is not a prefix of a path of $T$, so $k \notin K$. In the first case, after all symbols, $s = cell(u)$ for the node $u$ with path $k$. By the construction of $T$, $u$ has a child on code 0 if and only if $k \in K$, so by Lemma 2 line L5 finds the leaf cell exactly when $k$ is a key. Line L12 stored the value of $k$ there when the leaf was placed, so line L6 returns it. $\square$

**Prefix searches.** The common prefix search of a text $x$ is the walk of Lemma 3 on the symbols of $x$ with a test of code 0 after each step. By Lemma 3 applied to each prefix of $x$, it reports exactly the keys that are prefixes of $x$, and it stops at the first prefix that is not a path of $T$, after which no longer prefix can be a key. Listing the keys below a node tests the codes $0, \ldots, R$ at each node reached, and by Lemma 2 this finds exactly its children in $T$; visiting them in increasing code order lists the keys in the order of the codes. $\blacksquare$

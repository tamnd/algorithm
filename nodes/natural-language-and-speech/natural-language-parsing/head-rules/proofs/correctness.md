---
title: Head rules turn every constituency tree into a projective dependency tree in which each constituent is a connected piece headed by its head word
proves: [correctness]
status: full
---

We use the pseudocode HEAD-CHILD and DEPENDENCIES of the page. The input is a finite ordered tree $t$ whose leaves are the words $w_1, \ldots, w_n$, left to right, with $n \ge 1$. Each internal node has at least one child. The head table can be any table: the proof uses only that HEAD-CHILD returns one index between 1 and the number of children. That is the part we prove. Whether the chosen heads are good linguistic heads is a separate question, and the table is a heuristic for it.

For a node $v$, $\mathrm{yield}(v)$ is the set of the positions of the words below $v$. For a word $i$, $h(i)$ is the value that DEPENDENCIES writes for $i$, with 0 standing for the artificial root. A word $y$ is a descendant of a word $x$ when following $h$ from $y$ reaches $x$ after zero or more steps.

## Lemma 1: HEAD-CHILD returns a valid index

For a node with $m \ge 1$ children, HEAD-CHILD returns an index $k$ with $1 \le k \le m$.

*Proof.* Line L1 returns 1 when $m = 1$. Line L7 returns an index of the scan order of line L4, which lists $1, \ldots, m$ in some order. Line L8 returns the first index of that order. The NP branch is the same: lines L15 to L19 return $m$, an index found by a scan of $1, \ldots, m$, or $m$. $\square$

## Lemma 2: yields are intervals

For every node $v$, $\mathrm{yield}(v)$ is an interval $\{a, \ldots, b\}$ of positions, and the yields of the children of $v$, in order, are consecutive intervals that cover it.

*Proof.* The words are numbered in the left-to-right order of the leaves, and the leaves below a node are a contiguous run of that order, since the tree is ordered. $\square$

## Lemma 3: the invariant of the walk

DEPENDENCIES visits the nodes children first. When it has finished a node $v$, it has set $\mathrm{head}(v) \in \mathrm{yield}(v)$, and:

1. every word $i \in \mathrm{yield}(v)$ with $i \ne \mathrm{head}(v)$ has an arc, and $h(i) \in \mathrm{yield}(v)$;
2. following $h$ from any word of $\mathrm{yield}(v)$ reaches $\mathrm{head}(v)$ after at most $|\mathrm{yield}(v)| - 1$ steps;
3. no arc is written for $\mathrm{head}(v)$ yet, and no arc written later changes $h(i)$ for a word $i \in \mathrm{yield}(v)$ other than $\mathrm{head}(v)$.

*Proof.* By induction on the height of $v$. A preterminal over word $i$ gets $\mathrm{head}(v) = i$ at line L10 and writes no arc, so parts 1 and 2 hold. For part 3, see the last paragraph.

Let $v$ have the children $u_1, \ldots, u_m$, which are finished before $v$ because the walk is children first. Line L11 picks $c$, a valid index by Lemma 1, and sets $\mathrm{head}(v) = \mathrm{head}(u_c)$. Line L12 writes $h(\mathrm{head}(u_k)) = \mathrm{head}(u_c)$ for each $k \ne c$. These words lie in disjoint yields by Lemma 2, so each gets one arc here.

Part 1: a word $i$ of $\mathrm{yield}(u_k)$ other than $\mathrm{head}(u_k)$ has $h(i) \in \mathrm{yield}(u_k) \subseteq \mathrm{yield}(v)$ by part 1 for $u_k$. The word $\mathrm{head}(u_k)$ with $k \ne c$ now has $h = \mathrm{head}(u_c) \in \mathrm{yield}(v)$.

Part 2: from a word of $\mathrm{yield}(u_k)$, part 2 for $u_k$ reaches $\mathrm{head}(u_k)$ in at most $|\mathrm{yield}(u_k)| - 1$ steps, and one more step reaches $\mathrm{head}(v)$ if $k \ne c$. The total is at most $|\mathrm{yield}(u_k)| \le |\mathrm{yield}(v)| - 1$ when $k \ne c$, since $u_c$ has at least one word outside $\mathrm{yield}(u_k)$.

Part 3: line L12 at a node $u$ writes arcs only for the head words of the children of $u$. If $u$ is a proper ancestor of $v$, the only word of $\mathrm{yield}(v)$ that is the head word of a child of $u$ is $\mathrm{head}(v)$, because the head word of a node is passed up only from its head child. If $u$ is not an ancestor of $v$ and not below it, its yield is disjoint from $\mathrm{yield}(v)$. So after $v$ is finished, the only word of $\mathrm{yield}(v)$ that can still get an arc is $\mathrm{head}(v)$. $\square$

## Theorem

The list $h$ returned by DEPENDENCIES is a dependency tree on the words $1, \ldots, n$ with the root 0: exactly one word has $h(i) = 0$, every other word has a head among the words, and following $h$ from any word reaches 0. The tree is projective. For every node $v$ of $t$, exactly one word of $\mathrm{yield}(v)$, namely $\mathrm{head}(v)$, has its head outside $\mathrm{yield}(v)$ or at 0, and every other word of $\mathrm{yield}(v)$ reaches $\mathrm{head}(v)$ through words of $\mathrm{yield}(v)$.

*Proof.* Apply Lemma 3 to the root $r$, whose yield is all of $1, \ldots, n$. Every word except $\mathrm{head}(r)$ has a head among the words (part 1), and line L13 sets $h(\mathrm{head}(r)) = 0$. By part 2 every word reaches $\mathrm{head}(r)$, and then 0, so there is no cycle.

Constituents: fix a node $v$. By part 3 the arcs of the words of $\mathrm{yield}(v)$ other than $\mathrm{head}(v)$ are final when $v$ is finished. By part 1 their heads lie in $\mathrm{yield}(v)$, and by part 2 they reach $\mathrm{head}(v)$ inside $\mathrm{yield}(v)$. The word $\mathrm{head}(v)$ gets its head later at an ancestor, outside $\mathrm{yield}(v)$ because the yields of the other children are disjoint from it, or 0 at line L13.

Projectivity: take an arc $h(d) = x$ with $d \ne x$, written at line L12 while processing a node $v$. Then $x = \mathrm{head}(v)$, and both $d$ and $x$ are in $\mathrm{yield}(v)$, which is an interval by Lemma 2. So every word strictly between them is in $\mathrm{yield}(v)$, and by part 2 for $v$ it reaches $\mathrm{head}(v) = x$. Every word between $d$ and $x$ is thus a descendant of $x$, which is the definition of a projective arc. $\square$

The subtree of $\mathrm{head}(v)$ in the final tree can be larger than $\mathrm{yield}(v)$: when $v$ is the head child of its parent, the heads of its siblings attach to $\mathrm{head}(v)$ too.

## Termination and cost

Each node is pushed once unfinished and once finished, so the walk of line L9 runs $2s$ times for a tree of $s$ nodes. HEAD-CHILD on a node with $m$ children scans at most $m$ children once for each of the at most $\ell$ labels of the priority list, so its cost is $O(m \ell)$, and the sum of $m$ over all nodes is $s - 1$. The total time is $O(s \ell)$, which is linear for a fixed table. $\blacksquare$

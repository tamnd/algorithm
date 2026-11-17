---
title: The matching method returns the fewest paths that hold every fragment, and their number is the largest set of pairwise incompatible fragments
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G$ is a DAG whose nodes are numbered so that every edge $(u, v)$ has $u < v$. A *path* is a sequence of nodes $p_1 < p_2 < \cdots$ with an edge between each consecutive pair, so every path is increasing. A fragment is a path. A path $P$ *holds* a fragment $x$ if $x$ is a contiguous part of $P$. A *cover* is a set of paths that together hold every fragment. We write $f(x)$ and $l(x)$ for the first and the last node of $x$.

## 1. Line L1 does not change the covers

A path that holds $y$ holds every contiguous part of $y$. So if $x$ is a contiguous part of another fragment $y$, a set of paths is a cover of the fragments if and only if it is a cover of the fragments without $x$. Duplicates are the same. After line L1, no fragment of $F$ is a contiguous part of another.

**Lemma 1.** Two distinct fragments of $F$ have different first nodes, or they are not held by a common path.

*Proof.* If a path $P$ holds $x$ and $y$ and $f(x) = f(y)$, then both start at the same position of $P$, because $P$ visits each node once. Then the shorter one is a prefix of the longer one, which line L1 removed. $\square$

## 2. The order

For $x, y \in F$, lines L2 to L4 define $x \prec y$ when $f(x) < f(y)$ and either $f(y)$ is in $x$, at index $i$, and $x[i..] = y[..|x| - i]$, or $f(y)$ is not in $x$, $l(x) < f(y)$, and $f(y)$ can be reached from $l(x)$.

**Lemma 2.** For $x, y \in F$ with $f(x) < f(y)$: $x \prec y$ if and only if some path of $G$ holds both $x$ and $y$.

*Proof.* Suppose a path $P$ holds both, with $x = P[a..b]$ and $y = P[c..d]$. Then $a < c$, because $P$ is increasing and $f(x) < f(y)$. If $c \le b$, then $f(y) = P[c]$ is in $x$ at index $i = c - a$, and $x[i..] = P[c..b] = y[..b - c]$, with $b - c + 1 = |x| - i$. If $c > b$, then $f(y)$ is not in $x$ (the nodes of $x$ are $P[a..b]$ and all are smaller than $P[c]$), $l(x) = P[b] < P[c] = f(y)$, and $P[b..c]$ is a path from $l(x)$ to $f(y)$. In both cases $x \prec y$.

Conversely, suppose $x \prec y$. In the first case, $y$ is not a contiguous part of $x$, so $|y| > |x| - i$, and $P = x$ followed by $y[|x| - i..]$ is a walk: its parts are paths, and they join at $l(x) = y[|x| - i - 1]$. In the second case, $P = x$, then a path from $l(x)$ to $f(y)$ without its ends, then $y$, is a walk. In a DAG every walk is a path, and $P$ holds $x$ and $y$. $\square$

**Lemma 3.** $\prec$ is a strict partial order on $F$.

*Proof.* It is irreflexive, because $f(x) < f(x)$ is false. Let $x \prec y$ and $y \prec z$. By Lemma 2 there is a path $P$ with $x$ and $y$; by the construction in its proof we may take $P$ to end with $y$. Merging $P$ with $z$ in the same way, which works because the end of $P$ is $y$ and $y \prec z$, gives a path that starts with $x$ and ends with $z$. Since $f(x) < f(y) < f(z)$, Lemma 2 gives $x \prec z$. $\square$

## 3. Covers and chains

A *chain* is a set of fragments that are pairwise comparable under $\prec$.

**Lemma 4.** The fragments held by one path form a chain.

*Proof.* By Lemma 1, two distinct fragments held by the path have different first nodes; the one that starts first precedes the other by Lemma 2. $\square$

**Lemma 5 (merging, line L8).** Let $x_1 \prec x_2 \prec \cdots \prec x_k$. Line L8 builds a path $P_k$ that holds $x_1, \ldots, x_k$, and the part of $P_j$ that starts at $f(x_j)$ is exactly $x_j$, for each $j$.

*Proof.* By induction on $j$. $P_1 = x_1$. Suppose the claim holds for $P_j$. Since $x_j \prec x_{j+1}$ and $P_j$ ends with $x_j$, the step of line L8 is the construction in the proof of Lemma 2 applied to the end $x_j$ of $P_j$. In the overlap case it appends $x_{j+1}[|x_j| - i..]$, and in the other case a connecting path and then $x_{j+1}$ minus its first node. The result is a path, by the same argument as in Lemma 2, its part from $f(x_{j+1})$ is $x_{j+1}$, and the earlier fragments are still held, because line L8 only appends. $\square$

**Theorem 1.** The least number of paths in a cover equals the least number of chains that cover $F$.

*Proof.* Given a cover by $c$ paths, give each fragment to one path that holds it. By Lemma 4 the fragments given to one path form a chain, so there are at most $c$ chains. Conversely, the elements of a chain are totally ordered by $\prec$ (Lemma 3), and Lemma 5 turns each chain into one path that holds all of its elements. $\square$

## 4. Chains and matchings

Line L5 builds the bipartite graph $H$ with a left copy and a right copy of each fragment and an edge $(x, y)$ for each $x \prec y$. Line L6 finds a maximum matching $M$ of $H$, and line L7 follows the matched edges.

**Theorem 2.** The least number of chains that cover $F$ is $|F| - |M|$, and lines L7 and L8 return that many paths, which form a cover.

*Proof.* In a matching, each fragment has at most one matched successor and at most one matched predecessor, and following successors increases $f$, so the matched edges form disjoint sequences $x_1 \prec x_2 \prec \cdots$ that together contain every fragment. Each sequence starts at a fragment with no matched predecessor, which is what line L7 looks for. There are $|F| - |M|$ sequences, because each matched edge joins two fragments into one sequence. Each sequence is a chain, by the transitivity of Lemma 3.

Conversely, a cover by $c$ disjoint chains gives a matching of size $|F| - c$: in each chain, sorted by $\prec$, match each element to the next one. A cover by chains that are not disjoint can be made disjoint by dropping repeated elements, and a subset of a chain is a chain. So the least number of chains is $|F|$ minus the largest matching. By Lemma 5 each sequence becomes a path that holds its fragments, so the output is a cover with $|F| - |M|$ paths, which is the least possible by Theorem 1. $\square$

**Corollary (Dilworth).** The number of paths returned equals the largest number of fragments of which no two are held by a common path.

*Proof.* Two fragments are held by a common path if and only if they are comparable (Lemma 2 and Lemma 1). By Dilworth's theorem, the least number of chains that cover a finite partial order equals the size of its largest antichain. $\blacksquare$

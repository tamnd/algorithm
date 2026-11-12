---
title: The majority clusters form a tree, and that tree is a Robinson-Foulds median
proves: [correctness]
status: full
---

**Setting.** $T_1, \ldots, T_k$ are rooted trees on the same leaf set $X$, $|X| = n$, without nodes of one child. For a tree $T$, $\mathcal{C}(T)$ is the set of its nontrivial clusters, which are the clusters of size 2 to $n - 1$. For a set $c \subseteq X$, $n_c = |\{i : c \in \mathcal{C}(T_i)\}|$. The majority family is $M = \{c : n_c > k/2\}$. Two sets $a, b$ are *compatible* if $a \cap b = \emptyset$, $a \subseteq b$ or $b \subseteq a$. The clusters of one tree are pairwise compatible, because two nodes are either in an ancestor relation or have no common leaf.

**Lemma 1 (the majority family is compatible).** Any two members of $M$ are compatible.

*Proof.* Let $a, b \in M$. The sets $I_a = \{i : a \in \mathcal{C}(T_i)\}$ and $I_b$ are subsets of $\{1, \ldots, k\}$ with $|I_a| + |I_b| > k$. So they have a common index $i$, and $a$ and $b$ are both clusters of $T_i$. So they are compatible. $\square$

**Lemma 2 (the construction).** Lines L5 to L9 return a tree $T$ with $\mathcal{C}(T) = M$, in which each internal node has at least two children.

*Proof.* The procedure takes the members of $M$ by decreasing size and keeps, for each taxon $x$, the node $\mathrm{owner}(x)$, which is the last processed set that contains $x$, or $X$ at the start. We claim that when $c$ is processed, $\mathrm{owner}(x)$ is the same for every $x \in c$, and it is the smallest set among $X$ and the processed members that contains $c$. Let $P$ be that smallest set. It is unique, because two processed sets that both contain $c$ meet, so by Lemma 1 one contains the other. A processed set $q$ with $x \in q$ meets $c$, so by Lemma 1 it contains $c$ or lies in $c$. It cannot lie strictly inside $c$, because it was processed earlier and so is at least as large, and it is not equal to $c$, because $M$ is a set. So $q \supseteq c$, and the last processed set that contains $x$ is the smallest processed set that contains $c$, which is $P$. So line L7 makes $c$ a child of $P$, and $P$ is the smallest member of $M \cup \{X\}$ that strictly contains $c$, because all larger members were processed before $c$. Line L9 hangs each taxon below the smallest member that contains it. This is exactly the tree of the laminar family $M \cup \{X\}$, in which the parent of each set is the smallest set that strictly contains it, so the cluster of the node of $c$ is $c$. A node $c$ has at least two children: the children cover $c$, and each child is a proper subset of $c$, either a smaller member or a single taxon, and $|c| \ge 2$. $\square$

So the majority-rule tree exists for every profile, and lines L1 to L4 compute $n_c$ for every cluster that occurs, which by Lemma 2 gives the right tree.

**Lemma 3 (the sum of distances).** Let $d(T, T') = |\mathcal{C}(T) \,\triangle\, \mathcal{C}(T')|$ be the Robinson-Foulds distance of rooted trees. For every tree $T$ on $X$,
$$\sum_{i=1}^{k} d(T, T_i) = \sum_{i=1}^{k} |\mathcal{C}(T_i)| + \sum_{c \in \mathcal{C}(T)} (k - 2 n_c).$$

*Proof.* For finite sets, $|S \triangle Q| = |S| + |Q| - 2|S \cap Q|$. With $S = \mathcal{C}(T)$ and $Q = \mathcal{C}(T_i)$, summing over $i$ gives $k |S| + \sum_i |\mathcal{C}(T_i)| - 2 \sum_i |S \cap \mathcal{C}(T_i)|$. The last sum counts each pair $(c, i)$ with $c \in S$ and $c \in \mathcal{C}(T_i)$, so it equals $\sum_{c \in S} n_c$. Write $k|S| = \sum_{c \in S} k$. $\square$

**Theorem (median).** The majority-rule tree $T_M$ minimizes $\sum_i d(T, T_i)$ over all rooted trees $T$ on $X$. If $k$ is odd, it is the only tree that does.

*Proof.* By Lemma 3, it is enough to compare $g(S) = \sum_{c \in S} (k - 2 n_c)$ for $S = \mathcal{C}(T)$. A term is negative exactly when $n_c > k/2$, that is, when $c \in M$. Let $S$ be the cluster set of any tree. Then
$$g(S) = \sum_{c \in S \cap M} (k - 2n_c) + \sum_{c \in S \setminus M} (k - 2n_c) \ge \sum_{c \in S \cap M} (k - 2n_c) \ge \sum_{c \in M} (k - 2 n_c) = g(M).$$
The first inequality holds because the terms outside $M$ are at least 0. The second holds because $S \cap M \subseteq M$ and the terms of $M$ are negative. By Lemma 2, $M = \mathcal{C}(T_M)$, so $T_M$ attains the minimum.

If $k$ is odd, no term is 0. If $S \ne M$, then either $S$ has a member outside $M$, whose term is positive, so the first inequality is strict, or $S$ misses a member of $M$, whose term is negative, so the second inequality is strict. In both cases $g(S) > g(M)$. A tree is fixed by its cluster set, so $T_M$ is the only median. $\square$

**Running time.** Each tree has fewer than $n$ internal nodes. Line L3 computes the bit set of a node as the union of the bit sets of its children. Each union and each hash of an $n$-bit set takes $O(n / w)$ word operations, so lines L2 and L3 take $O(kn^2 / w)$ time, with expected $O(1)$ hash table probes per cluster. The table holds at most $k(n-1)$ keys, but line L4 keeps at most $n - 2$ of them, because $M$ is the cluster set of a tree. Sorting $M$ takes $O(n \log n)$ time, and lines L6 to L8 take $O(n)$ time per member, so $O(n^2)$ in total. The total is $O(kn^2 / w + n^2)$ expected time. The table takes $O(kn \cdot n / w)$ words in the worst case. Amenta, Clarke and St. John (2003) avoid the explicit bit sets with a randomized algorithm that takes $O(kn)$ expected time. $\blacksquare$

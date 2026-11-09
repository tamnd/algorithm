---
title: Prüfer decoding returns the unique tree with the given code
proves: [correctness]
status: full
---

Let $V$ be a finite totally ordered set with $|V| = n \ge 2$, and let $\max V$ be its largest element. For a tree $T$ on $V$, the *encoder* does the following for $i = 1, \ldots, n - 2$: let $b_i$ be the smallest leaf of the current tree, write $a_i$ = the only neighbor of $b_i$, and delete $b_i$. The *code* of $T$ is $(a_1, \ldots, a_{n-2})$. Let $T_i$ be the tree before step $i$, so $T_1 = T$, and let $T_{n-1}$ be the tree left at the end, which has two vertices and one edge. For a sequence $a \in V^{n-2}$ and $1 \le i \le n - 1$, let $\mathrm{occ}_i(u) = \#\{j \ge i : a_j = u\}$.

**Lemma 1 (degrees during encoding).** For $1 \le i \le n - 1$ and every vertex $u$ of $T_i$, $\deg_{T_i}(u) = 1 + \mathrm{occ}_i(u)$.

*Proof.* By downward induction on $i$. For $i = n - 1$, $T_{n-1}$ is one edge, both its vertices have degree 1, and $\mathrm{occ}_{n-1} = 0$. For $i < n - 1$, $T_i$ is $T_{i+1}$ plus the leaf $b_i$ joined to $a_i$. So $\deg_{T_i}(a_i) = \deg_{T_{i+1}}(a_i) + 1$, the degree of every other vertex of $T_{i+1}$ is the same in $T_i$, and $\deg_{T_i}(b_i) = 1$. On the other side, $\mathrm{occ}_i(a_i) = \mathrm{occ}_{i+1}(a_i) + 1$, $\mathrm{occ}_i(u) = \mathrm{occ}_{i+1}(u)$ for $u \ne a_i$, and $\mathrm{occ}_i(b_i) = 0$, because $a_i \ne b_i$ and every $a_j$ with $j > i$ is a vertex of $T_{j} \subseteq T_{i+1}$, which does not contain $b_i$. $\square$

So the leaves of $T_i$ are the vertices of $T_i$ that do not occur in $a_i, \ldots, a_{n-2}$, and

$$b_i = \min\big(V \setminus (\{b_1, \ldots, b_{i-1}\} \cup \{a_i, \ldots, a_{n-2}\})\big). \tag{1}$$

For any $a \in V^{n-2}$, define $b_1, \ldots, b_{n-2}$ by (1), and let $S_i$ be the set in (1). Then $|S_i| \ge n - (i - 1) - (n - 1 - i) = 2$, so $b_i$ exists and $b_i < \max S_i$. Let $\{b_{n-1}, c\}$ with $b_{n-1} < c$ be the two elements of $V \setminus \{b_1, \ldots, b_{n-2}\}$, and let $D(a)$ be the graph on $V$ with the edges $\{b_i, a_i\}$ for $i \le n - 2$ and $\{b_{n-1}, c\}$.

**Lemma 2 (the largest vertex stays).** $\max V$ is never one of $b_1, \ldots, b_{n-2}$, so $c = \max V$.

*Proof.* If $\max V \in S_i$, then $S_i$ has a smaller element, because $|S_i| \ge 2$, so $b_i \ne \max V$. So $\max V$ stays outside $\{b_1, \ldots, b_i\}$ for every $i$, and it is the larger of the two remaining elements. $\square$

**Lemma 3 (bijection).** For every $a \in V^{n-2}$, $D(a)$ is a tree on $V$ whose code is $a$. For every tree $T$ on $V$, $D(\mathrm{code}(T)) = T$.

*Proof.* The second claim: by (1), the encoder of $T$ removes exactly the vertices $b_i$ computed from $\mathrm{code}(T)$, and $T$ is the union of the edges $\{b_i, a_i\}$ with the edge of $T_{n-1}$, whose vertices are the two that are never removed. So $T = D(\mathrm{code}(T))$.

The first claim, by induction on $n$. For $n = 2$, $a$ is empty, and $D(a)$ is the single edge on $V$, a tree with the empty code. Let $n \ge 3$. Then $b_1 = \min(V \setminus \{a_1, \ldots, a_{n-2}\})$. Put $V' = V \setminus \{b_1\}$ and $a' = (a_2, \ldots, a_{n-2}) \in V'^{\,n-3}$; this is valid, since no $a_j$ equals $b_1$. Rule (1) for $a'$ on $V'$ gives $b'_i = b_{i+1}$, because the sets agree after removing $b_1$. So $D(a)$ is $D(a')$ plus the edge $\{b_1, a_1\}$ with $a_1 \in V'$. By induction $D(a')$ is a tree on $V'$ with code $a'$, so $D(a)$ is a tree on $V$ in which $b_1$ is a leaf. By Lemma 1 for $D(a')$, every vertex that occurs in $a'$ has degree at least 2 in $D(a')$, and $a_1$ gains the edge to $b_1$. So every vertex that occurs in $a$ has degree at least 2 in $D(a)$, and the leaves of $D(a)$ are among $V \setminus \{a_1, \ldots, a_{n-2}\}$, whose smallest element is $b_1$. So the encoder of $D(a)$ first removes $b_1$ and writes $a_1$, and then it runs on $D(a')$ and writes $a'$. The code of $D(a)$ is $a$. $\square$

It remains to show that PRUEFER-DECODE outputs the edges of $D(a)$, with $V = [n]$. Call the vertices $b_1, \ldots, b_{i-1}$ *used* before the pass of the loop with index $i$.

**Lemma 4 (invariant of the loop).** Before the pass with index $i$, for $1 \le i \le n - 1$ (where $i = n - 1$ means after the last pass):

1. $\deg[u] = 1 + \mathrm{occ}_i(u)$ for every vertex $u$ that is not used;
2. $\mathit{leaf} = b_i$;
3. every used vertex and $\mathit{leaf}$ are less than or equal to $\mathit{ptr}$, and $\mathit{ptr}$ is used or equal to $\mathit{leaf}$;
4. every vertex $u \ne \mathit{leaf}$ that is not used and has $\deg[u] = 1$ satisfies $u > \mathit{ptr}$.

*Proof.* For $i = 1$: lines L1 and L2 give part 1, with no used vertex. Line L3 sets $\mathit{ptr}$ to the smallest $u$ with $\deg[u] = 1$, that is, the smallest vertex not in $a$, which is $b_1$ by (1); line L4 sets $\mathit{leaf} = b_1$. Parts 3 and 4 hold because $\mathit{ptr} = \mathit{leaf}$ is the smallest vertex with $\deg = 1$.

Assume the invariant before the pass with index $i \le n - 2$, and let $v = a_i$. Line L6 outputs $\{b_i, a_i\}$. After line L7, part 1 holds for index $i + 1$ for all vertices that are not used after this pass, that is, all except $b_1, \ldots, b_i$. By (1) and part 1, $b_{i+1}$ is the smallest vertex $u \notin \{b_1, \ldots, b_i\}$ with $\deg[u] = 1$; call these vertices the *candidates*. Each candidate is either a candidate of the old state other than $b_i$, and then it is greater than $\mathit{ptr}$ by part 4, or it is $v$, if line L7 lowered $\deg[v]$ to 1. Also $v \ne \mathit{ptr}$, since $v = a_i$ is not used after the pass, while $\mathit{ptr}$ is used or equal to $b_i$ by part 3.

- *Case L8: $\deg[v] = 1$ and $v < \mathit{ptr}$.* Then $v$ is a candidate below all the others, so $b_{i+1} = v = \mathit{leaf}$. The pointer does not change; $b_i \le \mathit{ptr}$, $v < \mathit{ptr}$, and the old pointer is used or equal to $b_i$, which is now used, so part 3 holds, and all other candidates are above $\mathit{ptr}$, so part 4 holds.
- *Case L9.* Then $\deg[v] \ne 1$ or $v > \mathit{ptr}$, so every candidate is greater than the old $\mathit{ptr}$. Line L9 scans upward from $\mathit{ptr} + 1$ and stops at the first $u$ with $\deg[u] = 1$. Every used vertex is at most the old $\mathit{ptr}$ by part 3, and $b_i \le \mathit{ptr}$, so every vertex in the scanned range is not used, and the scan stops at the smallest candidate, which is $b_{i+1}$. A candidate exists, since $|S_{i+1}| \ge 2$, so the scan stops at most at $n$. After line L10, $\mathit{ptr} = \mathit{leaf} = b_{i+1}$, all used vertices are below it, and all other candidates are above it. Parts 3 and 4 hold.

In both cases part 2 holds for index $i + 1$. $\square$

**Theorem.** For $n \ge 2$ and $a \in [n]^{n-2}$, PRUEFER-DECODE outputs the edges of the unique tree on $[n]$ whose Prüfer code is $a$.

*Proof.* By Lemma 4, the pass with index $i$ outputs $\{b_i, a_i\}$ for $i = 1, \ldots, n - 2$, and after the last pass $\mathit{leaf} = b_{n-1}$, the smaller of the two vertices that are never used. By Lemma 2 the other one is $n$, so line L11 outputs $\{b_{n-1}, n\}$. The output is the edge set of $D(a)$, which is a tree with code $a$ by Lemma 3. It is the only such tree, since a tree $T$ with code $a$ satisfies $T = D(a)$ by Lemma 3. $\blacksquare$

---
title: Bubble popping stops with no poppable bubble, keeps reachability, and pops the bubble of an error inside a read
proves: [correctness]
status: full
---

We use the pseudocode of the page. The graph $G$ is the edge-centric de Bruijn graph of order $k$, with the count $\mathrm{count}(x)$ of each $k$-mer $x$. A *unitig* is a maximal path whose inner vertices have in-degree 1 and out-degree 1. Distinct unitigs share no edge. For a path $P$ of $m_P$ edges, $\mathrm{cov}(P)$ is the mean count of its edges.

A unitig $P$ from $u$ to $w$ is **poppable** for the bounds $\ell$ and $\delta$ if $u \ne w$, $m_P \le \ell$, and the path $Q$ chosen in line L5 exists and satisfies $m_Q \le \ell$, $|m_P - m_Q| \le \delta$ and $\mathrm{cov}(Q) \ge \mathrm{cov}(P)$. The path $Q$ goes from $u$ to $w$ through unitigs other than $P$; among such paths it has the fewest edges, and among those the largest total count.

## 1. Line L5 finds the right path

Line L5 runs Dijkstra's algorithm on the graph whose vertices are the non-simple vertices of $G$ and whose arcs are the unitigs other than $P$. The weight of a unitig $U$ is the pair $(m_U, -\sum_{x \in U} \mathrm{count}(x))$, and pairs are compared in lexicographic order. The weight of a path is the sum of the weights.

**Lemma 1.** Dijkstra's algorithm with these weights returns a path from $u$ to $w$ with the fewest edges and, among those, the largest total count.

*Proof.* The weights form a totally ordered set with addition that respects the order. Each weight has a first component $m_U \ge 1$, so adding a weight to a path makes its weight strictly larger. These are the properties that the proof of [Dijkstra's algorithm](/dijkstra/) uses, in place of non-negative real weights. So the algorithm returns a path of least weight. A path of least weight has the fewest edges, because the first component decides first, and among those it has the largest total count, because the second component is minus that total. $\square$

## 2. The loop stops, and the result has no poppable bubble

**Theorem 2.** BUBBLE-POPPING stops after at most $m_0 + 1$ rounds, where $m_0$ is the number of edges of the input. The output is a subgraph of the input with the same counts on the remaining edges, and it has no poppable unitig. Each deleted edge was on a poppable unitig of the graph at the time.

*Proof.* A round that does not return deletes all edges of one unitig, so at least one edge. So after at most $m_0$ such rounds a round returns. Line L8 only deletes edges and never changes a count. The loop returns at line L9 only when lines L3 to L7 found no poppable unitig. Line L8 deletes only the edges of the unitig that line L6 accepted, and line L6 accepts exactly the poppable unitigs. $\square$

## 3. Popping keeps reachability

**Theorem 3.** Let $G'$ be the graph after one pop. For any two vertices $x$ and $y$ that still have an edge in $G'$, there is a walk from $x$ to $y$ in $G'$ if and only if there is one in $G$.

*Proof.* $G'$ is a subgraph of $G$, so a walk in $G'$ is a walk in $G$. For the other direction, let $P = e_1 \cdots e_m$ be the popped unitig from $u$ to $w$, and let $Q$ be the path of line L5. The inner vertices of $P$ have in-degree 1 and out-degree 1 in $G$, and both their edges are on $P$. So after the pop they have no edge, and $x$ and $y$ are not inner vertices of $P$. Take a walk from $x$ to $y$ in $G$. Each time it uses an edge of $P$, it is at an inner vertex of $P$ or at $u$. An inner vertex can only be entered by the previous edge of $P$ and left by the next one, and the walk starts and ends outside the inner vertices. So each use of $P$ is a full run $e_1 \cdots e_m$ from $u$ to $w$. Replace each such run by $Q$. The edges of $Q$ are on unitigs other than $P$, so none is deleted, and the result is a walk from $x$ to $y$ in $G'$. $\square$

By induction, the final graph has the same reachability as the input on the vertices that keep an edge.

## 4. An error inside a read makes a poppable bubble

Let the genome be $S$ and let a read $r$ of length $L$ be the copy of $S[p \ldots p+L-1]$ (indices from 0) with one wrong letter at index $i$ of $r$.

**Lemma 4.** Assume that $k - 1 \le i \le L - k$, and that

1. no $(k-1)$-mer that contains index $i$ of $r$ occurs in $S$ or in another read, and none occurs twice in $r$;
2. the $k$ genome $k$-mers $t_j = S[p+i-k+1+j \ldots p+i+j]$, for $0 \le j \le k-1$, are kept, and the vertices $u = S[p+i-k+1 \ldots p+i-1]$ and $w = S[p+i+1 \ldots p+i+k-1]$ are distinct;
3. $k \le \ell$, and each path from $u$ to $w$ that avoids the false $k$-mers has at least $k - \delta$ edges.

Then the $k$ false $k$-mers of $r$ form a poppable unitig from $u$ to $w$, and its deletion removes no $k$-mer of $S$.

*Proof.* The $k$-mers of $r$ that contain index $i$ start at the positions $i - k + 1, \ldots, i$ of $r$. All of them lie inside $r$, because $i - k + 1 \ge 0$ and $i + k - 1 \le L - 1$. Call them $y_0, \ldots, y_{k-1}$. By assumption 1 each one has count 1 and is not a $k$-mer of $S$.

The tail of $y_0$ is $r[i-k+1 \ldots i-1]$, which ends before index $i$, so it equals $u$. The head of $y_{k-1}$ is $r[i+1 \ldots i+k-1]$, which starts after index $i$, so it equals $w$. For $0 \le j \le k - 2$, the head of $y_j$ is $r[i-k+2+j \ldots i+j]$, which contains index $i$. By assumption 1, its only edges are $y_j$ in and $y_{j+1}$ out, so it is simple. The vertex $u$ has the two out-edges $y_0$ and $t_0$, which differ in the last letter, and $w$ has the two in-edges $y_{k-1}$ and $t_{k-1}$. So neither is simple, and $P = y_0 \cdots y_{k-1}$ is a unitig from $u$ to $w$ with $m_P = k$ and $\mathrm{cov}(P) = 1$.

The genome path $t_0 \cdots t_{k-1}$ goes from $u$ to $w$ and uses no edge of $P$. It splits into consecutive unitigs at its non-simple vertices, so it is a path in the graph of unitigs, and the path $Q$ of line L5 exists. By Lemma 1, $m_Q \le k \le \ell$, and by assumption 3, $m_Q \ge k - \delta$, so $|m_P - m_Q| \le \delta$. Each count is at least 1, so $\mathrm{cov}(Q) \ge 1 = \mathrm{cov}(P)$. So $P$ is poppable. Its edges are false $k$-mers, so its deletion removes no $k$-mer of $S$. $\square$

The two sides of this bubble spell $r[i-k+1 \ldots i+k-1]$ and $S[p+i-k+1 \ldots p+i+k-1]$, two strings of length $2k - 1$ that differ only in the middle letter.

The lemma says that the error bubble is poppable, not that the loop pops it before it pops a true path. If the genome $k$-mers next to the error also have count 1, the two sides tie, and the order of line L2 decides. The page gives an example in which a true path is popped.

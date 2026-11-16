---
title: Vertex cover branching finds a cover of size at most k exactly when one exists, with at most 2^(k+1) - 1 search tree nodes
proves: [correctness]
status: full
---

For a graph $H$ we write $\tau(H)$ for the least size of a vertex cover of $H$. For a vertex $u$ of $H$, $H - u$ is $H$ without $u$ and without the edges at $u$. The result NONE means that the call found no cover.

**Lemma 1 (an edge forces a choice).** Let $\{u, v\}$ be an edge of $H$ and let $j \ge 1$. Then $\tau(H) \le j$ if and only if $\tau(H - u) \le j - 1$ or $\tau(H - v) \le j - 1$. Moreover, if $S'$ is a cover of $H - u$, then $S' \cup \{u\}$ is a cover of $H$, and the same holds for $v$.

*Proof.* Let $S$ be a cover of $H$ with $|S| \le j$. The edge $\{u, v\}$ has an endpoint in $S$. Say $u \in S$. Every edge of $H - u$ is an edge of $H$ that does not meet $u$, so it has an endpoint in $S \setminus \{u\}$. Hence $\tau(H - u) \le |S| - 1 \le j - 1$. The case $v \in S$ is the same.

For the second part, let $S'$ cover $H - u$. An edge of $H$ either meets $u$, and then $u$ covers it, or it is an edge of $H - u$, and then $S'$ covers it. So $S' \cup \{u\}$ covers $H$. This also gives the converse of the first part: a cover $S'$ of $H - u$ with $|S'| \le j - 1$ yields a cover of $H$ with at most $j$ vertices. $\square$

**Theorem 1 (correctness).** For every graph $G$ and every integer $k \ge 0$, VC-BRANCH$(G, k)$ returns a vertex cover $S$ of $G$ with $|S| \le k$ if $\tau(G) \le k$, and NONE if $\tau(G) > k$.

*Proof.* By induction on $k$. We show the claim for every graph at once.

*Line L1.* If $G$ has no edge, $\emptyset$ is a cover of size $0 \le k$, and the call returns it. This step runs before L2, so it also covers $k = 0$.

*Line L2.* If $G$ has an edge and $k = 0$, then every cover has at least one vertex, so $\tau(G) > 0 = k$, and the call correctly returns NONE. This settles the base case $k = 0$.

*Lines L3 to L6.* Now $k \ge 1$ and $G$ has an edge $\{u, v\}$. By the induction hypothesis for $k - 1$, the call at L4 returns a cover $S$ of $G - u$ with $|S| \le k - 1$ if $\tau(G - u) \le k - 1$, and NONE otherwise. If it returns $S$, then by Lemma 1, $S \cup \{u\}$ covers $G$ and has at most $k$ vertices, so the result of L4 is correct. Otherwise $\tau(G - u) > k - 1$, and line L5 runs. In the same way, it returns a correct cover if $\tau(G - v) \le k - 1$. If both calls return NONE, then $\tau(G - u) > k - 1$ and $\tau(G - v) > k - 1$, so $\tau(G) > k$ by Lemma 1, and NONE at line L6 is correct. $\square$

**Theorem 2 (size of the search tree).** The calls of VC-BRANCH$(G, k)$ form a rooted tree in which each node has at most two children. Its depth is at most $k$, it has at most $2^k$ leaves and at most $2^{k+1} - 1$ nodes.

*Proof.* A call with budget $j$ either stops at L1 or L2, which makes it a leaf, or calls itself at most twice with budget $j - 1$. A call with budget 0 stops at L1 or L2. So the budgets fall by one along every edge of the tree, from $k$ at the root, and no node has a depth greater than $k$. A tree of depth at most $k$ in which each node has at most two children has at most $2^d$ nodes at depth $d$, so at most $2^k$ leaves and at most $\sum_{d=0}^{k} 2^d = 2^{k+1} - 1$ nodes. $\square$

The bound is tight. Let $G$ be $k + 1$ disjoint edges. Every call with budget $j \ge 1$ that has not covered all $k + 1$ edges picks an uncovered edge, and each child still has an uncovered edge, because a cover of $k + 1$ disjoint edges needs $k + 1$ vertices. So every call with budget $j \ge 1$ has two children, and every call at depth $k$ stops at L2. The tree is the full binary tree of depth $k$, with $2^{k+1} - 1$ nodes.

**Theorem 3 (running time and space).** VC-BRANCH runs in $O(2^k (n + m))$ time and $O(n + m)$ extra space, where $n$ and $m$ are the numbers of vertices and edges of $G$.

*Proof.* The implementation keeps one set $C$ of chosen vertices instead of building $G - u$. The graph of a node is $G - C$, and an edge of $G$ is an edge of $G - C$ exactly when neither of its ends is in $C$. At each node, the scan for an uncovered edge (lines L1 and L3) reads each edge at most once, in $O(m)$ time with hashing or indexed vertices. Adding and removing one vertex of $C$ takes $O(1)$ time. So each node costs $O(n + m)$ time, and by Theorem 2 the total time is $O((2^{k+1} - 1)(n + m)) = O(2^k (n + m))$.

The set $C$ holds at most $k \le n$ vertices, and the stack holds at most $k$ frames of two integers each, so the extra space is $O(n + k) = O(n + m)$ when $k \le n$. If $k > n$, the algorithm can replace $k$ by $n$, since $V$ itself is a cover. $\square$

**Lemma 2 (the iterative program).** The program with an explicit stack visits the same nodes, in the same order, as the recursive VC-BRANCH that always picks the first uncovered edge in the list, and it returns the same result.

*Proof.* Let the edges be $e_0, e_1, \ldots, e_{m-1}$. Consider a node of the recursive algorithm with the chosen set $C$ and the budget $j$. We claim that all edges before its branching edge, or all edges at all if it is a leaf at L1, have an end in $C$, and that the program finds the same first uncovered edge when it starts the scan at the index after the parent's branching edge. Indeed, the parent picked the first edge $e_i$ with no end in $C_{\text{parent}}$, so $e_0, \ldots, e_{i-1}$ have an end in $C_{\text{parent}} \subseteq C$, and $e_i$ has an end in $C$, because the child added $u$ or $v$ of $e_i$. So starting the scan at index $i + 1$ gives the same first uncovered edge as a scan from 0.

The stack holds one frame $[i, s]$ for each node on the path from the root to the current node, except the current one: $i$ is the index of the branching edge of that ancestor, and $s$ is the side it is trying, 0 for $u$ at L4 and 1 for $v$ at L5. The chosen set $C$ is the set of the vertices $e_i[s]$ of the frames. So the budget of the current node is $k - (\text{number of frames})$, and the test "number of frames $< k$" is the test "budget $> 0$" of L2.

When a node returns NONE, the program pops frames from the top. For a frame with $s = 0$, it removes $u$ from $C$, adds $v$ and sets $s = 1$; this is the move from L4 to L5 in the recursive call. For a frame with $s = 1$, it removes $v$ and pops the frame; this is line L6, and the parent sees NONE and goes on in the same way. When the stack is empty and the root has failed, the result is NONE. When a node finds no uncovered edge at L1, the recursive calls return through every ancestor at L4 or L5 and add the vertex of that ancestor's branch, so the result is $C$; the program returns a copy of $C$ at once. In each step both programs make the same move, so they visit the same nodes in the same order and return the same result. $\square$

By Theorem 1 and Lemma 2, the program returns a cover of size at most $k$ exactly when $\tau(G) \le k$, and by Theorems 2 and 3 it visits at most $2^{k+1} - 1$ nodes and runs in $O(2^k (n + m))$ time.

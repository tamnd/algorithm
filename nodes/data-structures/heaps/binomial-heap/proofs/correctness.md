---
title: The operations of a binomial heap keep its invariants and return a minimum
proves: [correctness, termination]
status: full
---

We write $K(H)$ for the multiset of keys of the heap $H$. A list of roots is *valid* when each of its trees is a binomial tree $B_k$ with the min-heap property, the parent pointers inside each tree are right, each root has parent nil, and no two trees have the same order $k$. The invariant of a heap is that $H.roots$ is valid and $H.n$ is the number of its nodes. The order of a $B_k$ is the degree of its root, by property 3 of the representation section.

**Lemma 1 (LINK).** Let $x$ and $y$ be the roots of two heap-ordered binomial trees $B_k$, with $x.key \le y.key$. After LINK$(y, x)$, the tree of $x$ is a heap-ordered $B_{k+1}$ with the same nodes as the two trees, and its children are in increasing order of degree.

*Proof.* By the definition, a $B_k$ with the root of the other $B_k$ as a new child of its root is a $B_{k+1}$. Lines L1 and L2 do that and line L3 sets the degree to $k + 1$. The children of $x$ had the degrees $0, \ldots, k - 1$ in this order, and $y$ is added last with degree $k$. The new edge $(x, y)$ is ordered because $x.key \le y.key$, and the other edges are unchanged. $\square$

**Lemma 2 (UNION-ROOTS).** Let $R_1$ and $R_2$ be valid lists of roots on disjoint sets of nodes. Then UNION-ROOTS$(R_1, R_2)$ stops and returns a valid list of roots on the union of the two sets of nodes.

*Proof.* We claim that, before each iteration of line L5 and before each test of line L7, the following hold. (a) Each entry $T[d]$ is a heap-ordered $B_d$ with its root's parent nil. (b) The trees of $T$, the tree of the current $x$ (inside the loop of line L7), and the trees of $R_1$ and $R_2$ not yet visited hold each node of the input exactly once. (c) Inside the loop of line L7, $x$ is a heap-ordered $B_d$ and is not in $T$.

At the start, $T$ is empty and nothing is visited, so (a) and (b) hold. At line L6, the next root $x$ of degree $d$ is the root of a heap-ordered $B_d$, so (c) holds. In an iteration of the loop, line L8 takes $y = T[d]$, a heap-ordered $B_d$ by (a), out of $T$. Line L9 makes $x.key \le y.key$, and then both $x$ and $y$ are roots of heap-ordered $B_d$. By Lemma 1, after line L10 the tree of $x$ is a heap-ordered $B_{d+1}$, and $d$ is now $d + 1$. So (c) holds for the new $d$, and (b) holds because the two trees became one. When the test of line L7 fails, $T[d]$ is empty, and line L11 stores the $B_d$ of $x$ there, so (a) and (b) hold after the iteration.

Each pass of the loop of line L7 links two trees into one, so the number of trees goes down by 1. There are $|R_1| + |R_2|$ trees at the start, so there are fewer than $|R_1| + |R_2|$ links in total, and the procedure stops. At the end, by (a) and (b), the trees of $T$ are heap-ordered binomial trees of distinct orders, one for each $d$ with $T[d] \ne \text{nil}$, and they hold each node once. The parent of each root is nil, because LINK changes only the parent of the root that becomes a child. So the list $R$ of line L12 is valid. $\square$

**Union.** By Lemma 2, $H_1.roots$ becomes a valid list on the nodes of both heaps, and $H_1.n$ becomes the sum. So $K(H_1)$ becomes the union of the two multisets, and $H_2$ becomes an empty, valid heap.

**Insert.** Line L14 makes $x$ a heap-ordered $B_0$. We claim that before each test of line L15, with $d = x.degree$, the node $x$ is the root of a heap-ordered $B_d$, the list $H.roots$ is valid on the other nodes, and each root in it has degree at least $d$. This holds at the start with $d = 0$. So a root of degree $d$, if it exists, is the root of least degree, which is the one that line L15 tests. Lines L16 to L18 remove it and, by Lemma 1, make the tree of $x$ a heap-ordered $B_{d+1}$. The other roots had distinct degrees larger than $d$, so they have degree at least $d + 1$, and the claim holds again. Each iteration removes a root, so the loop stops. When it stops, each root has a degree larger than $d$, so line L19 makes a valid list on the old nodes and $x$, with $x$ of least degree. $K(H)$ gains the key of $x$.

**Minimum.** Let $H.n \ge 1$. Each node is in some tree, and by the global form of the [heap property](/heap-property/), its key is at least the key of the root of that tree. So a root of least key, which line L21 returns, holds a minimum of $K(H)$.

**Extract-min.** Let $x$ be the root that MINIMUM returns, a minimum of $K(H)$, and let $x$ be the root of a $B_k$. Line L23 removes it, and the other roots form a valid list on the other trees. By property 3, the children of $x$ are the roots of heap-ordered binomial trees of the orders $0, 1, \ldots, k - 1$, which are distinct, and line L24 sets their parents to nil, so $R$ is a valid list. The two lists have disjoint nodes. By Lemma 2, line L25 makes a valid list on all nodes except $x$, and $H.n$ drops by 1. So $K(H)$ loses one copy of its minimum, which line L26 returns.

**Decrease-key.** Let $k \le x.key$, as line L27 checks. Line L28 lowers the key. No line of DECREASE-KEY changes the shape of a tree, so each tree is still a binomial tree, and the list is valid except for the heap order. We claim that before each test of line L29, the only edge that may not be ordered is the edge $(x.p, x)$, and that $x.p.key \le c.key$ for each child $c$ of $x$ when $x.p \ne \text{nil}$. This is the condition (U) of the sift-up lemma on the [binary heap](/binary-heap/) page, and the proof of that lemma works on each rooted tree: line L30 exchanges the contents of $x$ and $x.p$, which plays the swap, and line L31 moves up one level. At the start, after line L28, the claim holds because the edges from $x$ to its children were ordered with the old, larger key, and the old key of $x$ was at least the key of its parent. Each iteration goes up one level, so the loop stops after at most $k$ iterations in a $B_k$. When it stops, either $x$ is a root or the edge $(x.p, x)$ is ordered, so each edge is ordered. Line L30 moves the items with their keys and updates the handles, so each handle still names the node of its item. $K(H)$ has the old key replaced by $k$.

**Delete.** Line L32 is a decrease to a key below all others, so by the case above the item reaches the root of its tree, and then this root has the least key, so MINIMUM returns it at line L33, and EXTRACT-MIN removes it. In code, the climb to the root can be done without comparisons, as the Python code does.

**Theorem.** Starting from empty heaps, after each sequence of operations each heap satisfies its invariant, MINIMUM and EXTRACT-MIN return an item of minimum key, and the multiset of keys of each heap is the one that the meldable priority queue type gives for the same sequence. Each operation stops.

*Proof.* The empty heap has the empty valid list. Each operation keeps the invariant and changes the keys as the type says, by the cases above, and each stops. $\blacksquare$

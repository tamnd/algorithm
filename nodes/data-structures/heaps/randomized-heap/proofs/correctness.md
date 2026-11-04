---
title: Randomized meld is correct and takes O(log n) expected time
proves: [correctness, time.expected]
status: full
---

A tree is in heap order if the key of each node is at least the key of its parent. Write $K(T)$ for the multiset of keys of $T$ and $|T|$ for its number of nodes.

**Lemma 1 (correctness).** For every result of the coins, if $A$ and $B$ are heap-ordered trees with roots $a$ and $b$, possibly empty, then $\mathrm{MELD}(a, b)$ returns a heap-ordered tree $T$ with $K(T) = K(A) \uplus K(B)$.

*Proof.* By induction on $|A| + |B|$. If one tree is empty, line L1 returns the other. Otherwise, after line L2, $a.key \le b.key$, and $a.key$ is a smallest key of $A \cup B$, because every key of $A$ is at least $a.key$ and every key of $B$ is at least $b.key$. Let $C$ be the subtree $a.c$ chosen at line L3. The call at line L4 has fewer nodes, since $a$ is not in $C$ or $B$, so by induction it returns a heap-ordered tree $M$ with $K(M) = K(C) \uplus K(B)$, every key of which is at least $a.key$. The other subtree of $a$ is unchanged. So the tree with root $a$ is heap-ordered and holds $K(A) \uplus K(B)$. $\square$

**Theorem 1.** INSERT, DELETE-MIN and MELD keep heap order and the right multiset, and DELETE-MIN returns a smallest key.

*Proof.* As for any heap-ordered tree: insert melds with a one-node tree, and delete-min removes the root, which holds a smallest key, and melds its two subtrees, which hold all other keys. Lemma 1 gives the rest. $\square$

**Lemma 2 (random walk).** For a binary tree $T$, let $W(T)$ be the number of nodes visited by a walk that starts at the root, and at each node moves to the left or the right child with probability $1/2$ each, independently, until it reaches an empty subtree. Then $\mathbb{E}[W(T)] \le \lg(|T| + 1)$.

*Proof.* By induction on $|T|$. If $T$ is empty, $W = 0 = \lg 1$. Otherwise let $T$ have subtrees $L$ and $R$ with $\ell$ and $r$ nodes, so $|T| = \ell + r + 1$. Then
$$\mathbb{E}[W(T)] = 1 + \tfrac12 \mathbb{E}[W(L)] + \tfrac12 \mathbb{E}[W(R)] \le 1 + \tfrac12 \lg(\ell + 1) + \tfrac12 \lg(r + 1).$$
Because $\lg$ is concave, $\tfrac12 \lg u + \tfrac12 \lg v \le \lg \frac{u + v}{2}$ for $u, v > 0$. With $u = \ell + 1$ and $v = r + 1$,
$$\mathbb{E}[W(T)] \le 1 + \lg \frac{\ell + r + 2}{2} = \lg(\ell + r + 2) = \lg(|T| + 1). \quad \square$$

**Lemma 3 (the meld path).** Let the shapes of $A$ and $B$ be fixed before the meld, and let the coins of the meld be fresh. Then the number of calls of MELD that reach line L2 is at most $X_A + X_B$, where $X_A$ has the distribution of a prefix of $W(A)$ and $X_B$ of a prefix of $W(B)$. So the expected number of calls, with the last call at line L1, is at most $\lg(|A| + 1) + \lg(|B| + 1) + 1$.

*Proof.* Each call that reaches line L2 has two nonempty roots. One of them, the smaller one $a$, is the node at which this call flips its coin; call it the node *charged* to the call. Each node is charged at most once, because after its call the path goes into a subtree of it. Consider the nodes of $A$ that are charged, in the order of the calls. The first one, if any, is the root of $A$. If $u$ is a charged node of $A$, the call at $u$ chooses a child $u.c$ by its coin. The next call involves the subtree $u.c$ with its original root: if that subtree is not empty, its root is either charged in this next call or, if it loses the comparison, it is passed on unchanged as the second argument, and every later call keeps the root of this subtree as one of its two arguments until that root is charged or the meld ends. So the charged nodes of $A$ are a prefix of the walk in $A$ driven by the coins flipped at nodes of $A$. These coins are independent and fair. The same holds for $B$. Every call that reaches line L2 charges a node of $A$ or of $B$, so the number of such calls is at most $X_A + X_B$, where $X_A \le W(A)$ and $X_B \le W(B)$ for walks with these coins. Lemma 2 and linearity of expectation give the bound. $\square$

**Theorem 2.** Against a sequence of operations fixed in advance, each meld of heaps of sizes $n_1$ and $n_2$ makes at most $\lg(n_1 + 1) + \lg(n_2 + 1) + 1$ calls in expectation, insert at most $\lg(n + 1) + 2$, and delete-min at most $2 \lg n + 1$, where $n$ is the size before the operation.

*Proof.* The shapes before an operation depend only on earlier coins, and the coins of the operation are independent of them, so Lemma 3 applies conditioned on the shapes, and then also without the condition. Insert melds with one node: $\lg(n + 1) + \lg 2 + 1$. Delete-min melds two subtrees of total size $n - 1$; with $n_1 + n_2 = n - 1$, concavity gives $\lg(n_1 + 1) + \lg(n_2 + 1) \le 2 \lg \frac{n + 1}{2} \le 2 \lg n$ for $n \ge 1$, so the bound is $2 \lg n + 1$. Each call does $O(1)$ work, so each operation takes $O(\log n)$ expected time. $\blacksquare$

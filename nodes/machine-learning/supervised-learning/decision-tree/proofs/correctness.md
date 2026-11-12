---
title: The leaf cells of a decision tree partition the input space, and PREDICT returns the value of the cell that holds the input
proves: [correctness]
status: full
---

We use the binary tree of the page. Each internal node $v$ holds a feature index $j(v)$ and a threshold $\theta(v)$, and has a left child and a right child. Each leaf $\ell$ holds a value $c(\ell)$. The input space is $\mathcal{X} = \mathbb{R}^d$. For a node $v$ with root path $r = v_0, v_1, \ldots, v_t = v$, its *cell* is

$$ C(v) = \{\, x \in \mathcal{X} : \text{for each } i < t,\ x_{j(v_i)} \le \theta(v_i) \text{ if } v_{i+1} \text{ is the left child of } v_i, \text{ and } x_{j(v_i)} > \theta(v_i) \text{ otherwise} \,\}. $$

So $C(r) = \mathcal{X}$, and for an internal node $v$ with children $a$ (left) and $b$ (right), $C(a) = C(v) \cap \{x : x_{j(v)} \le \theta(v)\}$ and $C(b) = C(v) \cap \{x : x_{j(v)} > \theta(v)\}$.

**Representation invariant.** (R1) Each internal node has exactly two children, and the parent of each child is that node. (R2) The tree is finite and each node other than the root has exactly one parent.

**Lemma 1 (partition).** For each node $v$, the cells of the leaves in the subtree of $v$ are pairwise disjoint and their union is $C(v)$.

*Proof.* By induction on the height of the subtree of $v$. If $v$ is a leaf, the only leaf is $v$ and the claim is $C(v) = C(v)$. If $v$ is internal, by (R1) it has children $a$ and $b$, and the subtrees of $a$ and $b$ have smaller height. By the induction hypothesis, the leaf cells under $a$ partition $C(a)$ and the leaf cells under $b$ partition $C(b)$. The sets $\{x_{j(v)} \le \theta(v)\}$ and $\{x_{j(v)} > \theta(v)\}$ partition $\mathcal{X}$, because the order on $\mathbb{R}$ is total. So $C(a)$ and $C(b)$ partition $C(v)$. A leaf under $a$ and a leaf under $b$ have disjoint cells, since these cells lie in $C(a)$ and $C(b)$. So all leaf cells under $v$ are pairwise disjoint and their union is $C(a) \cup C(b) = C(v)$. $\square$

Applied to the root, Lemma 1 says that the leaf cells partition $\mathcal{X}$. So for each $x$ exactly one leaf $\ell(x)$ has $x \in C(\ell(x))$, and the tree defines the function $f(x) = c(\ell(x))$.

**Claim (PREDICT).** For each $x \in \mathcal{X}$, PREDICT$(T, x)$ stops after at most $h$ executions of line L3 or L4, where $h$ is the depth of $T$, and returns $f(x)$.

*Proof.* We use this invariant of the loop of line L2: **(I)** $v$ is a node of $T$ and $x \in C(v)$.

*Initialization.* Line L1 sets $v = r$ and $C(r) = \mathcal{X}$ holds $x$.

*Maintenance.* Assume (I) and that $v$ is internal, with children $a$ and $b$. If $x_{j(v)} \le \theta(v)$, line L3 sets $v = a$, and $x \in C(v) \cap \{x_{j(v)} \le \theta(v)\} = C(a)$. Otherwise line L4 sets $v = b$, and $x \in C(b)$ in the same way. In both cases (I) holds again, and the depth of $v$ grows by exactly one.

*Termination.* The depth of $v$ starts at 0, grows by one in each iteration, and is at most $h$. So the loop runs at most $h$ times and stops with a leaf $v$. By (I), $x \in C(v)$. By Lemma 1, the only leaf whose cell holds $x$ is $\ell(x)$, so $v = \ell(x)$, and line L5 returns $c(\ell(x)) = f(x)$. $\square$

**Claim (SPLIT-LEAF).** If $T$ satisfies (R1) and (R2) and $v$ is a leaf, then after SPLIT-LEAF$(T, v, j, \theta, a, b)$ the tree satisfies (R1) and (R2), it has one more internal node and one more leaf, and the new function $f'$ satisfies $f'(x) = f(x)$ for $x \notin C(v)$, $f'(x) = a$ for $x \in C(v)$ with $x_j \le \theta$, and $f'(x) = b$ for the other $x \in C(v)$.

*Proof.* The operation gives $v$ two new leaves whose parent is $v$, and changes no other node, so (R1) and (R2) hold. The leaf $v$ becomes internal and two leaves appear, so the counts change by $+1$ internal and $+1$ leaf. The cells of the other leaves do not change, since their root paths do not change. The new leaves have cells $C(v) \cap \{x_j \le \theta\}$ and $C(v) \cap \{x_j > \theta\}$. By Lemma 1 the cell of the leaf that holds $x$ gives $f'(x)$, which is the stated function. $\square$

**Claim (PRUNE).** If $T$ satisfies (R1) and (R2) and $v$ is a node, then after PRUNE$(T, v, c)$ the tree satisfies (R1) and (R2), and the new function is $f'(x) = c$ for $x \in C(v)$ and $f'(x) = f(x)$ for the other $x$.

*Proof.* The operation removes the descendants of $v$ and makes $v$ a leaf. The other nodes keep their children and their parents, so (R1) and (R2) hold. The leaves outside the subtree of $v$ keep their cells, and by Lemma 1 applied to $v$ before the change, the removed leaf cells partition $C(v)$, which is now the cell of the one leaf $v$. So $f'$ is as stated. $\square$

**Counts.** A tree that satisfies (R1) has $L = I + 1$ leaves, where $I$ is the number of internal nodes. Proof by induction on $I$: a single leaf has $I = 0$ and $L = 1$; each tree with $I \ge 1$ arises from a tree with $I - 1$ internal nodes by one SPLIT-LEAF on a leaf whose two children are leaves (take an internal node of largest depth), and that operation adds one to both counts. A tree of depth $h$ has at most $2^h$ leaves, since level $i$ holds at most $2^i$ nodes, so $h \ge \lceil \lg L \rceil$. $\blacksquare$

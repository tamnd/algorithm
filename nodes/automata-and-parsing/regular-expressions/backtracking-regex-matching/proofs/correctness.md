---
title: Backtracking regex matching stops and returns true exactly for the strings of the expression
proves: [correctness, termination]
status: full
---

Let $r$ be a regular expression with $m$ nodes and let $w = w_1 \cdots w_n$. For $0 \le i \le i' \le n$, write $w[i:i'] = w_{i+1} \cdots w_{i'}$. The size $|x|$ of an expression is the number of nodes of its syntax tree, and $|\mathrm{CHECK}(s^*, j)| = 0$.

**The tree of configurations.** For a configuration $c = (i, k)$, its *children* are the configurations that lines L9 to L14 push when $c$ is popped. There are at most two. The configuration $(i, [\,])$ has no children, nor has $(i, \emptyset :: k')$, a symbol that does not fit, or a marker $\mathrm{CHECK}(s^*, j)$ with $i \le j$. A *path* is a sequence of configurations in which each one is a child of the one before. The configurations reachable from $(0, [r])$ form a tree $T$ (a configuration reachable on two paths appears twice). A configuration is *successful* if a path leads from it to $(n, [\,])$.

**Lemma 1 (search).** If $T$ is finite, BACKTRACK returns true if and only if $(0, [r])$ is successful.

*Proof.* Line L1 pushes the root. Each pop at line L3 removes one node of $T$ from $K$ and pushes its children. By induction on the number of pops, $K$ always holds nodes of $T$ that have not been popped, and every node of $T$ that has not been popped is a descendant of a node in $K$. Each node is pushed once, as a child of its parent, so if $T$ is finite the loop ends after at most $|T|$ pops. The algorithm returns true only at line L5, when it pops $(n, [\,])$, which is a node of $T$; then the root is successful. Conversely, if the root is successful, $(n, [\,])$ is a node of $T$. While it has not been popped it is a descendant of a node in $K$, so $K$ is not empty and the loop goes on; since the loop ends, it ends at line L5. $\square$

**Lemma 2 (termination).** $T$ is finite.

*Proof.* Each node has at most two children, so by König's lemma it suffices to show that no path is infinite.

Now take an infinite path. Its positions never decrease and are at most $n$, so from some configuration $c_0$ on they are constant, equal to $i$. Every marker made after $c_0$ has $j = i$ and fails at line L14. The list of $c_0$ is finite, so it has finitely many markers with $j < i$, and each step of line L14 that pushes a child removes one of them from the head of the list. So after some configuration $c_1$ of the path, line L14 never pushes a child. From $c_1$ on, each step is one of lines L9, L11, L12 or L13, and each lowers $\sum_{x \in k} |x|$ by at least 1: line L9 removes $\varepsilon$, line L11 replaces $1 + |s| + |t|$ by $|s|$ or $|t|$, line L12 replaces $1 + |s| + |t|$ by $|s| + |t|$, and line L13 replaces $1 + |s|$ by $|s| + 0$. This sum is a natural number, so the path is finite, which is a contradiction. $\square$

**Lemma 3 (soundness).** For an item $x$, let $L(x)$ be the language of $x$ if $x$ is an expression, and $L(\mathrm{CHECK}(s^*, j)) = L(s^*)$. For a list, $L([\,]) = \{\varepsilon\}$ and $L(x :: k) = L(x) L(k)$. If $(i, k)$ is successful, then $w[i:n] \in L(k)$.

*Proof.* By induction on the length of a path from $(i, k)$ to $(n, [\,])$. For length 0, $(i, k) = (n, [\,])$ and $w[n:n] = \varepsilon \in L([\,])$. Otherwise let $(i', k')$ be the next configuration, with $w[i':n] \in L(k')$ by induction, and let $x$ be the head of $k$ and $k''$ its tail.

- L9: $x = \varepsilon$, $i' = i$, $k' = k''$, and $L(k'') = L(\varepsilon) L(k'')$.
- L10: $x = a = w_{i+1}$, $i' = i + 1$, $k' = k''$, so $w[i:n] = a \cdot w[i+1:n] \in L(a) L(k'')$.
- L11: $k' = s :: k''$ or $t :: k''$, and $L(s), L(t) \subseteq L(s \mid t)$.
- L12: $L(s :: t :: k'') = L(st) L(k'')$.
- L13: $k' = k''$, and $L(k'') \subseteq L(s^*) L(k'')$ since $\varepsilon \in L(s^*)$; or $k' = s :: \mathrm{CHECK}(s^*, i) :: k''$, and $L(s) L(s^*) L(k'') \subseteq L(s^*) L(k'')$.
- L14: $k' = s^* :: k''$ and $L(k') = L(\mathrm{CHECK}(s^*, j)) L(k'') = L(k)$.

In each case $L(k') \subseteq L(k)$ with $i' = i$, or the step reads $w_{i+1}$ as shown, so $w[i:n] \in L(k)$. $\square$

**Lemma 4 (completeness).** Let $x$ be an expression and $k$ a list. If $w[i:i'] \in L(x)$ and $(i', k)$ is successful, then $(i, x :: k)$ is successful.

*Proof.* By induction on the pair $(i' - i, |x|)$ in lexicographic order.

- $x = \emptyset$: $L(x)$ is empty, so there is nothing to prove.
- $x = \varepsilon$: then $i' = i$, and line L9 makes $(i, k)$ a child.
- $x = a$: then $i' = i + 1$ and $w_{i+1} = a$, and line L10 makes $(i + 1, k)$ a child.
- $x = s \mid t$: $w[i:i']$ is in $L(s)$ or in $L(t)$; by induction ($|s|, |t| < |x|$), $(i, s :: k)$ or $(i, t :: k)$ is successful, and both are children by line L11.
- $x = st$: choose $p$ with $w[i:p] \in L(s)$ and $w[p:i'] \in L(t)$. By induction on $t$ (with $i' - p \le i' - i$ and $|t| < |x|$), $(p, t :: k)$ is successful. By induction on $s$ with the list $t :: k$ (with $p - i \le i' - i$ and $|s| < |x|$), $(i, s :: t :: k)$ is successful, and it is the child of $(i, x :: k)$ by line L12.
- $x = s^*$: if $i' = i$, the child $(i, k)$ of line L13 is successful. Otherwise $w[i:i'] = u_1 \cdots u_q$ with $q \ge 1$ and $u_1, \ldots, u_q \in L(s)$. Drop the empty factors; since $w[i:i']$ is not empty, at least one factor is left, so $w[i:i'] = v_1 \cdots v_p$ with $p \ge 1$ and each $v_l$ nonempty and in $L(s)$. Let $e = i + |v_1|$, so $i < e \le i'$ and $w[e:i'] \in L(s^*)$. By induction ($i' - e < i' - i$), $(e, s^* :: k)$ is successful. Since $e > i$, line L14 makes $(e, s^* :: k)$ a child of $(e, \mathrm{CHECK}(s^*, i) :: k)$, which is therefore successful. By induction on $s$ with the list $\mathrm{CHECK}(s^*, i) :: k$ (with $e - i \le i' - i$ and $|s| < |x|$), $(i, s :: \mathrm{CHECK}(s^*, i) :: k)$ is successful, and it is a child of $(i, s^* :: k)$ by line L13. $\square$

**Theorem.** BACKTRACK$(r, w)$ stops, and it returns true if and only if $w \in L(r)$.

*Proof.* By Lemma 2, $T$ is finite, so by Lemma 1 the algorithm stops and returns true if and only if $(0, [r])$ is successful. If it is, Lemma 3 gives $w = w[0:n] \in L([r]) = L(r)$. If $w \in L(r)$, then $w[0:n] \in L(r)$ and $(n, [\,])$ is successful with a path of length 0, so Lemma 4 with $i = 0$, $i' = n$ and $k = [\,]$ shows that $(0, [r])$ is successful. $\blacksquare$

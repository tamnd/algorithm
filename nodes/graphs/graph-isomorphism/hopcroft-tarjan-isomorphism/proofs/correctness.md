---
title: Dart refinement decides isomorphism of 3-connected planar graphs
proves: [correctness, termination]
status: full
---

**Setting.** A map $M$ is a connected simple graph with a rotation system. Its darts $D(M)$ are the ordered pairs $(u, v)$ with $uv$ an edge; $\sigma(u, v) = (u, v')$ where $v'$ follows $v$ in the rotation of $u$, and $\alpha(u, v) = (v, u)$. A map isomorphism $M_1 \to M_2$ is a bijection $f : D(M_1) \to D(M_2)$ with $f \sigma = \sigma f$ and $f \alpha = \alpha f$. The algorithm works on the disjoint union $D = D(M_1) \cup D(M_2)$, where $\sigma$ and $\alpha$ act on each side separately. A partition $P$ of $D$ is **stable** when, for every block $B$, both $\sigma^{-1}(B)$ and $\alpha^{-1}(B)$ are unions of blocks; equivalently, darts in one block have their $\sigma$-images in one block and their $\alpha$-images in one block.

**Lemma 1 (refine computes the coarsest stable refinement).** Given a partition $P$ and a queue that contains every block, or that contains enough blocks that every block of $P$ outside the queue is already a union of preimages as described below, REFINE stops and returns the coarsest stable partition finer than $P$.

*Proof.* *Termination:* each split increases the number of blocks, which is at most $|D|$, and each loop iteration removes one queue entry, while entries are added only at splits. *Never too fine:* let $Q$ be any stable partition finer than $P$. Suppose all blocks so far are unions of blocks of $Q$. A split cuts a block $C$ into $C \cap \tau^{-1}(S)$ and $C \setminus \tau^{-1}(S)$ for a block $S$ and $\tau \in \{\sigma, \alpha\}$. Since $S$ is a union of $Q$-blocks and $Q$ is stable, $\tau^{-1}(S)$ is a union of $Q$-blocks, so both pieces are too. *Stable at the end:* this is Hopcroft's argument. Invariant: for every current block $C$ and $\tau$, $\tau^{-1}(C)$ is a union of blocks, or $C$ is in the queue, or $C$ is one piece of a split $X = C \cup C'$ where $\tau^{-1}(X)$ is already a union of blocks and $C'$ is in the queue. In the last case $\tau^{-1}(C) = \tau^{-1}(X) \setminus \tau^{-1}(C')$, and after $C'$ is processed every block lies inside or outside $\tau^{-1}(C')$, so $\tau^{-1}(C)$ is a union of blocks. The code keeps the invariant: when a queued block splits, both pieces are queued; otherwise the smaller piece is queued and the other is covered by the third case. When the queue is empty, the invariant gives stability. $\square$

**Lemma 2 (invariance).** Let $f$ be a map isomorphism $M_1 \to M_2$, and let $\Pi_f$ be the partition of $D$ into the pairs $\{d, f(d)\}$, $d \in D(M_1)$. Then $\Pi_f$ is stable, and if every block of a partition $P$ is a union of such pairs, so is every block of the coarsest stable refinement of $P$.

*Proof.* $\sigma$ maps the pair $\{d, f(d)\}$ to $\{\sigma(d), \sigma(f(d))\} = \{\sigma(d), f(\sigma(d))\}$, another pair; the same holds for $\alpha$. Since $\sigma$ and $\alpha$ are permutations, preimages of pairs are pairs too, so $\Pi_f$ is stable. If $P$ is coarser than $\Pi_f$, then $\Pi_f$ is a stable partition finer than $P$, and the coarsest stable refinement of $P$ is coarser than every such partition, by Lemma 1. $\square$

The initial blocks of L1 are unions of pairs, since $f$ keeps the degree of the tail (the length of the $\sigma$-cycle) and the length of the face (the $\sigma\alpha$-cycle). So after L2 every block is a union of pairs of $\Pi_f$.

**Lemma 3 (pairs give isomorphisms).** If a stable partition has every block of the form $\{a, b\}$ with $a \in D(M_1)$ and $b \in D(M_2)$, then $f(a) = b$ is a map isomorphism, and $\varphi(\text{tail}(a)) = \text{tail}(f(a))$ is a well defined graph isomorphism.

*Proof.* $f$ is a bijection. Stability says $\sigma(a)$ and $\sigma(b)$ lie in one block, which must be $\{\sigma(a), \sigma(b)\}$ since $\sigma$ keeps sides, so $f\sigma = \sigma f$; the same for $\alpha$. The darts with tail $u$ form one $\sigma$-cycle, which $f$ maps onto one $\sigma$-cycle, so $\varphi$ is well defined and a bijection on vertices. An edge $uv$ gives the dart $(u, v)$ and $f(u, v) = (\varphi(u), w)$ with $f(v, u) = f\alpha(u, v) = \alpha f(u, v) = (w, \varphi(u))$, so $w = \varphi(v)$ and $\varphi(u)\varphi(v)$ is an edge. $\square$

**Lemma 4 (one dart decides).** In a connected map, $\sigma$ and $\alpha$ generate a group that acts transitively on the darts. If a map isomorphism $f$ with $f(x) = y$ exists, refining after the pair $\{x, y\}$ is individualized ends with exactly the partition $\Pi_f$.

*Proof.* From $(u, v)$, $\sigma$ reaches every dart with tail $u$ and $\alpha$ moves to a dart with tail $v$; by connectivity every dart of the map is reached, so every dart of $M_1$ is $w(x)$ and every dart of $M_2$ is $w(y)$ for words $w$ in $\sigma, \alpha$ and their inverses. In a stable partition $Q$, darts in one block have their images under $\sigma$ in one block, and since $\sigma^{-1}$ is a power of $\sigma$, also their images under $\sigma^{-1}$; the same for $\alpha$. So if $\{x, y\}$ is a block of $Q$ and $c$ shares a block with $w(x)$, then $w^{-1}(c)$ shares a block with $x$, so $w^{-1}(c) \in \{x, y\}$ and $c \in \{w(x), w(y)\} = \{w(x), f(w(x))\}$. Hence the result $Q$ of the refinement is finer than $\Pi_f$. The starting partition is a union of pairs (the remark after Lemma 2, and $\{x, y\}$ is a pair), so by Lemma 2 $Q$ is also coarser than $\Pi_f$. $\square$

**Theorem (map isomorphism).** MAP-ISOMORPHISM returns a vertex bijection induced by a map isomorphism if one exists, and None otherwise.

*Proof.* If it returns $\varphi$, the check in L7 and Lemma 3 show that $\varphi$ comes from a map isomorphism. Conversely, let $f$ be a map isomorphism. By Lemma 2 every block after L2 is a union of pairs $\{d, f(d)\}$, so each block has equally many darts from each side and L3 does not reject. The block chosen in L4 contains $x$ and $f(x)$, and L5 tries every dart $y$ of $M_2$ in it, including $f(x)$; by Lemma 4 that trial succeeds, so some trial returns. If no map isomorphism exists, no trial can pass L7 by Lemma 3, and the algorithm returns None in L8 or rejects in L3. $\square$

**Theorem (3-connected planar graphs).** For 3-connected planar graphs $G_1, G_2$ with planar rotation systems $R_1, R_2$, TRICONNECTED-PLANAR-ISOMORPHISM returns an isomorphism exactly when $G_1 \cong G_2$.

*Proof.* Any returned $\varphi$ is a graph isomorphism by Lemma 3. Conversely, let $\psi : G_1 \to G_2$ be an isomorphism. Transporting $R_1$ along $\psi$ gives a planar rotation system of $G_2$. By Whitney's theorem, a 3-connected planar graph has only one planar embedding up to reflection, so this system equals $R_2$ or its mirror. Then $\psi$ induces a map isomorphism $R_1 \to R_2$ or $R_1 \to \text{mirror}(R_2)$, and one of the two calls succeeds by the theorem above. $\square$

**Termination.** REFINE terminates by Lemma 1; the trial loop runs at most $|D|$ times; there are two calls. $\blacksquare$

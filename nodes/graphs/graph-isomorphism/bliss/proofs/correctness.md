---
title: The certificate search returns a canonical form and the automorphism group order
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a simple undirected graph on $V = \{0, \ldots, n-1\}$ with a vertex coloring $c$. A node of the search is an ordered partition $\pi$ (an array of vertices cut into cells at given start positions) with a certificate $\mathrm{cert}(\pi)$, the list of refinement traces from the root to $\pi$. At a discrete leaf with vertex order $v_0, \ldots, v_{n-1}$, the labeling is $\lambda(v_i) = i$ and the key is $\mathrm{cert}(\pi)$ followed by the colors of $v_0, \ldots, v_{n-1}$ and the adjacency rows of $G$ relabeled by $\lambda$. Keys are compared as sequences (lexicographically). The full tree $T(G)$ contains every child $\pi \downarrow w$, refined, for every $w$ in the target cell, the first largest cell. A permutation $\gamma$ of $V$ acts on everything by renaming vertices.

**Lemma 1 (invariance).** For every permutation $\gamma$, the refinement of $\pi^\gamma$ in $G^\gamma$ is the image under $\gamma$ of the refinement of $\pi$ in $G$, as a sequence of cells, with the same trace; individualization of $\gamma(w)$ in $\pi^\gamma$ is the image of individualization of $w$ in $\pi$; the target cell has the same start; and leaves $\pi$ and $\pi^\gamma$ have the same key.

*Proof.* Every decision of REFINE depends on cell starts, cell sizes, and the numbers of neighbors in the splitter: the queue holds starts, the touched cells are processed by start, pieces are ordered by neighbor count, and the piece left out of the queue is the first largest one. These quantities do not change under renaming, and the trace records only them. The order of vertices inside a cell may change, but no later decision and no trace entry depends on it. The target cell rule uses only sizes and starts. A leaf of $G^\gamma$ lists $\gamma(v_0), \ldots, \gamma(v_{n-1})$, whose colors and adjacencies in $G^\gamma$ are those of $v_0, \ldots, v_{n-1}$ in $G$. $\square$

So $\gamma$ maps $T(G)$ onto $T(G^\gamma)$ and preserves certificates and keys; and an automorphism that fixes a node maps the subtrees of its children onto each other with equal keys.

**Lemma 2 (equal keys give automorphisms).** If leaves $\pi, \pi'$ have equal keys, then $\gamma$, which maps the vertex at each position of $\pi$ to the vertex at the same position of $\pi'$, is an automorphism. This is the map recorded in L7.

*Proof.* The keys end with the same colors and relabeled rows, so $\gamma$ keeps colors and adjacency. $\square$

**Lemma 3 (the cut in L4 is safe).** If a node $\nu$ with certificate $C$ has $C$ worse than the best key $B$, that is, at the first index where they differ $C$ is smaller, then every leaf below $\nu$ has a key smaller than $B$.

*Proof.* Every leaf key below $\nu$ starts with $C$, so it differs from $B$ at the same index, with the same comparison. $\square$

**Lemma 4 (the orbit cut in L10 is safe).** Skipping a child that is in the orbit of a tried child under found automorphisms fixing the prefix loses no key.

*Proof.* Such automorphisms fix the node, by Lemma 1, so they map the subtree of the tried child onto the subtree of the skipped child with the same keys. $\square$

**Theorem.** The search terminates and returns the leaf of largest key in $T(G)$. Its form is the same for isomorphic colored graphs and different for non-isomorphic ones, and L12 returns $|\mathrm{Aut}(G)|$.

*Proof.* *Termination.* Individualization adds a cell and refinement never merges cells, so the depth is at most $n$ and every node has at most $n$ children. REFINE stops: each queue entry is processed once, and only a split, at most $n - 1$ of them, adds entries.

*Maximum.* By Lemmas 3 and 4, every cut subtree holds only keys smaller than the current best or keys already present in an explored subtree. By induction, the best key at the end is the largest key of $T(G)$.

*Canonical form.* By Lemma 1, $T(G^\gamma)$ has the same keys as $T(G)$, so the largest keys and their final parts are equal. Conversely, the final part is the colored graph relabeled by a bijection, so equal final parts imply isomorphic graphs.

*Group order.* Let $\nu_0, \ldots, \nu_k$ be the first path, $P_d$ the prefix and $w_d$ the first child of $\nu_d$, and $A_d$ the automorphisms fixing $P_d$ pointwise. As in the proof for [nauty](/nauty/), $|\mathrm{Aut}(G)| = \prod_d |w_d^{A_d}|$, and it suffices that every explored child $u$ of $\nu_d$ in the $A_d$-orbit of $w_d$ yields a recorded automorphism in $A_d$ mapping $w_d$ to $u$. Some $\beta \in A_d$ maps the subtree of $w_d$ onto that of $u$, so the subtree of $u$ contains a leaf with the key of the first leaf, and every node on the way has a certificate equal to a prefix of the first key. L4 never cuts such nodes, because of the condition $\mathrm{cert} \ne$ prefix of the first key, and L10 only replaces a subtree by an image under an automorphism fixing the prefix, which contains another leaf with that key. So the search reaches a leaf $\pi$ below $u$ with the key of the first leaf, and L7 records $\gamma$ with $\gamma$ mapping positions of $\nu_k$ to positions of $\pi$. Cells are split in place, so a vertex that is a singleton of $\nu_d$, and the vertex individualized from the target cell of $\nu_d$, have the same positions in all leaves below $\nu_d$. Hence $\gamma$ fixes $P_d$ and maps $w_d$ to $u$. $\blacksquare$

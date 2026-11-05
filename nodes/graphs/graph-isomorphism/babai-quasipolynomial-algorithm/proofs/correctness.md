---
title: The framework model of Babai's algorithm decides string and graph isomorphism
proves: [correctness, termination]
status: full
---

This proof is about the implementation on this page: Luks's recursion with the giant case detected and solved by running over all cosets. It does not prove Babai's quasipolynomial bound, which rests on the tools described on the page and in Babai's paper.

**Setting.** $G$ is a permutation group on $\Omega = \{0, \ldots, n-1\}$, given by generators; products apply the left factor first, $(gh)(d) = h(g(d))$. For a $G$-invariant window $\Delta$ and strings $x, y$ on $\Omega$, $\mathrm{Iso}^\Delta_G(x, y) = \{ g \in G : x(d) = y(g(d)) \ \forall d \in \Delta \}$. The routine returns $(A, \tau)$ with $\mathrm{Iso}^\Delta_G(x, y) = A\tau$, or none when the set is empty. The Schreier-Sims structure returns generators of the same group as its input, since every input generator is either kept or sifts to a product of transversal elements.

**Lemma 1 (cosets).** If $\tau \in \mathrm{Iso}^\Delta_G(x, y)$, then $\mathrm{Iso}^\Delta_G(x, y) = A\tau$ with $A = \mathrm{Iso}^\Delta_G(x, x)$, a subgroup.

*Proof.* $A$ is a subgroup because $\Delta$ is $G$-invariant. For $a \in A$, $y(\tau(a(d))) = x(a(d)) = x(d)$. For $g$ in the set, $a = g\tau^{-1}$ satisfies $x(a(d)) = y(\tau(a(d))) = y(g(d)) = x(d)$. $\square$

**Lemma 2 (shift).** For $H \le \mathrm{Sym}(\Omega)$ keeping $\Delta$ and any $t$: the elements $ht$ with $x(d) = y((ht)(d))$ on $\Delta$ are exactly $\mathrm{Iso}^\Delta_H(x, y \circ t)\,t$, because $y((ht)(d)) = (y \circ t)(h(d))$. $\square$

**Lemma 3 (L2, chain rule).** If $O_1, \ldots, O_r$ are the $G$-orbits on $\Delta$, then after handling $O_1, \ldots, O_i$ the pair $(A, \tau)$ satisfies $A\tau = \mathrm{Iso}^{O_1 \cup \cdots \cup O_i}_G(x, y)$.

*Proof.* Induction on $i$, starting from $A\tau = G$. Each $O_{i+1}$ is invariant under $A \le G$, and by Lemma 2 the elements of $A\tau$ that also satisfy the condition on $O_{i+1}$ form $\mathrm{Iso}^{O_{i+1}}_A(x, y \circ \tau)\,\tau$; the recursive call returns it as $A'g$, and the new pair is $(A', g\tau)$. $\square$

**Lemma 4 (L3 to L7, cosets of the kernel).** Let $G$ be transitive on $\Delta$ with $|\Delta| \ge 2$, $\mathcal B$ a block system with at least two blocks, $N$ the kernel of the action on $\mathcal B$, and $T$ a transversal. Then $\mathrm{Iso}^\Delta_G(x, y) = \bigcup_{t \in T} \mathrm{Iso}^\Delta_N(x, y \circ t)\,t$, and when this is not empty it equals $\langle A, \tau_t \tau_1^{-1} \rangle \tau_1$.

*Proof.* The Schreier generators $t s \,\overline{ts}^{-1}$ generate $N$ by Schreier's lemma. Every block is $N$-invariant, so $\Delta$ is. The union is Lemma 2 applied to $G = \bigcup_t Nt$. Every nonempty term is $A g_t t$ with the same $A = \mathrm{Aut}^\Delta_N(x)$ by Lemma 1. With $K = \mathrm{Aut}^\Delta_G(x)$, the union is $K\tau_1$ by Lemma 1; $A \le K$ and $\tau_t\tau_1^{-1} \in K$; and each $k \in K$ has $k\tau_1 \in A\tau_t$ for some $t$, so $k \in A\tau_t\tau_1^{-1}$. $\square$

The giant test in L4 only computes an order and updates a counter, so it does not change the result.

**Theorem 1 (string isomorphism).** STRING-ISO returns $\mathrm{Iso}^\Delta_G(x, y)$ as a coset, or none if it is empty.

*Proof.* Induction on $(|\Delta|, s)$ in lexicographic order, with $s = 1$ when $G$ is transitive on $\Delta$. Calls in L2 are on proper orbits, which are smaller. The calls in L6 keep $\Delta$, but $N$ keeps each of at least two blocks, so it is intransitive and $s$ drops. The base case $\Delta = \{d\}$ holds because $G$ fixes $d$. The other cases are Lemmas 3 and 4. $\square$

**Lemma 5 (joint color refinement).** If $\varphi$ is an isomorphism from $(X, c_1)$ to $(Y, c_2)$, then after every round of refinement on the disjoint union, with shared color names, $\varphi$ maps each vertex to a vertex of the same color. So the color counts of the two graphs agree in every round.

*Proof.* Induction on rounds. A vertex's new color is its old color with the multiset of its neighbors' old colors, and $\varphi$ maps neighbors bijectively to neighbors with the same old colors. $\square$

So when the counts differ the graphs are not isomorphic, and otherwise the isomorphisms are exactly the isomorphisms that keep the refined colors. Refinement stops, because each round that does not end it adds a color, and there are at most $2n$ colors.

**Theorem 2 (graph isomorphism).** GRAPH-ISOMORPHISM returns an isomorphism and $|\mathrm{Aut}(X, c_1)|$ when $X \cong Y$, and none otherwise.

*Proof.* After renaming $Y$ so that each refined color class sits on the same vertices as in $X$, an isomorphism is a permutation in $G = \prod_c \mathrm{Sym}(\text{class } c)$ that maps the edge set of $X$ onto that of the renamed $Y$. On the window of vertex pairs, with $x$ and $y$ marking edges, these are exactly the elements of $\mathrm{Iso}_G(x, y)$; composing with the inverse renaming gives an isomorphism to $Y$. $A = \mathrm{Aut}_G(x)$ is the group of automorphisms that keep the refined colors, which by Lemma 5 is the whole automorphism group of $(X, c_1)$, and $G$ acts faithfully on the vertices, so $|A|$ is the answer. $\square$

**Termination.** The measure $(|\Delta|, s)$ decreases at every recursive call; loops run over finite orbits, transversals and generator lists; color refinement adds a color per round; and Schreier-Sims enlarges a basic orbit or the base with every new strong generator. $\blacksquare$

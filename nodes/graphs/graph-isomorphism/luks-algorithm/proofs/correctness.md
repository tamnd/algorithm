---
title: Luks's divide and conquer computes the set of string isomorphisms
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a permutation group on $\Omega = \{0, \ldots, n-1\}$, given by generators; permutations are applied left to right, so $(gh)(d) = h(g(d))$. For a $G$-invariant window $\Delta \subseteq \Omega$ and strings $x, y : \Omega \to$ colors, let
$$\mathrm{Iso}^\Delta_G(x, y) = \{ g \in G : x(d) = y(g(d)) \text{ for all } d \in \Delta \}.$$
The routine returns a pair $(A, \tau)$ with $\mathrm{Iso}^\Delta_G(x, y) = A\tau = \{a\tau : a \in A\}$, or none when the set is empty. $\mathrm{Group}$ is the Schreier-Sims algorithm; we use only that its strong generators generate the same group as its input, which holds because every input generator either becomes a strong generator or sifts to the identity, that is, is a product of transversal elements, which are products of strong generators.

**Lemma 1 (cosets).** If $\mathrm{Iso}^\Delta_G(x, y)$ contains $\tau$, it equals $\mathrm{Aut}^\Delta_G(x)\,\tau$, where $\mathrm{Aut}^\Delta_G(x) = \mathrm{Iso}^\Delta_G(x, x)$ is a subgroup of $G$.

*Proof.* $\mathrm{Aut}^\Delta_G(x)$ contains the identity and is closed under products and inverses, since $\Delta$ is $G$-invariant. If $a \in \mathrm{Aut}$ then $y((a\tau)(d)) = y(\tau(a(d))) = x(a(d)) = x(d)$. Conversely, if $g$ and $\tau$ are both in Iso, then for $a = g\tau^{-1}$ and $d \in \Delta$: $x(a(d)) = y(\tau(a(d))) = y(g(d)) = x(d)$, so $g = a\tau$ with $a \in \mathrm{Aut}$. $\square$

**Lemma 2 (shift).** For $t \in \mathrm{Sym}(\Omega)$ and a subgroup $H$ with $\Delta$ invariant under $H$: $\{ ht : h \in H,\ x(d) = y((ht)(d)) \ \forall d \in \Delta \} = \mathrm{Iso}^\Delta_H(x, y \circ t)\, t$.

*Proof.* $y((ht)(d)) = y(t(h(d))) = (y \circ t)(h(d))$. $\square$

**Lemma 3 (chain rule, L2 to L5).** Let $\Delta = O_1 \cup \cdots \cup O_r$ be the $G$-orbits. After the $i$-th pass of L4, $A\tau = \mathrm{Iso}^{O_1 \cup \cdots \cup O_i}_G(x, y)$.

*Proof.* By induction on $i$; for $i = 0$, $A\tau = G$. The orbit $O_{i+1}$ is $G$-invariant, hence $A$-invariant. The elements of $A\tau$ that also satisfy the condition on $O_{i+1}$ are, by Lemma 2, $\mathrm{Iso}^{O_{i+1}}_A(x, y \circ \tau)\,\tau$. By induction on the size of the window (see termination) the recursive call returns this set as $A' g$, or none; the new coset is $A'(g\tau)$, which is what L4 stores. If the call returns none, the whole set is empty. $\square$

**Lemma 4 (transitive case, L6 to L9).** Let $G$ be transitive on $\Delta$, $|\Delta| \ge 2$, $\mathcal B$ a block system with at least two blocks, $N$ the kernel of the action on $\mathcal B$, and $T$ a transversal of $N$ in $G$. Then $\mathrm{Iso}^\Delta_G(x, y) = \bigcup_{t \in T} \mathrm{Iso}^\Delta_N(x, y \circ t)\, t$, and if it is not empty it equals $\langle A, \tau_i\tau_1^{-1} \rangle \tau_1$, where $\tau_i = g_i t_i$ are the elements found in L7 and $A = \mathrm{Aut}^\Delta_N(x)$.

*Proof.* The generators of $N$ come from Schreier's lemma: for the transversal $T$ indexed by the image in $\mathrm{Sym}(\mathcal B)$, the elements $t s \,\overline{ts}^{-1}$ for $t \in T$ and generators $s$ generate the kernel. Each block is $N$-invariant, so $\Delta$ is $N$-invariant and the recursive calls are allowed. $G = \bigcup_t Nt$, and Lemma 2 gives the union. Each nonempty term is $A g_t t$ by Lemma 1, with the same $A$ in every term. Let $K = \mathrm{Aut}^\Delta_G(x)$; by Lemma 1 the union is $K\tau_1$. Each $\tau_i\tau_1^{-1}$ lies in $K$ (it maps $x$ to $y$ and back), and $A \le K$, so $\langle A, \tau_i\tau_1^{-1} \rangle \le K$. Conversely, for $k \in K$, $k\tau_1$ lies in some term $A\tau_i$, so $k \in A\tau_i\tau_1^{-1}$. $\square$

**Base case (L1).** If $\Delta = \{d\}$, every $g \in G$ fixes $d$, so the set is $G$ when $x(d) = y(d)$ and empty otherwise.

**Theorem.** STRING-ISO returns $\mathrm{Iso}^\Delta_G(x, y)$ as a coset $A\tau$ with $A = \mathrm{Aut}^\Delta_G(x)$, or none when it is empty.

*Proof.* By induction on the measure $\mu = (|\Delta|, s)$ in lexicographic order, where $s = 1$ if $G$ is transitive on $\Delta$ and $0$ otherwise. Calls in L4 are on orbits of size less than $|\Delta|$, since there are at least two orbits. Calls in L7 have the same $\Delta$, but $N$ fixes every one of at least two blocks, so it is intransitive and $s$ drops from 1 to 0. The cases are covered by the base case and Lemmas 3 and 4. $\square$

**Graph isomorphism.** In COLORED-GRAPH-ISOMORPHISM, $G$ is the product of the symmetric groups on the color classes, acting on vertices and on unordered pairs of vertices, and $x, y$ mark the edges of the two graphs on the window of pairs. A vertex permutation $p$ that keeps colors lies in $\mathrm{Iso}$ exactly when $\{u, v\}$ is an edge of the first graph iff $\{p(u), p(v)\}$ is an edge of the second, that is, when it is an isomorphism. The group acts faithfully on vertices, so $|A|$ is the number of color-preserving automorphisms.

**Termination.** The measure $\mu$ decreases at every recursive call and takes finitely many values. Each loop is over a finite list: orbits, a finite transversal built by breadth-first search over a finite group, and Schreier-Sims, which adds strong generators only when they enlarge a basic orbit or the base, at most finitely often. $\blacksquare$

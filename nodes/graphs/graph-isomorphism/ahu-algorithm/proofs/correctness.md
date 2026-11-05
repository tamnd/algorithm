---
title: AHU-ISOMORPHIC decides rooted tree isomorphism
proves: [correctness, termination]
status: full
---

**Notation.** For a vertex $v$ of $T_1$ or $T_2$, $T(v)$ is the subtree of $v$, rooted at $v$: $v$ and all its descendants. Write $T(u) \cong T(v)$ when there is a bijection from the vertices of $T(u)$ onto those of $T(v)$ that maps $u$ to $v$ and edges to edges (a rooted isomorphism). Let $h = h(T_1) = h(T_2)$ after line L3. A rooted isomorphism maps the root to the root and keeps distances to the root, so it maps each level onto the level of the same number.

**Lemma 1 (children).** For vertices $u, v$, $T(u) \cong T(v)$ if and only if there is a bijection $\beta$ from the children of $u$ to the children of $v$ with $T(c) \cong T(\beta(c))$ for each child $c$.

*Proof.* If $\varphi : T(u) \to T(v)$ is a rooted isomorphism, then $\varphi(u) = v$, and $\varphi$ maps the neighbors of $u$ in $T(u)$, which are its children, bijectively onto the children of $v$. For a child $c$, $\varphi$ maps $T(c)$, the part of $T(u)$ reached from $c$ without passing $u$, onto the part of $T(v)$ reached from $\varphi(c)$ without passing $v$, which is $T(\varphi(c))$. So $\beta = \varphi$ restricted to the children works. Conversely, given $\beta$ and rooted isomorphisms $\varphi_c : T(c) \to T(\beta(c))$, the map that sends $u$ to $v$ and agrees with $\varphi_c$ on each $T(c)$ is a bijection, because the subtrees of the children partition $T(u) \setminus \{u\}$ and $T(v) \setminus \{v\}$. It maps the edges $\{u, c\}$ to $\{v, \beta(c)\}$ and the edges inside each $T(c)$ by $\varphi_c$; these are all the edges. $\square$

**Lemma 2 (invariant).** After line L7 has run for level $i$, for all vertices $u, v$ of level $i$ (each in $T_1$ or in $T_2$): $\mathrm{code}(u) = \mathrm{code}(v) \iff T(u) \cong T(v)$.

*Proof.* By induction on $h - i$.

*Base, $i = h$.* All vertices of level $h$ are leaves, so all keys are the empty list and all codes are 0. Every subtree is a single vertex, and any two single vertices are isomorphic.

*Step.* Assume the claim for level $i + 1$, and let $u, v$ be at level $i$. The children of $u$ and $v$ are at level $i + 1$. By line L7, $\mathrm{code}(u) = \mathrm{code}(v)$ if and only if $\mathrm{key}(u) = \mathrm{key}(v)$, because the rank in a list without copies is injective on its entries. The key is the sorted list of the children's codes, so $\mathrm{key}(u) = \mathrm{key}(v)$ if and only if the multisets of children's codes are equal, that is, if and only if there is a bijection $\beta$ between the children with $\mathrm{code}(c) = \mathrm{code}(\beta(c))$ for each $c$. By the induction hypothesis, this is a bijection with $T(c) \cong T(\beta(c))$. By Lemma 1, such a $\beta$ exists if and only if $T(u) \cong T(v)$. $\square$

**Theorem.** AHU-ISOMORPHIC$(T_1, r_1, T_2, r_2)$ terminates and returns true if and only if $T_1 \cong T_2$ by a map with $r_1 \mapsto r_2$.

*Proof.* Termination: the loop of line L4 runs $h + 1$ times, and each step works on finite lists.

*If the trees are isomorphic.* Let $\varphi$ be a rooted isomorphism. It is a bijection, so line L1 passes. It keeps levels, so both trees have the same height and line L3 passes. For each level $i$, $\varphi$ maps $L_i(T_1)$ bijectively onto $L_i(T_2)$, and its restriction to $T(v)$ is a rooted isomorphism onto $T(\varphi(v))$. By Lemma 2, $\mathrm{code}(v) = \mathrm{code}(\varphi(v))$. So the multisets of codes of $L_i(T_1)$ and $L_i(T_2)$ are equal, line L8 never returns false, and line L9 returns true.

*If the algorithm returns true.* Then line L8 passed at level 0. Level 0 holds only $r_1$ in $T_1$ and only $r_2$ in $T_2$, so $\mathrm{code}(r_1) = \mathrm{code}(r_2)$. By Lemma 2, $T(r_1) \cong T(r_2)$, and $T(r_1) = T_1$, $T(r_2) = T_2$.

So a return of false at lines L1, L3 or L8 happens only when no rooted isomorphism exists, and a return of true happens only when one exists. $\blacksquare$

**Free trees.** Every isomorphism $\psi : T_1 \to T_2$ of free trees maps the set of centers onto the set of centers, because it keeps eccentricities. If $c$ is a center of $T_1$, then $\psi$ is a rooted isomorphism from $(T_1, c)$ to $(T_2, \psi(c))$, and $\psi(c)$ is a center of $T_2$. So trying $T_1$ rooted at one center against $T_2$ rooted at each center of $T_2$ finds an isomorphism when one exists. Conversely, a rooted isomorphism is in particular an isomorphism of the free trees.

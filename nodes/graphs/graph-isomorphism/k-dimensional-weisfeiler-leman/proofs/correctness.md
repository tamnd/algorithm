---
title: k-WL terminates, and a difference in its colors proves non-isomorphism
proves: [correctness, termination]
status: full
---

**Setting.** $G$ is a simple undirected graph on $V = \{0, \ldots, n-1\}$ with a vertex coloring, and $k \ge 2$. For a $k$-tuple $t$ and $w \in V$, $t[i/w]$ is $t$ with entry $i$ replaced by $w$. The colorings $\chi_0, \chi_1, \ldots$ of $V^k$ are: $\chi_0(t)$ is the atomic type of $t$, and $\chi_{r+1}(t)$ is the rank, in the sorted list of all signatures, of
$$\sigma_r(t) = \Big(\chi_r(t),\ \{\!\{ (\chi_r(t[1/w]), \ldots, \chi_r(t[k/w])) : w \in V \}\!\}\Big).$$
When two graphs are compared, the ranks are taken in the sorted list of the signatures of both graphs together.

**Lemma 1 (refinement).** For every $r$, $\chi_{r+1}(t) = \chi_{r+1}(u)$ implies $\chi_r(t) = \chi_r(u)$.

*Proof.* Equal ranks mean equal signatures, and the signature starts with $\chi_r$. $\square$

**Lemma 2 (stability).** If $\chi_{r+1}$ has as many classes as $\chi_r$, then $\chi_{r+1}$ and $\chi_r$ induce the same partition of $V^k$, and so do all later colorings.

*Proof.* By Lemma 1 every class of $\chi_{r+1}$ lies inside a class of $\chi_r$. With the same number of classes, each class of $\chi_r$ is exactly one class of $\chi_{r+1}$, so the partitions are equal. Then $\sigma_{r+1}(t) = \sigma_{r+1}(u)$ iff $\sigma_r(t) = \sigma_r(u)$, because $\sigma_{r+1}$ is $\sigma_r$ with every color renamed by the same bijection; hence $\chi_{r+2}$ induces the same partition again, and by induction all later ones. $\square$

**Lemma 3 (termination).** The loop L2 to L5 ends after at most $n^k$ rounds.

*Proof.* By Lemmas 1 and 2, every round that does not stop strictly increases the number of classes, which is at most $|V^k| = n^k$. $\square$

**Lemma 4 (invariance).** Let $\gamma : V(G) \to V(H)$ be an isomorphism of colored graphs, and run the joint refinement. Then $\chi^H_r(\gamma(t)) = \chi^G_r(t)$ for all $r$ and all $t$, where $\gamma(t)$ applies $\gamma$ entrywise.

*Proof.* By induction on $r$. For $r = 0$, an isomorphism keeps colors, equalities and edges, so atomic types agree. For the step, $\gamma(t)[i/\gamma(w)] = \gamma(t[i/w])$, and $w \mapsto \gamma(w)$ is a bijection of $V(G)$ onto $V(H)$, so the multisets in $\sigma_r(t)$ and $\sigma_r(\gamma(t))$ are equal by the induction hypothesis, as are the first entries. The two signatures are equal, so they get the same rank in the shared sorted list. $\square$

**Theorem.** kwl_colors terminates and returns a stable coloring that refines the atomic types. kwl_distinguishes terminates, and if it returns true, the graphs are not isomorphic.

*Proof.* Termination of both functions is Lemma 3, applied to the joint coloring of the disjoint pair of tuple sets: the joint number of classes is at most $2 n^k$ and grows strictly in every round that does not stop. On stopping, Lemma 2 says the coloring is stable. If $G \cong H$ by $\gamma$, Lemma 4 shows that $t \mapsto \gamma(t)$ is a bijection of $V(G)^k$ onto $V(H)^k$ that keeps colors in every round, so the color histograms are equal in every round and the function never returns true. Also, once the joint partition is stable, the histograms do not change any more up to the same renaming of colors, so comparing them at the stopping round is enough. $\blacksquare$

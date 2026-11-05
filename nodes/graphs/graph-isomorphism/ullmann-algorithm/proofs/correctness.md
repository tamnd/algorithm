---
title: Ullmann's algorithm outputs every embedding exactly once
proves: [correctness, termination]
status: full
---

**Setting.** $G_1 = (V_1, E_1)$ with $V_1 = \{0, \ldots, k-1\}$ is the pattern and $G_2 = (V_2, E_2)$ with $|V_2| = n$ the host, both simple and undirected, with labels $\ell_1, \ell_2$. An *embedding* is an injective $f : V_1 \to V_2$ with $\ell_2(f(a)) = \ell_1(a)$ for all $a$ and $\{a, b\} \in E_1 \implies \{f(a), f(b)\} \in E_2$; in the induced mode also the converse. A matrix $M$ *admits* $f$ when $M[r][f(r)] = 1$ for every row $r$.

**Lemma 1 (L1 admits every embedding).** The initial matrix admits every embedding.

*Proof.* An embedding keeps labels, and it maps the $\deg_1(a)$ neighbors of $a$ injectively to neighbors of $f(a)$, so $\deg_1(a) \le \deg_2(f(a))$. $\square$

**Lemma 2 (REFINE keeps admitted embeddings and terminates).** If $M$ admits $f$, then after REFINE($M$) the matrix still admits $f$. REFINE stops after at most $kn + 1$ passes.

*Proof.* Consider the first entry $M[i][j]$ cleared by L10 at a moment when the current matrix admits $f$, and suppose $j = f(i)$. L10 found a neighbor $x$ of $i$ with $M[x][y] = 0$ for all $y \in N_2(j)$. But $f(x) \in N_2(f(i)) = N_2(j)$ since $f$ is an embedding, and $M[x][f(x)] = 1$ because the matrix admits $f$. Contradiction; so no entry $M[i][f(i)]$ is ever cleared. Every pass that does not stop clears at least one of at most $kn$ entries, and entries are never set back to 1, so there are at most $kn$ changing passes and one final pass. $\square$

**Lemma 3 (L5 keeps the embeddings of the branch).** Let $M$ admit $f$ and let $f(i) = j$. Then the matrix $M'$ of L5 admits $f$.

*Proof.* Row $i$ of $M'$ has its 1 at $j = f(i)$. In a row $r > i$, only column $j$ is cleared, and $f(r) \ne j$ because $f$ is injective. Rows above $i$ are unchanged. $\square$

**Lemma 4 (the rows above the current one are fixed and distinct).** At a node of the search at row $i$, with matrix $M$, every row $r < i$ has exactly one 1, in a column $c_r$, and the $c_r$ are pairwise distinct.

*Proof.* By induction on $i$. For $i = 0$ there is nothing to show. Going from row $i$ to row $i + 1$, L5 sets row $i$ to a single 1 at $c_i = j$ and clears column $j$ in all rows below $i$, so no later row can hold $j$. REFINE only clears entries, and L6 discards the matrix when a row becomes empty, so the single 1 of each fixed row survives. Earlier fixed columns $c_r$, $r < i$, were cleared from row $i$ before $j$ was chosen, so $j \ne c_r$. $\square$

**Theorem.** The search terminates and outputs exactly the embeddings of $G_1$ into $G_2$, each once.

*Proof.* *Termination.* Each node at row $i$ has at most $n$ children, all at row $i + 1$, and REFINE terminates by Lemma 2, so the search tree is finite and depth-first search visits it once.

*Soundness.* An output happens at row $k - 1$ after REFINE succeeded. By Lemma 4 applied with $i = k$ (the row $k - 1$ is fixed in L5 in the same way), every row has exactly one 1, in distinct columns, so $f(r) = c_r$ is injective. L1 and the fact that entries are only cleared give equal labels. L7 checks every edge of $G_1$, and in the induced mode every non-edge, before it outputs. So every output is an embedding.

*Completeness.* Let $f$ be an embedding. By Lemmas 1 and 2 the root matrix admits $f$, so no row is empty and the search starts. Suppose the search reaches a node at row $i$ whose matrix $M$ admits $f$ and whose fixed columns are $c_r = f(r)$ for $r < i$. Then $M[i][f(i)] = 1$, so L4 tries $j = f(i)$. By Lemmas 3 and 2 the refined $M'$ admits $f$, so no row is empty and L6 does not reject. If $i < k - 1$, the search goes on at row $i + 1$ with the same two properties. If $i = k - 1$, the single 1 of each row $r$ is at $f(r)$, and the edge check of L7 passes because $f$ is an embedding, so $f$ is output.

*Uniqueness.* Two different leaves differ at the first row where their paths choose different columns, so they output different maps. $\blacksquare$

---
title: The Ncut relaxation is a lower bound and the sweep cut is within the Cheeger bound
proves: [correctness]
status: full
---

We use the pseudocode of the page. $W$ is symmetric with $w_{ij} \ge 0$, $w_{ii} = 0$ and each degree $d_i = \sum_j w_{ij} > 0$. $D = \mathrm{diag}(d_i)$, $L = D - W$, $V = \{1, \ldots, n\}$ and $\mathrm{vol}(V) = \sum_i d_i$. Recall $y^T L y = \sum_{i<j} w_{ij}(y_i - y_j)^2$ for each real $y$ (see the [Laplacian matrix](/laplacian-matrix/) page), so $L$ is positive semidefinite.

**Lemma 1 (Ncut as a Rayleigh quotient).** Let $(A, B)$ be a bipartition with both sides non-empty, $b = \mathrm{vol}(A)/\mathrm{vol}(B)$, and $y_i = 1$ on $A$, $y_i = -b$ on $B$. Then $y^T D \mathbb{1} = 0$ and $y^T L y / y^T D y = \mathrm{Ncut}(A, B)$.

*Proof.* $y^T D \mathbb{1} = \sum_i d_i y_i = \mathrm{vol}(A) - b\,\mathrm{vol}(B) = 0$. In $\sum_{i<j} w_{ij}(y_i - y_j)^2$ a pair inside one side gives 0, and a pair across gives $w_{ij}(1 + b)^2$. So $y^T L y = (1 + b)^2 \mathrm{cut}(A, B)$. Next, $y^T D y = \mathrm{vol}(A) + b^2 \mathrm{vol}(B) = \mathrm{vol}(A) + b\,\mathrm{vol}(A) = (1 + b)\,\mathrm{vol}(A)$. The quotient is

$$\frac{(1 + b)\,\mathrm{cut}(A, B)}{\mathrm{vol}(A)} = \frac{\mathrm{cut}(A, B)}{\mathrm{vol}(A)} + \frac{b\,\mathrm{cut}(A, B)}{\mathrm{vol}(A)} = \frac{\mathrm{cut}(A, B)}{\mathrm{vol}(A)} + \frac{\mathrm{cut}(A, B)}{\mathrm{vol}(B)}. \qquad \square$$

The same computation with $f_i = |B|$ on $A$ and $f_i = -|A|$ on $B$ gives $f^T L f = n^2 \mathrm{cut}(A, B)$ and $f^T f = |A||B|^2 + |B||A|^2 = n|A||B|$, so $f^T L f / f^T f = n\,\mathrm{cut}(A, B)/(|A||B|) = \mathrm{RatioCut}(A, B)$, and $\sum_i f_i = 0$.

**Lemma 2 (the relaxation).** Let $M = D^{-1/2} L D^{-1/2}$ have the eigenvalues $0 = \lambda_1 \le \lambda_2 \le \cdots \le \lambda_n$, and let $v$ be a unit eigenvector of $\lambda_2$ that is orthogonal to $D^{1/2}\mathbb{1}$. Then $y = D^{-1/2} v$ satisfies $L y = \lambda_2 D y$ and $y^T D \mathbb{1} = 0$, and

$$\lambda_2 = \min \left\{ \frac{y^T L y}{y^T D y} : y \ne 0,\ y^T D \mathbb{1} = 0 \right\}.$$

*Proof.* $M (D^{1/2}\mathbb{1}) = D^{-1/2} L \mathbb{1} = 0$, and $M$ is positive semidefinite, so $D^{1/2}\mathbb{1}$ is an eigenvector of the least eigenvalue $\lambda_1 = 0$. Put $g = D^{1/2} y$. Then $y^T L y = g^T M g$, $y^T D y = g^T g$, and $y^T D \mathbb{1} = g^T D^{1/2}\mathbb{1}$. So the minimum is the least Rayleigh quotient of $M$ over the vectors orthogonal to an eigenvector of $\lambda_1$. By the [Courant-Fischer theorem](/courant-fischer-theorem/) (expand $g$ in an orthonormal eigenbasis that contains $D^{1/2}\mathbb{1}/\lVert D^{1/2}\mathbb{1} \rVert$), this minimum is $\lambda_2$, attained at $g = v$. Finally $L y = D^{1/2} M v = \lambda_2 D^{1/2} v = \lambda_2 D y$, and $y^T D \mathbb{1} = v^T D^{1/2}\mathbb{1} = 0$. $\square$

If $\lambda_2 > \lambda_1$, each eigenvector of $\lambda_2$ is orthogonal to $D^{1/2}\mathbb{1}$. If $\lambda_2 = 0$ the graph is not connected, and line L8 handles that case before line L9 is called.

**Lemma 3 (the sweep).** Lines L5 to L7 return a bipartition with both sides non-empty and with the least Ncut among the $n - 1$ sets $A_s$. The incremental update of the code computes each value exactly.

*Proof.* $1 \le s \le n - 1$, so $A_s$ and $V \setminus A_s$ are non-empty. When vertex $u$ moves from $B$ to $A$, the edges from $u$ to $B \setminus \{u\}$ start to cross and the edges from $u$ to $A$ stop crossing; all other pairs keep their status. So the new cut is the old cut plus $\sum_{j \in B \setminus \{u\}} w_{uj}$ minus $\sum_{j \in A} w_{uj}$, and the new $\mathrm{vol}(A)$ is the old one plus $d_u$, with $\mathrm{vol}(B) = \mathrm{vol}(V) - \mathrm{vol}(A)$. By induction on $s$, the code holds the exact cut and volume of $A_s$, so it compares the true values. $\square$

**Theorem 1 (lower bound).** Let OPT be the least Ncut over all bipartitions. The output $(A, B)$ of NCUT-BIPARTITION satisfies $\lambda_2 \le \mathrm{OPT} \le \mathrm{Ncut}(A, B)$.

*Proof.* Let $(A^*, B^*)$ be optimal. By Lemma 1 its vector $y^*$ is feasible for the minimum of Lemma 2 and has quotient OPT, so $\lambda_2 \le \mathrm{OPT}$. The output is a bipartition by Lemma 3, so its Ncut is at least OPT. $\square$

**Theorem 2 (upper bound).** The output satisfies $\mathrm{Ncut}(A, B) \le 2\sqrt{2\lambda_2} \le 2\sqrt{2\,\mathrm{OPT}}$.

*Proof.* Let $P = D^{-1} W$, the random walk on the graph. It is reversible with the stationary distribution $\pi_i = d_i/\mathrm{vol}(V)$, and its flow is $Q(i, j) = \pi_i P(i, j) = w_{ij}/\mathrm{vol}(V)$. From $L y = \lambda_2 D y$ we get $P y = (1 - \lambda_2) y$, and by Lemma 2 (the eigenvalues of $P$ are $1 - \lambda_i$) $1 - \lambda_2$ is the second largest eigenvalue of $P$. So $\gamma = \lambda_2$ is the spectral gap of $P$, and $y$ is an eigenfunction $f_2$ of the [Cheeger inequality](/cheeger-inequality/) proof. That proof (its remark on spectral partitioning) shows: after a change of sign of $y$ if needed, some set $S = \{i : y_i > t\}$ with $t \ge 0$, $S \ne \emptyset$ and $\pi(S) \le 1/2$ has conductance

$$\Phi(S) = \frac{Q(S, V \setminus S)}{\pi(S)} = \frac{\mathrm{cut}(S, V \setminus S)}{\mathrm{vol}(S)} \le \sqrt{2\gamma} = \sqrt{2\lambda_2}.$$

$S$ is the set of the vertices above a threshold of $y$, so $S$ or its complement is one of the sets $A_s$ of line L6 ($y$ takes both signs because $y^T D \mathbb{1} = 0$ and $y \ne 0$, so $S$ is a proper subset). Ncut is symmetric in its two sides. Since $\mathrm{vol}(S) \le \mathrm{vol}(V \setminus S)$,

$$\mathrm{Ncut}(S, V \setminus S) \le \frac{2\,\mathrm{cut}(S, V \setminus S)}{\mathrm{vol}(S)} = 2\Phi(S) \le 2\sqrt{2\lambda_2}.$$

By Lemma 3 the output is at most this value, and $\lambda_2 \le \mathrm{OPT}$ by Theorem 1. $\square$

**Theorem 3 (the recursion).** RECURSIVE-NCUT stops after at most $n - 1$ refinements of a part, and its output is a partition of $V$ in which each part $S$ with $|S| \ge 2$ is connected and its best sweep cut has Ncut greater than $\tau$.

*Proof.* Invariant: the parts on the stack and the parts in the output are disjoint, non-empty and cover $V$. It holds at the start. Line L8 outputs a singleton, or replaces a disconnected $S$ by its components, which partition $S$ into at least 2 non-empty parts. Line L10 moves $S$ to the output. Line L11 replaces $S$ by $A$ and $B$, which are non-empty by Lemma 3. So the invariant holds after each step. Each replacement increases the number of parts by at least 1, and there are at most $n$ parts, so there are at most $n - 1$ replacements. Each other step moves a part to the output, and this happens at most $n$ times. So the loop stops, and at the end the output alone covers $V$. A part is output only by line L8 (a singleton) or line L10 (connected, after line L8, and failing the test). $\square$

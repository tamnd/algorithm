---
title: Correctness of Thiele continued-fraction interpolation
proves: [correctness, termination]
status: full
---

Notation: distinct nodes $x_0, \ldots, x_{n-1}$ with values $y_i$, listed in the order produced by the algorithm (line L2 only permutes nodes that have not yet been used as pivots, so it is enough to argue in the final order). Arithmetic is on $\mathbb{F} \cup \{\infty\}$ for a field $\mathbb{F}$ (the rationals in the exact implementation), with $c/0 = \infty$ for $c \ne 0$, $c/\infty = 0$, and $\infty - c = \infty$. The algorithm keeps $m \le n$ coefficients $b_0, \ldots, b_{m-1}$, all finite. Let $(A_{-1}, B_{-1}) = (1, 0)$, $(A_0, B_0) = (b_0, 1)$ and
$$(A_k, B_k) = b_k\,(A_{k-1}, B_{k-1}) + (t - x_{k-1})\,(A_{k-2}, B_{k-2}), \qquad 1 \le k \le m - 1,$$
which are polynomials in $t$. Say a pair $(a, b) \in \mathbb{F}^2$ **fits** $y$ when $a = y\, b$.

**Definitions.** For $1 \le k \le m$ and $w \in \mathbb{F} \cup \{\infty\}$ put
$$P_k(t; w) = w\,(A_{k-1}, B_{k-1}) + (t - x_{k-1})\,(A_{k-2}, B_{k-2}), \qquad P_k(t; \infty) = (A_{k-1}, B_{k-1}),$$
and $P_0(t; w) = (w, 1)$, $P_0(t; \infty) = (1, 0)$. Then $P_k(t; b_k) = (A_k, B_k)$ for $k \le m - 1$. The values $\varphi_k(x_i)$, $i \ge k$, are those held by the array after stage $k$ of line L2, with $b_k = \varphi_k(x_k)$.

**Lemma 1 (tail identity).** For $1 \le k \le m$, every $t$, and every $w \ne 0, \infty$, $P_k(t; w) = w\, P_{k-1}\big(t;\ b_{k-1} + (t - x_{k-1})/w\big)$. Also $P_k(t; 0) = (t - x_{k-1})\, P_{k-1}(t; \infty)$ and $P_k(t; \infty) = P_{k-1}(t; b_{k-1})$.

*Proof.* $P_{k-1}(t; v)$ is affine in $v$ with slope $(A_{k-2}, B_{k-2})$ (for $k = 1$: slope $(1, 0) = (A_{-1}, B_{-1})$), and $P_{k-1}(t; b_{k-1}) = (A_{k-1}, B_{k-1})$. Hence $w\, P_{k-1}(t; b_{k-1} + c/w) = w (A_{k-1}, B_{k-1}) + c\, (A_{k-2}, B_{k-2})$, which with $c = t - x_{k-1}$ is $P_k(t; w)$. The two other identities are the definitions read off, since $P_{k-1}(t; \infty) = (A_{k-2}, B_{k-2})$. $\square$

**Lemma 2 (invariant).** For $0 \le k \le m$ and every node $x_i$ with $i \ge k$ (when $k = m < n$, for every remaining node), the pair $P_k(x_i; \varphi_k(x_i))$ fits $y_i$.

*Proof.* Induction on $k$. For $k = 0$, $P_0(x_i; y_i) = (y_i, 1)$ fits $y_i$. Let $k \ge 1$ and $i \ge k$; by hypothesis $P_{k-1}(x_i; \varphi_{k-1}(x_i))$ fits $y_i$. Line L2 sets $\varphi_k(x_i)$ in one of three ways.
(a) $\varphi_{k-1}(x_i) = \infty$: then $\varphi_k(x_i) = 0$ and by Lemma 1, $P_k(x_i; 0) = (x_i - x_{k-1})\, P_{k-1}(x_i; \infty)$, a multiple of a fitting pair.
(b) $\varphi_{k-1}(x_i) = b_{k-1}$: then $\varphi_k(x_i) = \infty$ and $P_k(x_i; \infty) = P_{k-1}(x_i; b_{k-1})$ fits.
(c) Otherwise $w = \varphi_k(x_i) = (x_i - x_{k-1})/(\varphi_{k-1}(x_i) - b_{k-1})$ is finite and nonzero (the nodes are distinct), and $b_{k-1} + (x_i - x_{k-1})/w = \varphi_{k-1}(x_i)$. By Lemma 1, $P_k(x_i; w) = w\, P_{k-1}(x_i; \varphi_{k-1}(x_i))$, a multiple of a fitting pair.
A multiple of a fitting pair fits, which completes the step. $\square$

**Lemma 3 (earlier nodes are kept).** For $0 \le k \le m - 1$ and every $i \le k$, $(A_k(x_i), B_k(x_i))$ fits $y_i$.

*Proof.* Induction on $k$. For $i = k$ this is Lemma 2 with $w = \varphi_k(x_k) = b_k$. For $i = k - 1$, the second term of the recurrence vanishes at $t = x_{k-1}$, so $(A_k, B_k)(x_{k-1}) = b_k (A_{k-1}, B_{k-1})(x_{k-1})$, a multiple of a pair that fits by induction. For $i \le k - 2$ both $(A_{k-1}, B_{k-1})(x_i)$ and $(A_{k-2}, B_{k-2})(x_i)$ fit $y_i$ by induction, and the set of pairs fitting $y_i$ is a linear subspace. $\square$

**Lemma 4 (degrees and nondegeneracy).** $\deg A_k \le \lceil k/2 \rceil$, $\deg B_k \le \lfloor k/2 \rfloor$, and $A_k B_{k-1} - A_{k-1} B_k = (-1)^{k-1} \prod_{j=0}^{k-1} (t - x_j)$. In particular $B_{m-1} \not\equiv 0$.

*Proof.* The degree bounds follow from the recurrence by induction, since $t - x_{k-1}$ raises the degree of the pair two steps back by one. For the determinant, $A_k B_{k-1} - A_{k-1} B_k = (t - x_{k-1})(A_{k-2} B_{k-1} - A_{k-1} B_{k-2}) = -(t - x_{k-1})(A_{k-1} B_{k-2} - A_{k-2} B_{k-1})$, and at $k = 0$ the value is $A_0 B_{-1} - A_{-1} B_0 = -1$; induction gives the product formula. If $B_{m-1} \equiv 0$ with $m \ge 2$, Lemma 3 at $i = m - 1$ gives $A_{m-1}(x_{m-1}) = 0$, so the determinant vanishes at $x_{m-1}$, contradicting $\prod_{j < m-1} (x_{m-1} - x_j) \ne 0$; for $m = 1$, $B_0 = 1$. $\square$

**Theorem.** Let $(A, B) = (A_{m-1}, B_{m-1})$. Then $A$ and $B$ have degrees at most $\lceil (m-1)/2 \rceil$ and $\lfloor (m-1)/2 \rfloor$, $B \not\equiv 0$, and $A(x_i) = y_i B(x_i)$ for every node $x_0, \ldots, x_{n-1}$. Consequently THIELE returns $y_i$ at every node with $B(x_i) \ne 0$; at a node with $B(x_i) = 0$ also $A(x_i) = 0$ and the evaluation reports $0/0$ instead of a value. If the rational interpolation problem of type $(\lceil (n-1)/2 \rceil, \lfloor (n-1)/2 \rfloor)$ has a solution $p/q$, then $A/B = p/q$ as rational functions.

*Proof.* Nodes $x_0, \ldots, x_{m-1}$ are covered by Lemma 3 with $k = m - 1$. If $m < n$, the algorithm stopped because $\varphi_m(x_i) = \infty$ for every $i \ge m$, and Lemma 2 gives that $P_m(x_i; \infty) = (A_{m-1}, B_{m-1})(x_i)$ fits $y_i$. Degrees and $B \not\equiv 0$ are Lemma 4. For the last claim, $(A, B)$ and $(p, q)$ both solve the linearized problem, so $A q - p B$ has degree at most $n - 1$ (the degrees of the type add to $n - 1$, and $m \le n$) and vanishes at the $n$ nodes, where it equals $y_i B q - y_i q B = 0$. Hence $A q = p B$. $\square$

**Termination.** Line L2 runs at most $n - 1$ stages of at most $n$ inverse differences each, every one a constant number of field operations or $\infty$ rules, and line L4 runs $m - 1$ steps. The search for a finite value in stage $k$ scans at most $n - k$ entries. So the algorithm stops after $O(n^2)$ operations. $\square$

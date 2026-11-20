---
title: The 3-user 2x2 closed form aligns the interference at every receiver
proves: [correctness]
status: full
---

Three transmitter-receiver pairs have two antennas each. $H_{kj} \in \mathbb C^{2 \times 2}$ is the channel from transmitter $j$ to receiver $k$, and every cross channel $H_{kj}$, $j \ne k$, is invertible. Each transmitter sends one stream along a nonzero beam $v_j \in \mathbb C^2$, and receiver $k$ applies a unit vector $u_k$. Two nonzero vectors $a, b \in \mathbb C^2$ are parallel, $a \parallel b$, when $b = c\, a$ for some $c \in \mathbb C$, which holds exactly when $\det[a\ b] = a_1 b_2 - a_2 b_1 = 0$.

**Lemma 1 (orthogonal vector).** For nonzero $a \in \mathbb C^2$, $u = (-\bar a_2, \bar a_1)/\|a\|$ is a unit vector with $u^H a = 0$, and every $b \parallel a$ also has $u^H b = 0$.

*Proof.* $\|u\|^2 = (|a_2|^2 + |a_1|^2)/\|a\|^2 = 1$. $u^H a = (-a_2 a_1 + a_1 a_2)/\|a\| = 0$. If $b = c\, a$, then $u^H b = c\, u^H a = 0$. $\square$

**Lemma 2 (2x2 eigenvector).** For $E \in \mathbb C^{2 \times 2}$ and a root $\lambda$ of $\lambda^2 - \operatorname{tr}(E) \lambda + \det E = 0$, let $(r_1, r_2)$ be a nonzero row of $E - \lambda I$. Then $x = (-r_2, r_1)$ is a nonzero vector with $E x = \lambda x$. If both rows are zero, $E = \lambda I$ and every nonzero vector is an eigenvector.

*Proof.* $\lambda$ is an eigenvalue, so $\det(E - \lambda I) = 0$, and $E - \lambda I$ has rank at most $1$. If its rank is $1$, both rows are multiples of the nonzero row $r$, and its null space is the line of vectors orthogonal (in the bilinear sense) to $r$: $r_1 x_1 + r_2 x_2 = -r_1 r_2 + r_2 r_1 = 0$, so $x$ is in the null space of every row. If the rank is $0$, $E = \lambda I$. $\square$

The code picks the row with the larger entries, which is a nonzero row whenever $E \ne \lambda I$, and returns the vector scaled to unit length.

**Theorem (alignment).** Let $A = H_{12} H_{32}^{-1} H_{31}$ and $B = H_{13} H_{23}^{-1} H_{21}$, both invertible, and $E = B^{-1} A$. Let $v_1$ be an eigenvector of $E$ with eigenvalue $\lambda$, and put $v_2 = H_{32}^{-1} H_{31} v_1$, $v_3 = H_{23}^{-1} H_{21} v_1$. Then $v_2, v_3 \ne 0$, and

$$H_{31} v_1 \parallel H_{32} v_2, \qquad H_{21} v_1 \parallel H_{23} v_3, \qquad H_{12} v_2 \parallel H_{13} v_3.$$

With $u_k$ orthogonal to one interference vector at receiver $k$ as in Lemma 1, $u_k^H H_{kj} v_j = 0$ for both $j \ne k$.

*Proof.* $v_2$ and $v_3$ are images of $v_1 \ne 0$ under invertible matrices, so they are nonzero. $H_{32} v_2 = H_{31} v_1$ and $H_{23} v_3 = H_{21} v_1$ by construction, which gives the first two relations with $c = 1$. For the third, $H_{12} v_2 = H_{12} H_{32}^{-1} H_{31} v_1 = A v_1$ and $H_{13} v_3 = H_{13} H_{23}^{-1} H_{21} v_1 = B v_1$. From $B^{-1} A v_1 = \lambda v_1$ we get $A v_1 = \lambda B v_1$, so $H_{12} v_2 = \lambda H_{13} v_3$. Since $A$ is invertible and $v_1 \ne 0$, $\lambda \ne 0$, so the two vectors are nonzero multiples of each other. At each receiver, the two interference vectors are parallel and nonzero, so by Lemma 1 the vector $u_k$ built from either one is orthogonal to both. $\square$

**Wanted signal.** The wanted gain $u_k^H H_{kk} v_k$ is nonzero unless $H_{kk} v_k$ falls on the interference line at receiver $k$. The beams and filters do not depend on $H_{kk}$, so for direct channels drawn from any continuous law, independent of the cross channels, this happens with probability $0$: for fixed $u_k$ and $v_k$, the set of $H_{kk}$ with $u_k^H H_{kk} v_k = 0$ is a proper linear subspace of $\mathbb C^{2 \times 2}$. Then each receiver sees its stream with gain $g_k = |u_k^H H_{kk} v_k|^2 > 0$ and no interference, and with power $P$ per user and unit noise the sum rate is $\sum_k \log_2(1 + P g_k)$, which grows like $3 \log_2 P$: three degrees of freedom. The tests check this slope.

**The code.** Lines L1 to L4 of the page compute $E$, $v_1$, $v_2$ and $v_3$ as in the theorem; the code scales each beam to unit length, which keeps every parallel relation. Line L5 builds $u_k$ from the interferer $j = k + 1 \bmod 3$ by Lemma 1. In floating point the relations hold up to rounding, which the tests bound by $10^{-9}$ for random Gaussian channels.

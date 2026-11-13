---
title: On noiseless samples of p distinct exponentials, Prony's method returns the exact exponents and amplitudes
proves: [correctness]
status: full
---

The notation is that of the page. The samples are $x[t] = \sum_{j=1}^{p} h_j z_j^t$ for $t = 0, \dots, N-1$, with $N \ge 2p$, the $z_j$ distinct and nonzero, and every $h_j \ne 0$. Write $P(z) = \prod_{j=1}^{p}(z - z_j) = z^p + c_1 z^{p-1} + \dots + c_p$.

**Lemma 1 (the samples obey the recurrence of $P$).** For every $t$ with $p \le t \le N-1$, $x[t] + \sum_{i=1}^{p} c_i\, x[t-i] = 0$.

*Proof.* With $c_0 = 1$, $\sum_{i=0}^{p} c_i x[t-i] = \sum_j h_j z_j^{t-p} \sum_{i=0}^{p} c_i z_j^{p-i} = \sum_j h_j z_j^{t-p} P(z_j) = 0$. $\square$

**Lemma 2 (the system of line L1 has full column rank).** Let $M$ be the $(N-p) \times p$ matrix with entry $M_{t,i} = x[t-i]$ for rows $t = p, \dots, N-1$ and columns $i = 1, \dots, p$. Then $M$ has rank $p$.

*Proof.* $M_{t,i} = \sum_j z_j^{t-p}\, h_j\, z_j^{p-i}$, so $M = W D U$ with $W_{t,j} = z_j^{t-p}$ of size $(N-p) \times p$, $D = \operatorname{diag}(h_1, \dots, h_p)$ and $U_{j,i} = z_j^{p-i}$ of size $p \times p$. The first $p$ rows of $W$ form a Vandermonde matrix in the distinct $z_j$, which is nonsingular, and $N - p \ge p$, so $W$ has rank $p$. $D$ is nonsingular because every $h_j \ne 0$. $U$ is a Vandermonde matrix with its columns in reverse order, so it is nonsingular. A product of a rank-$p$ matrix with $p$ columns and two nonsingular $p \times p$ matrices has rank $p$. $\square$

**Lemma 3 (line L2 returns the coefficients of $P$).** The least-squares problem of line L2, minimize $\|M c + y\|^2$ with $y_t = x[t]$, has the unique solution $c = (c_1, \dots, c_p)$.

*Proof.* By Lemma 1 the vector of coefficients of $P$ gives residual zero, which is the smallest possible value. If $c'$ also gives zero, then $M(c - c') = 0$, and Lemma 2 gives $c = c'$. The normal equations $M^H M c = -M^H y$ have the same unique solution, since $M^H M$ is nonsingular when $M$ has full column rank. When $N = 2p$, $M$ is square and nonsingular and the solve is exact. $\square$

**Lemma 4 (lines L3 and L4).** The roots of line L3 are $z_1, \dots, z_p$, and the least-squares problem of line L4 has the unique solution $(h_1, \dots, h_p)$.

*Proof.* By Lemma 3 the polynomial of line L3 is $P$, whose roots are the $z_j$ by its definition. The matrix of line L4 is the $N \times p$ Vandermonde matrix $V_{t,j} = z_j^t$, which has rank $p$ because its first $p$ rows are nonsingular. The true amplitudes give residual zero, and full column rank makes the minimizer unique, as in Lemma 3. $\square$

**Theorem.** If $x$ consists of $N \ge 2p$ samples of a sum of $p$ exponentials with distinct nonzero $z_j$ and nonzero amplitudes, the algorithm returns $\{z_j\}$ and the matching amplitudes $h_j$. With exact arithmetic for lines L1, L2 and L4 and exact roots in line L3 the output is exact; in floating point, the error is that of the two linear solves and of the root finder.

*Proof.* Lemmas 3 and 4. The order of the roots returned by line L3 does not matter, because line L4 fits the amplitude of each root in the order given. $\blacksquare$

When some $h_j = 0$ or two $z_j$ coincide, the samples obey a recurrence of order less than $p$, $M$ loses rank, and the coefficients of line L2 are not unique. Then the method has to be run with the smaller order, or with a confluent model in which $t\,z^t$ terms appear for a double root.

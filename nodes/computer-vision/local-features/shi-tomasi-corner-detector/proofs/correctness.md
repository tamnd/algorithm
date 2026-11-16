---
title: Correctness of the Shi-Tomasi corner detector
proves: [correctness]
status: full
---

We prove three things: line L3 computes the smaller eigenvalue of $M$, which is the smallest value of the quadratic form over unit vectors; the algorithm returns the list defined in The problem; and the exact comparison of the implementation gives the sign of $(p_1 - \sqrt{n_1}) - (p_2 - \sqrt{n_2})$.

**Lemma 1 (the smaller eigenvalue).** Let $M = \begin{pmatrix} A & C \\ C & B \end{pmatrix}$ be real and symmetric, and let $\lambda = \frac{A + B}{2} - \sqrt{(\frac{A - B}{2})^2 + C^2}$. Then $\lambda$ is the smaller eigenvalue of $M$ and $\lambda = \min_{\|s\| = 1} s^{\mathsf T} M s$. If $M$ is a sum of matrices $w g g^{\mathsf T}$ with $w \ge 0$, then $\lambda \ge 0$.

*Proof.* The characteristic polynomial is $\mu^2 - (A + B)\mu + (AB - C^2)$. Its discriminant is $(A + B)^2 - 4(AB - C^2) = (A - B)^2 + 4C^2 \ge 0$, so both roots are real, and they are $\frac{A + B}{2} \pm \sqrt{(\frac{A - B}{2})^2 + C^2}$. The root with the minus sign is the smaller one, $\lambda$. Since $M$ is symmetric, it has an orthonormal basis of eigenvectors $e_1, e_2$ with eigenvalues $\lambda \le \lambda'$. A unit vector is $s = \alpha e_1 + \beta e_2$ with $\alpha^2 + \beta^2 = 1$, and $s^{\mathsf T} M s = \alpha^2 \lambda + \beta^2 \lambda' \ge \lambda$, with equality at $s = e_1$. For the last claim, $s^{\mathsf T} (w g g^{\mathsf T}) s = w (g \cdot s)^2 \ge 0$ for each term, so the minimum is at least $0$. $\square$

In the algorithm, $M = \sum w \, (X, Y)^{\mathsf T} (X, Y)$ with binomial weights $w > 0$, so the response of line L3 is the smaller eigenvalue of $M$ and is at least $0$.

**Lemma 2 (the candidates).** After line L6, $P$ holds exactly the pixels $p$ with $\lambda(p) > q \lambda_{\max}$ and $\lambda(p) \ge \lambda(p')$ for each of the eight neighbours $p'$ of $p$ inside the image, in order of decreasing $\lambda$, ties in order of $v$ and then $u$.

*Proof.* Line L4 sets $\lambda_{\max}$ to the largest response. Line L5 applies the two tests of the definition to each pixel, and line L6 sorts by the stated key. Since the key is a total order on the pixels (two pixels with equal response differ in $(v, u)$), the order is unique. $\square$

**Theorem (output).** SHI-TOMASI returns the list of The problem: the candidates in the order of Lemma 2, where a candidate is kept exactly when, at its turn, fewer than $N$ points are kept and it is at least $d$ from each kept point.

*Proof.* We prove by induction on $i$ that after the $i$-th pass of line L8, kept is the list defined for the first $i$ candidates. For $i = 0$ both are empty (line L7). At pass $i + 1$, line L9 tests the two conditions of the definition against the current kept list, which by the hypothesis is the defined list for the first $i$ candidates, and line L10 appends the candidate exactly when both hold. No line removes a point or changes the order. After the last candidate, line L11 returns the defined list. $\square$

**Lemma 3 (exact comparison).** For integers $a$, $b$ and $n \ge 0$, the function $\mathrm{sign}(a + b\sqrt{n})$ of the implementation is correct: if $b\sqrt{n} = 0$ the sign is the sign of $a$; if $a = 0$ or $a$ and $b$ have the same sign, the sign is the sign of $b$; otherwise the sign is the sign of $a$ when $a^2 > b^2 n$, the opposite sign when $a^2 < b^2 n$, and $0$ when they are equal.

*Proof.* The first two cases are clear, since a sum of two numbers of the same sign, or of a number and zero, has that sign. In the last case $a$ and $b\sqrt{n}$ are nonzero with opposite signs, so the sum has the sign of the term of larger absolute value, and $|a| > |b\sqrt{n}|$ exactly when $a^2 > b^2 n$. Equal absolute values give $0$. $\square$

**Lemma 4.** For integers $p_1$, $p_2$ and $n_1, n_2 \ge 0$, the function compare_roots returns the sign of $(p_1 - \sqrt{n_1}) - (p_2 - \sqrt{n_2})$.

*Proof.* Put $e = p_1 - p_2$ and $x = e + \sqrt{n_2}$. The difference is $x - \sqrt{n_1}$. If $x < 0$, which Lemma 3 decides as the sign of $e + 1 \cdot \sqrt{n_2}$, then $x - \sqrt{n_1} < 0$ since $\sqrt{n_1} \ge 0$, and the function returns $-1$. Otherwise $x \ge 0$ and $\sqrt{n_1} \ge 0$, and the map $t \mapsto t^2$ is strictly increasing on $[0, \infty)$, so $x - \sqrt{n_1}$ has the sign of $x^2 - n_1 = (e^2 + n_2 - n_1) + 2e\sqrt{n_2}$, which Lemma 3 decides. $\square$

The implementation stores $2\lambda = s - \sqrt{D}$ with $s = A + B$ and $D = (A - B)^2 + 4C^2$, which is twice the formula of Lemma 1. For $q = q_a / q_b$ with $q_a \ge 0$ and $q_b > 0$, the test $\lambda > q \lambda_{\max}$ is equivalent, after multiplication by $2 q_b > 0$, to $q_b s - \sqrt{q_b^2 D} > q_a s^{\ast} - \sqrt{q_a^2 D^{\ast}}$, where $(s^{\ast}, D^{\ast})$ is the pair of $\lambda_{\max}$; this is one call of compare_roots. Every comparison of responses in lines L4 to L6 is one call of compare_roots on the pairs, so by Lemma 4 each is exact. With Lemma 2 and the Theorem, the implementation returns the defined list. $\blacksquare$

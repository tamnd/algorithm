---
title: The Hamiltonian bisection and the level set iteration return an interval that holds the H-infinity norm
proves: [correctness]
status: full
---

Let $G(s) = C(sI - A)^{-1}B + D$ with $A \in \mathbb{R}^{n \times n}$, $B \in \mathbb{R}^{n \times m}$, $C \in \mathbb{R}^{p \times n}$ and $D \in \mathbb{R}^{p \times m}$, and let $\|G\|_\infty = \sup_{\omega \in \mathbb{R}} \sigma_{\max}(G(j\omega))$. The two procedures on the page assume that $A$ is Hurwitz, so $G$ has no pole in the closed right half plane and the norm is finite. All statements below hold in exact arithmetic. The last section says what changes in floating point.

For $\gamma > 0$ that is not a singular value of $D$, the matrix

$$M_\gamma = \begin{bmatrix} D & -\gamma I_p \\ -\gamma I_m & D^T \end{bmatrix}$$

is invertible (a vector $(u, v)$ in its kernel has $D u = \gamma v$ and $D^T v = \gamma u$, so it is zero unless $\gamma$ is a singular value of $D$). Define

$$H_\gamma = \begin{bmatrix} A & 0 \\ 0 & -A^T \end{bmatrix} + \begin{bmatrix} B & 0 \\ 0 & -C^T \end{bmatrix} M_\gamma^{-1} \begin{bmatrix} -C & 0 \\ 0 & -B^T \end{bmatrix}.$$

For $D = 0$ this is $H_\gamma = \begin{bmatrix} A & \gamma^{-1} B B^T \\ -\gamma^{-1} C^T C & -A^T \end{bmatrix}$.

## Lemma 1 (singular values and imaginary eigenvalues)

Assume that $A$ has no eigenvalue on the imaginary axis and that $\gamma > 0$ is not a singular value of $D$. Then for every real $\omega_0$, $\gamma$ is a singular value of $G(j\omega_0)$ if and only if $j\omega_0$ is an eigenvalue of $H_\gamma$.

*Proof.* Write $G^*$ for the conjugate transpose. Since $A$ is real, $G(j\omega_0)^* = B^T(-j\omega_0 I - A^T)^{-1} C^T + D^T$.

($\Rightarrow$) Let $\gamma$ be a singular value of $G(j\omega_0)$. Then there are vectors $u \in \mathbb{C}^m$ and $v \in \mathbb{C}^p$, not both zero, with $G(j\omega_0) u = \gamma v$ and $G(j\omega_0)^* v = \gamma u$. Put $x = (j\omega_0 I - A)^{-1} B u$ and $q = (-j\omega_0 I - A^T)^{-1} C^T v$. Both inverses exist because $A$ has no imaginary eigenvalue. Then

$$j\omega_0 x = A x + B u, \qquad j\omega_0 q = -A^T q - C^T v,$$

and the two singular value equations read $C x + D u - \gamma v = 0$ and $B^T q + D^T v - \gamma u = 0$, that is

$$M_\gamma \begin{bmatrix} u \\ v \end{bmatrix} = \begin{bmatrix} -C x \\ -B^T q \end{bmatrix}.$$

Solve this for $(u, v)$ and put it into the two differential equations. The result is $H_\gamma (x, q) = j\omega_0 (x, q)$. The vector $(x, q)$ is not zero: if $x = 0$ and $q = 0$, the last display gives $M_\gamma (u, v) = 0$, so $(u, v) = 0$, which is false. So $j\omega_0$ is an eigenvalue of $H_\gamma$.

($\Leftarrow$) Let $H_\gamma (x, q) = j\omega_0 (x, q)$ with $(x, q) \neq 0$. Define $(u, v) = M_\gamma^{-1}(-C x, -B^T q)$. The two block rows of the eigenvalue equation say $(j\omega_0 I - A) x = B u$ and $(-j\omega_0 I - A^T) q = C^T v$, so $x = (j\omega_0 I - A)^{-1} B u$ and $q = (-j\omega_0 I - A^T)^{-1} C^T v$. If $(u, v) = 0$ then $(x, q) = 0$, which is false. The definition of $(u, v)$ gives $C x + D u = \gamma v$ and $B^T q + D^T v = \gamma u$, that is $G(j\omega_0) u = \gamma v$ and $G(j\omega_0)^* v = \gamma u$. If $u = 0$, the first equation gives $v = 0$; so $u \neq 0$, and $G(j\omega_0)^* G(j\omega_0) u = \gamma^2 u$. So $\gamma$ is a singular value of $G(j\omega_0)$. $\square$

## Lemma 2 (the characteristic polynomial is even)

Under the hypotheses of Lemma 1, $\det(sI - H_\gamma) = r(s^2)$ for a real polynomial $r$ of degree $n$. Hence $j\omega_0$ is an eigenvalue of $H_\gamma$ if and only if $t = -\omega_0^2$ is a root of $r$, and the imaginary eigenvalues of $H_\gamma$ are exactly the numbers $\pm j\sqrt{-t}$ for the real roots $t \le 0$ of $r$.

*Proof.* Let $J = \begin{bmatrix} 0 & I_n \\ -I_n & 0 \end{bmatrix}$. We show that $J H_\gamma$ is symmetric. First, $J \begin{bmatrix} A & 0 \\ 0 & -A^T \end{bmatrix} = \begin{bmatrix} 0 & -A^T \\ -A & 0 \end{bmatrix}$ is symmetric. Next, write $L = \begin{bmatrix} B & 0 \\ 0 & -C^T \end{bmatrix}$ and $R = \begin{bmatrix} -C & 0 \\ 0 & -B^T \end{bmatrix}$. A direct product gives $J L = R^T P$ with the permutation $P = \begin{bmatrix} 0 & I_p \\ I_m & 0 \end{bmatrix}$, so $J L M_\gamma^{-1} R = R^T (P M_\gamma^{-1}) R$. Now $P M_\gamma^{-1} = (M_\gamma P^T)^{-1}$ and

$$M_\gamma P^T = \begin{bmatrix} D & -\gamma I_p \\ -\gamma I_m & D^T \end{bmatrix} \begin{bmatrix} 0 & I_m \\ I_p & 0 \end{bmatrix} = \begin{bmatrix} -\gamma I_p & D \\ D^T & -\gamma I_m \end{bmatrix},$$

which is symmetric. The inverse of a symmetric matrix is symmetric, so $J L M_\gamma^{-1} R$ is symmetric, and so is $J H_\gamma$. Then $(J H_\gamma)^T = J H_\gamma$ gives $-H_\gamma^T J = J H_\gamma$, so $J H_\gamma J^{-1} = -H_\gamma^T$. Thus $H_\gamma$ is similar to $-H_\gamma^T$, and with $p(s) = \det(sI - H_\gamma)$,

$$p(s) = \det(sI + H_\gamma^T) = \det(sI + H_\gamma) = (-1)^{2n} \det(-sI - H_\gamma) = p(-s).$$

A polynomial of even degree $2n$ with $p(s) = p(-s)$ has only even powers, so $p(s) = r(s^2)$ with $\deg r = n$. The coefficients are real because $H_\gamma$ is real. The equivalence for $s = j\omega_0$ follows from $s^2 = -\omega_0^2$. $\square$

## Lemma 3 (the level test)

Let $A$ be Hurwitz and $\gamma > \sigma_{\max}(D)$. Then $\|G\|_\infty \ge \gamma$ if and only if $H_\gamma$ has an eigenvalue on the imaginary axis.

*Proof.* The function $f(\omega) = \sigma_{\max}(G(j\omega))$ is continuous on $\mathbb{R}$, because $G$ has no pole on the imaginary axis and singular values depend continuously on the matrix. As $|\omega| \to \infty$, $G(j\omega) \to D$, so $f(\omega) \to \sigma_{\max}(D) < \gamma$.

If $\|G\|_\infty \ge \gamma$: there is $R > 0$ with $f < \gamma$ for $|\omega| \ge R$, so the supremum of $f$ is its maximum on $[-R, R]$, reached at some $\omega_1$ with $f(\omega_1) \ge \gamma$. On $[\omega_1, R]$ the continuous function $f$ goes from a value at least $\gamma$ to a value below $\gamma$, so $f(\omega_0) = \gamma$ for some $\omega_0$. Then $\gamma$ is a singular value of $G(j\omega_0)$, and Lemma 1 gives the eigenvalue $j\omega_0$. (Every singular value of $D$ is at most $\sigma_{\max}(D) < \gamma$, so Lemma 1 applies.)

If $H_\gamma$ has an eigenvalue $j\omega_0$: Lemma 1 says that $\gamma$ is a singular value of $G(j\omega_0)$, so $\|G\|_\infty \ge f(\omega_0) \ge \gamma$. $\square$

## Lemma 4 (the start interval of the bisection)

Let $A$ be Hurwitz, $W_c$ and $W_o$ the solutions of $A W_c + W_c A^T + B B^T = 0$ and $A^T W_o + W_o A + C^T C = 0$, and $\sigma_1 \ge \dots \ge \sigma_n \ge 0$ the square roots of the eigenvalues of $W_c W_o$ (the Hankel singular values). Then

$$\max(\sigma_{\max}(D), \sigma_1) \le \|G\|_\infty \le \sigma_{\max}(D) + 2(\sigma_1 + \dots + \sigma_n).$$

*Proof.* The first lower bound is the limit of $f$ at infinity. The second is the classical fact that the Hankel norm $\sigma_1$ is the norm of the Hankel operator of $G$, which maps past inputs to future outputs; this operator is a compression of the input-output map of $G$ on $L_2(-\infty, \infty)$, whose induced norm is $\|G\|_\infty$ (Glover 1984, also Zhou, Doyle and Glover 1996, the chapter on Hankel norm approximation). The upper bound is the error bound of balanced truncation, $\|G - G_r\|_\infty \le 2(\sigma_{r+1} + \dots + \sigma_n)$, applied with $r = 0$, where $G_0 = D$, together with the triangle inequality (see [the balanced truncation error bound](/balanced-truncation-error-bound/); Enns 1984 and Glover 1984). A non-minimal realization only adds zero values to the list, because the nonzero eigenvalues of $W_c W_o$ are those of a minimal realization. $\square$

## Theorem 1 (bisection)

Let $A$ be Hurwitz and $\varepsilon > 0$. HINF-BISECTION stops, and it returns $(lo, hi)$ with $lo \le \|G\|_\infty \le hi$ and $hi - lo \le 2\varepsilon\, lo$. If $lo_0 = \max(\sigma_{\max}(D), \sigma_1) > 0$, the loop runs at most $\lceil \log_2(n/\varepsilon) \rceil$ times.

*Proof.* **Invariant:** $lo \le \|G\|_\infty \le hi$ and $lo \ge lo_0$. It holds after line L6 by Lemma 4 (line L6 also sets $hi$ to at least $lo$, which does not break the invariant, because then the norm equals $lo$). In line L8, $\gamma = (lo + hi)/2 > lo \ge \sigma_{\max}(D)$, because the loop runs only while $hi > lo$. So Lemma 3 applies to $\gamma$: if line L9 finds an imaginary eigenvalue, then $\|G\|_\infty \ge \gamma$ and the new $lo = \gamma$ keeps the invariant; if not, $\|G\|_\infty < \gamma$ and the new $hi = \gamma$ keeps it.

**Termination and count.** If $lo_0 = 0$, then $D = 0$ and all $\sigma_i = 0$, so $hi_0 = 0$ and the loop does not run; in this case $G = 0$. Otherwise each pass halves $hi - lo$, and $lo$ never decreases. The start width is $hi_0 - lo_0 \le \sigma_{\max}(D) + 2 n \sigma_1 - lo_0 \le 2 n\, lo_0$, since $\sigma_{\max}(D) \le lo_0$ and $\sigma_1 \le lo_0$. After $k$ passes the width is at most $2n\, lo_0 / 2^k \le 2n\, lo / 2^k$, which is at most $2\varepsilon\, lo$ once $2^k \ge n/\varepsilon$. At exit the loop condition is false, so $hi - lo \le 2\varepsilon\, lo$. $\square$

## Theorem 2 (level set iteration)

Let $A$ be Hurwitz, $\varepsilon > 0$, and let the start value $lb_0$ of line L11 be positive. HINF-LEVEL-SET stops after at most $1 + \log(\|G\|_\infty / lb_0) / \log(1 + 2\varepsilon)$ passes of the loop, and it returns $(lb, \gamma, \omega)$ with $lb \le \|G\|_\infty \le \gamma = (1 + 2\varepsilon) lb'$ for the value $lb' \le lb$ held at the start of the last pass, so $\gamma - lb \le 2\varepsilon\, lb$. Here $lb = \sigma_{\max}(G(j\omega))$, or $lb = \sigma_{\max}(D)$ with $\omega = \infty$.

*Proof.* **Invariant:** $lb$ is a value of $f$ (or the limit $\sigma_{\max}(D)$), so $lb \le \|G\|_\infty$. Line L11 sets $lb$ this way, and line L15 replaces it only by a larger value of $f$ at a midpoint.

**The level is valid.** Since $lb > 0$ and $lb \ge \sigma_{\max}(D)$, the level $\gamma = (1 + 2\varepsilon) lb$ is larger than $\sigma_{\max}(D)$, so Lemma 3 applies.

**Exit at line L14.** If $H_\gamma$ has no imaginary eigenvalue, Lemma 3 gives $\|G\|_\infty < \gamma$.

**Exit at line L16.** Suppose $H_\gamma$ has imaginary eigenvalues but every midpoint value is at most $\gamma$. We show that $\|G\|_\infty \le \gamma$. Assume instead $\|G\|_\infty > \gamma$. The set $\Omega = \{\omega : f(\omega) > \gamma\}$ is open, not empty, and bounded (because $f \to \sigma_{\max}(D) < \gamma$). Let $(a, b)$ be one of its components. Then $a$ and $b$ are finite, and $f(a) = f(b) = \gamma$ by continuity. By Lemma 1, $ja$ and $jb$ are eigenvalues of $H_\gamma$, so $a$ and $b$ are in the sorted list $\omega_1 < \dots < \omega_k$ of line L15, which holds the frequencies of line L13 with both signs (the eigenvalues of the real matrix $H_\gamma$ come in conjugate pairs, and $f(-\omega) = f(\omega)$). Let $\omega_i = a$; then $\omega_{i+1} \le b$, and the midpoint $(\omega_i + \omega_{i+1})/2$ lies in $(a, b) \subset \Omega$. Its value is larger than $\gamma$, which is false. So $\|G\|_\infty \le \gamma$, and the returned $lb$ is at least the old $lb$, so $\gamma - lb \le 2\varepsilon\, lb$.

**Progress.** If the loop does not exit, line L16 found a midpoint value larger than $\gamma$, so the new $lb$ is larger than $(1 + 2\varepsilon)$ times the old one. Since $lb \le \|G\|_\infty$ always, after $k$ such passes $(1 + 2\varepsilon)^k lb_0 < \|G\|_\infty$, which bounds $k$. $\square$

The count in Theorem 2 is a worst case that grows like $1/\varepsilon$. Boyd and Balakrishnan (1990) proved much more: the lower bounds of the level set iteration converge quadratically to the norm. That result rests on the regularity of $f$ near a peak and is not reproved here.

## Floating point

The implementation forms $H_\gamma$ in floating point, computes $\det(sI - H_\gamma)$ with the Faddeev-LeVerrier recursion, keeps the even coefficients as $r$, and finds the roots of $r$ with the Durand-Kerner method of the shared helper. A root $t$ counts as real when $|\operatorname{Im} t| \le 10^{-6}(1 + |t|)$, and as nonpositive when $\operatorname{Re} t \le 10^{-10}(1 + |t|)$. When $\gamma$ is far from $\|G\|_\infty$ in relative terms, every root of $r$ is either clearly real and negative or clearly not, and the decision is the exact one. Near $\gamma = \|G\|_\infty$ two real roots of $r$ merge into a double root, which the root finder computes with an error near $10^{-8}$; the tolerance then accepts the pair as real, and a decision can be wrong only when $\gamma$ is within about $10^{-12}$ (relative) of the norm. Since the methods are stopped with $\varepsilon \ge 10^{-10}$ in practice, such an error moves the returned interval by much less than its width. The tests compare the floating point decision with an exact count of the nonpositive roots of $r$ in rational arithmetic (a Sturm sequence) on random systems.

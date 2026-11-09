---
title: CIRCLE-LINE returns exactly the common points of the line and the circle
proves: [correctness, termination]
status: full
---

**Notation.** The line is $\ell = \{p : A p_x + B p_y + C = 0\}$ with $(A, B) \ne (0, 0)$, and the circle is $\Gamma = \{p : |p - c| = r\}$ with $r \ge 0$. Let $n = (A, B)$, $N = |n|^2 = A^2 + B^2 > 0$, $e = n \cdot c + C$, $h = c - (e / N)\, n$, $D = r^2 N - e^2$, and $w = (-B, A)$, so that $n \cdot w = 0$ and $|w|^2 = N$.

**Lemma 1.** $h \in \ell$, and every point of $\ell$ is $h + t w$ for exactly one real $t$.

*Proof.* $n \cdot h + C = n \cdot c - (e / N)\, N + C = e - e = 0$, so $h \in \ell$. For $p \in \ell$, $n \cdot (p - h) = (n \cdot p + C) - (n \cdot h + C) = 0$, so $p - h$ is orthogonal to $n \ne 0$; in the plane this means $p - h = t w$ for one real $t$, since $w \ne 0$ spans the orthogonal complement of $n$. Conversely $n \cdot (h + t w) + C = 0$ for every $t$. $\square$

**Lemma 2.** For $p = h + t w$, $|p - c|^2 = e^2 / N + t^2 N$.

*Proof.* $p - c = t w - (e / N)\, n$. Since $n \cdot w = 0$, $|p - c|^2 = t^2 |w|^2 + (e / N)^2 |n|^2 = t^2 N + e^2 / N$. $\square$

**Lemma 3.** $p = h + t w$ lies on $\Gamma$ if and only if $t^2 N^2 = D$.

*Proof.* By Lemma 2, $|p - c| = r$ if and only if $t^2 N + e^2 / N = r^2$; multiplying by $N > 0$ gives $t^2 N^2 = r^2 N - e^2 = D$. $\square$

**Theorem.** CIRCLE-LINE terminates. For $(A, B) = (0, 0)$ it stops at line L1. Otherwise it returns $\ell \cap \Gamma$: the empty set if $D < 0$, the single point $h$ if $D = 0$, and the two distinct points $h \pm \sqrt{D}\, u$ with $u = w / N$ if $D > 0$.

*Proof.* There is no loop, so the algorithm terminates. By Lemma 1 the map $t \mapsto h + t w$ is a bijection from $\mathbb{R}$ onto $\ell$, so $\ell \cap \Gamma$ is the image of the real solutions $t$ of $t^2 N^2 = D$ by Lemma 3. If $D < 0$ there is no solution, since $t^2 N^2 \ge 0$, and line L5 returns $\emptyset$. If $D = 0$ the only solution is $t = 0$, which gives $h$, and line L6 returns $\{h\}$. If $D > 0$ the solutions are $t = \pm \sqrt{D} / N$, two distinct values, so the points $h \pm (\sqrt{D} / N)\, w = h \pm \sqrt{D}\, u$ are distinct by the injectivity of the map, and line L7 returns them. Lines L2 to L4 compute $N$, $e$, $h$ and $D$ as defined. $\blacksquare$

**Remark.** With integer input, $N$, $e$ and $D$ are integers and $h$ and $u$ have rational coordinates, so the case test of lines L5 and L6 is exact, and a point $h + s \sqrt{D}\, u$ with $s = \pm 1$ is rational exactly when $D$ is a perfect square.

---
title: The shifted edge functions and the grown box give exactly the pixels whose squares meet the triangle
proves: [correctness]
status: full
---

Let $T$ be a triangle with nonzero area, oriented by line L2 so that its edge functions $E_k(x) = n_k \cdot x + c_k$, with $n_k = (A_k, B_k)$, are at least 0 exactly on the closed half-plane $H_k$ that contains $T$. Then $T = H_0 \cap H_1 \cap H_2$. Let $h$ be half the pixel width and $C = [-h, h]^2$. Pixel $p$ (its center) has the closed square $Q_p = p + C$. Write $K \oplus L = \{a + b : a \in K, b \in L\}$ for the [Minkowski sum](/minkowski-sum/) and $\sigma_K(u) = \max_{x \in K} u \cdot x$ for the support function of a compact set $K$.

**Claim.** In the overestimate mode, line L10 accepts pixel $p$ of the screen if and only if $Q_p \cap T \neq \emptyset$. In the underestimate mode, it accepts $p$ if and only if $Q_p \subseteq T$.

**Step 1 (to a point test).** $Q_p \cap T \ne \emptyset$ if and only if $p = t - q$ for some $t \in T$ and $q \in C$, that is, $p \in T \oplus (-C) = T \oplus C$, because $C = -C$.

**Lemma 1 (a half-plane).** For a closed half-plane $H = \{x : n \cdot x + c \ge 0\}$ with $n = (A, B)$,

$$H \oplus C = \{x : n \cdot x + c + h(|A| + |B|) \ge 0\} .$$

*Proof.* $x \in H \oplus C$ if and only if $x - q \in H$ for some $q \in C$, that is, $\max_{q \in C} (n \cdot x - n \cdot q + c) \ge 0$. The maximum of $-n \cdot q$ over the square is $h|A| + h|B|$, at the corner $q = (-h\,\mathrm{sgn} A, -h\,\mathrm{sgn} B)$. $\square$

**Lemma 2 (seven half-planes).** Let $R$ be the bounding box of $T$. Then

$$T \oplus C = (H_0 \oplus C) \cap (H_1 \oplus C) \cap (H_2 \oplus C) \cap (R \oplus C) .$$

*Proof.* The left side is contained in each set on the right, because $T$ is contained in $H_0$, $H_1$, $H_2$ and $R$, and $K \subseteq L$ gives $K \oplus C \subseteq L \oplus C$.

For the other direction, let $x$ be in the right side and suppose $x \notin T \oplus C$. The set $T \oplus C$ is compact and convex, so by the separation theorem there is a vector $u \neq 0$ with $\varphi(u) = u \cdot x - \sigma_T(u) - \sigma_C(u) > 0$, since $\sigma_{T \oplus C} = \sigma_T + \sigma_C$. Let $D$ be the set of the seven directions $-n_0, -n_1, -n_2$ (the outward normals of $T$) and $\pm(1, 0)$, $\pm(0, 1)$ (the outward normals of $C$ and of $R$). Sort them by angle; they cut the plane into closed cones, each spanned by two consecutive directions of $D$. Inside one cone, the maximum $\sigma_T(u)$ is at one fixed vertex of $T$, because the cone lies between two consecutive outward normals of $T$, and $\sigma_C(u)$ is at one fixed corner of $C$, because the cone lies in one quadrant. So $\varphi$ is linear on the cone. Write $u = \alpha d_1 + \beta d_2$ with $\alpha, \beta \ge 0$ for the two directions $d_1, d_2$ that span its cone; then $\varphi(u) = \alpha \varphi(d_1) + \beta \varphi(d_2) > 0$, so $\varphi(d) > 0$ for some $d \in D$.

If $d = -n_k$, then $\sigma_T(-n_k) = c_k$, since $\min_{t \in T} n_k \cdot t = -c_k$ is attained on edge $k$, and $\sigma_C(-n_k) = h(|A_k| + |B_k|)$. So $\varphi(d) > 0$ says $n_k \cdot x + c_k + h(|A_k| + |B_k|) < 0$, which by Lemma 1 contradicts $x \in H_k \oplus C$. If $d = (1, 0)$, then $\varphi(d) > 0$ says $x_1 > \max_{t \in T} t_1 + h$, which contradicts $x \in R \oplus C$; the other three axis directions are the same. $\square$

**The overestimate.** Line L5 adds $r_k = h(|A_k| + |B_k|)$ to $c_k$, so by Lemma 1 the test $E_k(p) + r_k \ge 0$ of line L10 is $p \in H_k \oplus C$. Line L6 visits exactly the pixels whose squares meet $R$: in units of $1/s$ pixel, the square $[i s, (i + 1) s]$ meets $[x_{\min}, x_{\max}]$ if and only if $\lceil x_{\min}/s \rceil - 1 \le i \le \lfloor x_{\max}/s \rfloor$, and the same for $y$; this is $p \in R \oplus C$. By Lemma 2 and Step 1, a visited pixel is accepted if and only if $Q_p \cap T \ne \emptyset$, and an unvisited one has $p \notin R \oplus C$, so $Q_p \cap T = \emptyset$.

**The underestimate.** $T = H_0 \cap H_1 \cap H_2$, so $Q_p \subseteq T$ if and only if $\min_{q \in Q_p} E_k(q) \ge 0$ for each $k$. By the argument of Lemma 1, the minimum is $E_k(p) - h(|A_k| + |B_k|)$, which is the test of line L10 with the constant of line L5. A square inside $T$ is inside $R$, so the box of line L6, the pixels whose squares are inside $R$, loses no accepted pixel.

**The evaluation.** Each $E_k$ is affine, so the steps of lines L11 and L12, $s A_k$ per pixel and $s B_k$ per row, give the value at each visited center, starting from the value of line L7. All the coordinates, $c_k$ and $r_k$ are integers when the vertices are integers in units of $1/s$ and $s$ is even, so each test is exact. Lines L8 and L9 visit a finite box, so the loop ends. $\blacksquare$

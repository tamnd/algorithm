---
title: The root locus rules describe the locus of D + K N exactly
proves: [correctness]
status: full
---

Let $p_1, \ldots, p_n$ and $z_1, \ldots, z_m$ be the poles and zeros, with $n \ge 1$ and $m \le n$, both lists closed under complex conjugation, and no pole equal to a zero. These are the conditions that line L1 checks. Let $D(s) = \prod_i (s - p_i)$, $N(s) = \prod_k (s - z_k)$, $G = N/D$ and $\chi_K = D + K N$. Then $D$ and $N$ are monic with real coefficients and no common root. For $K > 0$ the leading coefficient of $\chi_K$ is 1 if $m < n$ and $1 + K$ if $m = n$, so $\chi_K$ has degree $n$ for every $K \ge 0$. The locus is $\mathcal{L} = \{ s : \chi_K(s) = 0 \text{ for some } K > 0 \}$. All statements are in exact arithmetic, with the roots of $W$ and $R$ computed exactly.

Two facts are used several times.

**Fact 1 (continuity of the roots).** The roots of a polynomial of fixed degree, with multiplicity, depend continuously on its coefficients. More precisely, by Rouché's theorem: if $f$ and $g$ are analytic on a closed disc and $|g| < |f|$ on its boundary circle, then $f$ and $f + g$ have the same number of zeros inside the disc.

**Fact 2 (simple roots move analytically).** If $s_0$ is a simple root of $\chi_{K_0}$, then by the implicit function theorem there is an analytic function $s(K)$ near $K_0$ with $s(K_0) = s_0$ and $\chi_K(s(K)) = 0$, and it is the only root near $s_0$. Its derivative is $s'(K_0) = -N(s_0)/\chi_{K_0}'(s_0)$.

## Lemma 1: the angle and magnitude conditions

*No pole and no zero is in $\mathcal{L}$. For any other $s$, $s \in \mathcal{L}$ if and only if $G(s)$ is a negative real number, that is $\angle G(s) = \sum_k \angle(s - z_k) - \sum_i \angle(s - p_i) = 180$ degrees modulo 360. The gain is then unique: $K = -D(s)/N(s) = 1/|G(s)|$.*

*Proof.* At a pole $p$, $\chi_K(p) = K N(p) \ne 0$ for $K > 0$, because $N(p) \ne 0$. At a zero $z$, $\chi_K(z) = D(z) \ne 0$. For other $s$, both $D(s)$ and $N(s)$ are nonzero, and $\chi_K(s) = 0$ if and only if $K = -D(s)/N(s) = -1/G(s)$. Such a $K > 0$ exists if and only if $G(s)$ is real and negative, and then $K = 1/|G(s)|$. The angle of a product is the sum of the angles of the factors, modulo 360 degrees, which gives the angle form. $\square$

## Lemma 2: the real axis segments

*Let $x$ be real and not a pole or zero. Then $x \in \mathcal{L}$ if and only if the number $c(x)$ of real poles and real zeros greater than $x$, counted with multiplicity, is odd. The union of the intervals returned by line L2 is the closure of $\mathcal{L} \cap \mathbb{R}$.*

*Proof.* $G(x)$ is real because $G$ has real coefficients, so by Lemma 1, $x \in \mathcal{L}$ if and only if $G(x) < 0$. A complex pole or zero $a + jb$, $b \ne 0$, comes with $a - jb$ (closure under conjugation), and the pair gives the factor $(x - a)^2 + b^2 > 0$ in $N(x)$ or $D(x)$. A real pole or zero $r$ gives the factor $x - r$, which is negative exactly when $r > x$. So the sign of $G(x)$ is $(-1)^{c(x)}$, and $G(x) < 0$ if and only if $c(x)$ is odd.

Let $x_1 > x_2 > \cdots > x_\ell$ be the distinct real poles and zeros, with multiplicities $c_1, \ldots, c_\ell$, and set $x_0 = +\infty$, $x_{\ell + 1} = -\infty$. The count $c(x)$ is constant on each open interval $(x_{i+1}, x_i)$ and equals $c_1 + \cdots + c_i$. Line L2 computes this running sum and records the interval $[x_{i+1}, x_i]$ when the sum is odd; on $(x_1, \infty)$ the count is 0, which is even. When two recorded intervals share an endpoint, line L2 joins them. So the union of the output intervals is the union of the closures of the open intervals where $c$ is odd. By the first part, $\mathcal{L} \cap \mathbb{R}$ is the union of these open intervals, and its closure is the union of their closures. $\square$

## Lemma 3: the asymptotes

*Let $q = n - m \ge 1$, $\sigma = (\sum_i p_i - \sum_k z_k)/q$ and $\theta_k = (2k + 1)\,180/q$ degrees. For every $\varepsilon > 0$ there is $K_1$ such that for $K > K_1$ the polynomial $\chi_K$ has exactly $\nu$ roots in the disc $|s - z| < \varepsilon$ for each distinct zero $z$ of multiplicity $\nu$, in total $m$ roots, and exactly one root in each disc $|s - \sigma - K^{1/q} e^{j\theta_k}| < \varepsilon$, $k = 0, \ldots, q - 1$. If $q \ge 2$, the mean of these $q$ roots tends to $\sigma$.*

*Proof.* Near the zeros: on a small circle around a zero $z$ of multiplicity $\nu$ that contains no other root of $N D$, $|N| \ge \eta > 0$ and $|D| \le M$; then for $K > M/\eta$, $|D| < |K N|$ on the circle, and by Fact 1 the polynomial $K N + D$ has as many zeros inside as $K N$, that is $\nu$. This gives $m$ roots near the zeros. (Lemma 5 gives one root per direction at a multiple zero.)

Far away: let $a = \sum_i p_i$ and $b = \sum_k z_k$. Then $D(s) = s^n - a s^{n-1} + O(s^{n-2})$ and $N(s) = s^m - b s^{m-1} + O(s^{m-2})$, so for large $|s|$

$$\frac{D(s)}{N(s)} = s^q \left(1 - \frac{a - b}{s} + O(s^{-2})\right) = (s - \sigma)^q \bigl(1 + O(s^{-2})\bigr),$$

because $(s - \sigma)^q = s^q (1 - q\sigma/s + O(s^{-2}))$ and $q \sigma = a - b$. Take the principal $q$-th root of the last factor: for $|s| \ge \rho_0$ the function $h(s) = (s - \sigma)(1 + O(s^{-2}))^{1/q} = s - \sigma + O(1/s)$ is analytic, and $D/N = h^q$. For $|s| \ge \rho_0$, $\chi_K(s) = 0$ if and only if $h(s)^q = -K$, that is $h(s) = w_k := K^{1/q} e^{j\theta_k}$ for some $k$. Fix $k$ and let $c_k = \sigma + w_k$. On the circle $|s - c_k| = \varepsilon$, the function $f(s) = s - c_k$ has $|f| = \varepsilon$, and $g(s) = h(s) - w_k - f(s) = h(s) - (s - \sigma) = O(1/|s|) = O(K^{-1/q})$. For $K$ large, $|g| < \varepsilon$ on the circle, and by Fact 1, $h - w_k = f + g$ has exactly one zero in the disc. The $q$ discs are disjoint for large $K$, because the centers are at distance at least $2 K^{1/q} \sin(180/q)$ apart when $q \ge 2$. Together with the $m$ roots near the zeros this gives $n$ roots, which are all the roots of $\chi_K$.

The mean: if $q \ge 2$, the term $K N$ has degree $m \le n - 2$, so the coefficient of $s^{n-1}$ in $\chi_K$ is $-a$ for every $K$, and the sum of all $n$ roots is $a$. The $m$ roots near the zeros have a sum that tends to $b$, so the sum of the $q$ far roots tends to $a - b = q\sigma$. $\square$

So the far branches approach the $q$ rays from $\sigma$ at the angles $\theta_k$, which line L3 returns. For $q = 1$ the single far root is $\sigma - K + o(1)$, real and going to $-\infty$.

## Lemma 4: the breakaway points

*Let $r_1, \ldots, r_d$ be the distinct poles and zeros, $w_i$ the multiplicity of $r_i$ as a pole, or minus its multiplicity as a zero, and $W = \sum_i w_i \prod_{j \ne i} (s - r_j)$, the polynomial of line L4. Then $\chi_{K_0}$ with $K_0 > 0$ has a multiple root at $s_0$ if and only if $W(s_0) = 0$ and $K_0 = -D(s_0)/N(s_0)$.*

*Proof.* First, $W$ in terms of $D$ and $N$. Let $Q = \prod_i (s - r_i)$. The logarithmic derivatives are $D'/D = \sum_{\text{poles}} \mu_i/(s - r_i)$ and $N'/N = \sum_{\text{zeros}} \nu_k/(s - r_k)$, so

$$\frac{N D' - N' D}{N D} = \frac{D'}{D} - \frac{N'}{N} = \sum_i \frac{w_i}{s - r_i} = \frac{W}{Q}.$$

Hence $N D' - N' D = H W$ with $H = N D/Q = \prod_i (s - r_i)^{|w_i| - 1}$, whose roots are the repeated poles and zeros. Also $W(r_i) = w_i \prod_{j \ne i}(r_i - r_j) \ne 0$, so $W$ has no root at a pole or zero, and $W$ is not the zero polynomial.

Now let $K_0 > 0$. The point $s_0$ is a multiple root of $\chi_{K_0}$ if and only if $D(s_0) + K_0 N(s_0) = 0$ and $D'(s_0) + K_0 N'(s_0) = 0$. Suppose both hold. Then $N(s_0) \ne 0$, since otherwise $D(s_0) = 0$ too, and $D$ and $N$ would have a common root. So $K_0 = -D(s_0)/N(s_0)$, and substituting into the second equation and multiplying by $N(s_0)$ gives $N D' - N' D = 0$ at $s_0$. As $s_0$ is not a pole or zero (Lemma 1), $H(s_0) \ne 0$ and $W(s_0) = 0$. Conversely, let $W(s_0) = 0$ and $K_0 = -D(s_0)/N(s_0) > 0$; here $N(s_0) \ne 0$ because $W$ does not vanish at zeros. Then $\chi_{K_0}(s_0) = 0$, and $\chi_{K_0}'(s_0) = D'(s_0) - D(s_0) N'(s_0)/N(s_0) = (H W)(s_0)/N(s_0) = 0$. $\square$

Line L5 keeps exactly the roots of $W$ with $-D/N$ real and positive, so by Lemma 4 it returns every point where $\chi_K$ has a multiple root for some $K > 0$, with that gain, and nothing else. Since $K(s) = -D(s)/N(s)$ has the derivative $-(N D' - N' D)/N^2 = -H W/N^2$, these points are the critical points of $K(s)$ on the locus; this is the rule $dK/ds = 0$.

**Consequence: where branches meet.** By Fact 2, near a gain $K_0$ where all roots of $\chi_{K_0}$ are simple, each root moves analytically with $K$ and no two roots meet. Since the coefficients are real, the conjugate of a root is a root; a simple real root therefore stays real, because its conjugate is a root near it and the root near it is unique. Hence the number of real roots of $\chi_K$ is constant on every interval of gains in $(0, \infty)$ that contains no gain from line L5 with a real point. Branches meet, and real roots leave or enter the real axis, only at the points of line L5.

## Lemma 5: the departure and arrival angles

*Let $p$ be a pole of multiplicity $\mu$ and let $\theta_j = (180 + 360 j + \sum_k \angle(p - z_k) - \sum_{q \ne p} \angle(p - q))/\mu$ for $j = 0, \ldots, \mu - 1$, where the second sum runs over the other poles with multiplicity. For every $\delta > 0$ small enough there is $K_2 > 0$ such that for $0 < K < K_2$ the polynomial $\chi_K$ has exactly $\mu$ roots in $|s - p| < 2\varepsilon$, with $\varepsilon = (K |c|)^{1/\mu}$ and $c$ as below, and exactly one of them in each disc $|s - p - \varepsilon e^{j\theta_j}| < \delta \varepsilon$. The same holds at a zero $z$ of multiplicity $\nu$ for large $K$, with $\varepsilon = (|c|/K)^{1/\nu}$ and the angles $\varphi_j = (180 + 360 j + \sum_i \angle(z - p_i) - \sum_{y \ne z} \angle(z - y))/\nu$ of line L7.*

*Proof.* Write $D = (s - p)^\mu D_1$ with $D_1(p) \ne 0$. Near $p$, $\chi_K = D_1 \cdot \bigl((s - p)^\mu + K c(s)\bigr)$ with $c(s) = N(s)/D_1(s)$ analytic and $c = c(p) \ne 0$. The equation $(s - p)^\mu + K c = 0$ has the $\mu$ roots $p + \varepsilon e^{j\theta_j}$, because $-c = |c| e^{j(180 + \angle c)}$ and $\angle c = \angle N(p) - \angle D_1(p) = \sum_k \angle(p - z_k) - \sum_{q \ne p} \angle(p - q)$.

Scale $s = p + \varepsilon u$. Then $(s - p)^\mu + K c(s) = \varepsilon^\mu \bigl(u^\mu - e^{j \mu \theta_0} + g(u)\bigr)$ with $|g(u)| = |c(s) - c|/|c| \le C \varepsilon |u|$ for a constant $C$, since $c$ is analytic. The polynomial $f(u) = u^\mu - e^{j\mu\theta_0}$ has the simple roots $u_j = e^{j\theta_j}$, spaced $360/\mu$ degrees on the unit circle. For $\delta < \sin(180/\mu)$ when $\mu \ge 2$ (any $\delta < 1$ when $\mu = 1$), the circles $|u - u_j| = \delta$ are disjoint and $|f| \ge \kappa > 0$ on them, and on $|u| = 2$, $|f| \ge 2^\mu - 1 \ge 1$. Choose $K_2$ so small that $2 C \varepsilon$ is less than $\kappa$ and less than 1. By Fact 1, $f + g$ has exactly one zero in each disc $|u - u_j| < \delta$ and exactly $\mu$ zeros in $|u| < 2$. The factor $D_1$ has no zeros near $p$. In the variable $s$ this is the claim.

At a zero, write $N = (s - z)^\nu N_1$ and divide by $K$: $\chi_K / K = N_1 \cdot \bigl((s - z)^\nu + K^{-1} c(s)\bigr)$ with $c(s) = D(s)/N_1(s)$. The same argument with $1/K$ in place of $K$ gives the angles $(180 + 360 j + \angle D(z) - \angle N_1(z))/\nu$, which are the $\varphi_j$. $\square$

So, as $K$ grows from 0, the $\mu$ branches that start at $p$ leave it in the directions $\theta_j$, and as $K \to \infty$, $\nu$ branches arrive at $z$ from the directions $\varphi_j$. Lines L6 and L7 compute exactly these angles. For a simple pole the formula is the angle condition of Lemma 1 at a point near $p$, solved for the angle of $s - p$.

## Lemma 6: the imaginary axis crossings

*Write $D(s) = \sum_a d_a s^a$, $N(s) = \sum_b n_b s^b$, $r_k = \sum_{a + b = k} d_a n_b (-1)^b$, and $R(u) = \sum_{i \ge 0} \epsilon_{2i+1} r_{2i+1} u^i$ with $\epsilon_k = 1$ for $k \equiv 1$ and $\epsilon_k = -1$ for $k \equiv 3$ modulo 4. Then $\operatorname{Im} D(j\omega) N(-j\omega) = \omega R(\omega^2)$ for real $\omega$. For $\omega > 0$, if $R$ is not the zero polynomial, $j\omega \in \mathcal{L}$ if and only if $R(\omega^2) = 0$ and $K = -D(j\omega)/N(j\omega) > 0$. The point $0$ is in $\mathcal{L}$ if and only if $-D(0)/N(0) > 0$.*

*Proof.* The coefficients are real, so $\overline{N(j\omega)} = N(\overline{j\omega}) = N(-j\omega)$. Then

$$D(j\omega) N(-j\omega) = \sum_a d_a j^a \omega^a \sum_b n_b (-1)^b j^b \omega^b = \sum_k j^k r_k \omega^k,$$

and $\operatorname{Im} j^k$ is 0 for even $k$, 1 for $k \equiv 1$ and $-1$ for $k \equiv 3$ modulo 4. So the imaginary part is $\sum_{k \text{ odd}} \epsilon_k r_k \omega^k = \omega R(\omega^2)$.

By Lemma 1, $j\omega \in \mathcal{L}$ if and only if $N(j\omega) \ne 0$ and $-D(j\omega)/N(j\omega)$ is real and positive. This quotient equals $-D(j\omega) \overline{N(j\omega)}/|N(j\omega)|^2$, which is real if and only if $\omega R(\omega^2) = 0$; for $\omega > 0$ that is $R(\omega^2) = 0$. If $N(j\omega) = 0$ then $D(j\omega) \ne 0$ and $j\omega \notin \mathcal{L}$; line L8 rejects this case because the gain is undefined. At $\omega = 0$, $D(0)$ and $N(0)$ are real, and Lemma 1 gives the last claim. $\square$

Line L8 takes the positive real roots $u$ of $R$, sets $\omega = \sqrt u$, and keeps the ones with $K > 0$; it tests $\omega = 0$ on its own. So, when $R \ne 0$, its list is exactly $\mathcal{L} \cap \{ j\omega : \omega \ge 0 \}$ with the gains. The crossings for $\omega < 0$ are the conjugates. When $R = 0$, the gain $-D(j\omega)/N(j\omega)$ is real for every $\omega$ with $N(j\omega) \ne 0$, and the part of the axis where it is positive is on the locus; line L8 reports this case with the flag.

**Consequence: changes of stability.** For $K > 0$ the degree of $\chi_K$ is $n$, so by Fact 1 the number of roots in the open right half plane is constant on every interval of gains on which no root lies on the imaginary axis. When $R \ne 0$, the gains with a root on the axis are the gains of line L8, a finite set. So the number of unstable closed-loop poles can change only at a listed crossing gain.

## The theorem

*For every input that passes line L1, the algorithm returns: the closure of $\mathcal{L} \cap \mathbb{R}$ (Lemma 2); if $n > m$, the centroid and angles of the asymptotes of the far branches (Lemma 3); every point where $\chi_K$ has a multiple root for some $K > 0$, with its gain, and no other point (Lemma 4); the limit directions of the branches at every pole and zero (Lemma 5); and, unless the flag is set, every point $j\omega$, $\omega \ge 0$, of the locus with its gain (Lemma 6).*

*Proof.* Lines L2, L3, L6 and L7 compute the formulas of Lemmas 2, 3 and 5 directly. In line L3 the centroid is real, because the sums of a conjugation-closed list are real. Line L4 computes the polynomial $W$ of Lemma 4; its coefficients are real, because the set of pairs $(r_i, w_i)$ is closed under conjugation, so the conjugate of $W(\bar s)$ is $W(s)$. Line L5 applies Lemma 4, and line L8 applies Lemma 6. Every loop runs over a finite list, so the algorithm stops. $\square$

## Floating point

The implementation computes the roots of $W$ and $R$ with the Durand-Kerner method in floating point, and it uses the tolerances stated on the page. The segments, the centroid and the angles are then correct to rounding. A breakaway point is a double root of $\chi_K$, and the computed roots of $\chi_K$ at that gain split by about the square root of the unit roundoff; but $\chi_{K_0}(s) = N(s)(K_0 - K(s))$, so the multiplicity of $s_0$ as a root of $\chi_{K_0}$ is one more than its multiplicity as a root of $W$. At a double root of $\chi_{K_0}$ the root of $W$ is therefore simple, and the computed point and its gain are accurate. A root of $W$ or $R$ whose $K$ has an imaginary part close to the tolerance $10^{-6}(1 + |K|)$ can be accepted or rejected wrongly; this is the only case in which the output can differ from the exact one by more than rounding.

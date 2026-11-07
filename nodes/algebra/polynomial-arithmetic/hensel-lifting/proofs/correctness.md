---
title: HENSEL-LIFT returns the unique lift of f = g h from modulus p to modulus p^k
proves: [correctness]
status: full
---

Let $f \in \mathbb{Z}[x]$ have degree $n$, let $p$ be a prime that does not divide the leading coefficient $\mathrm{lc}(f)$, and let $g_0, h_0 \in \mathbb{Z}[x]$ with $h_0$ monic of degree $e$, $f \equiv g_0 h_0 \pmod p$, and $g_0 \bmod p$, $h_0 \bmod p$ coprime. Congruence of polynomials modulo $m$ means that every coefficient of the difference is a multiple of $m$. Since $h_0$ is monic and $\mathrm{lc}(f) \not\equiv 0 \pmod p$, the reduction of $g_0$ modulo $p$ has degree $n - e$ and leading coefficient $\equiv \mathrm{lc}(f)$.

**Lemma 1 (division by a monic polynomial).** Let $m \ge 2$ and $h$ monic of degree $e$. Every $a \in \mathbb{Z}[x]$ has $q, r$ with $a \equiv q h + r \pmod m$ and $\deg r < e$, and if $a \equiv 0 \pmod{m'}$ for a divisor $m'$ of $m$, then $q \equiv r \equiv 0 \pmod{m'}$.

*Proof.* Long division by $h$ subtracts $c x^j h$, where $c$ is the current leading coefficient, and never divides, so it works over $\mathbb{Z}/m\mathbb{Z}$. The quotient and remainder are unique modulo $m$: if $q h + r \equiv q' h + r'$ with $\deg r, \deg r' < e$, and $q - q' \not\equiv 0$, then the top coefficient of $(q - q') h$ is that of $q - q'$, because $h$ is monic, so $(q - q')h$ has degree at least $e$ modulo $m$, while $r' - r$ has degree less than $e$. So $q \equiv q'$, $r \equiv r'$. Division is also unique modulo $m'$, and reducing a division modulo $m$ gives one modulo $m'$. If $a \equiv 0 \pmod{m'}$, then $0 = 0 \cdot h + 0$ is the division of $a$ modulo $m'$, so $q \equiv r \equiv 0 \pmod{m'}$. $\square$

**Lemma 2 (cofactors).** Line L1 returns $s, t$ with $s g_0 + t h_0 \equiv 1 \pmod p$, $\deg s < e$ and $\deg t < n - e$.

*Proof.* $\mathbb{Z}/p\mathbb{Z}$ is a field and the reductions of $g_0, h_0$ are coprime, so the extended Euclidean algorithm gives $s, t$ with $s g_0 + t h_0 \equiv 1$. If $\deg s \ge e$, replace $s$ by $s \bmod h_0$ and $t$ by $t + (s \operatorname{div} h_0)\, g_0$; the sum is unchanged. Then $t h_0 \equiv 1 - s g_0$ has degree less than $e + (n - e) = n$, and since $h_0$ is monic, $\deg t < n - e$. The standard extended Euclidean algorithm already returns cofactors with these degrees. $\square$

**Invariant.** At line L3, with $m = p^{2^i}$ after $i$ iterations:

1. $f \equiv g h \pmod m$ and $s g + t h \equiv 1 \pmod m$;
2. $h$ is monic of degree $e$, $\deg g \le n - e$, $\deg s < e$, $\deg t < n - e$;
3. $g \equiv g_0$ and $h \equiv h_0 \pmod p$.

**Initialization.** Before the first iteration, $m = p$, $g = g_0$ and $h = h_0$, so the invariant holds by the hypotheses and Lemma 2.

**Maintenance.** Assume the invariant at the top of an iteration. All arithmetic in lines L4 to L9 is modulo $m^2$, and we write $g^*, h^*, s^*, t^*$ for the new values.

*The factors.* $e = f - gh \equiv 0 \pmod m$ by part 1, so $s e \equiv 0 \pmod m$, and by Lemma 1 with $m' = m$, $q \equiv r \equiv 0 \pmod m$. Hence $g^* = g + te + qg \equiv g$ and $h^* = h + r \equiv h \pmod m$, which gives part 3 since $p$ divides $m$. As $\deg r < e$, $h^*$ is monic of degree $e$. Next, using $s e = q h + r$,

$$f - g^* h^* = e - g r - t e h - q g h - (t e + q g)\, r = e - g(qh + r) - teh - (te + qg)\, r = e\,(1 - s g - t h) - (t e + q g)\, r.$$

In the first product $e \equiv 0$ and $1 - sg - th \equiv 0 \pmod m$; in the second $te + qg \equiv 0$ and $r \equiv 0 \pmod m$. So $f \equiv g^* h^* \pmod{m^2}$. For the degree of $g^*$: if $g^*$ had a coefficient $\not\equiv 0 \pmod{m^2}$ at some degree $j > n - e$, take the largest such $j$; then the coefficient of $x^{j + e}$ in $g^* h^*$ is that coefficient, since $h^*$ is monic, but $f$ has no term of degree $j + e > n$. This contradicts $f \equiv g^* h^*$, so $\deg g^* \le n - e$.

*The cofactors.* $b = s g^* + t h^* - 1 \equiv s g + t h - 1 \equiv 0 \pmod m$. With $s b = c h^* + d$ from line L8,

$$s^* g^* + t^* h^* = s g^* - d g^* + t h^* - t b h^* - c g^* h^* = (1 + b) - g^*(d + c h^*) - t b h^* = 1 + b - b\,(s g^* + t h^*) = 1 + b - b(1 + b) = 1 - b^2.$$

Since $b \equiv 0 \pmod m$, $b^2 \equiv 0 \pmod{m^2}$, so $s^* g^* + t^* h^* \equiv 1 \pmod{m^2}$. For the degrees, $\deg d < e$ and $\deg s < e$ give $\deg s^* < e$. Then $t^* h^* \equiv 1 - s^* g^*$ has degree less than $e + (n - e) = n$ modulo $m^2$, and as $h^*$ is monic of degree $e$, $\deg t^* < n - e$, by the same top coefficient argument as for $g^*$.

Line L10 sets $m \leftarrow m^2 = p^{2^{i+1}}$, so the invariant holds at the next test of line L3.

**Termination.** After $i$ iterations $m = p^{2^i}$, and the test $m < p^k$ fails once $2^i \ge k$. So the loop runs $\lceil \log_2 k \rceil$ times.

**Output.** At line L11, $m = p^{2^i}$ with $2^i \ge k$, so $p^k$ divides $m$, and part 1 gives $f \equiv g h \pmod{p^k}$. Reducing modulo $p^k$ keeps $h$ monic of degree $e$, because its leading coefficient is $1$, and keeps $g \equiv g_0$ and $h \equiv h_0 \pmod p$ by part 3. So the output meets the specification.

**Uniqueness.** If $g', h'$ is another output, with $h'$ monic of degree $e$, $f \equiv g' h' \pmod{p^k}$, $g' \equiv g_0$ and $h' \equiv h_0 \pmod p$, then $g' \equiv g$ and $h' \equiv h \pmod{p^k}$ by the uniqueness theorem in [Hensel's lemma](/hensel-lemma/), which needs exactly that $g_0, h_0$ are coprime modulo $p$ and that $h, h'$ are monic of the same degree. With coefficients in $\{0, \ldots, p^k - 1\}$, the output is therefore unique. $\blacksquare$

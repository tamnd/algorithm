---
title: Falcon verification accepts every signature that the signer returns
proves: [correctness]
status: full
---

Let $R = \mathbb{Z}[x]/(x^n + 1)$ and $q = 12289$. Let $(f, g, F, G)$ come from lines L1 to L3, so that $f G - g F = q$ in $R$ and $f$ has an inverse $f^{-1}$ in $R_q = R / qR$, and let $h = g f^{-1} \bmod q$ (line L4). Define $\Lambda = \{(a, b) \in R^2 : a + b h \equiv 0 \pmod q\}$.

**Lemma 1 (the secret basis is in the lattice).** The vectors $(g, -f)$ and $(G, -F)$ are in $\Lambda$, and so is every vector $\sum_i z_i x^i (g, -f) + \sum_i z'_i x^i (G, -F)$ with integers $z_i, z'_i$.

*Proof.* Modulo $q$, $g + (-f) h \equiv g - f g f^{-1} = 0$. Also $f (G - F h) \equiv f G - F g = f G - g F = q \equiv 0$, and $f$ is invertible modulo $q$, so $G - F h \equiv 0$. $\Lambda$ is closed under addition and under multiplication of both coordinates by any element of $R$ (in particular by $x^i$ and by integers), because the condition $a + b h \equiv 0$ is linear over $R$. $\square$

**Lemma 2 (the hash equation).** If $v \in \Lambda$ and $(s_1, s_2) = (c, 0) - v$, then $s_1 + s_2 h \equiv c \pmod q$.

*Proof.* $s_1 + s_2 h = c - v_1 - v_2 h = c - (v_1 + v_2 h) \equiv c$. $\square$

**Lemma 3 (centering does not increase the norm).** For $a \in \mathbb{Z}$ let $\bar a$ be the representative of $a \bmod q$ in $(-q/2, q/2]$. Then $|\bar a| \le |a|$.

*Proof.* $\bar a$ has the smallest absolute value among the integers congruent to $a$ modulo $q$, because the elements of the class are spaced $q$ apart and exactly one lies in the half-open interval of length $q$ around 0, and every other element is at distance at least $q/2$ from 0. $a$ is one of them. $\square$

**Lemma 4 (Compress and Decompress).** If Compress$(s_2, slen)$ returns a string $s \ne \bot$, then Decompress$(s, n) = s_2$.

*Proof.* Compress writes, for each coefficient $x$ with $|x| \le 2047$, the sign bit, the 7 low bits of $|x|$, then $\lfloor |x| / 128 \rfloor$ zeros and a one, and pads with zeros to $slen$ bytes. Decompress reads the fields in the same order: the sign, the 7 low bits, and the unary high part up to the next one, which recovers $|x|$ and its sign. The encoder writes the sign bit 0 for $x = 0$, so the decoder does not reject it as a "minus zero", and the padding it writes is all zero, so the padding check passes. $\square$

**Theorem.** Let $sig = (r, s)$ be returned at line L14 for the message $m$, with the public key $h$. Then lines L15 to L18 return true.

*Proof.* Line L15 computes HashToPoint on the same bytes $r \| m$ as line L8, so it gets the same $c$. By Lemma 4, line L16 recovers the $s_2$ of the last pass through line L11. The vector $v$ of line L10 is an integer combination of the rows of $B$ (ffSampling picks integer coefficients for the rows and returns their combination), so $v \in \Lambda$ by Lemma 1, and Lemma 2 gives $s_1 + s_2 h \equiv c$ for the $s_1$ of line L11. Line L17 computes $s_1'$ with $s'_{1,i} \equiv c_i - (s_2 h)_i \equiv s_{1,i} \pmod q$ and $s'_{1,i}$ centered, so $|s'_{1,i}| \le |s_{1,i}|$ for each $i$ by Lemma 3. Then $\|(s_1', s_2)\|^2 \le \|(s_1, s_2)\|^2 \le \lfloor \beta^2 \rfloor$ by line L12, and line L18 returns true. $\blacksquare$

**What the proof does not cover.** The proof does not use how ffSampling picks the coefficients, only that they are integers. The distribution of $v$ matters for security and for how often line L12 or line L13 makes the signer restart, not for correctness. The toy signer of this page uses Klein's sampler, which also returns an integer combination of the rows of $B$, so the same proof applies to it.

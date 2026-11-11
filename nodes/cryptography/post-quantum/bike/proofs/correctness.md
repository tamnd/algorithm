---
title: BIKE decapsulation returns the encapsulated key whenever the decoder returns the error, so the KEM fails only with the decoding failure rate
proves: [correctness]
status: full
---

We use the notation of the page. $\mathcal{R} = \mathbb{F}_2[x]/(x^r - 1)$, and for $a \in \mathcal{R}$ we write $a_i$ for the coefficient of $x^i$, with indices modulo $r$. The secret blocks $h_0, h_1$ have odd weight $d < r$, and $r$ is prime with 2 primitive modulo $r$.

**Lemma 1 (the key exists).** $h_0$ is invertible in $\mathcal{R}$.

*Proof.* Since 2 has order $r - 1$ modulo $r$, the cyclotomic polynomial $\Phi_r = 1 + x + \cdots + x^{r-1}$ is irreducible over $\mathbb{F}_2$, and $x^r - 1 = (x + 1)\Phi_r$ with coprime factors. By the Chinese remainder theorem, $h_0$ is invertible if and only if $(x + 1) \nmid h_0$ and $\Phi_r \nmid h_0$. First, $h_0(1)$ is the weight of $h_0$ modulo 2, which is 1, so $(x+1) \nmid h_0$. Second, $h_0$ has degree less than $r$, so a multiple of $\Phi_r$ would be $0$ or $\Phi_r$ itself, which has weight $r > d$. $\square$

**Lemma 2 (the syndrome).** $c_0 h_0 = e_0 h_0 + e_1 h_1$.

*Proof.* $c_0 h_0 = e_0 h_0 + e_1 h_1 h_0^{-1} h_0 = e_0 h_0 + e_1 h_1$, because $\mathcal{R}$ is commutative. $\square$

Write $H = (h_0 \mid h_1)$ for the $r \times 2r$ matrix whose column $j$ of block $b$ is the coefficient vector of $x^j h_b$. Then $(e_0, e_1)H^T = e_0 h_0 + e_1 h_1$, so Lemma 2 says that $c_0 h_0$ is the syndrome of $(e_0, e_1)$ under $H$.

**Lemma 3 (the counters).** For a syndrome $s$, the counter of position $j$ in block $b$, $\mathrm{ctr}_{b,j} = \sum_{k \in \mathrm{supp}(h_b)} s_{j+k}$, equals $|s \wedge x^j h_b|$, the number of unsatisfied parity checks that contain position $j$.

*Proof.* The coefficient vector of $x^j h_b$ has ones exactly at $j + k$ for $k \in \mathrm{supp}(h_b)$, and these are distinct modulo $r$. So $|s \wedge x^j h_b| = \sum_{k} s_{j+k}$. Row $i$ of $H$ is a parity check that contains position $(b, j)$ exactly when $(x^j h_b)_i = 1$, and it is unsatisfied when $s_i = 1$. $\square$

**Lemma 4 (soundness of the decoder).** If BGF returns $e'$, then $e' H^T = s$.

*Proof.* Line B5 returns $e$ only after it checks $s = eH^T$. $\square$

**Theorem (correctness up to decoding failure).** Fix a key pair and an encapsulation with message $m$, error $(e_0, e_1) = \mathbf{H}(m)$ and key $K = \mathbf{K}(m, c)$. If BGF$(c_0 h_0, h_0, h_1)$ returns $(e_0, e_1)$, then DECAPS returns $K$. In general,

$$\Pr[\mathrm{DECAPS}(sk, c) \ne K] \le \Pr[\mathrm{BGF}(c_0 h_0, h_0, h_1) \ne (e_0, e_1)] = \mathrm{DFR}.$$

*Proof.* By Lemma 2, line L8 runs the decoder on the syndrome of $(e_0, e_1)$. If it returns $e' = (e_0, e_1)$, then line L9 gives $m' = c_1 \oplus \mathbf{L}(e_0, e_1) = m \oplus \mathbf{L}(e_0, e_1) \oplus \mathbf{L}(e_0, e_1) = m$. Then $\mathbf{H}(m') = (e_0, e_1) = e'$, so line L10 returns $\mathbf{K}(m, c) = K$. The event DECAPS $\ne K$ is therefore contained in the event that the decoder does not return $(e_0, e_1)$, which is the definition of a decoding failure. $\blacksquare$

**Remarks.** (1) If the decoder returns another $e'' \ne (e_0, e_1)$ with the same syndrome, then $e'' + (e_0, e_1)$ is a nonzero codeword of the MDPC code, and line L10 rejects unless $\mathbf{H}(c_1 \oplus \mathbf{L}(e'')) = e''$, which is a hash collision event. (2) Unlike a Goppa decoder, bit flipping has no proven radius: no theorem says that it corrects all errors of weight $t$. This is why the DFR is estimated by models and simulation, and why the CCA bound of the Fujisaki-Okamoto style transform (Hofheinz, Hövelmanns and Kiltz, 2017) contains a term for the correctness error.

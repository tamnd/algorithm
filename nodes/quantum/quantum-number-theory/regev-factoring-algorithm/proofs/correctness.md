---
title: Regev's algorithm returns only true factors, and succeeds under its assumption
proves: [correctness]
status: full
---

We use the pseudocode and the notation of the page: $N$ is composite, $b_1, \dots, b_d$ are the first $d$ primes, $a_i = b_i^2$, $h(z) = \prod_i a_i^{z_i} \bmod N$, $\mathcal{L} = \ker h$ and $\mathcal{L}_0 = \{z : \prod_i b_i^{z_i} \equiv \pm 1\}$. The box is $B = \{-D/2, \dots, D/2 - 1\}^d$, and for $y \in \mathbb{Z}^d$ we write $[y]$ for the point of $B$ congruent to $y$ modulo $D$. Congruences without a modulus are modulo $N$, and $m = d + 4$ is the number of runs.

Part 1 shows, with no assumption, that every value the algorithm returns is a nontrivial factor of $N$. Part 2 shows that, under Regev's assumption and for his parameters, one attempt succeeds with probability at least about $1/4$.

## Part 1: every answer is a factor

**Lemma 1.** If REGEV returns a value $f$, then $1 < f < N$ and $f$ divides $N$.

*Proof.* Line L1 returns 2 only for even $N \ge 4$, and $r$ only when $N = r^k$ with $r \ge 2$ and $k \ge 2$, so $1 < r < N$. Line L2 returns $b_i$ only when $b_i$ divides $N$, and $b_i < N$ because $N$ is composite. After line L2 every $b_i$ is a unit modulo $N$, so the products with negative exponents in lines L11 and L12 are defined. Suppose line L13 returns $\gcd(x - 1, N)$. Line L11 ensures $u \in \mathcal{L}$, so $x^2 \equiv \prod_i b_i^{2u_i} = \prod_i a_i^{u_i} \equiv 1$, and $N$ divides $(x - 1)(x + 1)$. As $x \not\equiv 1$, $\gcd(x - 1, N) \ne N$. If $\gcd(x - 1, N) = 1$, then $N$ would divide $x + 1$, against $x \not\equiv -1$. So $1 < \gcd(x - 1, N) < N$. $\square$

## Part 2: the quantum step and the post-processing

**Lemma 2 (the outcome distribution).** Let $\rho = \rho_R$ and $Z = \sum_{z \in B} \rho(z)^2$. For every $u \in \mathbb{Z}^d$, the outcome $w$ of line L7 satisfies

$$\chi(u) := \mathbb{E}\bigl[e^{2\pi i \langle u, w \rangle / D}\bigr] = \frac{1}{Z} \sum_{z \in B} \rho(z) \rho([z + u]) \, \bigl[h(z) = h([z + u])\bigr].$$

Let $B_u = \{z \in B : z + u \in B\}$, $G(u) = Z^{-1} \sum_{z \in B_u} \rho(z) \rho(z + u)$ and $W(u) = Z^{-1} \sum_{z \in B \setminus B_u} \rho(z) \rho([z + u])$. Then $|\chi(u) - G(u)| \le W(u)$ if $u \in \mathcal{L}$, and $|\chi(u)| \le W(u)$ if $u \notin \mathcal{L}$.

*Proof.* After line L6 the state is $Z^{-1/2} \sum_{z \in B} \rho(z) |z\rangle |c \cdot h(z)\rangle$ with the constant $c = h(D/2, \dots, D/2)$. The register $|e\rangle$ is not touched again, so the distribution of $w$ is the same as if it were measured now. For a value $e$, let $f_e(z) = \rho(z)$ if $c \cdot h(z) = e$ and $f_e(z) = 0$ otherwise, and let $F_e(w) = \sum_{z \in B} f_e(z) \omega^{\langle z, w \rangle}$ with $\omega = e^{2\pi i / D}$. The QFT over $(\mathbb{Z}_D)^d$ maps $|z\rangle$ to $D^{-d/2} \sum_w \omega^{\langle z, w \rangle} |w\rangle$, and the phase $\omega^{\langle z, w \rangle}$ does not depend on the representative of $z$ modulo $D$. So

$$\Pr[w] = \frac{1}{D^d Z} \sum_e |F_e(w)|^2 .$$

Now $\sum_w |F_e(w)|^2 \omega^{\langle u, w \rangle} = \sum_{z, z' \in B} f_e(z) f_e(z') \sum_w \omega^{\langle z - z' + u, w \rangle}$. The inner sum is $D^d$ if $z' = [z + u]$ and 0 otherwise. Hence $\chi(u) = Z^{-1} \sum_e \sum_{z \in B} f_e(z) f_e([z + u])$, and for each $z$ the product $f_e(z) f_e([z+u])$ is nonzero for exactly one $e$ if $h(z) = h([z + u])$, and for no $e$ otherwise. This is the formula.

For $z \in B_u$ we have $[z + u] = z + u$ and $h(z + u) = h(z) h(u)$. As $h(z)$ is a unit, the indicator is 1 for all $z \in B_u$ when $u \in \mathcal{L}$ and 0 for all of them when $u \notin \mathcal{L}$. The terms with $z \notin B_u$ are nonnegative and sum to at most $W(u)$. $\square$

Since $\|z\|^2 + \|z + u\|^2 = 2\|z + u/2\|^2 + \|u\|^2/2$, every term of $G(u)$ equals $e^{-\pi \|u\|^2 / (2R^2)} e^{-2\pi \|z + u/2\|^2 / R^2}$; so for short $u$ and $D$ large compared with $R$, $G(u)$ is close to $e^{-\pi \|u\|^2/(2R^2)}$ and $W(u)$ is close to 0. Lemma 2 says that $w/D$ concentrates near points $v$ with $\langle u, v \rangle \in \mathbb{Z}$ for all short $u \in \mathcal{L}$, that is, near the dual lattice $\mathcal{L}^*$ modulo $\mathbb{Z}^d$. The rest of the proof uses the sharper form that Regev proves (his Section 3, Claim A.5, Proposition A.6 and Claim A.7):

**Fact (Regev).** If $R > 2\sqrt{d}$ and $D \in [2\sqrt{d} R, 4\sqrt{d} R)$, the distribution of $w/D$ is within statistical distance $1/\mathrm{poly}(d)$ of a process that picks a uniform coset $v \in \mathcal{L}^*/\mathbb{Z}^d$ and outputs a grid point whose torus distance from $v$ is less than $\delta = \sqrt{d}/(\sqrt{2} R)$, except with probability $O(2^{-d})$.

**Lemma 3 (short lifts).** Let $w_1, \dots, w_m \in (\mathbb{Z}_D)^d$, and suppose $w_k/D$ is at torus distance less than $\delta$ from some $v_k \in \mathcal{L}^*$ for every $k$. Then every $u \in \mathcal{L}$ has a lift $u' \in \mathcal{L}'$ whose first $d$ coordinates are $u$ and with $\|u'\| \le \|u\| (1 + m D^2 \delta^2)^{1/2}$.

*Proof.* The combination $\sum_j u_j c_j$ of the first $d$ columns $c_j$ of line L8 has first coordinates $u$ and last coordinates $\langle u, w_k \rangle$. Subtract integer multiples of the columns $D e_k$ so that each last coordinate becomes the residue $t_k \equiv \langle u, w_k \rangle \pmod D$ of least absolute value; then $|t_k|$ is the distance from $\langle u, w_k \rangle$ to the nearest multiple of $D$. Write $w_k/D = v_k + \eta_k + y_k$ with $y_k \in \mathbb{Z}^d$ and $\|\eta_k\| < \delta$. Since $u \in \mathcal{L}$ and $v_k \in \mathcal{L}^*$, $\langle u, v_k + y_k \rangle$ is an integer, so by the Cauchy-Schwarz inequality $|t_k| \le D |\langle u, \eta_k \rangle| < D\delta\|u\|$. Summing the squares gives the bound. $\square$

**Lemma 4 (no short false vectors).** Let $v_1, \dots, v_m$ be independent uniform cosets of $\mathcal{L}^*/\mathbb{Z}^d$ and let the $w_k$ be as in Lemma 3. Put $\varepsilon = (4 \det \mathcal{L})^{-1/m} / 3$. With probability at least $1/4$ over the $v_k$, every nonzero $u' \in \mathcal{L}'$ with $\|u'\| < \min(D, \delta^{-1}) \, \varepsilon / 2$ has its first $d$ coordinates in $\mathcal{L} \setminus \{0\}$.

*Proof.* This is Regev's Lemma 4.4 with $S = D$. The group $G = \mathcal{L}^*/\mathbb{Z}^d$ is finite of order $\det \mathcal{L}$ and needs $r \le d$ generators. By a theorem of Pomerance, quoted by Regev as Theorem 4.1, the expected number of independent uniform elements needed to generate $G$ is less than $r + 2.12$. If $r + 4$ uniform elements failed to generate $G$ with probability more than $1/2$, this number would be at least $r + 5$ with probability more than $1/2$, and its expectation would exceed $r + 5/2$. So the $m \ge r + 4$ cosets $v_k$ generate $G$ with probability at least $1/2$.

Fix $u \in \mathbb{Z}^d \setminus \mathcal{L}$. The map $v \mapsto \langle u, v \rangle \bmod 1$ is a homomorphism from $G$ to $\mathbb{R}/\mathbb{Z}$, and it is not zero because $(\mathcal{L}^*)^* = \mathcal{L}$. So for uniform $v$ its value is uniform on $\{0, 1/t, \dots, (t-1)/t\}$ for some $t \ge 2$. If $t < 1/\varepsilon$ and the $v_k$ generate $G$, some $\langle u, v_k \rangle \bmod 1$ is a nonzero multiple of $1/t$, so its distance from $\mathbb{Z}$ is at least $1/t > \varepsilon$. If $t \ge 1/\varepsilon$, each $\langle u, v_k \rangle$ lies within $\varepsilon$ of $\mathbb{Z}$ with probability $(1 + 2\lfloor t\varepsilon \rfloor)/t \le 3\varepsilon$, so all $m$ of them do with probability at most $(3\varepsilon)^m$. A union bound over the fewer than $\det \mathcal{L}$ nonzero classes $u + \mathcal{L}$ gives at most $\det \mathcal{L} \cdot (3\varepsilon)^m = 1/4$. Hence, with probability at least $1/2 - 1/4 = 1/4$, every $u \notin \mathcal{L}$ has some $k$ with $\langle u, v_k \rangle$ at distance more than $\varepsilon$ from $\mathbb{Z}$.

Assume this event and take a nonzero $u' \in \mathcal{L}'$ with first coordinates $u$. If $u = 0$, then $u'$ is a nonzero vector of $D\mathbb{Z}^m$ and $\|u'\| \ge D$. If $u \notin \mathcal{L}$ and $\|u\| \ge \varepsilon/(2\delta)$, then $\|u'\| \ge \|u\| \ge \delta^{-1}\varepsilon/2$. If $u \notin \mathcal{L}$ and $\|u\| < \varepsilon/(2\delta)$, take $k$ from the event: $\langle u, w_k/D \rangle$ is at distance more than $\varepsilon - \delta\|u\| > \varepsilon/2$ from $\mathbb{Z}$, so coordinate $d + k$ of $u'$, which is $\langle u, w_k \rangle$ minus a multiple of $D$, exceeds $D\varepsilon/2$ in absolute value. In all three cases $\|u'\| \ge \min(D, \delta^{-1})\varepsilon/2$. $\square$

**Lemma 5 (what LLL gives).** Let $c_1, \dots, c_k$ be an LLL-reduced basis, with parameter $3/4$, of a lattice $\Lambda \subset \mathbb{R}^k$, with Gram-Schmidt vectors $c^*_i$, and let $T' > 0$. Let $\ell$ be the least index with $\|c^*_{\ell+1}\| > 2^{k/2} T'$, or $\ell = k$ if there is none. Then every vector of $\Lambda$ of length at most $T'$ is an integer combination of $c_1, \dots, c_\ell$, and $\|c_i\| \le \sqrt{k} \, 2^{k/2} T'$ for $i \le \ell$.

*Proof.* The basis is size-reduced, $|\mu_{ij}| \le 1/2$, and the Lovász condition with parameter $3/4$ gives $\|c^*_{i+1}\|^2 \ge \|c^*_i\|^2/2$ (Lenstra, Lenstra and Lovász). For $i > \ell$ this gives $\|c^*_i\|^2 \ge 2^{-(i - \ell - 1)} \|c^*_{\ell+1}\|^2 > 2^{-k} \cdot 2^k T'^2$, so $\|c^*_i\| > T'$. If $x = \sum_i \gamma_i c_i$ with integers $\gamma_i$ and the largest index $j$ with $\gamma_j \ne 0$ is above $\ell$, then $\|x\| \ge |\gamma_j| \|c^*_j\| > T'$. For $i \le \ell$, every $j \le i$ has $\|c^*_j\| \le 2^{k/2} T'$ by the choice of $\ell$, so $\|c_i\|^2 = \|c^*_i\|^2 + \sum_{j < i} \mu_{ij}^2 \|c^*_j\|^2 \le \sum_{j \le i} \|c^*_j\|^2 \le k \, 2^k T'^2$. $\square$

**Theorem.** Assume that $\mathcal{L} \setminus \mathcal{L}_0$ contains a vector of length at most $T$. Let $k = 2d + 4$, $D \in [2\sqrt{d} R, 4\sqrt{d} R)$ with $R > 2\sqrt{d}$, $\delta = \sqrt{d}/(\sqrt{2} R)$, $\varepsilon_0 = (4 \cdot 2^n)^{-1/m}/3$ and $T' = T (1 + 8 d^2 m)^{1/2}$, and assume

$$\sqrt{k} \, 2^{k/2} \, T' < \delta^{-1} \varepsilon_0 / 2 .$$

Then one attempt of REGEV returns a nontrivial factor of $N$ with probability at least $1/4 - O(m/\mathrm{poly}(d))$. With $d = \sqrt{n}$ and $T = \exp(O(\sqrt{n}))$, the condition holds for $R = \exp(C\sqrt{n})$ with a large enough constant $C$.

*Proof.* If lines L1 or L2 return, the answer is correct by Lemma 1. Otherwise, by the Fact and a union bound over the $m$ runs, the samples are $\delta$-close to independent uniform cosets $v_k$, except with probability $O(m/\mathrm{poly}(d))$. Then Lemma 4 applies. Since $\det \mathcal{L} \le N < 2^n$, its $\varepsilon$ is at least $\varepsilon_0$, and $D \ge 2\sqrt{d} R > \delta^{-1}$, so with probability at least $1/4$ every nonzero $u' \in \mathcal{L}'$ with $\|u'\| < \delta^{-1}\varepsilon_0/2$ has its first $d$ coordinates in $\mathcal{L} \setminus \{0\}$.

Let $u \in \mathcal{L} \setminus \mathcal{L}_0$ with $\|u\| \le T$. As $D\delta < 4\sqrt{d} R \cdot \sqrt{d}/(\sqrt{2} R) = 2\sqrt{2}\,d$, Lemma 3 gives a lift $u'$ with $\|u'\| \le T (1 + 8 d^2 m)^{1/2} = T'$. Apply Lemma 5 to the reduced basis of line L9: $u'$ is an integer combination of $c_1, \dots, c_\ell$, and each of these is nonzero with length at most $\sqrt{k} \, 2^{k/2} T' < \delta^{-1}\varepsilon_0/2$. So the first $d$ coordinates $z_1, \dots, z_\ell$ of $c_1, \dots, c_\ell$ all lie in $\mathcal{L} \setminus \{0\}$, and line L11 accepts each of them. If all were in $\mathcal{L}_0$, then $u$, which is an integer combination of them, would lie in the lattice $\mathcal{L}_0$; it does not. So some $z_i \in \mathcal{L} \setminus \mathcal{L}_0$, for which line L12 gives $x \not\equiv \pm 1$, and line L13 returns. Line L10 tries every reduced vector, so the attempt returns at the latest at this $z_i$, and the returned value is a factor by Lemma 1.

For the parameters, $\log_2(\delta^{-1}\varepsilon_0/2) = \log_2 R - O(\log d) - (n + 2)/m$ and $\log_2(\sqrt{k} \, 2^{k/2} T') = d + O(\log d) + \log_2 T$. With $d = \sqrt{n}$, both $n/m$ and $d$ are at most $\sqrt{n}$, and $\log_2 T = O(\sqrt{n})$, so $\log_2 R = C\sqrt{n}$ satisfies the condition for a large enough constant $C$. $\blacksquare$

**Remark.** Lemma 1 holds for every choice of parameters, so the algorithm is Las Vegas: the assumption only affects the probability of success, and an attempt that reaches line L14 is repeated.

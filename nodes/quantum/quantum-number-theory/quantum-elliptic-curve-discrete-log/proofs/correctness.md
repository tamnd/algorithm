---
title: The quantum elliptic curve discrete logarithm algorithm returns x with xP = Q
proves: [correctness]
status: full
---

We use the pseudocode of the page. $E$ is an elliptic curve over $\mathbb{F}_p$, $P \in E(\mathbb{F}_p)$ has order $r$, $Q = xP$ with $0 \le x < r$, and $\omega = e^{2\pi i/r}$. Each exponent register has $n$ qubits with $2^n \ge r$, and $a_j$ is bit $j$ of $a$. The accumulator holds the code of a point, and distinct points have distinct codes. $F_r$ maps $|a\rangle$ to $r^{-1/2} \sum_{c=0}^{r-1} \omega^{ac} |c\rangle$.

**Lemma 1 (the controlled additions).** For a fixed point $C$, the map $|R\rangle \mapsto |R + C\rangle$ on point codes, extended by the identity on the codes of no point, is a permutation of the basis states, so it is unitary. Lines L4 and L5 map $|a\rangle|b\rangle|O\rangle$ to $|a\rangle|b\rangle|aP + bQ\rangle$ for all $a, b < 2^n$.

*Proof.* $R \mapsto R + C$ is a bijection of $E(\mathbb{F}_p)$ with inverse $R \mapsto R - C$, so the map permutes the point codes and fixes the rest. The controlled form acts as this permutation or as the identity, depending on a control bit that it does not change, so it is again a permutation. Line L4 adds $2^j P$ exactly for the $j$ with $a_j = 1$, so it adds $\sum_j a_j 2^j P = aP$. Line L5 adds $bQ$ in the same way. $E(\mathbb{F}_p)$ is abelian, so the order of the additions does not matter, and the accumulator ends at $O + aP + bQ$. $\square$

**Lemma 2 (the hidden subgroup).** $f(a, b) = aP + bQ$ on $\mathbb{Z}_r \times \mathbb{Z}_r$ satisfies $f(a, b) = f(a', b')$ if and only if $a + xb \equiv a' + xb' \pmod r$. So $f$ is constant on the cosets of $H = \{(-xt, t)\}$ and distinct on distinct cosets.

*Proof.* $f(a, b) = (a + xb)P$, and $uP = u'P$ if and only if $u \equiv u' \pmod r$ because $P$ has order $r$. $\square$

**Lemma 3 (the output distribution).** One run of lines L3 to L7 gives each pair $(c, d)$ with $d \equiv xc \pmod r$ with probability exactly $1/r$, and the other pairs with probability 0.

*Proof.* Line L3 gives $r^{-1} \sum_{a, b \in \mathbb{Z}_r} |a\rangle|b\rangle|O\rangle$. By Lemma 1, lines L4 and L5 give $r^{-1} \sum_{a, b} |a\rangle|b\rangle|(a + xb)P\rangle$. Group the terms by $s = a + xb \bmod r$; for fixed $s$ the pairs are $(s - xb, b)$ with $b \in \mathbb{Z}_r$. After line L6 the amplitude of $|c\rangle|d\rangle|sP\rangle$ is

$$\frac{1}{r^2} \sum_{b=0}^{r-1} \omega^{(s - xb)c + bd} = \frac{\omega^{sc}}{r^2} \sum_{b=0}^{r-1} \omega^{b(d - xc)}.$$

The geometric sum is $r$ if $d \equiv xc \pmod r$ and 0 otherwise. The codes $sP$ for different $s$ are distinct basis states, so the probability of $(c, d)$ is the sum over the $r$ values of $s$ of $1/r^2$, which is $1/r$ for each of the $r$ allowed pairs. $\square$

So $c$ is uniform on $\mathbb{Z}_r$, and $d = xc \bmod r$.

**Lemma 4 (one congruence).** For an allowed pair, let $e = \gcd(c, r)$ and $m = r/e$. Then $e$ divides $d$, and the solutions of $cx' \equiv d \pmod r$ are the $x'$ with $x' \equiv (d/e)(c/e)^{-1} \pmod m$. The true $x$ is one of them.

*Proof.* $x$ solves the congruence by Lemma 3, so $e$ divides $d = cx - kr$ for some integer $k$. Dividing by $e$ gives $(c/e)x' \equiv d/e \pmod m$ with $c/e$ invertible modulo $m$. $\square$

**Theorem (correctness and runs).** Lines L8 and L9 keep $x \equiv x_\star \pmod M$, and after runs with outcomes $c_1, \dots, c_t$ the modulus is $M = r/\gcd(c_1, \dots, c_t, r)$. If the algorithm returns $x_\star$, then $x_\star P = Q$. After $t$ runs, $M = r$ with probability exactly $\prod_{s \mid r} (1 - s^{-t})$ over the primes $s$ that divide $r$, and the expected number of runs is less than 2.775. If $r$ is prime, one run succeeds with probability $(r - 1)/r$.

*Proof.* Each run adds a congruence that the true $x$ satisfies, by Lemma 4, so all of them are compatible, and the [Chinese remainder theorem](/chinese-remainder-theorem/) merges them into one modulo the least common multiple of the moduli $r/e_i$. For each prime $s$, the valuation of this least common multiple is $v_s(r) - \min_i v_s(e_i)$, so it equals $r/\gcd(e_1, \dots, e_t)$. Line L10 returns only after the check $x_\star P = Q$. The $c_i$ are independent and uniform by Lemma 3, and $M = r$ if and only if no prime $s \mid r$ divides all the $c_i$, which has probability $\prod_{s \mid r}(1 - s^{-t})$. The bound on the expected number of runs is the same computation as for the [quantum discrete logarithm](/quantum-discrete-logarithm/): $\mathbb{E}[T] \le 2 + \sum_{s \text{ prime}} 1/(s(s-1)) < 2.775$. For prime $r$, the run succeeds exactly when $c \ne 0$. $\square$

---
title: The quantum discrete logarithm algorithm returns log_g h and needs fewer than 2.775 runs on average
proves: [correctness]
status: full
---

We use the pseudocode of the page. $G = \langle g \rangle$ is a cyclic group of known order $r$, $h = g^x$ with $0 \le x < r$, and $\omega = e^{2\pi i/r}$. The Fourier transform $F_r$ of $\mathbb{Z}_r$ maps $|a\rangle$ to $r^{-1/2} \sum_{c=0}^{r-1} \omega^{ac} |c\rangle$. The oracle maps $|a\rangle|b\rangle|y\rangle$ to $|a\rangle|b\rangle|y \oplus f(a, b)\rangle$ with $f(a, b) = g^a h^{-b}$, where group elements have unique bit strings.

**Lemma 1 (the hidden subgroup).** $f(a, b) = f(a', b')$ if and only if $a - xb \equiv a' - xb' \pmod r$. So $f$ is constant on the cosets of $H = \{(xt, t) : t \in \mathbb{Z}_r\}$ in $\mathbb{Z}_r \times \mathbb{Z}_r$, and it takes distinct values on distinct cosets.

*Proof.* $f(a, b) = g^a g^{-xb} = g^{a - xb}$, and $g^u = g^{u'}$ if and only if $u \equiv u' \pmod r$, because $g$ has order $r$. The map $(a, b) \mapsto a - xb$ is a homomorphism onto $\mathbb{Z}_r$ with kernel $H$. $\square$

**Lemma 2 (the output distribution).** One run of lines L3 to L6 gives each pair $(c, d)$ with $d \equiv -xc \pmod r$ with probability exactly $1/r$, and the other pairs with probability 0.

*Proof.* Line L3 gives $r^{-1} \sum_{a, b} |a\rangle|b\rangle|0\rangle$, and line L4 gives $r^{-1} \sum_{a,b} |a\rangle|b\rangle|g^{a - xb}\rangle$. Group the terms by $s = a - xb \bmod r$. For a fixed $s$ the pairs are $(s + xb, b)$ with $b \in \mathbb{Z}_r$, so the state is $r^{-1} \sum_s \bigl(\sum_b |s + xb\rangle|b\rangle\bigr)|g^s\rangle$. After line L5 the amplitude of $|c\rangle|d\rangle|g^s\rangle$ is

$$\frac{1}{r^2} \sum_{b=0}^{r-1} \omega^{(s + xb)c + bd} = \frac{\omega^{sc}}{r^2} \sum_{b=0}^{r-1} \omega^{b(xc + d)}.$$

The geometric sum is $r$ if $xc + d \equiv 0 \pmod r$, and 0 otherwise, because then $\omega^{xc+d} \ne 1$ is an $r$-th root of unity. So the amplitude has modulus $1/r$ on the allowed pairs. Summing $1/r^2$ over the $r$ values of $s$ gives probability $1/r$ for each allowed pair. There are exactly $r$ allowed pairs, one for each $c$, so the total is 1. $\square$

In particular, $c$ is uniform on $\mathbb{Z}_r$, and $d$ is a function of $c$.

**Lemma 3 (one congruence).** For an allowed pair $(c, d)$, let $e = \gcd(c, r)$ and $m = r/e$. Then $e$ divides $d$, and the solutions of $cx' \equiv -d \pmod r$ are exactly the $x'$ with $x' \equiv x_0 \pmod m$, where $x_0 = (-d/e)(c/e)^{-1} \bmod m$. The true $x$ is one of them.

*Proof.* $x$ is a solution by Lemma 2, so $e$ divides $cx + d$ and $c$, hence $d$. Dividing by $e$, $cx' \equiv -d \pmod r$ holds if and only if $(c/e)x' \equiv -d/e \pmod m$. As $\gcd(c/e, m) = 1$, $c/e$ is invertible modulo $m$, and the solution set is one residue class modulo $m$. $\square$

**Lemma 4 (merging).** Lines L7 to L9 keep the invariant: $x \equiv x_\star \pmod M$, where $(x_\star, M)$ is the current state and $M = r/\gcd(c_1, \dots, c_t, r)$ after runs with outcomes $c_1, \dots, c_t$.

*Proof.* At the start $M = 1$, and $x \equiv 0 \pmod 1$. Each run adds the congruence $x \equiv x_0 \pmod{m}$ of Lemma 3, which the true $x$ satisfies. Two congruences that a common integer satisfies are compatible, so the [Chinese remainder theorem](/chinese-remainder-theorem/) for non-coprime moduli merges them into one congruence modulo $\mathrm{lcm}(M, m)$ with the same solution set. For each prime $s$, $v_s(\mathrm{lcm}_i\, r/e_i) = v_s(r) - \min_i v_s(e_i)$, and $\min_i v_s(e_i) = v_s(\gcd(e_1, \dots, e_t))$, so the merged modulus is $r/\gcd(e_1, \dots, e_t) = r/\gcd(c_1, \dots, c_t, r)$. $\square$

**Theorem 1 (correctness).** If the algorithm returns $x_\star$, then $g^{x_\star} = h$.

*Proof.* Line L10 ends the loop only when $M = r$ and the check $g^{x_\star} = h$ holds. By Lemma 4, $M = r$ already forces $x_\star = x$, so the check never fails on an exact machine; it guards against hardware errors. $\square$

**Theorem 2 (number of runs).** After $t$ runs, $M = r$ with probability exactly $\prod_{s \mid r} (1 - s^{-t})$, over the primes $s$ that divide $r$. The expected number of runs is less than $2.775$ for every $r$.

*Proof.* By Lemma 2, $c_1, \dots, c_t$ are independent and uniform on $\mathbb{Z}_r$. By Lemma 4, $M = r$ if and only if no prime $s \mid r$ divides all of $c_1, \dots, c_t$. By the [Chinese remainder theorem](/chinese-remainder-theorem/), the residues $c_i \bmod s$ for the different primes $s \mid r$ are independent and uniform, and $s$ divides a uniform $c_i$ with probability $1/s$. So the probability is $\prod_{s \mid r}(1 - s^{-t})$.

The number of runs $T$ satisfies $\mathbb{E}[T] = \sum_{t \ge 0} \Pr[T > t]$. Bound $\Pr[T > 0]$ and $\Pr[T > 1]$ by 1, and for $t \ge 2$ use the union bound $\Pr[T > t] \le \sum_{s \mid r} s^{-t}$. Then

$$\mathbb{E}[T] \le 2 + \sum_{s \text{ prime}} \sum_{t \ge 2} s^{-t} = 2 + \sum_{s \text{ prime}} \frac{1}{s(s - 1)}.$$

The terms for the primes $s \le 1000$ add up to less than $0.77303$, and the other terms add up to less than $\sum_{n > 1000} \frac{1}{n(n-1)} = \frac{1}{1000}$. So the sum is less than $0.7741$, and $\mathbb{E}[T] < 2.775$. $\square$

**Remark (when $r$ is prime).** Then every $c \ne 0$ is invertible, one run succeeds with probability $(r - 1)/r$, and $x = -d c^{-1} \bmod r$.

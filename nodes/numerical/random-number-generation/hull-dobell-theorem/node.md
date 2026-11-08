---
tag: P9CVWF
kind: theorem
slug: hull-dobell-theorem
name: Hull-Dobell theorem
aliases:
- full period theorem for linear congruential generators
area: numerical/random-number-generation
level: advanced
summary: An LCG s_(i+1) = (a s_i + c) mod m has full period m exactly when c is coprime to m, every prime factor of m divides a - 1, and 4 divides a - 1 when 4 divides m.
prereqs: [linear-congruential-generator, generator-period, greatest-common-divisor]
see_also: [multiplicative-order, primitive-root, chinese-remainder-theorem, park-miller-minimal-standard, marsaglia-hyperplane-theorem, jump-ahead]
sources:
  - book: isbn:9780201896848
    title: Donald E. Knuth, The Art of Computer Programming, Volume 2, Seminumerical Algorithms, third edition, 1997
    locator: Section 3.2.1.2, Choice of multiplier (Theorem A with its proof through Lemmas P, Q and R), and Section 3.2.1.3, Potency
  - paper: "T. E. Hull and A. R. Dobell, Random number generators, SIAM Review 4(3), 1962, pages 230 to 254"
    locator: the theorem on the conditions for full period of the mixed congruential method
  - paper: "Pierre L'Ecuyer, Uniform random number generation, Annals of Operations Research 53, 1994, pages 77 to 120"
    locator: the section on linear congruential generators and the conditions for full period
---

The Hull-Dobell theorem gives the exact conditions under which a [linear congruential generator](/linear-congruential-generator/) $s_{i+1} = (a s_i + c) \bmod m$ has full [period](/generator-period/) $m$, so that it visits every residue modulo $m$ once per cycle. The conditions only involve the prime factors of $m$, so they are checked in the time it takes to factor $m$. For the common modulus $m = 2^w$ they say: $c$ is odd and $a \equiv 1 \pmod 4$. Full period is a statement about the cycle only; it says nothing about the statistical quality of the outputs.

## Statement

**Theorem (Hull and Dobell 1962; Knuth, Section 3.2.1.2, Theorem A).** Let $m \ge 2$ and let $a$ and $c$ be integers. Let $f(s) = (a s + c) \bmod m$ on $S = \{0, 1, \ldots, m-1\}$. The following are equivalent.

1. The sequence $s_{i+1} = f(s_i)$ has period $m$ for some seed $s_0 \in S$.
2. It has period $m$ for every seed $s_0 \in S$.
3. All three conditions hold:
   - (i) $\gcd(c, m) = 1$;
   - (ii) every prime $p$ that divides $m$ divides $a - 1$;
   - (iii) if 4 divides $m$, then 4 divides $a - 1$.

We write $S_n(a) = 1 + a + \cdots + a^{n-1}$ for $n \ge 1$, and $v_p(x)$ for the exponent of the prime $p$ in a nonzero integer $x$.

## In plain words

A linear congruential generator multiplies the state, adds a constant and keeps the remainder. It runs through every possible remainder before it repeats only when three simple tests pass. The added constant must share no factor with the modulus. Each prime that divides the modulus must also divide the multiplier minus one. And if the modulus is a multiple of four, the multiplier minus one must be a multiple of four too.

When the modulus is a power of two, this means: the added constant is odd, and the multiplier leaves remainder one when divided by four. These tests are cheap. But passing them only means that no value is skipped; the numbers can still follow an obvious pattern.

## Proof

**Step 0: full period is a property of $f$.** If some seed has period $m$, the $m$ states of its cycle are all of $S$, so $f$ is one cycle through all of $S$, and every seed lies on it with period $m$. So 1 and 2 are equivalent, and $f$ is then a bijection. It remains to show that 1 holds if and only if (i), (ii) and (iii) hold.

**Step 1: the orbit of 0.** By induction, from $s_0 = 0$ we get $s_n \equiv c \, S_n(a) \pmod m$: indeed $s_1 = c$, and $a \cdot c S_n(a) + c = c\,(a + a^2 + \cdots + a^n + 1) = c\, S_{n+1}(a)$.

**Step 2: necessity of (i).** Let $d = \gcd(c, m)$. Every state reached from 0 is congruent to $c S_n(a)$ modulo $m$, a multiple of $d$, and a residue modulo $m$ of a multiple of $d$ is again a multiple of $d$ because $d \mid m$. So the orbit of 0 has at most $m/d$ states. If $d > 1$, the period from 0 is less than $m$, against step 0.

**Step 3: necessity of (ii).** Let $p$ be a prime that divides $m$ with $p \nmid a - 1$. Reduce modulo $p$: since $p \mid m$, the residues $y_n = s_n \bmod p$ satisfy $y_{n+1} = (a y_n + c) \bmod p$. Because $a - 1$ is invertible modulo $p$, the map $y \mapsto a y + c$ has the fixed point $y^* = -c (a-1)^{-1} \bmod p$. With full period, $s_n$ takes every value of $S$, so $y_n = y^*$ for some $n$, and then $y_k = y^*$ for all $k \ge n$. The sequence $s$ is purely periodic (step 0), so $y$ is purely periodic and therefore constant equal to $y^*$. But $s$ takes the values 0 and 1, whose residues modulo $p \ge 2$ differ. This is a contradiction.

**Step 4: necessity of (iii).** Let $4 \mid m$. By steps 2 and 3, $c$ and $a$ are odd. Suppose $a \equiv 3 \pmod 4$. Modulo 4, $y_{n+1} \equiv 3 y_n + c$, so $y_{n+2} \equiv 9 y_n + 3c + c = y_n + 4c \equiv y_n \pmod 4$. So $y$ takes at most two values modulo 4, but a full-period $s$ takes all four residues modulo 4. This is a contradiction, so $a \equiv 1 \pmod 4$.

**Step 5: two lemmas on $S_n(a)$.**

*Lemma A.* If $a \equiv 1 \pmod p$, then $S_n(a) \equiv n \pmod p$. *Proof:* each of the $n$ terms $a^j$ is $\equiv 1$.

*Lemma B.* Let $p$ be a prime and $a \equiv 1 \pmod p$; if $p = 2$, assume $a \equiv 1 \pmod 4$. Then $v_p(S_n(a)) = v_p(n)$ for all $n \ge 1$.

*Proof.* The identity $S_{uv}(a) = S_u(a) \cdot S_v(a^u)$ holds because both sides sum $a^{j}$ over $0 \le j < uv$, written as $j = i + u k$ with $0 \le i < u$ and $0 \le k < v$. Write $n = p^k n'$ with $p \nmid n'$. Then $S_n(a) = S_{p^k}(a) \, S_{n'}(a^{p^k})$. Since $a^{p^k} \equiv 1 \pmod p$, Lemma A gives $S_{n'}(a^{p^k}) \equiv n' \not\equiv 0 \pmod p$, so $v_p(S_n(a)) = v_p(S_{p^k}(a))$. We show $v_p(S_{p^k}(a)) = k$ by induction on $k$. For $k = 0$, $S_1 = 1$. For the step, $S_{p^{k+1}}(a) = S_{p^k}(a) \, S_p(b)$ with $b = a^{p^k}$, and $b \equiv 1 \pmod p$ (and $b \equiv 1 \pmod 4$ if $p = 2$). It suffices to show $v_p(S_p(b)) = 1$. Write $b = 1 + tp$. If $p$ is odd, the binomial theorem gives $b^j \equiv 1 + j t p \pmod{p^2}$, so $S_p(b) \equiv p + t p \cdot \frac{p(p-1)}{2} \equiv p \pmod{p^2}$, because $\frac{p-1}{2}$ is an integer. If $p = 2$, then $t$ is even and $S_2(b) = 1 + b = 2(1 + t)$ with $1 + t$ odd. In both cases $v_p(S_p(b)) = 1$. $\square$

**Step 6: sufficiency.** Assume (i), (ii) and (iii). Every prime factor of $m$ divides $a - 1$, so none divides $a$, and $\gcd(a, m) = 1$; thus $f$ is a bijection and the orbit of 0 is purely periodic. Its period is the least $n \ge 1$ with $s_n = 0$, that is, by step 1 and (i), the least $n \ge 1$ with $m \mid S_n(a)$. Let $p^e$ be the exact power of a prime $p$ in $m$. If $e = 1$, Lemma A and (ii) give: $p \mid S_n(a)$ if and only if $p \mid n$. If $e \ge 2$ and $p$ is odd, Lemma B applies by (ii). If $e \ge 2$ and $p = 2$, then $4 \mid m$, so (iii) gives $a \equiv 1 \pmod 4$ and Lemma B applies. In each case $p^e \mid S_n(a)$ if and only if $p^e \mid n$. Since the prime powers in $m$ are pairwise coprime, $m \mid S_n(a)$ if and only if $m \mid n$. So the least such $n$ is $m$, and the orbit of 0 has period $m$. $\blacksquare$

## Consequences

- **Power-of-two modulus.** For $m = 2^w$ with $w \ge 2$: full period if and only if $c$ is odd and $a \equiv 1 \pmod 4$. So exactly $2^{w-2} \cdot 2^{w-1}$ pairs $(a, c)$ in $[0, m)^2$ give full period; for $m = 256$ that is 8192 pairs, and for $m = 16$ it is 32.
- **Prime modulus.** For a prime $m = p$, condition (ii) forces $a \equiv 1 \pmod p$, so $a = 1$ and the generator is a counter. This is why prime moduli are used with $c = 0$ (the multiplicative generator), whose best period is $p - 1$, reached when $a$ is a [primitive root](/primitive-root/) modulo $p$.
- **Decimal modulus.** For $m = 10^k$ with $k \ge 2$: $c$ coprime to 10 and $a \equiv 1 \pmod{20}$.
- **Low-order bits.** With $m = 2^w$ and full period, the low $j$ bits form an LCG modulo $2^j$ that also satisfies the conditions (for $j \ge 2$), so they have period exactly $2^j$, and no more. This is the reason for the weak low bits.
- **Potency.** Knuth (Section 3.2.1.3) calls the least $s$ with $(a - 1)^s \equiv 0 \pmod m$ the potency. The conditions allow $a = 1$ (potency 1), which gives the counter $s_i = s_0 + i c$. A full-period multiplier should have potency at least 5 or so; the Hull-Dobell theorem does not exclude bad ones.
- **Jump-ahead and checks.** The proof gives the closed form $s_n = (a^n s_0 + c S_n(a)) \bmod m$, which is the basis of [jump-ahead](/jump-ahead/) for LCGs.

## Tightness

Each condition is necessary, and dropping any one gives a shorter period.

- **(i) fails.** $m = 16$, $a = 5$, $c = 2$: period 8 from seeds 0 and 1.
- **(ii) fails.** $m = 9$, $a = 2$, $c = 1$ (3 does not divide 1): period 6. $m = 12$, $a = 5$, $c = 1$ (3 does not divide 4): period 4.
- **(iii) fails.** $m = 16$, $a = 3$, $c = 1$: period 8. $m = 12$, $a = 7$, $c = 1$: $a - 1 = 6$ is divisible by 2 and 3 but not by 4, and the period is 6. For $m = 18 = 2 \cdot 9$, condition (iii) does not apply, and $a = 7$, $c = 1$ has period 18.
- **The lemma needs $a \equiv 1 \pmod 4$ at $p = 2$.** For $a = 3$, $S_4(3) = 40$ has $v_2 = 3$ while $v_2(4) = 2$.
- **Full period is not quality.** $a = 1$, $c = 1$ satisfies the conditions and outputs $0, 1, 2, \ldots$ A full period is necessary for a good mixed LCG but far from sufficient; the lattice of [Marsaglia's theorem](/marsaglia-hyperplane-theorem/) and the [spectral test](/spectral-test/) measure what it leaves out.

## History

Hull and Dobell proved the theorem for a general modulus in 1962, in a survey of random number generators in SIAM Review. Knuth (Section 3.2.1.2) gives it as Theorem A, proves it through Lemmas P, Q and R, and credits the special case of a power-of-two modulus to M. Greenberger (1961). The name "Hull-Dobell theorem" is common in textbooks.

## References

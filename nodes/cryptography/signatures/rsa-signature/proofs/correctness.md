---
title: RSA signatures verify, the CRT signer computes m^d mod N, and a fault in one CRT half reveals a factor
proves: [correctness]
status: full
---

We use the notation of the page. $N = pq$ with distinct primes $p$ and $q$, $\lambda(N) = \mathrm{lcm}(p - 1, q - 1)$, $ed \equiv 1 \pmod{\lambda(N)}$, $d_P = d \bmod (p - 1)$, $d_Q = d \bmod (q - 1)$ and $q_{\mathrm{inv}} = q^{-1} \bmod p$. $k$ is the length of $N$ in bytes.

**Lemma 1 (RSA is a permutation).** For every integer $m$ with $0 \le m < N$, $(m^d)^e \equiv m \pmod N$.

*Proof.* Write $ed = 1 + j\lambda(N)$ with an integer $j \ge 0$. Fix the prime $p$. If $p \mid m$, then both $m^{ed}$ and $m$ are $0 \bmod p$. Otherwise, $p - 1$ divides $\lambda(N)$, so by [Fermat's little theorem](/fermat-little-theorem/) $m^{ed} = m \cdot (m^{p-1})^{j\lambda(N)/(p-1)} \equiv m \pmod p$. The same argument gives $m^{ed} \equiv m \pmod q$. Since $p \ne q$ are primes, the [Chinese remainder theorem](/chinese-remainder-theorem/) gives $m^{ed} \equiv m \pmod N$. $\square$

**Lemma 2 (the CRT signer).** Lines L7 to L9 return $s = m^d \bmod N$.

*Proof.* Let $s_1 = m^{d_P} \bmod p$ and $s_2 = m^{d_Q} \bmod q$. If $p \nmid m$, then $m^d = m^{d_P} \cdot (m^{p-1})^{\lfloor d/(p-1) \rfloor} \equiv m^{d_P} \pmod p$ by Fermat; if $p \mid m$, both sides are $0 \bmod p$ when $d_P \ge 1$, which holds because $d$ is odd and $p - 1$ is even. So $m^d \equiv s_1 \pmod p$, and in the same way $m^d \equiv s_2 \pmod q$. Line L8 sets $h = q_{\mathrm{inv}} (s_1 - s_2) \bmod p$, so $0 \le h < p$, and line L9 sets $s = s_2 + qh$. Then $s \equiv s_2 \pmod q$, and $s \equiv s_2 + q q_{\mathrm{inv}} (s_1 - s_2) \equiv s_2 + (s_1 - s_2) = s_1 \pmod p$. Also $0 \le s \le (q - 1) + q(p - 1) = N - 1$. The CRT says that exactly one integer in $[0, N)$ has these two residues, and $m^d \bmod N$ is such an integer, so $s = m^d \bmod N$. $\square$

**Theorem 1 (correctness).** For every message $M$ and every hash $H$ with DigestInfo encoding $T$ such that $k \ge |T| + 11$, VERIFY$(N, e, M, \mathrm{SIGN}(K, M))$ returns valid.

*Proof.* SIGN computes $EM$ of exactly $k$ bytes (line L5: $2 + (k - |T| - 3) + 1 + |T| = k$), whose first byte is 0. So $m = \mathrm{OS2IP}(EM) < 256^{k-1} \le N$, since $N$ has $k$ bytes and its leading byte is not 0. By Lemma 2, $s = m^d \bmod N$, so $0 \le s < N$ and I2OSP$(s, k)$ is defined; this is $S$, of length $k$. VERIFY passes lines L11 and L12, because $|S| = k$ and $s < N$. Line L13 gives $s^e \bmod N = m^{de} \bmod N = m$ by Lemma 1. Line L14 gives back $EM$, because I2OSP and OS2IP are inverse on strings of length $k$. Line L15 computes the encoding of $M$ again, which is a deterministic function of $M$ and $k$, so $EM' = EM$, and line L16 returns valid. $\square$

**Lemma 3 (rejection is exact).** VERIFY returns valid if and only if $|S| = k$, $s = \mathrm{OS2IP}(S) < N$ and $s^e \bmod N = \mathrm{OS2IP}(\mathrm{EMSA}(M))$.

*Proof.* Lines L11 and L12 return invalid exactly when the first two conditions fail. When they hold, I2OSP$(s^e \bmod N, k)$ is the unique string of length $k$ whose integer is $s^e \bmod N$, and line L16 compares it with $EM'$ of the same length, so equality of the strings is equality of the integers. $\square$

Lemma 3 is why the verifier never parses the decoded block: it accepts exactly one value of $s^e \bmod N$ for each message. A verifier that parses the block and ignores bytes after the hash accepts many values, which the $e = 3$ forgery on the [chosen-message attack](/chosen-message-attack/) page exploits.

**Lemma 4 (the fault attack).** Suppose that line L7 returns a wrong value $s_1' \not\equiv m^{d_P} \pmod p$ and a correct $s_2$, and let $s'$ be the output of line L9. Then $\gcd(s'^e - m \bmod N, N) = q$.

*Proof.* By the computation in Lemma 2, $s' \equiv s_2 \equiv m^d \pmod q$, so $s'^e \equiv m^{de} \equiv m \pmod q$ by the argument of Lemma 1 restricted to $q$, and $q \mid s'^e - m$. Also $s' \equiv s_1' \pmod p$. Suppose $s'^e \equiv m \pmod p$. Raise both sides to the power $d_P$: $s'^{e d_P} \equiv m^{d_P} \pmod p$. Since $e d_P \equiv ed \equiv 1 \pmod{p - 1}$, Fermat gives $s'^{e d_P} \equiv s' \pmod p$ (for $p \nmid s'$; if $p \mid s'$ then $p \mid m$ and both $s'$ and $m^{d_P}$ are $0 \bmod p$, so $s_1' \equiv m^{d_P}$). Either way $s_1' \equiv m^{d_P} \pmod p$, a contradiction. So $p \nmid s'^e - m$, and the gcd with $N = pq$ is exactly $q$. $\square$

The symmetric statement holds for a fault in $s_2$, which reveals $p$. Checking $s^e \bmod N = m$ before the output, as `sign_checked` does, stops this attack, because by Lemma 4 a faulty $s'$ never passes the check.

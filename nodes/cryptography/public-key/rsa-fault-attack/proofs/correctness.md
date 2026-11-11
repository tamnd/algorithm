---
title: "One faulty CRT signature factors the modulus, and the two countermeasures are sound"
proves: [correctness]
status: full
---

Let $p \ne q$ be odd primes, $N = pq$, $\lambda(N) = \mathrm{lcm}(p-1, q-1)$, and let $e$ with $\gcd(e, \lambda(N)) = 1$ and $d$ with $ed \equiv 1 \pmod{\lambda(N)}$ be the exponents. Let $d_p = d \bmod (p-1)$, $d_q = d \bmod (q-1)$ and $qInv = q^{-1} \bmod p$. Fix a message representative $m$ with $0 \le m < N$, and write $s = m^d \bmod N$ for the correct signature.

The signer of the page computes $s_p = m^{d_p} \bmod p$, $s_q = m^{d_q} \bmod q$, $h = (s_p - s_q) qInv \bmod p$ and returns $(s_q + qh) \bmod N$. Its correctness, that the output is $s$, is Theorem 2 of the [RSA correctness proof](/rsa-cryptosystem/), and it is not repeated here.

**Definition (a fault in one half).** A run of the signer is *faulty in the half modulo $p$* when the value that enters the recombination in place of $s_p$ is some $\tilde{s}_p \ne s_p$ with $0 \le \tilde{s}_p < p$, while the value in place of $s_q$ is $s_q$. The output of such a run is written $s'$. The definition covers every cause: a changed $d_p$, a changed modulus inside the half, a changed intermediate square, or a changed stored result, because all of them reach the recombination as one wrong residue. The case of a fault in the half modulo $q$ is symmetric throughout.

**Lemma 1 (the good half survives).** If a run is faulty in the half modulo $p$, then $s' \equiv s \pmod q$ and $s' \not\equiv s \pmod p$.

*Proof.* The recombination returns $(s_q + qh) \bmod N$ with $h$ reduced modulo $p$, for whatever pair of residues it is given. Modulo $q$ the term $qh$ vanishes, so $s' \equiv s_q \pmod q$, and the same computation for the correct run gives $s \equiv s_q \pmod q$; the two agree. Modulo $p$ we get $s' \equiv s_q + q \cdot (\tilde{s}_p - s_q) q^{-1} \equiv \tilde{s}_p \pmod p$, and likewise $s \equiv s_p \pmod p$. By the definition $\tilde{s}_p \ne s_p$, and both lie in $[0, p)$, so they differ modulo $p$. $\square$

**Lemma 2 (the public exponent transports the agreement).** With the notation of Lemma 1, $q$ divides $s'^e - m$.

*Proof.* By Lemma 1, $s' \equiv s \pmod q$, so $s'^e \equiv s^e \pmod q$. Now $s \equiv m^d \pmod N$ gives $s^e \equiv m^{ed} \pmod N$ and hence modulo $q$. Because $q - 1$ divides $\lambda(N)$ and $ed = 1 + k\lambda(N)$ for some integer $k \ge 0$, Lemma 1 of the RSA correctness proof gives $m^{ed} \equiv m \pmod q$, for every $m$, including the multiples of $q$. So $s'^e \equiv m \pmod q$. $\square$

**Lemma 3 (and $p$ does not, except in one accident).** With the notation of Lemma 1, $p$ divides $s'^e - m$ if and only if $\tilde{s}_p^e \equiv m \pmod p$.

*Proof.* By Lemma 1, $s' \equiv \tilde{s}_p \pmod p$, so $s'^e \equiv \tilde{s}_p^e \pmod p$. $\square$

Because $x \mapsto x^e$ is a bijection modulo $p$ (its inverse is $x \mapsto x^{d_p}$), the condition $\tilde{s}_p^e \equiv m \pmod p$ holds for exactly one residue $\tilde{s}_p$, namely the correct $s_p$, which the definition of a fault excludes. So for a fault in one half the condition of Lemma 3 *never* holds, and $p \nmid s'^e - m$. If the fault model is weakened, so that the faulty value may be any element of $[0, p)$ drawn without the attacker's control, the probability of landing on $s_p$ is $1/p$, which is below $2^{-500}$ for a modulus of 2048 binary digits.

**Theorem 4 (the attack is correct).** Let $s'$ be the output of a run faulty in exactly one half, and suppose $s'^e \not\equiv m \pmod N$. Then line 2 of BELLCORE-ATTACK returns the prime whose half was computed correctly, line 4 returns the other prime, and line 5 returns a valid private exponent for $(N, e)$.

*Proof.* Say the fault was in the half modulo $p$; the other case swaps the names. Write $x = s'^e - m$. Since $\gcd(x \bmod N, N) = \gcd(x, N)$, line 2 computes $\gcd(x, N)$. The divisors of $N = pq$ are $1, p, q, N$. By Lemma 2, $q \mid x$. By Lemma 3 together with the paragraph above, $p \nmid x$, so $N \nmid x$ and $p \nmid \gcd(x, N)$. The only remaining divisor that $q$ divides is $q$ itself, so $\gcd(x, N) = q$, which is the prime of the half that was correct. Line 3 therefore does not return FAILURE, because $q \notin \{1, N\}$. Line 4 computes $N/q = p$. Line 5 computes $e^{-1} \bmod \mathrm{lcm}(q-1, p-1)$, which exists because $\gcd(e, \lambda(N)) = 1$, and any such value $d^*$ satisfies $ed^* \equiv 1 \pmod{\lambda(N)}$, so by Theorem 1 of the RSA correctness proof $x^{ed^*} \equiv x \pmod N$ for every $x$. It is a private exponent for the key. $\blacksquare$

**Theorem 5 (the hypothesis of Theorem 4 is checkable).** Line 1 of the attack returns FAILURE exactly when $s'^e \equiv m \pmod N$, which by Lemma 1 and Lemma 3 happens for a one-half fault only in the excluded accident, and happens always when no fault occurred. So the attack never returns a wrong factorization: when it returns a triple, that triple is the factorization and a private exponent.

*Proof.* The returned $g$ is a nontrivial divisor of $N$ by line 3, and $N$ has exactly two of them, $p$ and $q$. $\square$

**Theorem 6 (the difference form).** If $s$ and $s'$ are the correct and the faulty signature of the same message, with the fault in the half modulo $p$, then $\gcd(s - s', N) = q$.

*Proof.* Lemma 1 gives $q \mid s - s'$ and $p \nmid s - s'$. As in Theorem 4, the only divisor of $N$ that this allows is $q$. $\square$

**Theorem 7 (verification before output is sound).** SIGN-CRT-VERIFIED returns a value only when $s^e \equiv m \pmod N$. In that case the value is the correct signature, and no run that is faulty in one half returns a value.

*Proof.* The map $x \mapsto x^e \bmod N$ is a bijection on $\{0, 1, \ldots, N-1\}$, with inverse $x \mapsto x^d \bmod N$, by Theorem 1 of the RSA correctness proof. So $s^e \equiv m \pmod N$ and $0 \le s < N$ force $s = m^d \bmod N$, the correct signature. For the second part, a run faulty in one half gives an output $s'$ with $s'^e \not\equiv m \pmod p$ by Lemma 3, hence $s'^e \not\equiv m \pmod N$, and the check fails. $\blacksquare$

The proof assumes that the check itself runs without a fault, and that it reads an uncorrupted copy of $N$ and $e$. Both assumptions are part of the countermeasure, not of the mathematics.

**Theorem 8 (Shamir's trick detects any fault that one half shows modulo $r$).** Let $r$ be a prime with $\gcd(r, N) = 1$. In a correct run, $m^d \bmod pr$ and $m^d \bmod qr$ are congruent modulo $r$, so the check of line 9 passes and line 10 returns the correct signature. In a run where the value in place of $s_p^* = m^d \bmod pr$ is some $\tilde{s} \not\equiv s_p^* \pmod r$, the check fails.

*Proof.* For the first part, reduce both values modulo $r$: each is $m^d \bmod r$, because $r \mid pr$ and $r \mid qr$. Line 10 then recombines $s_p^* \bmod p = m^d \bmod p$ and $s_q^* \bmod q = m^d \bmod q$, which by the correctness of the CRT signer is the correct signature. The second part is the definition of the check. $\square$

The trick therefore misses exactly the faults that leave the half unchanged modulo $r$, which for a random fault happens with probability about $1/r$, and the faults that happen after the comparison. It needs no public exponent, which is the reason it exists.

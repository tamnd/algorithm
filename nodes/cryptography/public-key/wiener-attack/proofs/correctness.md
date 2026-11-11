---
title: "Wiener's attack returns the factorization exactly when it returns, and it always returns for d below N^(1/4)/3"
proves: [correctness]
status: full
---

Let $p > q$ be odd primes, $N = pq$, $\varphi(N) = (p-1)(q-1)$, and let $e, d$ be integers with $1 < e < \varphi(N)$, $1 < d < \varphi(N)$ and $ed \equiv 1 \pmod{\varphi(N)}$. Define

$$k = \frac{ed - 1}{\varphi(N)} ,$$

which is a positive integer because $ed > 1$ and $\varphi(N) \mid ed - 1$. The attack sees $(N, e)$ only.

## Part 1. Soundness

**Theorem 1.** If WIENER-ATTACK$(N, e)$ returns a triple $(P, Q, D)$, then $PQ = N$ with $P$ and $Q$ the two prime factors of $N$, and $eD \equiv 1 \pmod{\varphi(N)}$.

*Proof.* Line 11 returns only when $PQ = N$ with $P = (s + \sqrt{D_{\mathrm{isc}}})/2$ and $Q = (s - \sqrt{D_{\mathrm{isc}}})/2$ for the integers of lines 6 to 10, so $P$ and $Q$ are integers whose product is $N$. Both are at least 2: line 9 accepted a perfect square and line 11 accepted the product, and a factor 1 would force the other to be $N$ and then $s = N + 1$, hence $f = 0$ in line 5, which is impossible because $f = (eD-1)/k \ge 1$ for $eD > 1$. So $\{P, Q\}$ is a nontrivial factorization of $N = pq$, which has only one, namely $\{p, q\}$.

For the exponent, $s = P + Q = p + q$ and line 6 gives $f = N - s + 1 = pq - p - q + 1 = \varphi(N)$. Line 5 says $eD - 1 = k' f$ for the integer $k'$ of the candidate, so $eD \equiv 1 \pmod{\varphi(N)}$. $\blacksquare$

So the attack never lies, for every key and every public exponent. Everything below is about when it also *finds* something.

## Part 2. The approximation

**Lemma 2.** $\gcd(k, d) = 1$.

*Proof.* $ed - k\varphi(N) = 1$, so any common divisor of $k$ and $d$ divides 1. $\square$

**Lemma 3.** $k < d$.

*Proof.* $k\varphi(N) = ed - 1 < ed < \varphi(N) d$, using $e < \varphi(N)$. Divide by $\varphi(N) > 0$. $\square$

**Lemma 4.** If $q < p < 2q$, then $p + q < 3\sqrt{N}$.

*Proof.* From $p < 2q$ and $pq = N$ we get $N = pq < 2q^2$, so $q > \sqrt{N/2}$, and from $q < p$ we get $q^2 < N$, so $q < \sqrt{N}$. Write $g(x) = N/x + x$, so $p + q = g(q)$. On the interval $(0, \sqrt{N})$ the derivative $g'(x) = 1 - N/x^2$ is negative, so $g$ is strictly decreasing there. Since $q \in (\sqrt{N/2}, \sqrt{N})$,

$$p + q = g(q) < g\left(\sqrt{N/2}\right) = \sqrt{2N} + \sqrt{N/2} = \left(\sqrt 2 + \tfrac{1}{\sqrt 2}\right)\sqrt N < 2.122\sqrt N < 3\sqrt N . \qquad \square$$

**Theorem 5.** If $q < p < 2q$ and $d < N^{1/4}/3$, then

$$\left| \frac{e}{N} - \frac{k}{d} \right| < \frac{1}{2d^2} .$$

*Proof.* Multiply out the difference and use $ed = 1 + k\varphi(N)$:

$$\left| \frac{e}{N} - \frac{k}{d} \right| = \frac{|ed - kN|}{Nd} = \frac{|1 + k\varphi(N) - kN|}{Nd} = \frac{|1 - k(N - \varphi(N))|}{Nd} .$$

Now $N - \varphi(N) = pq - (p-1)(q-1) = p + q - 1 \ge 2$ and $k \ge 1$, so $k(N - \varphi(N)) \ge 2 > 1$ and the absolute value is $k(p + q - 1) - 1 < k(p+q)$. With Lemma 4,

$$\left| \frac{e}{N} - \frac{k}{d} \right| < \frac{k(p+q)}{Nd} < \frac{3k\sqrt N}{Nd} = \frac{3k}{d\sqrt N} .$$

It remains to show $3k/(d\sqrt N) \le 1/(2d^2)$, which after multiplying by $2d^2\sqrt{N}/1 > 0$ is $6kd \le \sqrt N$. By Lemma 3 and the hypothesis, $6kd < 6d^2 < 6 \cdot N^{1/2}/9 = \tfrac{2}{3}\sqrt N < \sqrt N$. The inequality is strict throughout. $\blacksquare$

**Theorem 6 (Legendre's criterion).** Let $x$ be a real number and let $a/b$ be a fraction in lowest terms with $b \ge 1$ and $|x - a/b| < 1/(2b^2)$. Then $a/b$ is a convergent of the continued fraction expansion of $x$.

This is the classical statement; see Khinchin, Chapter II, or the [continued fraction convergents](/continued-fraction-convergents/) page, item 7. It is used here as a black box.

**Corollary 7 (completeness).** If $q < p < 2q$ and $d < N^{1/4}/3$, then the pair $(k, d)$ appears as a convergent of $e/N$ in the loop of line 2.

*Proof.* The fraction $k/d$ is in lowest terms by Lemma 2 and $d \ge 1$. Theorem 5 gives the hypothesis of Theorem 6 with $x = e/N$, so $k/d$ is a convergent of $e/N$. Line 1 computes the expansion of $e/N$ exactly, by Euclid's algorithm on the integers $e$ and $N$, and line 2 enumerates every convergent of it, so the pair is reached. $\square$

## Part 3. The recovery from the right candidate

**Theorem 8.** When the loop reaches the true pair $(k, d)$, the body of the loop returns $(p, q, d)$.

*Proof.* Line 3 passes: $k \ge 1$, and $d$ is odd because $\gcd(d, \varphi(N)) = 1$ while $\varphi(N) = (p-1)(q-1)$ is even. Line 4 passes because $ed - 1 = k\varphi(N)$ is a multiple of $k$, and line 5 sets $f = \varphi(N)$. Line 6 sets $s = N - \varphi(N) + 1 = p + q$, which is even, since $p$ and $q$ are odd, and positive, so line 7 passes. Line 8 sets

$$D_{\mathrm{isc}} = (p+q)^2 - 4pq = (p - q)^2 ,$$

a perfect square, so line 9 passes, and its exact integer square root is $p - q$, which is positive by $p > q$. Line 10 returns $(s + (p-q))/2 = p$ and $(s - (p-q))/2 = q$. Their product is $N$, so line 11 returns $(p, q, d)$. $\blacksquare$

**Theorem 9 (correctness).** For every public key $(N, e)$ with $1 < e < \varphi(N)$: the attack returns FAILURE or a true factorization with a valid private exponent (Theorem 1), and if in addition $q < p < 2q$ and $d < N^{1/4}/3$, it returns a true factorization (Corollary 7 and Theorem 8). $\blacksquare$

Three remarks on the hypotheses.

- **The loop can return early.** A convergent that is not the true pair can pass all the filters, including line 11, only if it yields a factorization of $N$; by Theorem 1 that answer is correct as well, and the attack is still right. The private exponent it reports is then some $D$ with $eD \equiv 1 \pmod{\varphi(N)}$, which is as useful as $d$ itself.
- **$\varphi(N)$, not $\lambda(N)$.** The proof uses $ed \equiv 1 \pmod{\varphi(N)}$. If the key was built with $ed \equiv 1 \pmod{\lambda(N)}$, where $\lambda(N) = \varphi(N)/g$ with $g = \gcd(p-1, q-1)$, then line 5 gives a multiple of $\lambda(N)$ that is $\varphi(N)/t$ for some divisor $t$ of $g$, and line 6 then fails unless $t = 1$. For random primes $g$ is small, so an implementation that also tries $f, 2f, \ldots, 2^{20} f$ covers the usual cases. The code of this page builds its keys with $\varphi(N)$.
- **The bound is not necessary.** The chain of inequalities in Theorem 5 is loose at $p + q < 3\sqrt N$ (the truth is $2.122\sqrt N$ at worst) and at $k < d$ (typically $k$ is close to $ed/\varphi(N)$, which is smaller). So keys above the bound often fall too, which is the content of the Boneh and Durfee result and of the extensions that search near each convergent.

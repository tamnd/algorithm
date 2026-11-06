---
title: Baillie-PSW never rejects a prime and always terminates
proves: [correctness, termination]
status: full
---

We use the pseudocode BAILLIE-PSW$(n)$ of the page. The claim proved here is the part of correctness that is known: the answer false is always right, and the call ends. That no composite returns true is an open problem, checked by computer for $n < 2^{64}$ only.

**Lemma 1 (the doubling formulas).** Let $\alpha, \beta$ be the roots of $x^2 - Px + Q$ in a commutative ring where $\alpha - \beta$ is a unit, with $D = (\alpha - \beta)^2 = P^2 - 4Q$. Then $U_k = (\alpha^k - \beta^k)/(\alpha - \beta)$ and $V_k = \alpha^k + \beta^k$, and
$$U_{2k} = U_k V_k, \quad V_{2k} = V_k^2 - 2Q^k, \quad 2U_{k+1} = P U_k + V_k, \quad 2V_{k+1} = D U_k + P V_k.$$
The same identities hold for the integer sequences, and hence modulo $n$.

*Proof.* Both closed forms satisfy the recurrence $X_{k+1} = P X_k - Q X_{k-1}$, since $\alpha$ and $\beta$ are roots of $x^2 - Px + Q$, and they agree with $U_0 = 0$, $U_1 = 1$, $V_0 = 2$, $V_1 = P$. Then $U_k V_k = (\alpha^{2k} - \beta^{2k})/(\alpha - \beta) = U_{2k}$, and $V_k^2 = \alpha^{2k} + \beta^{2k} + 2(\alpha\beta)^k = V_{2k} + 2Q^k$. With $\alpha + \beta = P$: $P U_k + V_k = ((\alpha + \beta)(\alpha^k - \beta^k) + (\alpha - \beta)(\alpha^k + \beta^k))/(\alpha - \beta) = 2(\alpha^{k+1} - \beta^{k+1})/(\alpha - \beta) = 2U_{k+1}$, and $D U_k + P V_k = (\alpha - \beta)(\alpha^k - \beta^k) + (\alpha + \beta)(\alpha^k + \beta^k) = 2V_{k+1}$. For the integer sequences, take $\alpha, \beta$ in the complex numbers: they are distinct since $D \ne 0$ (each $D$ of the page is $\equiv 1 \pmod 4$), so the identities hold for the integers $U_k$ and $V_k$, and reducing them gives them modulo $n$. In any ring as in the statement, the reductions of the integer sequences satisfy the same recurrence and initial values as the closed forms, so they are equal to them. $\square$

So line L11, which reads the binary digits of $d$ and applies the doubling step and, for a digit 1, the step $k \to k + 1$ with the halving done by the inverse of 2 modulo the odd $n$, computes $U_d$, $V_d$ and $Q^d$ modulo $n$. Lines L13 to L15 compute $V_{2^r d}$ for $r = 1, \ldots, s - 1$, with $W = Q^{2^{r-1} d}$ before each pass.

**Lemma 2 (primes pass the strong test).** If $n$ is an odd prime, $n$ passes the strong test of line L3.

*Proof.* Write $n - 1 = 2^t e$ with $e$ odd. By Fermat's little theorem $2^{2^t e} \equiv 1 \pmod n$. Modulo a prime the only square roots of 1 are $\pm 1$. So in the sequence $2^e, 2^{2e}, \ldots, 2^{2^t e}$, either the first term is 1, or the term before the first 1 is $-1$, with index $r < t$. $\square$

**Lemma 3 (primes pass the strong Lucas test).** Let $n$ be an odd prime, let $D$ be an integer with $\left(\frac{D}{n}\right) = -1$, $P = 1$ and $Q = (1 - D)/4$. Write $n + 1 = 2^s d$ with $d$ odd. Then $U_d \equiv 0$, or $V_{2^r d} \equiv 0 \pmod n$ for some $0 \le r < s$.

*Proof.* Since $D$ is a quadratic non-residue modulo $n$, $\mathbb{F}_n(\sqrt D) = \mathbb{F}_n[x]/(x^2 - D)$ is a field with $n^2$ elements. Also $n \nmid Q$: if $n \mid Q$, then $D = 1 - 4Q \equiv 1$, a square. In this field put $\alpha = (1 + \sqrt D)/2$ and $\beta = (1 - \sqrt D)/2$, the roots of $x^2 - x + Q$; then $\alpha - \beta = \sqrt D \ne 0$ and $\alpha \beta = Q \ne 0$. The map $z \mapsto z^n$ is a ring map of the field that fixes $\mathbb{F}_n$, and by Euler's criterion $(\sqrt D)^n = D^{(n-1)/2} \sqrt D = -\sqrt D$. So $\alpha^n = \beta$ and $\alpha^{n+1} = \alpha \beta = Q$; likewise $\beta^{n+1} = Q$. Let $\gamma = \alpha / \beta$. Then $\gamma^{n+1} = 1$. By Lemma 1, $U_k \equiv 0 \pmod n$ if and only if $\alpha^k = \beta^k$, that is $\gamma^k = 1$; and $V_k \equiv 0$ if and only if $\alpha^k = -\beta^k$, that is $\gamma^k = -1$. In the sequence $\gamma^d, \gamma^{2d}, \ldots, \gamma^{2^s d} = 1$, either the first term is 1, so $U_d \equiv 0$, or there is a first index $r + 1 \le s$ with $\gamma^{2^{r+1} d} = 1$; then $\gamma^{2^r d}$ is a square root of 1 in a field other than 1, so it is $-1$ and $V_{2^r d} \equiv 0$, with $r < s$. $\square$

**Lemma 4 (the search for $D$ ends).** Let $n \ge 3$ be odd and not a perfect square. Then some $D$ in the sequence $5, -7, 9, -11, \ldots$ has $\left(\frac{D}{n}\right) = -1$.

*Proof.* The sequence consists of all integers $D \equiv 1 \pmod 4$ with $|D| \ge 5$. For such $D$ and odd $m = |D|$, the Jacobi symbol satisfies $\left(\frac{D}{n}\right) = \left(\frac{n}{m}\right)$: for $D = m > 0$ with $m \equiv 1 \pmod 4$ this is quadratic reciprocity; for $D = -m$ with $m \equiv 3 \pmod 4$, $\left(\frac{-m}{n}\right) = \left(\frac{-1}{n}\right)\left(\frac{m}{n}\right) = (-1)^{(n-1)/2} \cdot (-1)^{(n-1)/2} \left(\frac{n}{m}\right) = \left(\frac{n}{m}\right)$. So it is enough to find an odd $m \ge 5$ with $\left(\frac{n}{m}\right) = -1$. As $n$ is not a square, some prime $q$ divides $n$ to an odd power $q^a$; write $n = q^a n'$ with $q \nmid n'$. Take a quadratic non-residue $c$ modulo $q$, and by the Chinese remainder theorem an $m \ge 5$ with $m \equiv c \pmod q$ and $m \equiv 1 \pmod{4n'}$. Then $m$ is odd, $m \equiv 1 \pmod 4$, and by reciprocity $\left(\frac{n}{m}\right) = \left(\frac{m}{n}\right) = \left(\frac{m}{q}\right)^a \left(\frac{m}{n'}\right) = (-1)^a \cdot 1 = -1$. $\square$

**Theorem.** For every integer $n$, BAILLIE-PSW$(n)$ terminates, and if $n$ is prime it returns true. Equivalently, every answer false is right.

*Proof.* *Termination.* Lines L1 to L4 end. If the call reaches line L5, then $n > 97$ is odd and not a square, so by Lemma 4 the loop of lines L6 to L8 meets a $D$ with $\left(\frac{D}{n}\right) = -1$ after finitely many steps, unless it returns earlier at line L7. Lines L10 to L16 run a bounded number of steps.

*Primes return true.* Let $n$ be prime. If $n \le 97$, line L2 returns true at $p = n$, and no smaller prime divides $n$. If $n > 97$, no prime $p \le 97$ divides $n$, so line L2 passes. By Lemma 2, line L3 passes. A prime is not a square, so line L4 passes. In the loop, $\left(\frac{D}{n}\right) = 0$ means $n \mid D$, so $|D| \ge n$ and line L7 does not return. So the loop ends with $\left(\frac{D}{n}\right) = -1$, and by Lemma 1 lines L11 to L15 compute $U_d$ and $V_{2^r d}$ modulo $n$ for $r < s$. By Lemma 3 one of them is 0, so line L12 or line L15 returns true, and line L16 is not reached.

*False is right.* Line L1 returns false only for $n < 2$; line L2 only when a prime $p \ne n$ divides $n$; line L4 only for a square $n > 1$; line L7 only when $1 < \gcd(|D|, n) \le |D| < n$. Lines L3 and L16 are not reached by primes, by the argument above. $\blacksquare$

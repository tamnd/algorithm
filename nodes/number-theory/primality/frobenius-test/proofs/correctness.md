---
title: The Frobenius test never rejects a prime, and its false answers are proofs
proves: [correctness, termination]
status: full
---

We use the pseudocode FROBENIUS$(n)$ of the page, with $B = 50000$, $f(x) = x^2 - ax + b$ and $\Delta = a^2 - 4b$. For an odd $n$, $(\cdot / n)$ is the Jacobi symbol. We prove that the test ends with probability 1, that it returns true for every prime, and that every false answer is right. The bound $1/7710$ on the probability that a composite passes is Grantham's theorem (Journal of Number Theory 72, 1998; Crandall and Pomerance, Theorem 3.6.10) and is quoted, not proved, here.

**Lemma 1 (trial division).** Lines L1 to L3 return true only for primes and false only for non-primes, and they return for every $n < (B + 1)^2$.

*Proof.* Line L1 returns false for $n < 2$. In line L2 the primes $q \le B$ are tried in increasing order. If $q \mid n$ is found, the answer is $n = q$, which is right: a prime $n$ has no prime divisor other than itself, and a composite $n$ with $q \mid n$ is not $q$. If $q^2 > n$ is reached first, no prime below $q$ divides $n$, so $n$ has no prime factor up to $\sqrt n$, and $n \ge 2$ is prime. If the loop ends without a return, no prime up to $B$ divides $n$; if then $n < (B + 1)^2$, any prime factor $p \le \sqrt n$ would have $p \le B$, so there is none and $n$ is prime, as line L3 returns. $\square$

From now on, $n \ge (B + 1)^2$, $n$ has no prime factor up to $B$, and in particular $n$ is odd.

**Lemma 2 (squares).** Line L4 returns false only for a composite. If $n$ passes line L4, there is an integer $D$ with $(D / n) = -1$ such that $D$, $D - 1$ and $D + 1$ are all coprime to $n$.

*Proof.* A square $n = m^2$ with $n > 1$ is composite. If $n$ is not a square, some prime $p$ divides $n$ to an odd power $e$; write $n = p^e m$ with $p \nmid m$. As $p > B$, there are $(p - 1)/2 \ge 2$ quadratic non-residues modulo $p$, so one of them, $\delta$, has $\delta \not\equiv -1 \pmod p$; also $\delta \not\equiv 0, 1$, as 0 and 1 are not non-residues. By the Chinese remainder theorem take $D \equiv \delta \pmod p$ and $D \equiv 4 \pmod m$. Then $(D / n) = (D / p)^e (D / m) = (-1)^e (2 / m)^2 = -1$. Modulo $p$ the numbers $D, D - 1, D + 1$ are nonzero by the choice of $\delta$, and modulo every prime $\ell \mid m$ they are $4, 3, 5$, which are nonzero as $\ell > B$. So all three are coprime to $n$. $\square$

**Lemma 3 (line L5 ends).** If $n$ passes line L4, the random search of line L5 ends with probability 1.

*Proof.* Take $D$ as in Lemma 2. As $n$ is odd, 2 and 4 are invertible modulo $n$; let $a$ and $c$ in $[0, n)$ be the residues of $(1 + D)/2$ and $(D - 1)/4$, and let $b$ be the residue of $c^2$. By Lemma 2, $a$, $c$ and $b$ are units modulo $n$, so $a, b \in [1, n)$. Then $\Delta = a^2 - 4b \equiv \frac{(1 + D)^2 - (D - 1)^2}{4} = D \pmod n$, so $(\Delta / n) = -1$ and $\gcd(\Delta, n) = 1$, and $(b / n) = (c / n)^2 = 1$ with $\gcd(b, n) = 1$. So $(a, b)$ is an allowed pair. Each try draws it with probability $1/(n - 1)^2 > 0$, independently of the other tries, so with probability 1 some try ends the search, at this pair or earlier. $\square$

**Lemma 4 (line L6).** If line L6 returns false, $n$ is composite.

*Proof.* A divisor $d$ of $n$ with $1 < d < n$ exists. $\square$

**Lemma 5 (the field).** Let $n$ be an odd prime, and let $a, b$ be integers with $(\Delta / n) = -1$ and $(b / n) = 1$. Let $R = \mathbb{Z}_n[x]/(f)$ and write $x$ for the class of $x$ in $R$. Then:
1. $R$ is a field with $n^2$ elements, and $z \mapsto z^n$ is a ring automorphism of $R$ that fixes exactly $\mathbb{Z}_n$;
2. $x^n = a - x$ and $x^{n+1} = b$;
3. $y = x^{(n+1)/2}$ lies in $\mathbb{Z}_n$ and $y^2 = b$;
4. with $n^2 - 1 = 2^r s$, $s$ odd, either $x^s = 1$ or $x^{2^j s} = -1$ for some $0 \le j \le r - 2$.

*Proof.* (1) A root of $f$ modulo $n$ would give $\Delta = (2x - a)^2$ a square modulo $n$, against $(\Delta / n) = -1$. So $f$ is irreducible of degree 2 over the field $\mathbb{Z}_n$, and $R$ is a field with $n^2$ elements. In characteristic $n$, $(u + v)^n = u^n + v^n$ and $(uv)^n = u^n v^n$, so $z \mapsto z^n$ is a ring homomorphism; it is injective, as $R$ is a field, hence bijective. Its fixed points are the roots of $Z^n - Z$, at most $n$ of them, and every $c \in \mathbb{Z}_n$ is one, by Fermat's little theorem. So the fixed points are exactly $\mathbb{Z}_n$.

(2) Since $f$ has coefficients in $\mathbb{Z}_n$, $f(x^n) = f(x)^n = 0$, so $x^n$ is a root of $f$ in $R$. The roots of $f$ are $x$ and $a - x$, since $x + (a - x) = a$ and $x(a - x) = ax - x^2 = b$. If $x^n = x$, then $x \in \mathbb{Z}_n$ by (1), and $f$ would have a root in $\mathbb{Z}_n$. So $x^n = a - x$ and $x^{n+1} = x(a - x) = b$.

(3) $y^2 = x^{n+1} = b$. As $(b / n) = 1$ and $n$ is prime, $b \equiv \beta^2$ for some $\beta \in \mathbb{Z}_n$. In the field $R$, $Y^2 - b = (Y - \beta)(Y + \beta)$ has only the roots $\pm \beta$, so $y = \pm \beta \in \mathbb{Z}_n$.

(4) The group $R^\times$ has order $n^2 - 1$, so $x^{n^2 - 1} = 1$; note $x \ne 0$ as $b \ne 0$ in $\mathbb{Z}_n$. Also $x^{(n^2-1)/2} = (x^{n+1})^{(n-1)/2} = b^{(n-1)/2} = 1$, by Euler's criterion. Since $n$ is odd, $8 \mid n^2 - 1$ and $r \ge 3$. Let $z_j = x^{2^j s}$, so $z_{r-1} = x^{(n^2-1)/2} = 1$ and $z_{j+1} = z_j^2$. If $z_0 \ne 1$, let $j$ be the largest index with $z_j \ne 1$; then $j \le r - 2$ and $z_j^2 = z_{j+1} = 1$. In a field, $Y^2 - 1$ has only the roots $\pm 1$, so $z_j = -1$. $\square$

**Lemma 6 (the ring code is right).** Lines L7 and L10 compute $x^e$ in $\mathbb{Z}_n[x]/(f)$ correctly.

*Proof.* Each element of $\mathbb{Z}_n[x]/(f)$ has a unique form $u + v x$ with $u, v \in \mathbb{Z}_n$, as $f$ is monic of degree 2. Since $x^2 = ax - b$, $(u + vx)^2 = u^2 + 2uv x + v^2 (ax - b) = (u^2 - b v^2) + (2uv + a v^2) x$ and $(u + vx) x = -bv + (u + av) x$. The left-to-right binary method keeps the invariant that after the digits $e_1 \ldots e_i$ of $e$ have been read, the value is $x^{e_1 \ldots e_i}$ (the number with those binary digits): a squaring doubles the exponent and a product by $x$ adds one. After the last digit the value is $x^e$. $\square$

**Theorem.** For every $n \ge 0$, FROBENIUS$(n)$ ends with probability 1. If $n$ is prime it returns true. If it returns false, $n$ is not prime.

*Proof.* *Termination.* Line L2 has at most 5133 passes, line L5 ends with probability 1 by Lemma 3, and lines L7, L10 and L12 are loops of length $O(\log n)$.

*Primes.* Let $n$ be prime. If $n < (B + 1)^2$, Lemma 1 gives true. Otherwise $n$ is not a square, so line L4 does not fire, and line L6 does not fire, as $\gcd(b\Delta, n) \in \{1, n\}$. The pair drawn has $(\Delta / n) = -1$ and $(b / n) = 1$, so by Lemmas 5 and 6, $y \in \mathbb{Z}_n$ with $y^2 = b$, and lines L8 and L9 pass. By Lemma 5 (4), either $z = x^s = 1$ and line L11 returns true, or $z_j = -1$ for some $j \le r - 2$; the loop of line L12 checks $z_0, \ldots, z_{r-2}$ in order and returns true at the first $-1$. So line L13 is never reached.

*False answers.* Lines L1 to L3 are right by Lemma 1, line L4 by Lemma 2, and line L6 by Lemma 4. Lines L8, L9 and L13 return false only when a property fails that, by Lemma 5, every prime $n$ above $(B + 1)^2$ has for every allowed pair; so $n$ is composite.

*The error on composites.* A composite can pass only through lines L11 and L12, after lines L1 to L6. If $n$ has no prime factor up to 50000 and is not a square, Grantham's theorem bounds the fraction of allowed pairs for which it passes by $1/7710$. Line L5 draws pairs uniformly and keeps the first allowed one, so the kept pair is uniform among the allowed pairs, and the probability of a true answer is at most $1/7710$. $\blacksquare$

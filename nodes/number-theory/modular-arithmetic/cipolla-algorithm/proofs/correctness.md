---
title: Cipolla's algorithm returns a square root, and each trial succeeds with probability (p - 1)/(2p)
proves: [correctness]
status: full
---

**Claim.** Let $p$ be an odd prime and $n$ an integer. If $p \mid n$, the algorithm returns $0$. If $n$ is a quadratic nonresidue modulo $p$, it returns NONE. Otherwise, each trial of lines L3 and L4 succeeds with probability exactly $(p - 1)/(2p)$, so the loop ends with probability $1$, and line L11 returns $x$ with $x^2 \equiv n \pmod p$.

**Lines L1 and L2.** After line L1, $0 \le n < p$, and $0$ is a square root of $0$. For $n \ne 0$, [Euler's criterion](/euler-criterion/) says that $n^{(p-1)/2} \equiv 1$ if $n$ is a quadratic residue and $\equiv -1$ otherwise. So line L2 returns NONE exactly for nonresidues. From now on $n \not\equiv 0$ is a residue, say $n \equiv r^2$ with $r \not\equiv 0$.

**The trials succeed often.** Write $\chi(t) = t^{(p-1)/2} \bmod p$, read as $-1$, $0$ or $1$; by Euler's criterion it is the Legendre symbol. For each $a \in \mathbb{F}_p$, the number of $b \in \mathbb{F}_p$ with $b^2 = a^2 - n$ is $1 + \chi(a^2 - n)$. So the number $S$ of pairs $(a, b)$ with $a^2 - b^2 = n$ is $\sum_a \big(1 + \chi(a^2 - n)\big) = p + \sum_a \chi(a^2 - n)$. On the other hand, $(a, b) \mapsto (u, v) = (a - b, a + b)$ is a bijection of $\mathbb{F}_p^2$, because $2$ is invertible, and $a^2 - b^2 = uv$. The equation $uv = n$ with $n \ne 0$ has exactly $p - 1$ solutions, one for each $u \ne 0$. So $S = p - 1$ and $\sum_a \chi(a^2 - n) = -1$.

Let $N_0$, $N_+$ and $N_-$ count the $a$ with $\chi(a^2 - n)$ equal to $0$, $1$ and $-1$. Then $N_0 = 2$, for $a = \pm r$, which are distinct since $p$ is odd. Also $N_0 + N_+ + N_- = p$ and $N_+ - N_- = -1$. Hence $N_+ + N_- = p - 2$ and $N_- = (p - 1)/2$. Line L3 chooses $a$ uniformly in $\{0, \ldots, p - 1\}$, and line L4 accepts exactly when $\chi(d) = -1$ with $d = a^2 - n$. So each trial succeeds with probability $(p - 1)/(2p) \ge 1/3$, independently of the other trials, and the loop ends with probability $1$.

**The field.** Now $d$ is a nonresidue, so $X^2 - d$ has no root in $\mathbb{F}_p$ and is irreducible. The ring $F = \mathbb{F}_p[X]/(X^2 - d)$ is a field with $p^2$ elements. Write $\omega$ for the class of $X$, so $\omega^2 = d$, and every element is $x + y\omega$ with $x, y \in \mathbb{F}_p$, stored as the pair $(x, y)$. The product is
$$(x + y\omega)(b + c\omega) = (xb + ycd) + (xc + yb)\omega,$$
which is line L8, and the square of $b + c\omega$ is $(b^2 + c^2 d) + 2bc\,\omega$, which is line L9.

**The power.** Lines L5 to L10 are [binary exponentiation](/binary-exponentiation/) in $F$: with $e_0 = (p + 1)/2$, the loop keeps the invariant $(x + y\omega)(b + c\omega)^e = (a + \omega)^{e_0}$, since line L8 moves one factor $b + c\omega$ into $x + y\omega$ when $e$ is odd, and lines L9 and L10 square the base and halve $e$. When $e = 0$, $x + y\omega = (a + \omega)^{(p+1)/2} =: z$.

**$z^2 = n$.** In a field of characteristic $p$, $(u + v)^p = u^p + v^p$, because the binomial coefficients $\binom{p}{i}$ with $0 < i < p$ are multiples of $p$. By [Fermat's little theorem](/fermat-little-theorem/), $a^p = a$ for $a \in \mathbb{F}_p$. Also $\omega^p = \omega \cdot (\omega^2)^{(p-1)/2} = \omega \, d^{(p-1)/2} = -\omega$, since $d$ is a nonresidue. So $(a + \omega)^p = a - \omega$ and
$$z^2 = (a + \omega)^{p+1} = (a + \omega)^p (a + \omega) = (a - \omega)(a + \omega) = a^2 - d = n.$$

**$z$ lies in $\mathbb{F}_p$.** In the field $F$, the polynomial $T^2 - n$ has at most two roots. The elements $r$ and $-r$ of $\mathbb{F}_p$ are two different roots, so $z \in \{r, -r\} \subseteq \mathbb{F}_p$. Hence $y = 0$, and line L11 returns $x = z$ with $x^2 \equiv n \pmod p$. $\blacksquare$

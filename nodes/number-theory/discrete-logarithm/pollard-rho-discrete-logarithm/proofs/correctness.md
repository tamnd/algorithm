---
title: Correctness of Pollard's rho algorithm for discrete logarithms
proves: [correctness, termination]
status: full
---

Let $p$ be prime, $g \in (\mathbb{Z}/p\mathbb{Z})^*$ of order $n$, $H = \langle g \rangle$ and $h \in (\mathbb{Z}/p\mathbb{Z})^*$. All exponent arithmetic is modulo $n$, which is well defined because $g^n = 1$ and, when $h \in H$, $h^n = 1$.

**Lemma 1 (membership).** $h \in H$ if and only if $h^n = 1$.

*Proof.* If $h = g^x$ then $h^n = (g^n)^x = 1$. Conversely, $(\mathbb{Z}/p\mathbb{Z})^*$ is cyclic of order $p - 1$, and $n \mid p - 1$. A cyclic group has exactly one subgroup of each order dividing its order, and that subgroup is the set of solutions of $y^n = 1$, which has at most $n$ elements since it is the set of roots of a polynomial of degree $n$ over a field. $H$ has $n$ elements and all satisfy $y^n = 1$, so $H$ is exactly this set. $\square$

So line L1 returns NONE exactly when $h \notin H$. From now on assume $h \in H$, say $h = g^{x^*}$ with $0 \le x^* < n$. If $h = 1$ then $x^* = 0$ and line L2 is correct, so assume $h \ne 1$.

**Lemma 2 (invariant).** Throughout an attempt, $x = g^a h^b$ and $X = g^A h^B$.

*Proof.* Line L5 sets $x = g^{a_0} h^{b_0}$ with $(a, b) = (a_0, b_0)$, and line L6 copies it. Each case of STEP preserves the relation: $g^a h^b \cdot h = g^a h^{b+1}$ (line L17), $(g^a h^b)^2 = g^{2a} h^{2b}$ (line L18) and $g^a h^b \cdot g = g^{a+1} h^b$ (line L19); reducing exponents modulo $n$ changes nothing since $g^n = h^n = 1$. $\square$

**Lemma 3 (each attempt ends).** Let $x_0 = g^{a_0} h^{b_0}$ and $x_{i+1} = f(x_i)$, where $f$ is the element part of STEP for the current partition. After round $i$ of the loop of lines L7 to L10, $x = x_i$ and $X = x_{2i}$, and the loop ends after at most $n$ rounds.

*Proof.* The first claim follows by induction, since line L8 applies $f$ once and line L9 twice; the element part of STEP depends only on the element, not on the exponents. The sequence lies in the finite set $H$ of size $n$, so there are $\mu \ge 0$ and $\lambda \ge 1$ with $x_{i + \lambda} = x_i$ for all $i \ge \mu$, and $\mu + \lambda \le n$. Let $i$ be the least multiple of $\lambda$ with $i \ge \max(\mu, 1)$; then $i \le \mu + \lambda \le n$ and $x_{2i} = x_i$ because $2i - i$ is a multiple of $\lambda$ and $i \ge \mu$. $\square$

**Lemma 4 (the congruence).** When the loop of line L10 ends, $s x^* \equiv A - a \pmod n$ with $s = b - B \bmod n$.

*Proof.* By Lemma 2, $g^a h^b = x = X = g^A h^B$. Substituting $h = g^{x^*}$ gives $g^{a + b x^*} = g^{A + B x^*}$, so $a + b x^* \equiv A + B x^* \pmod n$ since $g$ has order $n$. $\square$

**Lemma 5 (the candidates).** If $s \not\equiv 0$ and $d = \gcd(s, n)$, then $d \mid A - a$, and the solutions in $\{0, \dots, n - 1\}$ of $s z \equiv A - a \pmod n$ are exactly $y + t n/d$ for $0 \le t < d$, where $y$ is computed at line L13. In particular $x^*$ is one of them.

*Proof.* By Lemma 4 the congruence has the solution $x^*$, so $d$, which divides $s$ and $n$, divides $A - a$. Dividing by $d$, $s z \equiv A - a \pmod n$ is equivalent to $(s/d) z \equiv (A - a)/d \pmod{n/d}$. Since $\gcd(s/d, n/d) = 1$, $s/d$ is invertible modulo $n/d$, and the unique solution modulo $n/d$ is $y$, with $0 \le y < n/d$. The solutions modulo $n$ are the $d$ integers $y + t n/d$ with $0 \le t < d$, all in $\{0, \dots, n - 1\}$. $\square$

**Soundness.** Line L15 returns a value only after checking $g^z = h$ for it, with $0 \le z < n$; since $g$ has order $n$, such a $z$ equals $x^*$. Line L1 returns NONE only if $h^n \ne 1$, which by Lemma 1 means $h \notin H$. So every output is correct.

**Completeness of an attempt.** If line L12 passes, then by Lemma 5 one of the $d$ candidates is $x^*$, and line L15 returns it. So an attempt fails only when $s \equiv 0$ or $d > \lfloor \sqrt n \rfloor + 1$.

**Termination with probability one.** Each attempt ends by Lemma 3, so it remains to show that some attempt succeeds. In line L16 the partition is a uniformly random map $H \to \{1, 2, 3\}$ and $a_0, b_0$ are uniform, independently of earlier attempts. We exhibit one choice that succeeds; since there are finitely many choices, each attempt after the first then succeeds with probability at least some $q > 0$, and the number of attempts is finite with probability $1$ (it is dominated by a geometric random variable).

Take $(a_0, b_0) = (0, 0)$, so $x_0 = 1$, and the partition with $S_1 = \{1\}$, $S_2 = \emptyset$ and $S_3 = H \setminus \{1\}$. Then $x_1 = h$ with $(a_1, b_1) = (0, 1)$. Since $h \ne 1$, the next steps multiply by $g$: $x_{1 + j} = h g^j = g^{x^* + j}$ with $(a, b) = (j, 1)$, and these differ from $1$ for $0 \le j < n - x^*$. At $j = n - x^*$ the walk returns to $x_0 = 1$. So $\mu = 0$ and $\lambda = n - x^* + 1 \ge 2$, and every pass around the cycle visits $S_1$ exactly once. Floyd's loop stops at $i = \lambda$, where the tortoise has made one pass and the hare two, so $b = 1$ and $B = 2$ (exponents of $h$ grow only at line L17). Hence $s \equiv -1$, $d = 1$, line L12 passes, and by the completeness of an attempt the algorithm returns $x^*$.

This proves termination with probability one for the algorithm as stated, with uniformly random partitions. An implementation draws the partition from a small keyed family, such as $x \mapsto (\kappa x \bmod p) \bmod 3$ for a random unit $\kappa$; for such a family, the success probability of an attempt is the subject of the random walk heuristic rather than of this proof. Under that heuristic $b - B$ is uniform modulo $n$, so for prime $n$ an attempt fails with probability about $1/n$. $\blacksquare$

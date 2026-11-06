---
title: Correctness of the Tonelli-Shanks algorithm
proves: [correctness, termination]
status: full
---

Let $p$ be an odd prime and $a$ an integer. All arithmetic is in the field $\mathbb{Z}_p$. We use two facts about $\mathbb{Z}_p$:

- **(F1)** The only solutions of $y^2 = 1$ are $y = \pm 1$, since $p \mid (y - 1)(y + 1)$ forces $p \mid y - 1$ or $p \mid y + 1$ by Euclid's lemma.
- **(F2)** If $u \in \mathbb{Z}_p^*$ and $u^{2^j} = 1$ for some $j \ge 0$, then the [multiplicative order](/multiplicative-order/) of $u$ is $2^i$ for some $0 \le i \le j$, because the order divides $2^j$. If the order is $2^i$ with $i \ge 1$, then $u^{2^{i-1}} = -1$: it is not 1 by minimality, and its square is 1, so it is $-1$ by (F1).

We also use Euler's criterion: for $a \not\equiv 0$, $a^{(p-1)/2} = 1$ if $a$ is a quadratic residue and $-1$ otherwise.

**Lines L1 and L2.** If $a \equiv 0$, then $x = 0$ is the only root, and line L1 returns it. Otherwise, by Euler's criterion, line L2 returns NONE exactly when $a$ is a nonresidue, which is correct, since then no root exists. From here on $a$ is a nonzero quadratic residue, so $a^{(p-1)/2} = 1$.

**Line L4.** If $s = 1$, then $p - 1 = 2q$ with $q$ odd, so $p \equiv 3 \pmod 4$ and $(p + 1)/4$ is an integer. For $x = a^{(p+1)/4}$, $x^2 = a^{(p+1)/2} = a \cdot a^{(p-1)/2} = a$. So the returned value is a root.

**Line L5.** From here on $s \ge 2$. Exactly half of $\mathbb{Z}_p^*$ are nonresidues, so a nonresidue exists in $\{2, \ldots, p - 1\}$ (1 is a residue), and the search stops at the least one, $z$, with $z^{(p-1)/2} = -1$.

**Invariant.** We claim that at the start of every pass of the loop of line L7 (that is, each time the test of line L7 is evaluated):

- **(I1)** $x^2 = a t$;
- **(I2)** $c^{2^{M-1}} = -1$;
- **(I3)** $t^{2^{M-1}} = 1$;
- **(I4)** $M \ge 1$.

*Initialization.* After line L6, $c = z^q$, $x = a^{(q+1)/2}$, $t = a^q$ and $M = s \ge 2$. (I1): $x^2 = a^{q+1} = a \cdot a^q = at$. (I2): $c^{2^{s-1}} = z^{q 2^{s-1}} = z^{(p-1)/2} = -1$. (I3): $t^{2^{s-1}} = a^{(p-1)/2} = 1$. (I4): $M = s \ge 1$.

*Maintenance.* Suppose (I1) to (I4) hold and $t \ne 1$. By (I3) and (F2), $t$ has order $2^i$ for some $i$ with $0 \le i \le M - 1$, and $i \ge 1$ because $t \ne 1$. Line L8 squares $t$ until it reaches 1, so it finds exactly this $i$, the least $i \ge 1$ with $t^{2^i} = 1$, after $i$ squarings. By (F2), $t^{2^{i-1}} = -1$.

Since $i \le M - 1$, the exponent $M - i - 1 \ge 0$, so line L9 is well defined and gives $b = c^{2^{M-i-1}}$. Then $b^{2^i} = c^{2^{M-1}} = -1$ by (I2).

Line L10 sets $M' = i$, $c' = b^2$, $t' = t b^2$ and $x' = x b$. Check the invariant for the new values:

- (I1): $x'^2 = x^2 b^2 = a t b^2 = a t'$.
- (I2): $c'^{2^{M'-1}} = b^{2 \cdot 2^{i-1}} = b^{2^i} = -1$.
- (I3): $t'^{2^{M'-1}} = t^{2^{i-1}} \cdot b^{2^i} = (-1)(-1) = 1$.
- (I4): $M' = i \ge 1$.

*Termination.* Each pass replaces $M$ by $i \le M - 1$, so $M$ strictly decreases, and by (I4) it stays at least 1. So there are at most $s - 1$ passes. Each inner loop also terminates: line L8 stops after $i \le M - 1$ squarings, and line L9 runs $M - i - 1$ times. The search of line L5 stops, as shown above.

*Conclusion.* When the loop stops, $t = 1$, and (I1) gives $x^2 = a$. So line L11 returns a square root of $a$ modulo $p$.

Together with the cases of lines L1, L2 and L4, this shows that the algorithm always terminates, returns NONE exactly when $a$ is a nonresidue, and otherwise returns an $x \in [0, p)$ with $x^2 \equiv a \pmod p$. $\blacksquare$

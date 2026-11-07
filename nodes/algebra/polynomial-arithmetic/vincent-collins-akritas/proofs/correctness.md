---
title: The Vincent-Collins-Akritas method isolates every real root exactly once
proves: [correctness]
status: full
---

Let $f = \sum_{i=0}^{n} f_i x^i \in \mathbb{Z}[x]$ be square-free with $n \ge 1$ and $f_n \ne 0$. For a polynomial $p$ of degree at most $n$ and real $a \ne b$ write $T_{a,b}\,p(y) = (y + 1)^n p((ay + b)/(y + 1))$, and write $\operatorname{Var}$ for the number of sign changes in a coefficient list, zeros ignored. The algorithm is the one in the main pseudocode, lines L1 to L12.

**Notation for the work list.** For integers $c \ge 0$ and $k \ge 0$ put $h_k = 2B/2^k$, $u_{c,k} = -B + c\, h_k$, and $I(c, k) = (u_{c,k}, u_{c,k} + h_k)$, an open interval with midpoint $m_{c,k} = u_{c,k} + h_k/2$.

**Claim 1 (the bound).** Every real root $\alpha$ of $f$ satisfies $|\alpha| < B$. Let $M = \max_{i < n} |f_i/f_n|$, so $B \ge 1 + M$ by line L1. If $M = 0$, then $f = f_n x^n$, and square-free forces $n = 1$ and $\alpha = 0$. If $M > 0$ and $|\alpha| \ge 1 + M$, then

$$\Big|\sum_{i<n} f_i \alpha^i\Big| \le M |f_n| \sum_{i<n} |\alpha|^i = M |f_n| \frac{|\alpha|^n - 1}{|\alpha| - 1} \le |f_n| (|\alpha|^n - 1) < |f_n \alpha^n|,$$

so $f(\alpha) \ne 0$. Hence $|\alpha| < 1 + M \le B$, and all real roots lie in $I(0, 0) = (-B, B)$.

**Claim 2 (the invariant of an entry).** Every entry $(A, c, k)$ that is pushed onto the stack satisfies

$$A(x) = \lambda\, f(u_{c,k} + h_k x) \quad \text{for some } \lambda > 0. \tag{J}$$

Line L2 sets $A = f(2Bx - B)$, which is (J) for $c = k = 0$ with $\lambda = 1$. Suppose $(A, c, k)$ satisfies (J), and let $u = u_{c,k}$ and $h = h_k$. Line L9 gives

$$A_L(x) = 2^n A(x/2) = 2^n \lambda\, f\big(u + \tfrac{h}{2} x\big), \qquad A_R(x) = A_L(x + 1) = 2^n \lambda\, f\big(u + \tfrac{h}{2} + \tfrac{h}{2} x\big).$$

Since $h_{k+1} = h/2$, $u_{2c, k+1} = u$ and $u_{2c+1, k+1} = u + h/2$, both children satisfy (J), with the constant $2^n \lambda > 0$. In particular each $A$ has degree exactly $n$, since its leading coefficient is $\lambda f_n h_k^n \ne 0$.

**Claim 3 (the test).** Let $(A, c, k)$ satisfy (J) and let $N$ be the number of roots of $f$ in $I(c, k)$. Then the number $v$ of line L6 satisfies $v \ge N$ and $v - N$ is even. In particular $v = 0$ implies $N = 0$, and $v = 1$ implies $N = 1$.

With $u = u_{c,k}$ and $h = h_k$,

$$(x + 1)^n A\Big(\frac{1}{x + 1}\Big) = \lambda (x + 1)^n f\Big(u + \frac{h}{x + 1}\Big) = \lambda (x + 1)^n f\Big(\frac{u x + (u + h)}{x + 1}\Big) = \lambda\, T_{u,\, u + h} f(x).$$

The map $x \mapsto (ux + u + h)/(x + 1)$ is a bijection from $(0, \infty)$ onto $(u, u + h)$, and $(x + 1)^n \ne 0$ for $x > 0$, so the positive roots of $T_{u, u+h} f$, with multiplicity, correspond to the roots of $f$ in $I(c, k)$. These roots are simple because $f$ is square-free, so there are $N$ of them. The factor $\lambda > 0$ does not change the signs. [Descartes' rule of signs](/descartes-rule-of-signs/) says that $v$ is at least the number of positive roots counted with multiplicity and differs from it by an even number. This is the claim.

**Claim 4 (the midpoint).** For $(A, c, k)$ with (J), $A_R(0) = A_L(1) = 2^n A(1/2) = 2^n \lambda f(m_{c,k})$. So line L10 reports $m_{c,k}$ if and only if it is a root of $f$.

**Claim 5 (the partition invariant).** At the start of each pass of the loop in line L4, the following hold.

- (P1) The open intervals of the stack entries and the items of `out` are pairwise disjoint.
- (P2) Each item of `out` is either an open interval $I(c, k)$ that contains exactly one root of $f$, or a single point that is a root of $f$.
- (P3) Each real root of $f$ lies in exactly one stack interval or in exactly one item of `out`, and not in both.

Initially the stack holds $(A, 0, 0)$ and `out` is empty. (P1) and (P2) hold trivially, and (P3) holds by claim 1. Suppose the invariant holds and line L5 pops $(A, c, k)$, with interval $I = I(c, k)$ and midpoint $m$.

- If $v = 0$, then $I$ holds no root by claim 3, so dropping it keeps (P3); (P1) and (P2) are unchanged.
- If $v = 1$, then $I$ holds exactly one root by claim 3. Moving $I$ from the stack to `out` keeps (P1), adds an item that satisfies (P2), and moves that root from a stack interval to an item of `out`, which keeps (P3).
- If $v \ge 2$, then $I = I(2c, k+1) \cup \{m\} \cup I(2c+1, k+1)$, a disjoint union. Line L10 adds $\{m\}$ to `out` exactly when $m$ is a root, by claim 4, and line L11 pushes the two halves. The new items are pairwise disjoint subsets of $I$, so (P1) holds, (P2) holds for $\{m\}$, and each root that was in $I$ is now in exactly one of the three parts, either reported or on the stack. If $m$ is not a root, dropping it loses nothing. So (P3) holds.

**Claim 6 (termination).** If $n = 1$, then $T_{u, u+h} f$ has degree at most $1$, so $v \le 1$ for every entry and the root entry is never split. Let $n \ge 2$ and let $\operatorname{sep}(f) > 0$ be the least distance between two distinct complex roots of $f$, which exists because $f$ is square-free. An entry at depth $k$ has interval length $h_k = 2B/2^k$. If $h_k \le \operatorname{sep}(f)/\sqrt 3$, then part 3 of [Vincent's theorem](/vincent-theorem/) gives $\operatorname{Var}(T_{u, u + h_k} f) \le 1$, so $v \le 1$ by claim 3 and the entry is not split. So no entry has depth greater than $K = \max(0, \lceil \log_2(2\sqrt 3\, B / \operatorname{sep}(f)) \rceil)$. Each pass of the loop pops one entry and pushes at most two entries of depth one more, and each pair $(c, k)$ with $k \le K$ is pushed at most once, since $(c, k)$ is pushed only by its parent $(\lfloor c/2 \rfloor, k - 1)$. So at most $2^{K+1} - 1$ entries are ever pushed, and the loop ends.

**Conclusion.** When the loop ends, the stack is empty. By (P3) every real root of $f$ lies in exactly one item of `out`, by (P2) every item holds exactly one root (an open interval) or is a root (a point), and by (P1) the items are disjoint. Line L12 only sorts the list. Hence the output is a list of disjoint isolating intervals and exact roots, one for each real root of $f$. $\blacksquare$

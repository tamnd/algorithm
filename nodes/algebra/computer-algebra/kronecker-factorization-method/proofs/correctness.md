---
title: Kronecker's method returns the factorization into irreducibles
proves: [correctness, termination]
status: full
---

All polynomials are in $\mathbb{Z}[x]$. The input $f_0$ is primitive of degree $d \ge 1$ with $\operatorname{lc} f_0 > 0$. Write $f$ for the current value of the variable $f$.

**Fact 1 (interpolation).** For distinct integers $a_0, \ldots, a_e$ and values $\delta_0, \ldots, \delta_e$, there is exactly one polynomial $g \in \mathbb{Q}[x]$ of degree at most $e$ with $g(a_i) = \delta_i$ for all $i$.

*Proof.* Existence is the Lagrange formula. If $g_1$ and $g_2$ both qualify, $g_1 - g_2$ has degree at most $e$ and $e + 1$ roots, so it is zero. $\square$

**Fact 2.** If $g$ divides $f$ and $f$ is primitive, then $g$ is primitive.

*Proof.* If $f = g h$, the content of $g$ divides every coefficient of $f$, so it divides $\operatorname{cont}(f) = 1$. $\square$

**Lemma (completeness of one round).** Let $1 \le e$ and let $f$ be primitive. If $f$ has a factor of degree $e$ in $\mathbb{Z}[x]$, the loop of line L5 finds a factor $g$ of $f$ of degree $e$. Any $g$ it returns divides $f$ and has degree $e$.

*Proof.* The second sentence is the test at line L7. For the first, let $f = g h$ with $\deg g = e$. Since $f(a_i) \ne 0$ and $f(a_i) = g(a_i) h(a_i)$ with integer factors, $g(a_i)$ is a nonzero divisor of $f(a_i)$. In particular $g(a_0) \ne 0$, and replacing $g, h$ by $-g, -h$ if necessary gives $g(a_0) > 0$. So $(g(a_0), \ldots, g(a_e)) \in D_0 \times \cdots \times D_e$. When the loop reaches this tuple, or an earlier one that passes the test, line L6 computes the unique interpolant of Fact 1, which for this tuple is $g$ itself, and $g$ passes line L7. The product is finite, so the loop reaches every tuple unless it stops earlier with a factor. $\square$

**Invariant.** At each test of line L2:

> **(K1)** $f_0 = \bigl(\prod_{g \in \text{factors}} g\bigr) \cdot f$, and $f$ is primitive with $\operatorname{lc} f > 0$.
> **(K2)** Each element of factors is irreducible of positive degree with a positive leading coefficient.
> **(K3)** $f$ has no factor of degree $j$ with $1 \le j < e$.

*Initialization.* factors is empty, $f = f_0$ and $e = 1$. (K1) and (K2) are clear, and (K3) is empty.

*Maintenance, a factor is found.* Line L8 appends $g$, normalized so that $\operatorname{lc} g > 0$, and replaces $f$ by $q = f / g$. Then $f_0 = (\prod \text{factors}) \cdot g \cdot q$, the leading coefficient of $q$ is positive, and $q$ is primitive by Fact 2 since $q \mid f$. So (K1) holds. The factor $g$ has degree $e \ge 1$. If $g = u v$ with $1 \le \deg u < e$, then $u$ would be a factor of $f$ of degree less than $e$, contradicting (K3). So $g$ is irreducible, and (K2) holds. Every factor of $q$ is a factor of $f$, so (K3) holds for $q$ with the same $e$.

*Maintenance, no factor is found.* By the lemma $f$ has no factor of degree $e$. Together with (K3) it has no factor of degree $j$ for $1 \le j < e + 1$, which is (K3) after line L9.

**Termination.** Each pass either increases $e$ by one or lowers $\deg f$ by $e \ge 1$, and both $e \le \deg f / 2 \le d/2$ and $\deg f \ge 0$ are bounded. So the number of passes is at most $d/2 + d$. Each pass runs over a finite product of finite divisor sets, since $f(a_i) \ne 0$.

**Correctness at exit.** At exit $2e > \deg f$. If $\deg f \ge 1$, suppose $f = u v$ with $1 \le \deg u \le \deg v$. Then $\deg u \le \deg f / 2 < e$, which contradicts (K3). So $f$ is irreducible, and line L10 appends it. It is primitive with positive leading coefficient by (K1). If $\deg f = 0$, then $f$ is a positive primitive constant, so $f = 1$. In both cases (K1) and (K2) show that the returned list consists of irreducible polynomials of positive degree with positive leading coefficients whose product is $f_0$. $\blacksquare$

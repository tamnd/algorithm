---
title: Column k of the Romberg table has degree of exactness 2k + 1 and error O(h^(2k+2))
proves: [correctness]
status: full
---

Let $a \ne b$, $I = \int_a^b f(x)\,dx$, and $h_i = (b - a)/2^i$. Write $T(h)$ for the composite [trapezoidal rule](/trapezoidal-rule/) with step $h$, that is with $(b - a)/h$ subintervals. ROMBERG builds $R[i, 0]$ in lines L2 and L5 and $R[i, k]$ for $1 \le k \le i$ in line L7.

**Step 1 (column 0 is the trapezoidal rule).** $R[i, 0] = T(h_i)$. For $i = 0$ this is line L2. For $i \ge 1$, the nodes of $T(h_i)$ with even index are the nodes of $T(h_{i-1})$, and the nodes with odd index are the $2^{i-1}$ new points $a + (2j - 1) h_i$. An old node has weight $h_{i-1} = 2 h_i$ in $T(h_{i-1})$ (or half of it at the ends) and weight $h_i$ in $T(h_i)$ (or half of it), so the old part of $T(h_i)$ is $\tfrac12 T(h_{i-1})$, and the new nodes add $h_i \sum_j f(a + (2j - 1) h_i)$. That is line L5.

**Step 2 (the combination coefficients).** By line L7 and induction, $R[i, k] = \sum_{l=0}^{k} \gamma^{(k)}_l\, T(2^l h_i)$ for coefficients $\gamma^{(k)}_l$ that do not depend on $i$ or $f$. Define $\varphi_j(k) = \sum_l \gamma^{(k)}_l\, 4^{j l}$, the value of the combination on the sequence $h \mapsto h^{2j}$ divided by $h_i^{2j}$. Then

$$\varphi_j(0) = 1, \qquad \varphi_j(k) = \varphi_j(k-1)\, \frac{4^k - 4^j}{4^k - 1}, \qquad\text{so}\qquad \varphi_j(k) = \prod_{l=1}^{k} \frac{4^l - 4^j}{4^l - 1}.$$

*Proof.* Line L7 is $R[i,k] = \big(4^k R[i, k-1] - R[i-1, k-1]\big)/(4^k - 1)$. Applied to $h^{2j}$, the first term contributes $4^k \varphi_j(k-1) h_i^{2j}$ and the second $\varphi_j(k-1) h_{i-1}^{2j} = 4^j \varphi_j(k-1) h_i^{2j}$. $\square$

So $\varphi_0(k) = 1$, meaning the coefficients sum to 1, and $\varphi_j(k) = 0$ exactly for $1 \le j \le k$, while $\varphi_{k+1}(k) \ne 0$.

**Lemma (Euler-Maclaurin, cited).** If $f \in C^{2K+2}[a, b]$ and $h = (b - a)/m$, then

$$T(h) = I + \sum_{j=1}^{K} c_j h^{2j} + \rho_K(h), \qquad c_j = \frac{B_{2j}}{(2j)!}\big(f^{(2j-1)}(b) - f^{(2j-1)}(a)\big),$$

$$\rho_K(h) = \frac{(b - a)\, B_{2K+2}}{(2K + 2)!}\, h^{2K+2} f^{(2K+2)}(\xi) \quad\text{for some } \xi \in [a, b],$$

with the Bernoulli numbers $B_2 = \tfrac16$, $B_4 = -\tfrac{1}{30}, \ldots$, all nonzero. This is the [Euler-Maclaurin formula](/euler-maclaurin-formula/) (Davis and Rabinowitz, Section 2.9; Atkinson, Section 5.4). For a polynomial of degree at most $2K + 1$ the remainder is 0 and the expansion is exact.

**Theorem 1 (order).** If $f \in C^{2k+2}[a, b]$ and $i \ge k$, then

$$|R[i, k] - I| \le \Big( \sum_{l=0}^{k} |\gamma^{(k)}_l|\, 4^{l (k+1)} \Big) \frac{(b - a)\, |B_{2k+2}|}{(2k + 2)!} \max_{[a,b]} |f^{(2k+2)}|\; h_i^{2k+2} = O(h_i^{2k+2}).$$

*Proof.* Insert the Lemma with $K = k$ into $R[i, k] = \sum_l \gamma^{(k)}_l T(2^l h_i)$. The constant terms give $I \varphi_0(k) = I$. Each term $c_j h^{2j}$ with $1 \le j \le k$ gives $c_j h_i^{2j} \varphi_j(k) = 0$ by Step 2. What is left is $\sum_l \gamma^{(k)}_l \rho_k(2^l h_i)$, and $|\rho_k(2^l h_i)| \le \frac{(b - a)|B_{2k+2}|}{(2k+2)!} \max|f^{(2k+2)}|\, 4^{l(k+1)} h_i^{2k+2}$. $\square$

**Theorem 2 (degree of exactness).** $R[i, k]$ is exact for every polynomial of degree at most $2k + 1$, and not for $x^{2k+2}$.

*Proof.* For $p$ of degree at most $2k + 1$, the Lemma with $K = k$ holds with $\rho_k = 0$, and the argument of Theorem 1 gives $R[i, k] = I(p)$ exactly. For $p = x^{2k+2}$, use the Lemma with $K = k + 1$; the remainder is 0 since $p^{(2k+4)} = 0$. The terms $j \le k$ are removed as before, and

$$R[i, k] - I(p) = c_{k+1}\, \varphi_{k+1}(k)\, h_i^{2k+2}, \qquad c_{k+1} = \frac{B_{2k+2}}{(2k+2)!}\, (2k + 2)!\,(b - a) = B_{2k+2}\,(b - a).$$

All three factors are nonzero, since $p^{(2k+1)}(x) = (2k + 2)!\, x$, $B_{2k+2} \ne 0$ and $\varphi_{k+1}(k) \ne 0$. $\square$

**Consequences.** $R[i, 1]$ is the composite Simpson rule and $R[i, 2]$ the composite Boole rule, as one checks from the coefficients; the test file verifies both identities in exact arithmetic. The algorithm returns $R[K, K]$, which has degree of exactness $2K + 1$ on $2^K + 1$ nodes. If $b < a$ every $h_i$ is negative and every entry is minus the entry for $[b, a]$; if $a = b$ every entry is 0. $\blacksquare$

**Termination and cost.** The loop of line L3 runs at most $K$ = `max_level` times. Level 0 evaluates $f$ twice and level $i \ge 1$ evaluates it $2^{i-1}$ times, so a run that stops at level $K$ makes $2 + \sum_{i=1}^{K} 2^{i-1} = 2^K + 1$ evaluations, one per node of $T(h_K)$, and $O(K^2)$ arithmetic operations for the table.

**Not proved here.** The weights of every $R[i, k]$ as a rule on the $2^i + 1$ nodes are positive, which makes the table stable and gives convergence of every column for every Riemann integrable $f$. This is a theorem of Bauer, Rutishauser and Stiefel (1963); the test file checks positivity for all $i \le 5$ in exact arithmetic.

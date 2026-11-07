---
title: Horner's rule, synthetic division and the Taylor shift compute what they claim
proves: [correctness]
status: full
---

Let $R$ be a commutative ring with $1$, let $f = \sum_{i=0}^{n} a_i x^i \in R[x]$ with $n \ge 0$ and $a_n \ne 0$, stored as the list $a = [a_0, \ldots, a_n]$, and let $u \in R$. For HORNER the point $u$ may also lie in an associative ring $S$ that contains the coefficients and in which $u$ commutes with them; the argument below uses only the ring axioms of $S$.

**Lemma 1 (HORNER).** HORNER$(a, u)$ returns $f(u) = \sum_{i=0}^{n} a_i u^i$, and HORNER$([\,], u)$ returns $0$.

*Proof.* The empty list is the zero polynomial, and line L1 returns $0$. Let $n \ge 0$. We prove the invariant

> **(H)** before the step of line L4 with index $i$ (for $i = n - 1, \ldots, 0$), and after the loop with $i = -1$, $s = \sum_{j=i+1}^{n} a_j u^{j-i-1}$.

*Initialization.* Line L2 sets $s = a_n$. For $i = n - 1$ the sum in (H) is the single term $a_n u^0 = a_n$.

*Maintenance.* Suppose (H) holds before the step with index $i$. Line L4 computes

$$s \cdot u + a_i = \Bigl(\sum_{j=i+1}^{n} a_j u^{j-i-1}\Bigr) u + a_i = \sum_{j=i+1}^{n} a_j u^{j-i} + a_i u^0 = \sum_{j=i}^{n} a_j u^{j-i}.$$

The middle step is distributivity and associativity of $S$ (with $a_j u^{k} u = a_j u^{k+1}$). This is (H) for the index $i - 1$.

*Termination.* The loop runs for $i = n - 1$ down to $0$ and stops; then (H) holds with $i = -1$, so $s = \sum_{j=0}^{n} a_j u^j = f(u)$, which line L5 returns. If $n = 0$ the loop does not run and $s = a_0 = f(u)$. $\square$

**Lemma 2 (SYNTHETIC-DIVISION).** Let $n \ge 1$. SYNTHETIC-DIVISION$(a, u)$ returns $b = [b_0, \ldots, b_{n-1}]$ and $r$ with

$$f = (x - u) \sum_{j=0}^{n-1} b_j x^j + r, \qquad r = f(u), \qquad b_{n-1} = a_n.$$

*Proof.* Lines S1 to S4 define $b_{n-1} = a_n$, $b_{i-1} = b_i u + a_i$ for $i = n - 1, \ldots, 1$, and $r = b_0 u + a_0$. Let $q = \sum_{j=0}^{n-1} b_j x^j$. Then

$$(x - u) q + r = \sum_{j=0}^{n-1} b_j x^{j+1} - \sum_{j=0}^{n-1} u b_j x^j + r.$$

Collect the coefficient of each power. For $x^n$ it is $b_{n-1} = a_n$. For $x^i$ with $1 \le i \le n - 1$ it is $b_{i-1} - u b_i = (b_i u + a_i) - u b_i = a_i$, by line S3 and commutativity of $R$. For $x^0$ it is $r - u b_0 = a_0$, by line S4. So $(x - u) q + r = f$. The values $b_{n-1}, \ldots, b_0, r$ are exactly the successive values of $s$ in HORNER$(a, u)$ (line L2, then line L4 for $i = n - 1, \ldots, 0$), so $r = f(u)$ by Lemma 1. $\square$

**Lemma 3 (TAYLOR-SHIFT).** TAYLOR-SHIFT$(a, u)$ returns $c = [c_0, \ldots, c_n]$ with $f(x) = \sum_{k=0}^{n} c_k (x - u)^k$. Equivalently, $f(x + u) = \sum_{k=0}^{n} c_k x^k$.

*Proof.* For $0 \le k \le n$ write $P_k(x) = \sum_{j=0}^{n-k} c[k + j]\, x^j$ for the polynomial formed by the top part of the current list. We prove the invariant

> **(T)** before round $k$ of the loop of line T2 (for $k = 0, \ldots, n$, with $k = n$ meaning after the loop), $f(x) = \sum_{j<k} c[j] (x - u)^j + (x - u)^k P_k(x)$.

*Initialization.* For $k = 0$, line T1 sets $c = a$, so $P_0 = f$, the first sum is empty, and (T) reads $f = f$.

*Maintenance.* Round $k$ runs line T4 for $i = n - 1$ down to $k$. Write $p_j = c[k + j]$ for the entries before the round, so $P_k = \sum_{j=0}^{n-k} p_j x^j$, and write $c'$ for the entries after the round. The entry $c[n]$ is not changed, so $c'[n] = p_{n-k}$. For $i$ from $n - 1$ down to $k$, line T4 sets $c'[i] = c[i] + u \cdot c'[i + 1]$, because $c[i + 1]$ was already updated (or is $c[n]$). With $\beta_{j} = c'[k + 1 + j]$ for $0 \le j \le n - k - 1$, this reads $\beta_{n-k-1} = p_{n-k}$, $\beta_{j-1} = \beta_j u + p_j$ for $j = n - k - 1, \ldots, 1$, and $c'[k] = \beta_0 u + p_0$. These are the recurrences of SYNTHETIC-DIVISION applied to $P_k$, if $n - k \ge 1$. By Lemma 2, $P_k = (x - u) P_{k+1} + c'[k]$, where $P_{k+1} = \sum_j \beta_j x^j$ is the polynomial formed by $c'[k+1..n]$, and $c'[k] = P_k(u)$. Entries below $k$ are not touched. Substituting into (T):

$$f = \sum_{j<k} c'[j](x - u)^j + (x - u)^k \bigl((x - u) P_{k+1} + c'[k]\bigr) = \sum_{j<k+1} c'[j] (x - u)^j + (x - u)^{k+1} P_{k+1},$$

which is (T) for $k + 1$. (Lemma 2 is stated for the list $a$, but its proof uses only the recurrences, so it applies to any list of length at least 2.)

*Termination.* The loop runs for $k = 0, \ldots, n - 1$. Then (T) holds for $k = n$, and $P_n = c[n]$ is a constant. So $f = \sum_{j<n} c[j](x - u)^j + c[n](x - u)^n = \sum_{k=0}^{n} c_k (x - u)^k$. Substituting $x + u$ for $x$, which is a ring homomorphism of $R[x]$, gives $f(x + u) = \sum c_k x^k$. If $n = 0$, the loop does not run and $c = [a_0]$, which is correct. $\square$

**Corollary (Taylor coefficients).** If $k!$ is a unit in $R$, then $c_k = f^{(k)}(u)/k!$, where $f^{(k)}$ is the $k$-th formal derivative. *Proof.* Differentiate $f = \sum_j c_j (x - u)^j$ formally $k$ times: the terms with $j < k$ vanish, the term $j = k$ gives $k!\, c_k$, and the terms with $j > k$ keep a factor $(x - u)$, which vanishes at $x = u$. So $f^{(k)}(u) = k!\, c_k$. In particular $c_0 = f(u)$ and $c_1 = f'(u)$ over every commutative ring. $\square$

**Theorem.** HORNER, SYNTHETIC-DIVISION and TAYLOR-SHIFT are correct, by Lemmas 1, 2 and 3. HORNER uses exactly $n$ multiplications and $n$ additions for degree $n$, because line L4 runs $n$ times; SYNTHETIC-DIVISION uses the same; TAYLOR-SHIFT runs line T4 $\sum_{k=0}^{n-1} (n - k) = n(n + 1)/2$ times. $\blacksquare$

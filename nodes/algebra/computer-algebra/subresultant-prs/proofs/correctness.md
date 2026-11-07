---
title: The subresultant PRS algorithm computes the subresultant chain
proves: [correctness]
status: full
---

**Setting.** $R$ is an integral domain with fraction field $F$; $f, g \in R[x]$ with $\deg f = m \ge \deg g = n \ge 1$. $S_0, \ldots, S_{n-1}$ are the subresultants as defined on the page, $s_j$ is the coefficient of $x^j$ in $S_j$, and $S_n = \operatorname{LC}(g)^{m-n-1} g \in F[x]$, with $s_n = \operatorname{LC}(g)^{m-n}$. Each $S_j$ with $j < n$ lies in $R[x]$, because its coefficients are determinants of matrices with entries in $R$.

**Theorem (structure of the subresultant chain).** This is the fundamental theorem of Brown and Traub (1971), in the form of von zur Gathen and Gerhard, Section 11.2, and of Ducos (2000); we use it without proof.

- (T0) $S_{n-1} = \operatorname{prem}(f, g) / (-1)^{m-n+1}$.
- (T1) Let $j < n$, let $S_{j+1}$ be regular ($\deg S_{j+1} = j + 1$), and let $S_j \ne 0$ have degree $d \le j$. Then $S_k = 0$ for $d < k < j$ and $S_d = (\operatorname{LC}(S_j) / s_{j+1})^{j-d} S_j$; in particular $S_d$ is regular.
- (T2) In the situation of (T1), if $d \ge 1$, then $S_{d-1} = \operatorname{prem}(S_{j+1}, S_j) / (-s_{j+1})^{j-d+2}$.
- (T3) If $S_{j+1}$ is regular and $S_j = 0$, then $S_k = 0$ for all $k < j$.

**Lemma 1.** For $\lambda \in F^*$, $\operatorname{prem}(\lambda B, C) = \lambda \operatorname{prem}(B, C)$. *Proof.* $\operatorname{prem}(B, C) = \operatorname{LC}(C)^{e} (B \bmod C)$ in $F[x]$ with $e = \deg B - \deg C + 1$, and $(\lambda B) \bmod C = \lambda (B \bmod C)$. $\square$

**Invariant.** At the start of each pass (line L5), with $b = \deg B$:

1. $B \ne 0$, $S_b$ is regular, $B = \mu S_b$ for some $\mu \in F^*$, and $s = s_b$;
2. $A$ is the member before $B$, and $\beta = -\operatorname{LC}(A) \cdot (-s_a)^{a - b}$ on every pass but the first, where $a = \deg A$ and $s_a$ is the principal coefficient of the regular $S_a$ (on the first pass, $\beta = (-1)^{m-n+1}$);
3. the entries $S_k$ for $k \ge b$ that the algorithm stores are correct, and the stored entries for $k < b$ are still 0.

*Start.* $A = f$, $B = g$, $b = n$, $S_n = \operatorname{LC}(g)^{m-n-1} g$ is regular with $s_n = \operatorname{LC}(g)^{m-n}$, as on line L3, and $B = \operatorname{LC}(g)^{-(m-n-1)} S_n$. Line L4 sets $\beta$ as in part 2. No entry is stored yet.

*One pass.* Let $j = b - 1$. Line L6 computes $C = \operatorname{prem}(A, B) / \beta$.

On the first pass, $C = S_{n-1}$ by (T0). On a later pass, $A = \nu S_a$ for some $\nu \in F^*$ by part 1 of the invariant from the previous pass, and the previous pass had $C = B$ equal to the subresultant $S_{a-1}$, of degree $b$, with $S_b$ regular by (T1). By (T2) applied with $j + 1 = a$ and $S_j = S_{a-1}$ of degree $b$, $S_{b-1} = \operatorname{prem}(S_a, S_{a-1}) / (-s_a)^{a-b+1}$. By Lemma 1 and $S_a = A / \nu$, with $\operatorname{LC}(A) = \nu s_a$:

$$S_{b-1} = \frac{\operatorname{prem}(A, B)}{\nu \, (-s_a)^{a-b+1}} = \frac{\operatorname{prem}(A, B)}{-\operatorname{LC}(A) \, (-s_a)^{a-b}} = \frac{\operatorname{prem}(A, B)}{\beta}.$$

So in every pass $C = S_{b-1} = S_j$, and $C \in R[x]$, so the division on line L6 is exact.

If $C = 0$, then $S_j = 0$, and by (T3) all $S_k$ with $k < j$ are zero, as stored. The algorithm returns at line L7 with the chain complete.

Otherwise line L8 stores $S_j = C$. Let $d = \deg C$ and $e = b - d \ge 1$. By (T1), with $S_{j+1} = S_b$ regular, $S_k = 0$ for $d < k < j$, which are still 0 as stored, and $S_d = (\operatorname{LC}(C) / s_b)^{j-d} C = \operatorname{LC}(C)^{e-1} C / s^{e-1}$. If $e = 1$, then $d = j$ and this is $C$ itself; if $e \ge 2$, line L9 stores it. In both cases $S_d$ is regular and lies in $R[x]$, so the division on line L9 is exact. If $d = 0$, all entries are now stored and the algorithm returns at line L10.

If $d \ge 1$, line L11 sets $\beta = -\operatorname{LC}(B) (-s_b)^{b-d}$, line L12 sets $s = s_d$, and line L13 shifts the pair to $(B, C)$. Now $C = S_j$ is a nonzero multiple of the regular $S_d$, by (T1). So the invariant holds for the next pass, with $a$ replaced by $b$ and $b$ by $d$.

*Termination.* $\deg B$ falls strictly in each pass, so the loop ends after at most $n$ passes, at line L7 or L10.

*The gcd.* Over $F$, $\operatorname{prem}(A, B)$ is a nonzero constant times $A \bmod B$, and so is $C$. So the pairs $(A, B)$ follow the Euclidean algorithm over $F$ up to constant factors, and they keep the set of common divisors in $F[x]$. At line L7, $B$ divides $A$ in $F[x]$, so $B$ is an associate of $\gcd(f, g)$ over $F$. At line L10, $C$ is a nonzero constant, so $\gcd(f, g) = 1$ over $F$. By Gauss's lemma, $\gcd(\operatorname{cont} f, \operatorname{cont} g) \cdot \operatorname{pp}(B)$ is the gcd in $\mathbb{Z}[x]$ in the first case, and the content gcd alone in the second. $\blacksquare$

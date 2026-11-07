---
title: Partial fractions by Chinese remaindering exist, are unique and are computed correctly
proves: [correctness, termination]
status: full
---

Fix a field $K$ and work in $K[x]$, one variable, with $\deg 0 = -\infty$. Let $b_1, \ldots, b_k$ have degree at least $1$ and be pairwise coprime, let $e_i \ge 1$, let $b = \prod_i b_i^{e_i}$, $d = \deg b$, and let $a \in K[x]$. Write $B_i = b_i^{e_i}$ and $c_i = b / B_i$.

**Fact 1 (coprimality).** $\gcd(c_i, B_i) = 1$. If an irreducible $p$ divides $B_i$ then $p \mid b_i$. If $p$ also divided $c_i = \prod_{j \ne i} b_j^{e_j}$, then $p \mid b_j$ for some $j \ne i$, so $p$ divides $\gcd(b_i, b_j) = 1$, which is impossible.

**Termination.** Line L2 is one division with remainder. The loop of line L3 runs $k$ times. In each pass, line L4 is one exact division (it is exact because $B_i \mid b$), line L5 is one run of the extended Euclidean algorithm, which stops because the degrees of the remainders strictly decrease, line L6 is one division, and the inner loop of line L7 runs exactly $e_i$ times, each a single division. So the algorithm stops.

**Line L5 succeeds.** By Fact 1 the extended Euclidean algorithm on $c_i$ and $B_i$ returns $s_i, t_i$ with $s_i c_i + t_i B_i = 1$, so $s_i c_i \equiv 1 \pmod{B_i}$.

**Claim 1.** After line L2, $a_{\text{old}} = q b + a$ with $\deg a < d$, by the division identity. So $a_{\text{old}} / b = q + a / b$, and it remains to decompose the proper fraction $a / b$.

**Claim 2.** With $r_i = (a s_i) \bmod B_i$ from line L6, $a = \sum_{i=1}^k r_i c_i$. Let $S = \sum_i r_i c_i$. Fix $i$. For $j \ne i$, $B_i \mid c_j$, so $r_j c_j \equiv 0 \pmod{B_i}$. Also $r_i c_i \equiv a s_i c_i \equiv a \pmod{B_i}$ by line L5. Hence $S \equiv a \pmod{B_i}$ for each $i$. The $B_i$ are pairwise coprime (Fact 1 applied to any pair), so their product $b$ divides $S - a$. Now $\deg (r_i c_i) < \deg B_i + \deg c_i = d$, so $\deg (S - a) < d$, and a multiple of $b$ of degree less than $d$ is $0$. So $S = a$. Dividing by $b$ gives $a / b = \sum_i r_i / B_i$.

**Claim 3.** The inner loop of lines L7 and L8 produces $a_{i e_i}, \ldots, a_{i 1}$ with $\deg a_{ij} < \deg b_i$ and $r_i = \sum_{j=1}^{e_i} a_{ij} b_i^{e_i - j}$. Let $\rho_0 = r_i$ and let the pass with index $j$ compute $\rho_{e_i - j + 1} = \rho_{e_i - j} \operatorname{quo} b_i$ and $a_{ij} = \rho_{e_i - j} \operatorname{rem} b_i$. By the division identity $\rho_t = a_{i, e_i - t} + \rho_{t+1} b_i$ for $t = 0, \ldots, e_i - 1$, with each $\deg a_{ij} < \deg b_i$. Substituting repeatedly gives $r_i = \sum_{t=0}^{e_i - 1} a_{i, e_i - t} b_i^t + \rho_{e_i} b_i^{e_i}$. Since $\deg r_i < \deg B_i = e_i \deg b_i$ and each division by $b_i$ lowers the degree by $\deg b_i$, we get $\deg \rho_{e_i} < 0$, so $\rho_{e_i} = 0$. With $j = e_i - t$ this is the claim. Dividing by $B_i = b_i^{e_i}$ gives $r_i / B_i = \sum_{j=1}^{e_i} a_{ij} / b_i^{j}$.

Claims 1 to 3 together give $a_{\text{old}} / b = q + \sum_i \sum_{j} a_{ij} / b_i^j$ with $\deg a_{ij} < \deg b_i$, which is the required output.

**Uniqueness.** Suppose $q + \sum_{i,j} a_{ij} / b_i^j = q' + \sum_{i,j} a'_{ij} / b_i^j$, both with numerator degrees below $\deg b_i$. Multiply by $b$ and set $\delta_{ij} = a_{ij} - a'_{ij}$. Then $(q - q') b = -\sum_{i,j} \delta_{ij} b_i^{e_i - j} c_i$. The right side has degree less than $d$, because $\deg (\delta_{ij} b_i^{e_i - j}) < e_i \deg b_i$, so $q = q'$ and $\sum_i R_i c_i = 0$ with $R_i = \sum_j \delta_{ij} b_i^{e_i - j}$. Reducing modulo $B_i$ gives $R_i c_i \equiv 0 \pmod{B_i}$, and since $c_i$ is invertible modulo $B_i$, $B_i \mid R_i$. But $\deg R_i < \deg B_i$, so $R_i = 0$. Finally $R_i = 0$ is a base $b_i$ expansion of $0$ with digits of degree below $\deg b_i$: the lowest digit $\delta_{i e_i} = R_i \operatorname{rem} b_i = 0$, and dividing by $b_i$ and repeating shows every $\delta_{ij} = 0$. So the decomposition is unique, and the algorithm returns it. $\blacksquare$

---
title: The Euclidean algorithm returns gcd(a, b) and stops after at most 1 + log_phi b steps
proves: [correctness, termination, time.worst]
status: full
---

We use the pseudocode EUCLID of the page. The inputs $a_0, b_0$ are any integers. We write $\gcd(x, y)$ for the greatest common divisor of $x$ and $y$, with $\gcd(x, 0) = |x|$ and $\gcd(0, 0) = 0$.

**Lemma 1 (the step keeps the gcd).** Let $a \ge 0$ and $b > 0$ be integers, and let $r = a \bmod b$. Then $\gcd(a, b) = \gcd(b, r)$.

*Proof.* Write $a = qb + r$ with $q = \lfloor a/b \rfloor$. If $d \mid a$ and $d \mid b$, then $d \mid a - qb = r$. If $d \mid b$ and $d \mid r$, then $d \mid qb + r = a$. So the pairs $(a, b)$ and $(b, r)$ have the same set of common divisors. Both pairs have a non-zero member ($b > 0$), so the set is finite and its largest element is the gcd of each pair. $\square$

**Theorem 1 (correctness).** EUCLID$(a_0, b_0)$ stops and returns $\gcd(a_0, b_0)$.

*Proof.* After line L1, $a = |a_0|$ and $b = |b_0|$. Since $d \mid x$ if and only if $d \mid |x|$, $\gcd(a, b) = \gcd(a_0, b_0)$. We use this invariant of the loop of line L2:

> **(G)** $a \ge 0$, $b \ge 0$, and $\gcd(a, b) = \gcd(a_0, b_0)$.

*Initialization.* True after line L1, as shown above.

*Maintenance.* Assume (G) and $b \ne 0$, so $b > 0$. Line L3 computes $r = a \bmod b$, with $0 \le r < b$. Lines L4 and L5 make the new pair $(a', b') = (b, r)$. Both are non-negative, and by Lemma 1, $\gcd(a', b') = \gcd(a, b) = \gcd(a_0, b_0)$.

*Termination.* The value $b$ is a non-negative integer, and each iteration replaces it by $r \le b - 1$. So it drops by at least $1$ at each iteration, and the loop runs at most $|b_0|$ times before $b = 0$.

*Conclusion.* At exit $b = 0$, and (G) gives $\gcd(a_0, b_0) = \gcd(a, 0) = a$, because $a \ge 0$. Line L6 returns $a$. $\blacksquare$

**Lemma 2 (Fibonacci bound).** Let $F_0 = 0$, $F_1 = 1$, $F_{j+2} = F_{j+1} + F_j$. If $a > b \ge 1$ and the loop runs $k \ge 1$ times on $(a, b)$, then $b \ge F_{k+1}$ and $a \ge F_{k+2}$.

*Proof.* By induction on $k$. Base $k = 1$: $b \ge 1 = F_2$, and $a > b \ge 1$ gives $a \ge 2 = F_3$. Step: let $k \ge 2$ and assume the lemma for $k - 1$. The first iteration turns $(a, b)$ into $(b, r)$ with $r = a \bmod b < b$. The loop runs $k - 1 \ge 1$ more times, so $r \ne 0$, and $b > r \ge 1$. By the induction hypothesis applied to $(b, r)$, $r \ge F_k$ and $b \ge F_{k+1}$. Since $a > b$, the quotient $q = \lfloor a/b \rfloor$ is at least $1$, so $a = qb + r \ge b + r \ge F_{k+1} + F_k = F_{k+2}$. $\square$

**Theorem 2 (Lamé's bound).** If $a \ge b \ge 1$, the loop runs at most $1 + \log_\varphi b$ times, where $\varphi = (1 + \sqrt 5)/2$. If $0 \le a < b$, it runs at most $2 + \log_\varphi a$ times when $a \ge 1$, once when $a = 0$, and not at all when $b = 0$.

*Proof.* Let the loop run $k$ times on $a \ge b \ge 1$. If $a = b$, then $a \bmod b = 0$ and $k = 1 \le 1 + \log_\varphi b$. If $a > b$, Lemma 2 gives $b \ge F_{k+1}$. We show $F_{j} \ge \varphi^{j-2}$ for $j \ge 1$ by induction. $F_1 = 1 \ge \varphi^{-1}$ and $F_2 = 1 = \varphi^0$. For $j \ge 3$, $F_j = F_{j-1} + F_{j-2} \ge \varphi^{j-3} + \varphi^{j-4} = \varphi^{j-4}(\varphi + 1) = \varphi^{j-2}$, since $\varphi^2 = \varphi + 1$. So $b \ge F_{k+1} \ge \varphi^{k-1}$, which gives $k \le 1 + \log_\varphi b$. If $0 < a < b$, the first iteration gives $(b, a)$ with $b > a \ge 1$, and the rest runs at most $1 + \log_\varphi a$ times. If $a = 0 < b$, the first iteration gives $(b, 0)$ and the loop stops. $\blacksquare$

**Tightness.** For $k \ge 1$, the input $(F_{k+2}, F_{k+1})$ makes the loop run exactly $k$ times. For $j \ge 3$, $F_{j+1} = 1 \cdot F_j + F_{j-1}$ with $0 \le F_{j-1} < F_j$, so $F_{j+1} \bmod F_j = F_{j-1}$ and one iteration maps $(F_{j+1}, F_j)$ to $(F_j, F_{j-1})$. Starting from $j = k + 1$, after $k - 1$ iterations the pair is $(F_3, F_2) = (2, 1)$, and one more iteration gives $(1, 0)$. So the bound $\Theta(\log b)$ is reached.

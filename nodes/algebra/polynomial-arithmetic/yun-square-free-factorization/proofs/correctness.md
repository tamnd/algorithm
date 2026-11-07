---
title: Yun's algorithm returns the square-free factorization, at the cost of a constant number of gcds
proves: [correctness]
status: full
---

Let $F$ be a field of characteristic $0$ or of characteristic $p > n$, and let $f \in F[x]$ be monic of degree $n \ge 1$ (the implementation first divides by the leading coefficient). Let $f = \prod_{j=1}^{k} a_j^{\,j}$ be the square-free factorization, with the $a_j$ monic, square-free, pairwise coprime and $a_k \ne 1$; it exists and is unique, as shown on the [square-free factorization](/square-free-factorization/) page.

**Step 0. Each $a_j$ is coprime to $j\, a_j'$.** If $a_j = 1$ there is nothing to show. Otherwise let $q$ be an irreducible factor of $a_j$. Over a field of characteristic $0$, $q' \ne 0$ because $\deg q \ge 1$. In characteristic $p > n$, $q' = 0$ would force $q$ to be a polynomial in $x^p$ and so $\deg q \ge p > n$, which is impossible. So $q' \ne 0$, $\deg q' < \deg q$, and $q \nmid q'$. Write $a_j = q\, r$ with $q \nmid r$, because $a_j$ is square-free. Then $a_j' = q' r + q r'$, and $q \nmid q' r$, so $q \nmid a_j'$. Also $j \le n$, so $j \ne 0$ in $F$, and $q \nmid j a_j'$. This holds for every irreducible factor $q$ of $a_j$, so $\gcd(a_j, j a_j') = 1$.

**Notation.** For $1 \le i \le k + 1$ let

$$b_i = \prod_{j \ge i} a_j, \qquad e_i = \sum_{j \ge i} (j - i + 1)\, a_j'\, \frac{b_i}{a_j}, \qquad d_i = e_i - b_i' = \sum_{j > i} (j - i)\, a_j'\, \frac{b_i}{a_j},$$

with $b_{k+1} = 1$. The last form of $d_i$ uses $b_i' = \sum_{j \ge i} a_j'\, b_i / a_j$, the product rule, and the term $j = i$ of $e_i$ has the factor $j - i + 1 = 1$.

**Lines L2 and L3.** By the product rule, $f' = \sum_j j\, a_j^{\,j-1} a_j' \prod_{l \ne j} a_l^{\,l}$. Let $g = \prod_j a_j^{\,j-1}$. Then $f = g\, b_1$ and $f' = g\, e_1$, since $j a_j^{j-1} a_j' \prod_{l \ne j} a_l^l = g \cdot j a_j' b_1 / a_j$. Also $\gcd(b_1, e_1) = 1$: for each $j$, every term of $e_1$ except the term $j$ is divisible by $a_j$, and the term $j$, $j a_j' b_1 / a_j$, is coprime to $a_j$ by Step 0 and because the $a_l$ are pairwise coprime. So $\gcd(f, f') = g \gcd(b_1, e_1) = g$, as $g$ is monic. Line L2 computes $b = g$ and line L3 computes $c = f / g = b_1$ and $d = f'/g - c' = e_1 - b_1' = d_1$.

**Loop invariant.** At the $i$th test of line L4, $c = b_i$ and $d = d_i$, and the list holds $a_1, \ldots, a_{i-1}$. It holds for $i = 1$ by the previous paragraph.

*Line L5.* We show $\gcd(b_i, d_i) = a_i$. Each term of $d_i$ has $j > i$, so its factor $b_i / a_j$ contains $a_i$; so $a_i \mid d_i$. For $j > i$, every term of $d_i$ other than the term $j$ is divisible by $a_j$, and the term $j$, $(j - i)\, a_j'\, b_i / a_j$, is coprime to $a_j$: $j - i$ is between $1$ and $n$, so it is nonzero in $F$, $a_j$ is coprime to $a_j'$ by Step 0, and $a_j$ is coprime to the other $a_l$. So $\gcd(a_j, d_i) = 1$ for $j > i$. Since $b_i = a_i \prod_{j > i} a_j$ with pairwise coprime factors, $\gcd(b_i, d_i) = a_i \cdot \prod_{j > i} \gcd(a_j, d_i / a_i) = a_i$; the gcd of $a_j$ with $d_i / a_i$ is $1$ because it divides $\gcd(a_j, d_i) = 1$. This also covers $a_i = 1$.

*Lines L6 to L8.* Line L6 appends $a_i$. Line L7 sets $c = b_i / a_i = b_{i+1}$. Line L8 sets $d = d_i / a_i - b_{i+1}'$. Now $d_i / a_i = \sum_{j > i} (j - i)\, a_j'\, b_{i+1} / a_j = \sum_{j \ge i+1} (j - (i + 1) + 1)\, a_j'\, b_{i+1} / a_j = e_{i+1}$, so $d = e_{i+1} - b_{i+1}' = d_{i+1}$. The invariant holds for $i + 1$.

**Termination and result.** $b_i = 1$ exactly when $a_j = 1$ for all $j \ge i$, that is when $i > k$, because $a_k \ne 1$. So the loop runs for $i = 1, \ldots, k$ and stops with the list $a_1, \ldots, a_k$, which line L9 returns with the leading coefficient of the input. A constant input is handled before line L1.

**Cost.** Let $n_i = \deg b_i = \sum_{j \ge i} \deg a_j$. Then $\sum_{i=1}^{k} n_i = \sum_j j \deg a_j = n$, and $\deg d_i < n_i$. Iteration $i$ makes one gcd of two polynomials of degree at most $n_i$, two exact divisions of polynomials of degree at most $n_i$, and one derivative. With the Euclidean algorithm and schoolbook division these cost $O(n_i^2)$, and $\sum_i n_i^2 \le (\sum_i n_i)^2 = n^2$. Lines L2 and L3 cost $O(n^2)$. So the total is $O(n^2)$ field operations. If a gcd of degree $d$ costs $G(d)$ with $G(d)/d$ nondecreasing, then $\sum_i G(n_i) \le \sum_i (n_i / n) G(n) = G(n)$, and with fast division the total is $O(G(n) + M(n) \log n) = O(M(n) \log n)$ with the fast Euclidean algorithm. $\blacksquare$

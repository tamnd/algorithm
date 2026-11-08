---
title: The in-place twist computes the MT recurrence, tempering is a bijection, and the period follows from primitivity
proves: [correctness]
status: full
---

We use the pseudocode of the page and the parameter names of Matsumoto and Nishimura: word size $w = 32$, degree $n = 624$, middle offset $m = 397$ (an index offset, not a modulus), separation point $r = 31$, twist constant $\mathbf a$, and tempering shifts $u, s, t, l$ and masks $\mathbf b, \mathbf c$. For a word $x$, $x^u$ is its upper $w - r$ bits (the other bits cleared) and $x^l$ its lower $r$ bits. For a word $y$ with lowest bit $y_0$, $y A = (y \gg 1)$ if $y_0 = 0$ and $(y \gg 1) \oplus \mathbf a$ if $y_0 = 1$. The recurrence is

$$x_{k+n} = x_{k+m} \oplus \left(x_k^u \mid x_{k+1}^l\right) A \qquad (k \ge 0). \tag{MT}$$

**Lemma 1 (one twist).** Suppose the array holds $x[i] = x_{jn+i}$ for $0 \le i < n$ before MT-TWIST. Then after it, $x[i] = x_{(j+1)n+i}$ for $0 \le i < n$.

*Proof.* We show the invariant: before the iteration with index $k$ of line L1, $x[i] = x_{(j+1)n+i}$ for $i < k$ and $x[i] = x_{jn+i}$ for $i \ge k$. It holds for $k = 0$. In iteration $k$, put $K = jn + k$; line L6 must store $x_{K+n}$, which by (MT) needs $x_K$, $x_{K+1}$ and $x_{K+m}$.

- $x[k]$ is not yet replaced, so it holds $x_K$.
- If $k + 1 < n$, $x[k+1]$ is not yet replaced and holds $x_{K+1}$. If $k = n - 1$, the index $(k+1) \bmod n = 0$ was replaced in iteration 0 and holds $x_{(j+1)n} = x_{K+1}$.
- If $k + m < n$, $x[k+m]$ holds $x_{K+m}$. If $k + m \ge n$, the index $k + m - n < k$ was replaced and holds $x_{(j+1)n + k + m - n} = x_{K+m}$.

Line L2 forms $y = x_K^u \mid x_{K+1}^l$, and lines L3 to L5 form $x_{K+m} \oplus (y \gg 1)$, XORed with $\mathbf a$ when $y$ is odd, which is $x_{K+m} \oplus yA$. So line L6 stores $x_{K+n}$ in $x[k]$, and the invariant holds for $k + 1$. At $k = n$ it is the claim. $\square$

**Lemma 2 (the output sequence).** After the initialization, which sets $x[i] = x_i$ for $0 \le i < n$ and $i = n$, the $q$-th call of MT-NEXT ($q = 0, 1, \ldots$) returns $T(x_{n+q})$, where $T$ is the tempering map of lines L11 to L14.

*Proof.* The call with $i = n$ runs MT-TWIST, which by Lemma 1 (with $j = 0$) leaves $x_{n}, \ldots, x_{2n-1}$, and resets $i$ to 0. Calls then read $x[i]$ for $i = 0, \ldots, n-1$, which are $x_{n+i}$, and the next twist gives the next block by Lemma 1 again. Induction on the number of twists finishes the proof. $\square$

**Lemma 3 (tempering is a bijection of 32-bit words).** Each of the four steps of $T$ is invertible, so $T$ is a bijection and is linear over GF(2).

*Proof.* Each step has the form $y \mapsto y \oplus ((y \gg k) \wedge M)$ or $y \mapsto y \oplus ((y \ll k) \wedge M)$ with $k \ge 1$. Consider the left-shift form. Bit $i$ of the result is $y_i \oplus (M_i \wedge y_{i-k})$. Given the result $z$, recover $y_0, \ldots, y_{k-1}$ from $z$ directly (they are not changed), and then $y_i = z_i \oplus (M_i \wedge y_{i-k})$ for $i = k, k+1, \ldots, 31$ in increasing order. So the step is injective on a finite set, hence bijective. The right-shift form is the same with the bits taken from the top. Each step is a XOR of $y$ with a masked shift of $y$, so it is GF(2)-linear, and so is the composition. $\square$

Lemma 3 also shows why the Mersenne Twister is not cryptographic: inverting $T$ on 624 consecutive outputs gives $x_{n+q}, \ldots, x_{n+q+623}$, which is a full state, and then (MT) predicts every later output.

**Lemma 4 (the state space).** The future of the sequence from index $k$ depends only on the $p = nw - r = 19937$ bits $(x_k^u, x_{k+1}, \ldots, x_{k+n-1})$, and the map from this state to the state at index $k+1$ is GF(2)-linear and bijective.

*Proof.* In (MT) the word $x_k$ enters only through $x_k^u$, and later equations use $x_{k+1}, x_{k+2}, \ldots$. So the state $\sigma_k = (x_k^u, x_{k+1}, \ldots, x_{k+n-1})$, with $(w - r) + (n-1)w = nw - r$ bits, determines $x_{k+n}$ and thus $\sigma_{k+1} = (x_{k+1}^u, x_{k+2}, \ldots, x_{k+n})$. The map is a composition of masks, shifts and XORs, so it is linear. It is injective: from $\sigma_{k+1}$ we know $x_{k+n}$, $x_{k+m}$ and $x_{k+1}^l$, so $(x_k^u \mid x_{k+1}^l) A = x_{k+n} \oplus x_{k+m}$ is known; $A$ is injective on words because $\mathbf a$ has its top bit set (the top bit of $yA$ equals $y_0$, and the other bits give $y_1, \ldots, y_{31}$), so $x_k^u$ is recovered. A linear injective map of a finite space onto itself is bijective. $\square$

**Theorem (period).** Let $\varphi$ be the characteristic polynomial of the transition matrix of Lemma 4. Matsumoto and Nishimura verified by computation that $\varphi$ is primitive of degree 19937 over GF(2). Hence every nonzero state $\sigma_0$ has period $2^{19937} - 1$, and the output sequence of MT-NEXT has the same period.

*Proof.* A linear map whose characteristic polynomial is primitive of degree $p$ has period $2^p - 1$ on each nonzero vector: the argument is the one for the Galois form of an [LFSR](/linear-feedback-shift-register/), because the matrix is similar to the companion matrix of $\varphi$ when $\varphi$ is irreducible (its minimal polynomial is then $\varphi$). So the state period is $2^{19937} - 1$. The output $T(x_{n+q})$ is a bijective function of the word $x_{n+q}$, and the state $\sigma_{n+q+1}$ is determined by the $n$ words $x_{n+q+1}, \ldots, x_{2n+q}$, so the output sequence determines the state sequence; the output period therefore equals the state period. $\blacksquare$

**What is proved by computation and what is not.** The primitivity of $\varphi$ and the dimensions of equidistribution are exact computations reported by the authors; the test file checks the degree independently: the Berlekamp-Massey algorithm finds linear complexity exactly 19937 for the lowest output bit, which is what an irreducible $\varphi$ of degree 19937 predicts. The statistical behaviour in test batteries is empirical.

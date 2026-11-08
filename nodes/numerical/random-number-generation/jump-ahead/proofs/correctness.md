---
title: Jump-ahead returns the state n steps later
proves: [correctness]
status: full
---

We use the pseudocode of the page. In the affine case $f(s) = (a s + c) \bmod m$ on $S = \{0, \ldots, m-1\}$, with $m \ge 1$. In the $\mathbb{F}_2$-linear case $S = \mathbb{F}_2^k$ and $f(s) = A s$ for a binary $k \times k$ matrix $A$, and $\varphi \in \mathbb{F}_2[x]$ has degree $k \ge 1$ and $\varphi(A) = 0$.

**Lemma 1 (affine maps).** For integers $A, C$ let $\tau_{A,C}(s) = (A s + C) \bmod m$. Then $\tau_{B,D} \circ \tau_{A,C} = \tau_{BA \bmod m, \, (BC + D) \bmod m}$ on $S$, and $\tau_{1,0}$ is the identity.

*Proof.* $B (A s + C) + D = (BA) s + (BC + D)$, and reducing any intermediate value modulo $m$ does not change the result modulo $m$. $\square$

**Lemma 2 (loop invariant of LCG-JUMP).** Let $n_0$ be the input distance. Before the test on line L3 in iteration $i \ge 0$ (that is, after $i$ completed iterations), $\tau_{A,C} = f^{\,n_0 \bmod 2^i}$, $\tau_{B,D} = f^{\,2^i}$ and $n = \lfloor n_0 / 2^i \rfloor$.

*Proof.* For $i = 0$, lines L1 and L2 give the identity $= f^0$ and $f = f^1$, and $n = n_0$. Assume the claim for $i$ and that $n > 0$. Let $b = n \bmod 2$, which is bit $i$ of $n_0$, so $n_0 \bmod 2^{i+1} = (n_0 \bmod 2^i) + b\, 2^i$. If $b = 1$, line L4 replaces $\tau_{A,C}$ by $\tau_{B,D} \circ \tau_{A,C} = f^{2^i} \circ f^{n_0 \bmod 2^i}$ by Lemma 1, which is $f^{n_0 \bmod 2^{i+1}}$; if $b = 0$ it is unchanged and already equal to $f^{n_0 \bmod 2^{i+1}}$. Line L5 replaces $\tau_{B,D}$ by $\tau_{B,D} \circ \tau_{B,D} = f^{2^{i+1}}$ by Lemma 1 (the pair $(B \cdot B, B \cdot D + D)$ is the composition with $A = B$, $C = D$). Line L6 gives $\lfloor n / 2 \rfloor = \lfloor n_0 / 2^{i+1} \rfloor$. $\square$

**Theorem 1.** LCG-JUMP$(s, n_0)$ returns $f^{n_0}(s)$ for every $s \in S$ and every $n_0 \ge 0$, after $\lfloor \log_2 n_0 \rfloor + 1$ iterations when $n_0 > 0$ and none when $n_0 = 0$.

*Proof.* $n$ is halved each iteration, so the loop ends; it ends at the first $i$ with $\lfloor n_0 / 2^i \rfloor = 0$, that is $2^i > n_0$, so $n_0 \bmod 2^i = n_0$. By Lemma 2, $\tau_{A,C} = f^{n_0}$, and line L7 returns $\tau_{A,C}(s)$. $\square$

**Corollary (leapfrog).** For $p \ge 1$, LCG-JUMP's final pair for $n_0 = p$ is $(a^p \bmod m, \; c \sum_{j<p} a^j \bmod m)$, and the subsequence $s_j, s_{j+p}, s_{j+2p}, \ldots$ satisfies $s_{j+(t+1)p} = \tau_{A,C}(s_{j+tp})$.

*Proof.* By induction on $p$, $f^p = \tau_{a^p, \, c S_p(a)}$ with $S_p(a) = \sum_{j<p} a^j$, since $f \circ \tau_{a^p, cS_p} = \tau_{a^{p+1}, \, a c S_p + c} = \tau_{a^{p+1}, \, c S_{p+1}}$ by Lemma 1. Two pairs in $\{0, \ldots, m-1\}^2$ that define the same map on $S$ are equal (evaluate at $s = 0$ and $s = 1$), so the computed pair is this one. $\square$

**Lemma 3 (reduction).** Let $r(x) = x^n \bmod \varphi(x)$. Then $A^n = r(A)$.

*Proof.* Division in $\mathbb{F}_2[x]$ gives $x^n = q(x) \varphi(x) + r(x)$. Substituting $A$ is a ring homomorphism from $\mathbb{F}_2[x]$ to the matrices over $\mathbb{F}_2$, so $A^n = q(A) \varphi(A) + r(A) = r(A)$. $\square$

**Lemma 4 (Horner loop).** Let $d = \deg r$ (the loop is empty when $r = 0$ and returns the zero state, which is $r(A) s$). After the iteration of lines L11 and L12 with index $j$, $t = \sum_{i=j}^{d} r_i A^{i-j} s$.

*Proof.* Before the first iteration $t = 0$. Iteration $j$ sets $t \leftarrow A t$ (line L11, since $f$ is multiplication by $A$) and then adds $r_j s$ (line L12, as $\oplus$ is addition in $\mathbb{F}_2^k$). If before iteration $j$ we have $t = \sum_{i=j+1}^{d} r_i A^{i-j-1} s$ (true for $j = d$ with the empty sum), then after it $t = \sum_{i=j+1}^{d} r_i A^{i-j} s + r_j s = \sum_{i=j}^{d} r_i A^{i-j} s$. $\square$

**Theorem 2.** F2-JUMP$(s, n, \varphi)$ returns $A^n s = f^n(s)$.

*Proof.* At the end of the iteration with $j = 0$, Lemma 4 gives $t = \sum_{i=0}^{d} r_i A^i s = r(A) s$, which is $A^n s$ by Lemma 3. $\square$

**Proposition (choice of $\varphi$).** Let $h : \mathbb{F}_2^k \to \mathbb{F}_2$ be linear and $b_i = h(A^i s)$. If the characteristic polynomial $\chi$ of $A$ is irreducible and the sequence $b$ is not identically zero, then the minimal polynomial of the sequence $b$ (the connection polynomial of least degree, which Berlekamp-Massey returns from $2k$ terms) equals $\chi$, so it may be used as $\varphi$.

*Proof.* By Cayley-Hamilton $\chi(A) = 0$, so for every $i$, $\sum_j \chi_j b_{i+j} = h(A^i \chi(A) s) = 0$: $\chi$ generates $b$, and the minimal polynomial $\mu$ of $b$ divides $\chi$. As $\chi$ is irreducible, $\mu = 1$ or $\mu = \chi$, and $\mu = 1$ would mean $b = 0$. The linear complexity of $b$ is then $k$, and Berlekamp-Massey determines the unique minimal polynomial from any $2k$ consecutive terms (Massey 1969). $\square$

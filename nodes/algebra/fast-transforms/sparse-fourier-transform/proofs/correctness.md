---
title: SPARSE-DFT reports only correct coefficients for every K-sparse spectrum when T ≥ K, and finds the whole spectrum exactly when the support contains no stopping set
proves: [correctness, complexity]
status: full
---

**Setting.** Let $R$ be a field, $n = f_1 \cdots f_d$ with pairwise coprime $f_i \ge 1$, $n \ne 0$ in $R$, and $\omega \in R$ of order exactly $n$. For $x \in R^n$ let $X_k = \sum_{j<n} x_j \omega^{jk}$. Write $\omega_f = \omega^{n/f}$ for a divisor $f$ of $n$; it has order exactly $f$. Since $n \ne 0$ in $R$, every divisor of $n$ is nonzero in $R$, so the fractions $f_i/n$ and $n/f_i$ exist. Let $S = \{0, \ldots, T\} \cup \{n/f_1, \ldots, n/f_d\}$, and for $Y \in R^n$ define the *aliased sums*
$$A^{(i,s)}_b(Y) = \frac{f_i}{n} \sum_{0 \le k < n,\ k \equiv b \ (f_i)} Y_k\, \omega^{-sk}.$$

**Statement.** Suppose $X$ has at most $K$ nonzero entries and $T \ge K$. Then SPARSE-DFT terminates, every pair $(k, v)$ it returns has $v = X_k \ne 0$, and the flag *success* is true if and only if the returned map equals the nonzero part of $X$. This happens if and only if the support of $X$ contains no nonempty *stopping set*, a set $D$ such that for every $i$ and $b$ the bucket $\{k : k \equiv b \ (f_i)\}$ meets $D$ in $0$ or at least $2$ elements. The algorithm reads $F |S|$ samples, $F = \sum_i f_i$, and does $O((K + d) F (F + K + d + \log n))$ additions and multiplications.

**Lemma 1 (aliasing).** Line L2 sets $Z^{(i,s)} = A^{(i,s)}(X)$.

*Proof.* The inverse DFT gives $x_j = \frac1n \sum_k X_k \omega^{-jk}$; this uses that $\omega$ has order $n$, so $\sum_{j<n} \omega^{jm} = 0$ for $m \not\equiv 0 \ (n)$, and that $n$ is invertible. With $j = t n/f + s$, $\omega^{-jk} = \omega_f^{-tk} \omega^{-sk}$, and the sum over $j$ is unchanged by reducing indices modulo $n$. So
$$\sum_{t<f} x_{tn/f + s}\, \omega_f^{tb} = \frac1n \sum_k X_k \omega^{-sk} \sum_{t<f} \omega_f^{t(b - k)}.$$
The inner sum is $f$ if $k \equiv b \ (f)$, since then each term is $1$, and $0$ otherwise, since $\omega_f^{b-k} \ne 1$ is a root of $u^f - 1 = (u - 1)(1 + u + \cdots + u^{f-1})$. $\square$

**Lemma 2 (invariant).** At all times $Z^{(i,s)} = A^{(i,s)}(Y)$ for all $i, s$, where $Y = X - \sum_{k \in \text{found}} \text{found}[k]\, e_k$ is the residual spectrum.

*Proof.* True after line L2 by Lemma 1, with found empty. The aliased sums are linear in $Y$, and $A^{(l,s)}_c(v e_k)$ is $\frac{f_l}{n} v \omega^{-sk}$ for $c = k \bmod f_l$ and $0$ for other $c$. So the update at line L9, which adds $v$ to found$[k]$ and subtracts exactly these values, keeps the equality. Nothing else changes $Z$ or found. $\square$

**Lemma 3 (Vandermonde).** Let $D \subseteq [0, n)$ with $|D| \le T + 1$, and $c \in R^D$ with $\sum_{k \in D} c_k \omega^{-sk} = 0$ for $s = 0, 1, \ldots, T$. Then $c = 0$.

*Proof.* The elements $\omega^{-k}$, $k \in D$, are distinct because $\omega$ has order $n$. The rows $s = 0, \ldots, |D| - 1 \le T$ of the system form the square Vandermonde matrix $(\omega^{-sk})_{s, k}$ on distinct nodes, whose determinant $\prod_{k < k'} (\omega^{-k'} - \omega^{-k})$ is nonzero in the field $R$. $\square$

**Lemma 4 (soundness of one peel).** Suppose $|\mathrm{supp}\, Y| \le K$ when bucket $b$ of stage $i$ passes line L8 with $(k, v)$. Then $k \equiv b \ (f_i)$, $v \ne 0$, and in the class $b$ modulo $f_i$ the residual is exactly $v e_k$: $Y_k = v$ and $Y_{k'} = 0$ for every other $k' \equiv b$.

*Proof.* At line L7, $k$ satisfies $k \equiv r_i = b \ (f_i)$ by the Chinese remainder theorem. Since $Z^{(i,0)}_b \ne 0$ (line L5) and $n/f_i \ne 0$, $v \ne 0$. Let $D$ be the union of $\{k\}$ and the residual support in the class $b$, so $|D| \le K + 1 \le T + 1$, and let $c_{k'} = Y_{k'} - v [k' = k]$ on $D$. Line L8 passed, so by Lemma 2, for $s = 0, \ldots, T$ (all in $S$),
$$0 = Z^{(i,s)}_b - \frac{f_i}{n} v \omega^{-sk} = \frac{f_i}{n} \sum_{k' \in D} c_{k'} \omega^{-sk'}.$$
By Lemma 3, $c = 0$. $\square$

**Lemma 5 (singletons pass).** If the residual meets the class $b$ modulo $f_i$ in exactly one frequency $k$, then bucket $b$ of stage $i$ passes lines L5 to L8 with this $k$ and $v = Y_k$.

*Proof.* By Lemma 2, $Z^{(i,s)}_b = \frac{f_i}{n} Y_k \omega^{-sk}$ for all $s \in S$, and $Z^{(i,0)}_b \ne 0$. For $j \ne i$, $Z^{(i, n/f_j)}_b = \omega^{-(n/f_j) k} Z^{(i,0)}_b = \omega^{-(n/f_j) r} Z^{(i,0)}_b$ with $r = k \bmod f_j$, because $\omega^{n} = 1$. The powers $\omega^{-(n/f_j) r} = \omega_{f_j}^{-r}$, $0 \le r < f_j$, are distinct, and $Z^{(i,0)}_b \ne 0$, so line L6 finds exactly $r_j = k \bmod f_j$, and $r_i = b = k \bmod f_i$. Since the $f_j$ are pairwise coprime, the solution in $[0, n)$ of the congruences is unique and equals $k$. Line L7 gives $v = \frac{n}{f_i} Z^{(i,0)}_b = Y_k$, and line L8 passes because its equations hold by the first sentence. $\square$

**Soundness.** By induction on the peels, the residual support is always a subset of $\mathrm{supp}\, X$, so it has at most $K$ elements: initially $Y = X$, and by Lemma 4 each peel picks $k$ with $Y_k = v \ne 0$ and sets $Y_k$ to $0$, leaving the other entries unchanged. So each peel removes one element of the residual support. A frequency is peeled at most once, since afterwards $Y_k = 0$ forever, and when it is peeled found$[k]$ goes from $0$ to $v = Y_k = X_k$ (the residual at $k$ equals $X_k$ until $k$ is peeled). Hence every returned pair has $v = X_k \ne 0$.

**Termination.** There are at most $|\mathrm{supp}\, X| \le K$ peels, and the budget at line L4 stops the loop after $K$ peels. A pass with no peel ends the loop. So there are at most $K + 1$ passes, each finite.

**The flag.** If success, all $Z^{(1,s)}_b = 0$; by Lemma 2 and Lemma 3, applied in each class modulo $f_1$ to the residual (at most $K \le T$ frequencies) with the shifts $0, \ldots, T$, $Y = 0$, so found is the nonzero part of $X$. Conversely, if $Y = 0$ then all aliased sums vanish and success is true.

**Stopping sets.** Let $D^*$ be the residual support at the end. Every stopping set $D \subseteq \mathrm{supp}\, X$ is contained in $D^*$: otherwise consider the first peel of an element $k \in D$, at bucket $b$ of stage $i$. Before it no element of $D$ has been peeled, so the residual contains $D$, and the class $b$ contains $k \in D$, hence at least two elements of $D$ and of the residual. This contradicts Lemma 4. On the other hand, $D^*$ is itself a stopping set. If the loop ended because of the budget, $K$ correct peels were made, so $|\mathrm{supp}\, X| = K$ and $D^* = \emptyset$. Otherwise the last pass peeled nothing, so the tables did not change during it and it examined every bucket in the final state; by Lemma 5 no class meets $D^*$ in exactly one element. So $D^*$ is the largest stopping set in $\mathrm{supp}\, X$, and success holds if and only if it is empty, that is, if and only if $\mathrm{supp}\, X$ contains no nonempty stopping set.

**Cost.** Line L2 reads $f_i$ samples per stage and shift, $F|S|$ in all, and computes each DFT of length $f_i$ directly with at most $f_i^2$ multiplications and $f_i^2$ additions, at most $|S| F^2$ of each. A pass examines $F$ buckets. Each examination does at most $\sum_j f_j = F$ multiplications and comparisons at line L6, $O(d)$ operations for the Chinese remainder step at line L7, and at most $3|S|$ multiplications and $|S|$ subtractions at line L8, besides the powers $\omega^{-sk}$: $\omega^{-k}$ costs $O(\log n)$ multiplications by repeated squaring, its powers for $s \le T$ one multiplication each, and for $s = n/f_j$ they are the table entries $\omega_{f_j}^{-(k \bmod f_j)}$. Each of the at most $K$ peels does $d|S|$ subtractions and $2d|S|$ multiplications, with the same powers. With at most $K + 1$ passes and $|S| \le T + 1 + d = K + 1 + d$, the total is $O(|S| F^2 + (K + 1) F (F + d + |S| + \log n) + K d |S|) = O((K + d) F (F + K + d + \log n))$, using $d \le F$. The tables hold $F|S| = O(F (K + d))$ entries, and found at most $K$. $\blacksquare$

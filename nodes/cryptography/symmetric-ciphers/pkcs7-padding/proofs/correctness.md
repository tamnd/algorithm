---
title: PKCS#7 unpadding inverts padding and accepts exactly the padded strings
proves: [correctness]
status: full
---

Fix a block length $b$ with $1 \le b \le 255$. Write $\mathrm{pad}$ for PKCS7-PAD$(\cdot, b)$ and $\mathrm{unpad}$ for the strict PKCS7-UNPAD$(\cdot, b)$. For a byte string $X$, $|X|$ is its length and $X[i]$ its $i$-th byte, counting from 1.

**Lemma 1 (shape of the output).** For every message $M$ with $n = |M|$, line L1 gives $k = b - (n \bmod b)$ with $1 \le k \le b$, and $|\mathrm{pad}(M)| = n + k$ is a positive multiple of $b$.

*Proof.* Since $0 \le n \bmod b \le b - 1$, we get $1 \le k \le b$. Then $n + k = n - (n \bmod b) + b = b(\lfloor n/b \rfloor + 1)$, which is a positive multiple of $b$. Since $k \le b \le 255$, the value $k$ fits in one byte, so line L2 is well defined. $\square$

**Lemma 2 (unpad inverts pad).** For every $M$, $\mathrm{unpad}(\mathrm{pad}(M)) = M$.

*Proof.* Let $X = \mathrm{pad}(M)$ and $k$ as in Lemma 1. By Lemma 1, $|X|$ is a positive multiple of $b$, so line L3 does not reject. The last $k$ bytes of $X$ are all equal to $k$ by line L2, so line L4 reads the value $k$. Since $1 \le k \le b$, line L5 does not reject. Line L6 checks the bytes $X[|X| - i + 1]$ for $i = 1, \ldots, k$, which are the $k$ appended bytes, all equal to $k$, so it does not reject. Line L7 returns the first $|X| - k = n$ bytes, which are $M$. $\square$

**Lemma 3 (unpad accepts only padded strings).** If $\mathrm{unpad}(X)$ returns $M$, then $X = \mathrm{pad}(M)$.

*Proof.* Since $X$ passed line L3, $|X| = qb$ for some $q \ge 1$. Let $k = X[|X|]$, read in line L4. Since $X$ passed line L5, $1 \le k \le b$. Since $X$ passed line L6, the last $k$ bytes of $X$ all equal $k$. Line L7 returns $M$ with $|M| = qb - k$. Now compute $\mathrm{pad}(M)$. We have $|M| \bmod b = (qb - k) \bmod b = b - k$ if $k < b$, and $0$ if $k = b$. In both cases line L1 gives $k' = b - (|M| \bmod b) = k$. So $\mathrm{pad}(M) = M \,\|\, (\text{byte } k \text{ repeated } k \text{ times})$, and this is $X$, because $X$ is $M$ followed by its last $k$ bytes, which all equal $k$. $\square$

**Theorem.** $\mathrm{pad}$ is injective, $\mathrm{unpad} \circ \mathrm{pad}$ is the identity, and the set of strings that $\mathrm{unpad}$ accepts is exactly the image of $\mathrm{pad}$.

*Proof.* The identity is Lemma 2. If $\mathrm{pad}(M) = \mathrm{pad}(M')$, then applying $\mathrm{unpad}$ and Lemma 2 gives $M = M'$, so $\mathrm{pad}$ is injective. By Lemma 2, every string $\mathrm{pad}(M)$ is accepted. By Lemma 3, every accepted string is $\mathrm{pad}(M)$ for some $M$. So the accepted set is the image of $\mathrm{pad}$. $\blacksquare$

**Remark (the lenient unpad).** If lines L3, L5 and L6 are removed, Lemma 2 still holds, but Lemma 3 fails: for $b = 16$, the string `ICE ICE BABY` followed by `01 02 03 04` is accepted and returns `ICE ICE BABY`, although it is not $\mathrm{pad}$ of any message. The tests of this page check this.

---
title: DUVAL returns the Lyndon factorization
proves: [correctness, termination]
status: full
---

**Notation.** $s = s[0..n-1]$ is a word over a totally ordered alphabet, with 0-based indices, and words are compared in lexicographic order, where a proper prefix is smaller. A Lyndon word is a nonempty word that is smaller than each of its proper nonempty suffixes. For a nonempty word $u$, $u^\omega = uuu\cdots$ is the infinite power. We use two facts proved on the [Chen-Fox-Lyndon theorem](/lyndon-schutzenberger-theorem/) page: the Lyndon factorization exists and is unique, and a proper nonempty suffix of a Lyndon word $u$ is larger than $u$ and is not a prefix of $u$.

**Lemma 1.** Let $u$ be a Lyndon word of length $p$. For each $q \ge 0$, $u^\omega[q..] \ge u^\omega$, comparing the infinite words letter by letter.

*Proof.* Let $r = q \bmod p$. Then $u^\omega[q..] = \rho^\omega$ with $\rho = u[r..p-1]\,u[0..r-1]$, a rotation of $u$. If $r = 0$ the two words are equal. Otherwise $u < \rho$, because a Lyndon word is smaller than its proper rotations, and since $|u| = |\rho|$ they differ inside the first $p$ letters, with the smaller letter in $u$. So $u^\omega < \rho^\omega$. $\square$

**Lemma 2 (extension).** Let $u$ be a Lyndon word of length $p$, $m \ge 1$, $u'$ a proper prefix of $u$, $a = u[|u'|]$, and $c > a$ a letter. Then $w = u^m u' c$ is a Lyndon word.

*Proof.* Let $N = |w| = mp + |u'| + 1$ and $x = u^m u' a = u^\omega[0..N-1]$, so $w$ is $x$ with its last letter $a$ replaced by $c$. Take a proper suffix $w[q..N-1]$ with $1 \le q < N$. By Lemma 1, $x[q..N-1] \ge x[0..N-1-q]$, these being prefixes of the same length of $u^\omega[q..]$ and $u^\omega$. So either the two words are equal, or they first differ at some offset $d$ with $x[q+d] > x[d]$.

- If they first differ at $d < N - 1 - q$, then $q + d < N - 1$ and $d < N - 1$, so $w$ agrees with $x$ at both indices, and $w[q..]$ and $w$ first differ at $d$ with the larger letter in $w[q..]$.
- Otherwise they agree on the offsets $0, \ldots, N - 2 - q$, and at the last offset $N - 1 - q$ we have $x[N-1] = a \ge x[N-1-q]$. Then $w[q..N-1]$ and $w[0..N-1-q]$ agree before the last offset, and at it $w[N-1] = c > a \ge x[N-1-q] = w[N-1-q]$.

In both cases $w[q..N-1] > w$, since the two first differ inside $w[q..N-1]$. So $w$ is smaller than each of its proper nonempty suffixes. $\square$

**Lemma 3 (output step).** Let $z = u^m u' y$, where $u$ is a Lyndon word, $m \ge 1$, $u'$ is a proper prefix of $u$, and either $y$ is empty or $y$ starts with a letter $c < u[|u'|]$. Then the Lyndon factorization of $z$ is $m$ copies of $u$ followed by the Lyndon factorization of $u' y$.

*Proof.* If $u'y$ is empty, the claim holds, since $u, \ldots, u$ is nonincreasing. Otherwise let $\ell$ be the first factor of the Lyndon factorization of $u' y$. If $|\ell| \le |u'|$, then $\ell$ is a prefix of $u'$, hence a prefix of $u$, so $\ell \le u$. If $|\ell| > |u'|$, then $y$ is nonempty and $\ell$ starts with $u' c$, while $u$ starts with $u'\,u[|u'|]$ and $c < u[|u'|]$, so $\ell < u$. In both cases the sequence $u, \ldots, u, \ell, \ldots$ is a nonincreasing sequence of Lyndon words with product $z$, and by uniqueness it is the Lyndon factorization of $z$. $\square$

**Outer invariant.** At each test of line L2: $0 \le i \le n$, the list $F$ holds the start indices of factors $\ell_1, \ldots, \ell_r$ with $\ell_1 \cdots \ell_r = s[0..i-1]$, and the Lyndon factorization of $s$ is $\ell_1, \ldots, \ell_r$ followed by the Lyndon factorization of $s[i..n-1]$. At the first test $i = 0$ and $F$ is empty, so this holds.

**Inner invariant.** At each test of line L4 in a round that starts at $i$: $i \le k < j \le n$, and with $p = j - k$, the word $u = s[i..i+p-1]$ is a Lyndon word and $s[i..j-1] = u^m u'$ with $m \ge 1$ and $u'$ a proper prefix of $u$. Since $s[i..j-1]$ is a prefix of $u^\omega$, the letter that continues the period is $u^\omega[j - i] = u^\omega[j - i - p] = s[k]$, and $s[k] = u[|u'|]$.

- *First test.* Line L3 sets $j = i + 1$ and $k = i$, so $p = 1$, $u = s[i]$, $m = 1$ and $u'$ is empty.
- *Equal letters.* If $s[j] = s[k]$, then $s[i..j] = u^m u' s[k]$, and $u'\,s[k]$ is a prefix of $u$. If it is a proper prefix, it is the new $u'$; if it equals $u$, then $m$ grows by one and the new $u'$ is empty. Line L5 sets $k \leftarrow k + 1$ and line L6 sets $j \leftarrow j + 1$, so $p$ is unchanged and the invariant holds.
- *Larger letter.* If $s[j] > s[k] = u[|u'|]$, then $s[i..j]$ is a Lyndon word by Lemma 2. Line L5 sets $k \leftarrow i$ and line L6 sets $j \leftarrow j + 1$, so the new $p$ is $j + 1 - i$, the new $u$ is $s[i..j]$, $m = 1$ and $u'$ is empty.

Each step increases $j$, and $j \le n$, so the inner loop stops.

**The output step.** When the inner loop stops, $s[i..j-1] = u^m u'$ as above, and either $j = n$ or $s[j] < s[k] = u[|u'|]$. By Lemma 3 with $y = s[j..n-1]$, the Lyndon factorization of $s[i..n-1]$ is $m$ copies of $u$ followed by the factorization of $s[i+mp..n-1]$. Lines L7 to L9 append $i, i + p, \ldots$ while $i \le k = j - p$, that is, while $i + p \le j$. Since $j - i = mp + |u'|$ with $|u'| < p$, they append exactly $m$ indices, the starts of the $m$ copies of $u$, and leave $i$ at the old $i$ plus $mp$. So the outer invariant holds again. Since $m \ge 1$, each round increases $i$, so the outer loop stops.

**Conclusion.** At the end $i = n$, so $s[i..n-1]$ is empty, and by the outer invariant $F$ holds the start indices of the Lyndon factorization of $s$. $\blacksquare$

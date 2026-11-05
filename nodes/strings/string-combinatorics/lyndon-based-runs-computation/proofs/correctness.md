---
title: RUNS returns exactly the runs of the string
proves: [correctness, termination]
status: full
---

**Notation.** $s = s[0..n-1]$ with $n \ge 1$ is a word over a totally ordered alphabet, with 0-based indices. For $\ell \in \{0, 1\}$, $<_0$ is the given order on letters and $<_1$ its reverse. Each order is extended to words lexicographically, with a proper prefix smaller than the longer word. A Lyndon word for $<_\ell$ is a nonempty word that is strictly smaller than each of its proper nonempty suffixes. $\mathrm{suf}(k) = s[k..n-1]$, with $\mathrm{suf}(n) = \varepsilon$. For a run we use half-open intervals here: a run is $[l, r)$ with smallest period $p$, $r - l \ge 2p$, and no extension with the period $p$ to the left or right; the algorithm reports it as the triple $(l, r - 1, p)$. Let $T_p = \{t : 0 \le t < n - p,\ s[t] = s[t+p]\}$, so that $s[x..y-1]$ has the period $p$ exactly when $[x, y - p) \subseteq T_p$.

**Lemma 1 (the Lyndon array).** For $0 \le i < n$ and a fixed order, let $j$ be the least index $j > i$ with $\mathrm{suf}(j) < \mathrm{suf}(i)$, or $j = n$ if there is none. Then $s[i..j-1]$ is the longest prefix of $\mathrm{suf}(i)$ that is a Lyndon word, so $\lambda[i] = j - i$.

*Proof.* First, $w = s[i..j-1]$ is a Lyndon word. Let $i < k < j$, and compare $x = s[k..j-1]$ with $w$; $|x| < |w|$. If $x$ is a prefix of $w$, then $\mathrm{suf}(k) = x \cdot \mathrm{suf}(j)$ and $\mathrm{suf}(i) = x \cdot \mathrm{suf}(i + j - k)$, and $\mathrm{suf}(k) > \mathrm{suf}(i)$ by the choice of $j$, so $\mathrm{suf}(j) > \mathrm{suf}(i+j-k)$. But $i < i + j - k < j$, so $\mathrm{suf}(i+j-k) > \mathrm{suf}(i) > \mathrm{suf}(j)$, a contradiction. So $x$ and $w$ differ at some offset $d < |x|$; the letters there are those of $\mathrm{suf}(k)$ and $\mathrm{suf}(i)$ at offset $d$, and $\mathrm{suf}(k) > \mathrm{suf}(i)$ gives $x > w$.

Second, no longer prefix $w' = s[i..m-1]$ with $j < m \le n$ is a Lyndon word. Its proper nonempty suffix $y = s[j..m-1]$ is either a prefix of $w'$, and then $y < w'$, or differs from $w'$ at an offset $d < |y|$, where $\mathrm{suf}(j) < \mathrm{suf}(i)$ gives $y < w'$. $\square$

**Lemma 2 (rotations of a primitive word).** Let $w$ be a primitive word of length $p$. Its $p$ rotations are pairwise distinct, and the least of them is a Lyndon word.

*Proof.* If the rotation by $k$, with $0 < k < p$, equals $w$, then $w[t] = w[(t + k) \bmod p]$ for every $t$, hence $w[t] = w[(t + mk) \bmod p]$ for every integer $m$. The multiples of $k$ modulo $p$ are the multiples of $d = \gcd(k, p) < p$, so $w = (w[0..d-1])^{p/d}$, which is not primitive. So the rotations are distinct, and so are the rotations of any rotation of $w$.

Let $w$ now be the least rotation and $v$ a proper nonempty suffix, $w = uv$. If $v$ is not a prefix of $w$, then $v$ and $w$ differ at an offset $d < |v|$, and so do $vu$ and $w$; $vu$ is a rotation, so $vu > w$, hence $v > w$. If $v$ is a proper prefix of $w$, write $w = vx$ with $|x| = |u|$. The rotation $vu$ differs from $w = vx$, so $vu > vx$, hence $u > x$, and the first difference of $u$ and $x$ is at an offset below $|u|$. So the rotation $xv$ of $w = vx$ is smaller than $uv = w$, a contradiction. $\square$

**Lemma 3 (Lyndon words are unbordered and primitive).** A Lyndon word $w$ has no nonempty proper factor that is both a prefix and a suffix, and $w$ is primitive.

*Proof.* Such a factor $v$ is a proper nonempty suffix and a proper prefix, so $v < w$, which a Lyndon word excludes. If $w = z^k$ with $k \ge 2$, then $z^{k-1}$ is such a factor. $\square$

**Lemma 4 (the extension of lines L6 and L7).** Let $0 \le i < n$, $1 \le p$, $j = i + p \le n$. Let $a$ be the length of the longest common suffix of $s[0..i-1]$ and $s[0..j-1]$, and $b$ the length of the longest common prefix of $\mathrm{suf}(i)$ and $\mathrm{suf}(j)$. Put $l = i - a$ and $r = j + b$. Then $[l, r - p) \subseteq T_p$, $l - 1 \notin T_p$ when $l > 0$, and $r - p \notin T_p$ when $r < n$. So $s[l..r-1]$ has the period $p$ and cannot be extended to the left or right with the period $p$.

*Proof.* By definition, $t \in T_p$ for $i - a \le t < i$ and for $i \le t < i + b$, which is $[l, r - p)$. By maximality of $a$, either $a = i$ (so $l = 0$) or $s[i - a - 1] \ne s[j - a - 1]$, that is $l - 1 \notin T_p$. By maximality of $b$, either $j + b = n$ or $s[i + b] \ne s[j + b]$, that is $r - p \notin T_p$. $\square$

**Soundness.** Suppose line L8 adds $(l, r - 1, p)$, found at $i$ with $p = \lambda_\ell[i]$, so $r - l \ge 2p$. By Lemma 4, $s[l..r-1]$ has the period $p$ and is not extendable with it, and $l \le i < i + p \le r$. Let $q$ be its smallest period and suppose $q < p$. Since $r - l \ge 2p \ge p + q$, the Fine and Wilf theorem makes $d = \gcd(p, q) < p$ a period of $s[l..r-1]$. Then the factor $s[i..i+p-1]$ has the period $d$, which divides its length $p$, so it equals $z^{p/d}$ with $p/d \ge 2$. But it is a Lyndon word for $<_\ell$ by Lemma 1, hence primitive by Lemma 3, a contradiction. So $p$ is the smallest period, and $(l, r - 1, p)$ is a run.

**Completeness.** Let $[l, r)$ be a run of $s$ with smallest period $p$. Choose $\ell$: if $r < n$, then $s[r] \ne s[r - p]$, and let $\ell$ be the order with $s[r] <_\ell s[r - p]$; if $r = n$, let $\ell = 0$.

*A Lyndon root.* The word $w = s[l..l+p-1]$ is primitive: if $w = z^k$ with $k \ge 2$, then $s[l..r-1]$, which has the period $p$, also has the period $|z| < p$, against the choice of $p$. Since $r - l \ge 2p$, for $l \le c < l + p$ the factor $s[c..c+p-1]$ is the rotation of $w$ by $c - l$. By Lemma 2, for the order $<_\ell$, the least of them, at some $c$ with $l \le c < l + p$, is a Lyndon word. Note $c + p \le l + 2p - 1 < r$.

*Its Lyndon array entry.* We show $\lambda_\ell[c] = p$. The prefix $s[c..c+p-1]$ of $\mathrm{suf}(c)$ is a Lyndon word. Let $m > c + p$ with $m \le n$; we show that $y = s[c..m-1]$ is not a Lyndon word. If $m \le r$, then $y$ has the period $p < |y|$, so $s[c+p..m-1]$ is a nonempty proper factor that is both a prefix and a suffix of $y$, which Lemma 3 excludes. If $m > r$, then $r < n$, and the proper suffix $y' = s[c+p..m-1]$ agrees with $y$ at the offsets $t < r - c - p$, since $c + t \in T_p$, while at the offset $r - c - p < |y'|$ it has $s[r]$ against $s[r - p]$ in $y$. As $s[r] <_\ell s[r-p]$, $y' < y$, and $y$ is not a Lyndon word.

*It is found.* So at $i = c$ the algorithm has $p = \lambda_\ell[c]$ and $j = c + p$. Since $[l, r - p) \subseteq T_p$ and $l \le c < r - p$, while $l - 1 \notin T_p$ (or $l = 0$) and $r - p \notin T_p$ (or $r = n$) by the maximality of the run, the values of Lemma 4 are $a = c - l$ and $b = r - p - c$. So lines L6 and L7 give exactly $l$ and $r$, and $r - l \ge 2p$, so line L8 adds $(l, r - 1, p)$.

**Termination and conclusion.** The two loops have $2 \cdot n$ iterations, each of constant work beyond the precomputed structures. Every triple added is a run (soundness), every run is added at least once (completeness), and $R$ is a set, so the algorithm returns exactly the set of runs of $s$. For $n = 0$ the loops are empty and there are no runs. $\blacksquare$

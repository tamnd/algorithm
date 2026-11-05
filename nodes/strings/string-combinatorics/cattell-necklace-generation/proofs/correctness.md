---
title: GEN visits every prenecklace of length n once, in increasing order, with p = lyn(a)
proves: [correctness, termination]
status: full
---

**Notation.** The alphabet is $\{0, \ldots, k-1\}$ with $k \ge 1$, ordered as integers, and words are compared lexicographically. Indices are 0-based. For a nonempty word $v$, $v^\infty$ is the infinite word $vvv\cdots$, and $v^\infty[0..m-1]$ is its prefix of length $m$. A Lyndon word is a nonempty word strictly smaller than each of its proper nonempty suffixes; equivalently, strictly smaller than its other rotations. A word $a$ is a **prenecklace** if it is a prefix of $v^\infty$ for some Lyndon word $v$. Prefixes of prenecklaces are prenecklaces. For a nonempty word $a$, $\mathrm{lyn}(a)$ is the length of the longest prefix of $a$ that is a Lyndon word; it is at least 1, since a single letter is a Lyndon word.

**Lemma 1 (suffixes of a prenecklace).** If $a$ is a prenecklace of length $m$ and $0 \le i < m$, then $a[i..m-1] \ge a[0..m-i-1]$.

*Proof.* Let $a$ be a prefix of $v^\infty$ with $v$ Lyndon, and let $r = i \bmod |v|$ and $v'$ the rotation $v[r..|v|-1]\,v[0..r-1]$. The suffix of $v^\infty$ from index $i$ is $v'^\infty$. Since $v$ is a Lyndon word, $v \le v'$, and both have length $|v|$; so either $v = v'$, or they differ inside their first $|v|$ letters with $v$ smaller. In both cases each prefix of $v^\infty$ is at most the prefix of $v'^\infty$ of the same length. The words $a[i..m-1]$ and $a[0..m-i-1]$ are these prefixes of length $m - i$. $\square$

**Lemma 2 (Duval).** Let $u$ be a Lyndon word of length $p$, let $u' = u[0..r-1]$ with $0 \le r < p$, let $e \ge 1$ and let $c$ be a letter with $c > u[r]$. Then $x = u^e u' c$ is a Lyndon word.

*Proof.* Let $0 < i < |x| = ep + r + 1$ and write $i = qp + t$ with $0 \le t < p$. We show $x[i..] > x$.

- *Case $t = 0$*, so $1 \le q \le e$. The suffix is $u^{e-q} u' c$. It agrees with $x$ on its first $(e-q)p + r$ letters, and the next letters are $c$ in the suffix and $x[(e-q)p + r] = u[r]$ in $x$, since $(e-q)p + r < ep$. As $c > u[r]$, the suffix is larger.
- *Case $t > 0$ and $q < e$.* The suffix starts with $u[t..p-1]$, a proper suffix of $u$, so $u[t..p-1] > u$. A shorter word that is larger than $u$ is not a prefix of $u$, so there is $d < p - t$ with $u[t..t+d-1] = u[0..d-1]$ and $u[t+d] > u[d]$. Then the suffix and $x$ first differ at offset $d$, and the suffix is larger.
- *Case $t > 0$ and $q = e$.* Then $t \le r$ and the suffix is $u[t..r-1]\,c$, of length $r - t + 1 \le p$, while $x$ starts with $u[0..r-t]$. Take $d$ as in the previous case. If $d < r - t$, the suffix is larger at offset $d$. Otherwise $u[t..r-1] = u[0..r-t-1]$ and $u[r] \ge u[r-t]$ (equality when $d > r - t$, strict when $d = r - t$), so $c > u[r] \ge u[r-t]$, and the suffix is larger at offset $r - t$. $\square$

**Lemma 3 (the longest Lyndon prefix of a periodic word).** Let $u$ be a Lyndon word of length $p$ and $m \ge p$. Then $\mathrm{lyn}(u^\infty[0..m-1]) = p$.

*Proof.* The prefix $u$ is Lyndon. Let $y = u^\infty[0..l-1]$ with $p < l \le m$, and write $y = u^e v$ with $e \ge 1$ and $v$ a proper prefix of $u$. If $v$ is nonempty, it is a proper nonempty suffix of $y$ and also a prefix of $y$, so $v < y$, and $y$ is not Lyndon. If $v$ is empty, then $e \ge 2$ and the proper suffix $u^{e-1}$ is a prefix of $y$, so again $y$ is not Lyndon. $\square$

**Lemma 4 (extension).** Let $a$ be a nonempty prenecklace of length $m$ with $q = \mathrm{lyn}(a)$, and suppose $a = u^\infty[0..m-1]$ with $u = a[0..q-1]$. Let $b$ be a letter and $c = a[m - q]$. Then:

- if $b = c$, $ab$ is a prenecklace, $ab = u^\infty[0..m]$ and $\mathrm{lyn}(ab) = q$;
- if $b > c$, $ab$ is a Lyndon word, so it is a prenecklace with $\mathrm{lyn}(ab) = m + 1$ and $ab = (ab)^\infty[0..m]$;
- if $b < c$, $ab$ is not a prenecklace.

*Proof.* Write $m = eq + r$ with $e \ge 1$ and $0 \le r < q$; then $a = u^e u[0..r-1]$ and $c = u[r]$, because $u^\infty$ has period $q$. If $b = c$, then $ab = u^\infty[0..m]$, a prenecklace, and $\mathrm{lyn}(ab) = q$ by Lemma 3. If $b > c$, $ab$ is Lyndon by Lemma 2; a Lyndon word $w$ is a prefix of $w^\infty$, and $\mathrm{lyn}(w) = |w|$. If $b < c$, the suffix of $ab$ at index $eq$ is $u[0..r-1]\,b$, and the prefix of $ab$ of the same length is $u[0..r-1]\,u[r]$, which is larger. By Lemma 1, $ab$ is not a prenecklace. $\square$

**Lemma 5 (structure).** Every nonempty prenecklace $a$ of length $m$ satisfies $a = u^\infty[0..m-1]$ with $u = a[0..\mathrm{lyn}(a)-1]$.

*Proof.* Induction on $m$. For $m = 1$, $\mathrm{lyn}(a) = 1$ and $u = a$. For $m \ge 2$, $a[0..m-2]$ is a prenecklace, the induction hypothesis applies to it, and since $a$ is a prenecklace, Lemma 4 leaves the first two cases, which both give the claim. $\square$

**The calls.** We show: for each $t$ with $1 \le t \le n$, the call GEN$(t, p)$ is made exactly once for each prenecklace $x$ of length $t$, at a moment when $a[0..t-1] = x$, and then $p = \mathrm{lyn}(x)$. Moreover, while a call GEN$(t, p)$ and the calls below it run, the cells $a[0..t-1]$ do not change, since the call writes only $a[t]$ and its descendants write only higher cells.

*Level 1.* Line L1 sets $a[0]$ to each letter $c$ in turn and calls GEN$(1, 1)$. Every one-letter word is a Lyndon word, hence a prenecklace with $\mathrm{lyn} = 1$, and there are no other prenecklaces of length 1.

*From $t$ to $t + 1$, for $t < n$.* A prenecklace $y$ of length $t + 1$ is $xb$, where $x = y[0..t-1]$ is a prenecklace (a prefix of a prenecklace) and $b$ a letter. By the hypothesis, GEN$(t, \mathrm{lyn}(x))$ runs exactly once with $a[0..t-1] = x$; it reads $c_0 = a[t - p] = x[t - p]$, which stays fixed during the call. By Lemma 5, Lemma 4 applies to $x$ with $q = p$: the extensions $xb$ that are prenecklaces are exactly those with $b \ge c_0$, with $\mathrm{lyn}(xb) = p$ for $b = c_0$ and $\mathrm{lyn}(xb) = t + 1$ for $b > c_0$. Line L5 sets $a[t] = c_0$ and calls GEN$(t + 1, p)$, and lines L6 and L7 set $a[t] = b$ and call GEN$(t + 1, t + 1)$ for each $b$ from $c_0 + 1$ to $k - 1$. So each prenecklace $xb$ gets exactly one call, with the right value of $p$, and no other word of length $t + 1$ gets a call.

**Order.** The calls form a tree in which the children of a call are made with increasing letters at index $t$. The words of length $n$ are reached in the order of a depth-first walk that takes children in increasing order, which is increasing lexicographic order: two leaves first differ at some index $t$, below the call for their common prefix, and the leaf with the smaller letter at $t$ is under the earlier child.

**Termination.** Each call makes at most $k$ calls, and the depth is at most $n$, so the tree is finite. The number of calls is $1 + \sum_{t=1}^{n} P_k(t)$, where $P_k(t)$ is the number of prenecklaces of length $t$.

**The tests of line L3.** Let $a$ be a prenecklace of length $n$ with $p = \mathrm{lyn}(a)$ and $u = a[0..p-1]$, so $a = u^\infty[0..n-1]$ by Lemma 5.

- *If $p$ divides $n$, $a$ is a necklace.* Then $a = u^{n/p}$. A rotation of $a$ by $i$ is $(u_r)^{n/p}$, where $u_r$ is the rotation of $u$ by $r = i \bmod p$, and $u \le u_r$ because $u$ is a Lyndon word. So $a$ is at most each of its rotations.
- *If $a$ is a necklace, $p$ divides $n$.* Write $a = z^{e}$ with $z$ primitive. Let $0 < r < |z|$ and let $z_r$ be the rotation of $z$ by $r$; it differs from $z$, because $z$ is primitive. The rotation of $a$ by $r$ is $z_r^{\,e} \ge z^e = a$, and since $z_r$ and $z$ have the same length, $z_r > z$. So $z$ is a Lyndon word, $a = z^\infty[0..n-1]$, and $\mathrm{lyn}(a) = |z|$ by Lemma 3, which divides $n$.
- *Lyndon words.* $a$ is a Lyndon word if and only if its longest Lyndon prefix is $a$ itself, that is, $p = n$. Every Lyndon word is a prenecklace, so each Lyndon word of length $n$ is visited.

**The number of calls.** By Lemmas 3 and 5, a prenecklace of length $t$ with $\mathrm{lyn} = q$ is $u^\infty[0..t-1]$ for exactly one Lyndon word $u$ of length $q$, and each Lyndon word $u$ of length $q \le t$ gives one. So $P_k(t) = \sum_{q=1}^{t} L_k(q)$, where $L_k(q)$ is the number of Lyndon words of length $q$, and the number of calls is
$$ 1 + \sum_{t=1}^{n} \sum_{q=1}^{t} L_k(q) = 1 + \sum_{q=1}^{n} L_k(q)\,(n - q + 1). $$
The $q$ rotations of a Lyndon word of length $q$ are distinct words, so $L_k(q) \le k^q / q$. Put $q = n - d$. For $d \le n/2$, $1/q \le 2/n$, and these terms sum to at most $\frac{2k^n}{n} \sum_{d \ge 0} (d + 1) k^{-d} = \frac{2k^n}{n} \left(\frac{k}{k-1}\right)^2$ for $k \ge 2$. For $d > n/2$, each term is at most $k^{n/2} (n + 1)$, and there are at most $n$ of them. The number $N$ of necklaces of length $n$ is at least $k^n / n$, since each necklace class has at most $n$ words. So the number of calls is at most $2(k/(k-1))^2 N + 1 + n(n+1)k^{n/2}$, and $n(n+1)k^{n/2} = o(k^n / n)$. Each call does $O(1)$ work besides the calls it makes, so the total time is $O(N)$ for $k \ge 2$. $\blacksquare$

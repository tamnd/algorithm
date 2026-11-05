---
title: FKM visits every prenecklace of length n once, in increasing order, with p = lyn(a)
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

So Lemma 4 applies to every nonempty prenecklace. In particular, for $q \le n$ the map $u \mapsto u^\infty[0..n-1]$ is a bijection from the Lyndon words of length $q$ onto the prenecklaces of length $n$ with $\mathrm{lyn} = q$: it lands there by Lemma 3, it is onto by Lemma 5, and $u$ is the prefix of length $q$ of its image.

**Lemma 6 (successor).** Let $a$ be a prenecklace of length $n$ other than $(k-1)^n$, let $j$ be the largest index with $a[j] < k - 1$, and let $x = a[0..j-1]\,(a[j]+1)$. Then $x$ is a Lyndon word, $a' = x^\infty[0..n-1]$ is a prenecklace with $\mathrm{lyn}(a') = j + 1$, and $a'$ is the least prenecklace of length $n$ greater than $a$.

*Proof.* If $j = 0$, $x$ is one letter, a Lyndon word. If $j \ge 1$, let $w = a[0..j-1]$, a nonempty prenecklace, and $q = \mathrm{lyn}(w)$. Since $wa[j] = a[0..j]$ is a prenecklace, Lemma 4 gives $a[j] \ge w[j - q]$, so $a[j] + 1 > w[j-q]$, and by Lemma 4 again $x$ is a Lyndon word. Then $a'$ is a prefix of $x^\infty$, a prenecklace, and $\mathrm{lyn}(a') = j + 1$ by Lemma 3, since $j + 1 \le n$.

The word $a'$ is greater than $a$, since they first differ at index $j$. Let $y$ be a word of length $n$ with $a < y < a'$. The letters of $a$ after index $j$ are all $k - 1$, so $y$ first exceeds $a$ at some index $i \le j$. If $i < j$, then $y[i] > a[i] = a'[i]$ and $y > a'$; so $i = j$, and $y[j] = a[j] + 1$, since a larger letter would again give $y > a'$. Hence $y$ begins with $x$, and since $y < a'$, there is an index $d > j$ with $y[0..d-1] = a'[0..d-1]$ and $y[d] < a'[d]$. The prenecklace $y[0..d-1] = x^\infty[0..d-1]$ has $\mathrm{lyn} = j + 1$ by Lemma 3, and $a'[d] = x^\infty[d] = x^\infty[d - j - 1] = y[d - j - 1]$. By Lemma 4, $y[0..d]$ is not a prenecklace, so neither is $y$. $\square$

**The loop invariant.** Each time line L3 is reached, $a$ is a prenecklace of length $n$ and $p = \mathrm{lyn}(a)$.

*Initialization.* Line L1 sets $a = 0^n = 0^\infty[0..n-1]$, a prenecklace because $0$ is a Lyndon word, and $p = 1 = \mathrm{lyn}(0^n)$ by Lemma 3.

*Maintenance.* Lines L4 and L5 stop at the largest $j$ with $a[j] < k - 1$, or at $j = -1$ if there is none. If $j \ge 0$, line L7 makes $a[0..j] = x$ as in Lemma 6 and sets $p = j + 1$, and line L8, running $i$ upward, sets $a[i] = a[i - p]$ for $p \le i < n$, so that $a = x^\infty[0..n-1] = a'$. By Lemma 6, $a'$ is a prenecklace with $\mathrm{lyn}(a') = j + 1 = p$.

**Each prenecklace is visited once, in increasing order.** The first word visited is $0^n$, the least word of length $n$. By Lemma 6, each later word visited is the least prenecklace greater than the one before it. So the visited words are increasing, and no prenecklace is skipped. The last one is $(k-1)^n$, a prefix of $(k-1)^\infty$ and hence a prenecklace, after which line L6 returns.

**Termination.** Each pass through lines L4 to L8 strictly increases $a$, and there are finitely many words of length $n$. Each inner loop runs at most $n$ times.

**The tests of VISIT.** Let $a$ be a prenecklace of length $n$ with $p = \mathrm{lyn}(a)$ and $u = a[0..p-1]$, so $a = u^\infty[0..n-1]$ by Lemma 5.

- *If $p$ divides $n$, $a$ is a necklace.* Then $a = u^{n/p}$. A rotation of $a$ by $i$ is $(u_r)^{n/p}$, where $u_r$ is the rotation of $u$ by $r = i \bmod p$, and $u \le u_r$ because $u$ is a Lyndon word. So $a$ is at most each of its rotations.
- *If $a$ is a necklace, $p$ divides $n$.* Write $a = z^{e}$ with $z$ primitive. Let $0 < r < |z|$ and let $z_r$ be the rotation of $z$ by $r$. It differs from $z$, because $z$ is primitive. The rotation of $a$ by $r$ is $z_r^{\,e}$, and $z_r^{\,e} \ge z^e = a$; since $z_r$ and $z$ have the same length, this forces $z_r \ge z$, so $z_r > z$. So $z$ is a Lyndon word, $a = z^\infty[0..n-1]$, and $\mathrm{lyn}(a) = |z|$ by Lemma 3, which divides $n$.
- *Lyndon words.* $a$ is a Lyndon word if and only if its longest Lyndon prefix is $a$ itself, that is, $p = n$. Every Lyndon word of length $n$ is a prenecklace, so it is visited. $\blacksquare$

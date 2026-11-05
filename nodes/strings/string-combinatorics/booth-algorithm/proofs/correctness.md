---
title: LEAST-ROTATION returns the least index of a least rotation
proves: [correctness, termination]
status: full
---

**Notation.** $s = s[0..n-1]$ with $n \ge 1$ is a word over a totally ordered alphabet, with 0-based indices. Let $t = ss$, and let $t'$ be the infinite word $sss\cdots$, so $t'[q] = s[q \bmod n]$ and $t[q] = t'[q]$ for $q < 2n$. For $q \ge 0$ let $R(q) = t'[q..q+n-1]$. Then $R(q) = R(q \bmod n)$, and $R(0), \ldots, R(n-1)$ are the rotations of $s$. Words are compared in lexicographic order. For a nonempty word $y$ and $0 \le r < |y|$, $F_y(r)$ is the length of the longest border of $y[0..r]$, minus one. A border of $y$ is always proper here: a word that is both a proper prefix and a proper suffix of $y$, possibly empty.

**Lemma 1 (first difference).** Let $q, k, e \ge 0$ with $t'[q..q+e-1] = t'[k..k+e-1]$ and $t'[q+e] \ne t'[k+e]$. Then $e < n$; and $R(q) < R(k)$ if $t'[q+e] < t'[k+e]$, while $R(q) > R(k)$ if $t'[q+e] > t'[k+e]$.

*Proof.* If $e \ge n$, then $R(q) = R(k)$, that is, $s[(q+d) \bmod n] = s[(k+d) \bmod n]$ for $0 \le d < n$. Both sides depend only on $d \bmod n$, so the equality holds for every $d \ge 0$, in particular for $d = e$, a contradiction. So $e < n$, and the words $R(q)$ and $R(k)$ of length $n$ agree before offset $e$ and differ at it. $\square$

**Lemma 2 (borders of a border).** Let $b$ be a border of $x$. A word shorter than $b$ is a border of $x$ if and only if it is a border of $b$.

*Proof.* A word shorter than $b$ is a prefix of $x$ if and only if it is a prefix of $b$, because $b$ is a prefix of $x$; the same holds for suffixes, because $b$ is a suffix of $x$. $\square$

Call an index $q$ **decided** for the candidate $k$ if $R(q) \ge R(k)$.

**Outer invariant.** At the start of the iteration for $j$, where $1 \le j \le 2n$ and $j = 2n$ means after the loop, let $x = t[k..j-1]$. Then:

- **(I1)** $k < j$, and $f[r] = F_x(r)$ for $0 \le r < |x|$.
- **(I2)** Each $q$ with $0 \le q < j$ and $q \ne k$ is decided, or has $q > k$ with $t[q..j-1]$ a nonempty border of $x$.

*Initialization.* At $j = 1$, $k = 0$, $x = t[0]$ and $f[0] = -1 = F_x(0)$. The only index below 1 is $k$ itself.

**Inner invariant.** Fix an iteration $j \le 2n - 1$ and let $c = t[j]$. At each test of line L4, with the current values of $k$ and $i$ and with $x = t[k..j-1]$:

- **(J1)** $k < j$, $f[r] = F_x(r)$ for $0 \le r < |x|$, and $i + 1$ is the length of a border of $x$.
- **(J2)** Each $q < j$ with $q \ne k$ is decided, or has $q > k$ with $t[q..j-1]$ a nonempty border of $x$ of length at most $i + 1$.
- **(J3)** Each nonempty border $u$ of $x$ longer than $i + 1$ has $x[|u|] \ne c$.

*First test.* Line L3 sets $i = f[|x| - 1] = F_x(|x| - 1)$, so $i + 1$ is the length of the longest border of $x$. Then (J1) and (J2) follow from (I1) and (I2), and (J3) is empty.

*One pass of lines L5 and L6.* The test passed, so $i \ge 0$ and $c \ne x[i+1]$, where $x[i+1] = t[k+i+1]$ exists because $i + 1 < |x|$. Let $b = x[0..i]$, a border of $x$, and $p = j - i - 1 > k$. Then $t[p..j-1] = b = t[k..k+i]$, and $t[p..j]$ and $t[k..k+i+1]$ first differ at offset $i + 1$, where $c$ meets $x[i+1]$.

- If $c > x[i+1]$, Lemma 1 gives $R(p) > R(k)$, so $p$ becomes decided. Line L6 sets $i$ to $f[i] = F_x(i)$, so $i + 1$ becomes the length of the longest border of $b$. The undecided indices of (J2) other than $p$ have borders of $x$ shorter than $b$, which by Lemma 2 are borders of $b$, so their length is at most the new $i + 1$. By Lemma 2, the borders of $x$ longer than the new $i + 1$ are those longer than the old $i + 1$, and $b$; all of them have $x[|u|] \ne c$. So (J1) to (J3) hold.
- If $c < x[i+1]$, Lemma 1 gives $R(p) < R(k)$, and line L5 sets $k$ to $p$. The new word $x$ is $b$, a prefix of the old $x$, so $f[r] = F_b(r)$ for $r \le i$. Each index decided for the old candidate is decided for $p$, since $R(q) \ge R(k_{\text{old}}) > R(p)$, and so is $k_{\text{old}}$ itself. Each other undecided index $q \ne p$ has a border of the old $x$ shorter than $b$, so $q > p$, and by Lemma 2 its border is a border of $b$, the new $x$. Line L6 sets $i$ to $f[i]$, the length of the longest border of $b$, minus one. So (J1) and (J2) hold, and (J3) is empty, because no border of $b$ is longer than its longest border.

Each pass decreases $i$, and $i \ge -1$, so the inner loop stops.

**Maintenance of the outer invariant.** At the exit from the inner loop, (J1) to (J3) hold, and either $i \ge 0$ with $c = x[i+1]$, or $i = -1$.

*Case A: $i \ge 0$ and $c = x[i+1]$.* Line L7 fails and line L10 sets $f[|x|] = i + 1$. Let $y = xc = t[k..j]$, the word $x$ of the iteration $j + 1$.

- *The table.* A nonempty border of $y$ has the form $uc$, where $u$ is a border of $x$ with $x[|u|] = c$. By (J3) the longest such $u$ is $x[0..i]$, so $F_y(|x|) = i + 1$. The entries below $|x|$ are unchanged and stay correct, since $y[0..r] = x[0..r]$.
- *The key claim.* Let $u$ be a border of $x$ with $|u| < i + 1$ and $x[|u|] \ne c$. Then $c > x[|u|]$. Indeed, $u$ is a border of $b = x[0..i]$ by Lemma 2, so $u$ ends $b$, and $bc = x[0..i+1]$ is a prefix of $x$. So $uc$ occurs in $t$ at the index $q' = k + i + 1 - |u|$, where $k < q' < j$ and $q' + |u| = k + i + 1 \le j - 1$. By (J2), $q'$ is decided, or $t[q'..j-1]$ is a border of $x$. In the second case $t[q'..j-1]$ is a prefix of $x$ that covers the index $q' + |u|$, so $x[|u|] = t[q' + |u|] = c$, which is excluded. In the first case $R(q') \ge R(k)$; but $t[q'..q'+|u|-1] = u = t[k..k+|u|-1]$, and at offset $|u|$ the letters are $c$ and $x[|u|]$, so $c < x[|u|]$ would give $R(q') < R(k)$ by Lemma 1. Hence $c > x[|u|]$.
- *The indices.* A decided index stays decided. An undecided $q < j$ has a border $u = t[q..j-1]$ of $x$ of length at most $i + 1$. If $x[|u|] = c$, then $t[q..j] = uc = x[0..|u|]$ is a border of $y$. If $x[|u|] \ne c$, then $|u| < i + 1$ (for $u = b$ the letter is $c$), so $c > x[|u|]$ by the key claim, and Lemma 1 at offset $|u|$ gives $R(q) > R(k)$. The new index $q = j$ is the case $u = \varepsilon$: if $x[0] = c$, then $t[j..j] = c$ is a border of $y$, and otherwise the key claim with $u = \varepsilon$ gives $c > x[0]$, so $R(j) > R(k)$.

So (I1) and (I2) hold at $j + 1$.

*Case B: $i = -1$.* By (J2) every $q < j$ other than $k$ is decided, and by (J3) every nonempty border $u$ of $x$ has $x[|u|] \ne c$. So the only possible nonempty border of $y = xc$ is $c$ itself, which is a border exactly when $c = x[0] = t[k]$. The new index $j$ meets $k$ at offset 0.

- If $c = t[k]$, line L10 sets $f[|x|] = 0 = F_y(|x|)$, and $j$ is undecided with the border $t[j..j] = c$ of $y$.
- If $c > t[k]$, line L9 sets $f[|x|] = -1 = F_y(|x|)$, and $R(j) > R(k)$ by Lemma 1.
- If $c < t[k]$, then $R(j) < R(k)$ by Lemma 1, and line L8 sets $k \leftarrow j$. Each $q < j$ has $R(q) \ge R(k_{\text{old}}) > R(j)$, so it is decided for $j$. The new $x$ is $t[j..j]$, and line L9 sets $f[0] = -1$, which is correct.

In all cases (I1) and (I2) hold at $j + 1$. The outer loop runs $2n - 1$ times and each inner loop stops, so the algorithm terminates.

**The output is a least rotation.** At the end, $j = 2n$ and $x = t[k..2n-1]$. Let $0 \le q < n$ with $q \ne k$. By (I2), $R(q) \ge R(k)$, or $q > k$ and $t[q..2n-1]$ is a border of $x$. In the second case this border has length $2n - q > n$ and is a prefix of $x$, so its first $n$ letters, $R(q)$, are the first $n$ letters of $x$, which are $R(k)$. So $R(k) \le R(q)$ for every $q < n$, and $R(k) = R(k \bmod n)$ is a least rotation.

**The output is the least such index, and $k < n$.** Let $m$ be the least index in $[0, 2n)$ with $R(m)$ minimal; since $R(m + n) = R(m)$, $m < n$. Each change of $k$, at line L5 or L8, is to an index with a strictly smaller rotation, by the cases above. So once $k = m$, it never changes. Suppose the final value $k_f$ differs from $m$. Then $R(k_f)$ is minimal, as shown, so $k_f > m \ge 0$ by the choice of $m$, and $k$ was set to $k_f$ at some step of some iteration $j_0$, from a candidate $k_c$ with $R(k_c) > R(k_f) = R(m)$. Then $k_c \ne m$ and $m < k_f \le j_0$. At the test of line L4 just before this step, (J2) holds, and $m$ is not decided for $k_c$, since $R(m) < R(k_c)$. So $t[m..j_0-1]$ is a nonempty border of $x$ of length at most $i + 1$. If the step is line L5, then $k_f = j_0 - i - 1$ and $j_0 - m > j_0 - k_f = i + 1$, a contradiction. If the step is line L8, then $i = -1$, and no nonempty border has length at most 0, a contradiction. So $k_f = m$: the algorithm returns the least index of a least rotation, and it lies in $[0, n)$. $\blacksquare$

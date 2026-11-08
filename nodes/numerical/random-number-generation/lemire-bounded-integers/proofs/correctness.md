---
title: Lemire's method returns an exactly uniform integer in [0, s)
proves: [correctness]
status: full
---

We use the pseudocode of the page. Fix $w \ge 1$ and $1 \le s \le 2^w$, let $W = \{0, \ldots, 2^w - 1\}$, and let RANDOM() return independent uniform elements of $W$. Write $t = 2^w \bmod s$, $q = \lfloor 2^w / s \rfloor$, so $2^w = q s + t$ with $0 \le t < s$ and $q \ge 1$. For $x \in W$ let $h(x) = \lfloor x s / 2^w \rfloor$ and $l(x) = x s \bmod 2^w$.

**Lemma 1 (threshold).** Line L5 computes $t$: $(2^w - s) \bmod s = 2^w \bmod s$.

*Proof.* $2^w - s \equiv 2^w \pmod s$, and $0 \le 2^w - s < 2^w$ fits in $w$ bits. $\square$

**Lemma 2 (accepted set).** Let $A = \{x \in W : l(x) \ge t\}$. For each $v \in \{0, \ldots, s-1\}$, $|\{x \in A : h(x) = v\}| = q$, and $h(x) \in \{0, \ldots, s-1\}$ for every $x \in W$. Consequently $|W \setminus A| = t$.

*Proof.* For $x \in W$, $x s \le (2^w - 1) s < 2^w s$, so $h(x) < s$. The conditions $h(x) = v$ and $l(x) \ge t$ together say $v 2^w + t \le x s < (v+1) 2^w$. The half-open interval $I_v = [v 2^w + t, (v+1) 2^w)$ has length $2^w - t = q s$, so it contains exactly $q$ multiples of $s$. Each multiple $x s$ in $I_v$ has $0 \le x < 2^w$ (because $x s < (v+1) 2^w \le s \cdot 2^w$), and distinct $x$ give distinct multiples. So exactly $q$ words $x \in A$ have $h(x) = v$. Summing over $v$, $|A| = q s = 2^w - t$. $\square$

**Lemma 3 (the test at L4 is safe).** If $l(x) \ge s$, then $x \in A$.

*Proof.* $l(x) \ge s > t$. $\square$

**Theorem.** BOUNDED$(s)$ terminates with probability 1 and returns $v$ with probability exactly $1/s$ for each $v \in \{0, \ldots, s-1\}$. The number of words drawn is geometric with success probability $|A| / 2^w = 1 - t/2^w > 1/2$.

*Proof.* Let $x_1, x_2, \ldots$ be the words drawn. The returned value is $h(x_N)$, where $N$ is the least $i$ with $x_i \in A$: if $l(x_1) \ge s$, then $x_1 \in A$ by Lemma 3 and lines L4 to L7 are skipped, so $N = 1$; otherwise line L5 sets $t$ correctly by Lemma 1, and the loop at L6 and L7 stops exactly at the first $x_i$ with $l(x_i) \ge t$, i.e. $x_i \in A$, with $m = x_i s$ at that moment. The $x_i$ are independent and uniform on $W$, and $|A| = 2^w - t \ge 2^w - s + 1 \ge 1$, so $N$ is finite with probability 1 and geometric with the stated parameter; $t \le s - 1 \le 2^w - 1$ and $t < 2^w / 2$ because $t < s$ and $t \le 2^w - s$ give $2t < 2^w$. Conditioned on $N = i$, $x_i$ is uniform on $A$, independently of $i$. By Lemma 2, $\Pr[h(x_N) = v] = q / |A| = q / (q s) = 1/s$. $\square$

**Proposition (rarity of the division).** The division at L5 is executed with probability exactly $\Pr[l(x_1) < s] = s / 2^w$.

*Proof.* Let $g = \gcd(s, 2^w)$ and $s = g s'$, $2^w = g M$ with $\gcd(s', M) = 1$. Then $x s \bmod 2^w = g\,(x s' \bmod M)$, and as $x$ ranges over $W$, the residue $x \bmod M$ takes each value $g$ times and $x s' \bmod M$ is a bijection of $\{0, \ldots, M-1\}$. So each multiple of $g$ in $[0, 2^w)$ is the value of $l(x)$ for exactly $g$ words. Since $g \mid s$, exactly $s / g$ multiples of $g$ lie in $[0, s)$, so $s/g \cdot g = s$ words have $l(x) < s$. $\square$

---
title: The loopless cool-lex program visits each fixed-weight string once
proves: [correctness]
status: full
---

Let $B(s, t)$ be the set of bit strings with $s$ zeros and $t$ ones, and let $n = s + t$. For a string $b$, let $p(b)$ be its shortest prefix that ends in $010$ or $011$, or $b$ itself if no prefix ends so. Let $\sigma(b)$ be $b$ with $p(b)$ rotated one place to the right. For a list $L$ of strings and a bit $a$, $L\,a$ is the list of the strings of $L$ with $a$ added at the end.

**Where the shortest prefix is.** A prefix ends in $010$ or $011$ exactly when it ends with the bits $0$, $1$ and one more bit. So if the first pair $01$ in $b$ is at positions $x - 1$ and $x$ and $x < n$, then $p(b) = b_1 \cdots b_{x+1}$. If $b$ has no pair $01$, or its first $01$ ends at position $n$, then $p(b) = b$. The only string of $B(s, t)$ with no pair $01$ is $1^t 0^s$, and when $s, t \ge 1$ the only string whose first $01$ ends at position $n$ is $1^{t-1} 0^s 1$. So, for $s, t \ge 1$ and $b \in B(s, t)$:

- (R1) $\sigma(1^t 0^s) = 0 1^t 0^{s-1}$ and $\sigma(1^{t-1} 0^s 1) = 1^t 0^s$.
- (R2) If $b \ne 1^{t-1} 0^s 1$, then $\sigma(b\,0) = \sigma(b)\,0$.
- (R3) If $b \ne 1^t 0^s$, then $\sigma(b\,1) = \sigma(b)\,1$.

*Proof of (R2) and (R3).* If $b$ has a prefix that ends in $010$ or $011$, then $b\,0$ and $b\,1$ have the same shortest such prefix, and the rotation does not touch the added bit. Otherwise $b$ is $1^t 0^s$ or $1^{t-1} 0^s 1$. In (R2), $b = 1^t 0^s$ with $s \ge 1$; then $b\,0 = 1^t 0^{s+1}$ has no pair $01$, and $\sigma(b\,0) = 0 1^t 0^s = \sigma(b)\,0$ by (R1). In (R3), $b = 1^{t-1} 0^s 1$; then $b\,1 = 1^{t-1} 0^s 1 1$ ends in $011$, its shortest prefix is all of it, and $\sigma(b\,1) = 1^t 0^s 1 = \sigma(b)\,1$. $\square$

**The recursive list.** Define $L(s, 0) = (0^s)$, $L(0, t) = (1^t)$, and for $s, t \ge 1$
$$L(s, t) = L(s - 1, t)\,0,\quad L'(s, t - 1)\,1,\quad (1^{t-1} 0^s 1),$$
where $L'$ is $L$ without its first string.

**Lemma 1.** For all $s, t \ge 0$: $L(s, t)$ holds each string of $B(s, t)$ exactly once, its first string is $1^t 0^s$, and if $s, t \ge 1$ its last string is $1^{t-1} 0^s 1$. Also each string of $L(s, t)$ except the last is followed by its image under $\sigma$.

*Proof.* By induction on $s + t$. The cases $s = 0$ or $t = 0$ have one string. Let $s, t \ge 1$.

*The strings.* By induction, $L(s - 1, t)\,0$ holds each string of $B(s, t)$ that ends in $0$ once. The list $L'(s, t - 1)$ holds each string of $B(s, t - 1)$ except its first, $1^{t-1} 0^s$, so $L'(s, t - 1)\,1$ holds each string that ends in $1$ once, except $1^{t-1} 0^s 1$, which is the last entry. The first string is the first of $L(s - 1, t)$ with a $0$, that is, $1^t 0^s$.

*Inside the first block.* Let $u, v$ be consecutive in $L(s - 1, t)$. Then $v = \sigma(u)$, and $u$ is not the last string of $L(s - 1, t)$. If $s - 1 \ge 1$, the last string is $1^{t-1} 0^{s-1} 1$, so by (R2), $\sigma(u\,0) = \sigma(u)\,0 = v\,0$. If $s - 1 = 0$, the block has one string.

*Inside the second block.* Let $u, v$ be consecutive in $L'(s, t - 1)$. Then $v = \sigma(u)$ and $u$ is not the first string $1^{t-1} 0^s$ of $L(s, t - 1)$, so by (R3), $\sigma(u\,1) = v\,1$.

*The first join.* The last string of the first block is $u = 1^{t-1} 0^{s-1} 1 0$ if $s \ge 2$, and $u = 1^t 0$ if $s = 1$. If $s \ge 2$, $u$ ends in $010$ and its first $01$ ends at position $n - 1$, so $p(u) = u$ and $\sigma(u) = 0 1^{t-1} 0^{s-1} 1$. If $s = 1$, $u$ has no pair $01$, and $\sigma(u) = 0 1^t$. In both cases $\sigma(u) = 0 1^{t-1} 0^{s-1} 1$. If $t \ge 2$, the next string is the second string of $L(s, t - 1)$ with a $1$, that is, $\sigma(1^{t-1} 0^s)\,1 = 0 1^{t-1} 0^{s-1} 1$ by (R1). If $t = 1$, the second block is empty, and the next string is $1^{0} 0^s 1 = 0^s 1$, which is the same string.

*The second join.* If $t \ge 2$, the last string of the second block is $u = 1^{t-2} 0^s 1 1$. Its first $01$ ends at position $n - 1$ and the prefix $u$ ends in $011$, so $\sigma(u) = 1 1^{t-2} 0^s 1 = 1^{t-1} 0^s 1$, which is the next string. $\square$

**Corollary.** For $1 \le t$, the strings $\sigma^i(1^t 0^s)$ for $0 \le i < C(n, t)$ are the strings of $L(s, t)$ in order, so they are all of $B(s, t)$, each once. The last one is $1^{t-1} 0^s 1$ when $s \ge 1$, and $\sigma$ maps it back to $1^t 0^s$ by (R1).

**Lemma 2 (the program computes $\sigma$).** Let $1 \le k \le n$ and $s = n - k$. At each test of line L4 after the first, the string $b$ is in $B(s, k)$, $b$ has a pair $01$, $y$ is the position of its first $0$, and $x$ is the position of the first $1$ after position $y$. If $x < n$, one pass of lines L5 to L9 changes $b$ to $\sigma(b)$ and keeps this invariant. At the first test, $b = 1^k 0^s$ and $x = y = k$, and if $k < n$ the first pass changes $b$ to $\sigma(b)$ and makes the invariant true.

*Proof.* *The first pass.* Let $k < n$, so $s \ge 1$. Line L5 sets $b_k \leftarrow 0$ and then $b_k \leftarrow 1$, so $b$ does not change, and $x = y = k + 1$. Since $b_{k+1} = 0$, line L7 sets $b_{k+1} \leftarrow 1$ and $b_1 \leftarrow 0$, which gives $0 1^k 0^{s-1} = \sigma(1^k 0^s)$ by (R1). Its first $0$ is at $1$, and its first $1$ after that is at $2$. If $k \ge 2$, then $y = k + 1 > 2$ and line L8 sets $x = 2$. If $k = 1$, then $x = 2$ already. Line L9 sets $y = 1$.

*A later pass.* Write $b = 1^a 0^m 1 c\, w$ with $a \ge 0$, $m \ge 1$, a bit $c$ and a rest $w$, so that $y = a + 1$ and $x = a + m + 1 < n$. Then $p(b) = 1^a 0^m 1 c$. Line L5 sets $b_x \leftarrow 0$ and $b_y \leftarrow 1$, which gives $1^{a+1} 0^m c\, w$, and makes $x = a + m + 2$ and $y = a + 2$. Now $b_x = c$.

- If $c = 1$: the rotation of $1^a 0^m 1 1$ is $1^{a+1} 0^m 1$, so $\sigma(b) = 1^{a+1} 0^m 1\, w$, which is the string now. Its first $0$ is at $a + 2 = y$, and the first $1$ after it is at $a + m + 2 = x$. Line L6 is false.
- If $c = 0$: the rotation of $1^a 0^m 1 0$ is $0 1^a 0^m 1$. Line L7 sets $b_x \leftarrow 1$ and $b_1 \leftarrow 0$. If $a \ge 1$, the string becomes $0 1^a 0^m 1\, w = \sigma(b)$. Its first $0$ is at $1$ and the first $1$ after it is at $2$. Here $y = a + 2 > 2$, so lines L8 and L9 set $x = 2$ and $y = 1$. If $a = 0$, then $y = 2$ and line L5 wrote $b_1 \leftarrow 1$, which line L7 undoes, so the string becomes $0^{m+1} 1\, w = 0 1^0 0^m 1\, w = \sigma(b)$. Its first $0$ is at $1$ and the first $1$ after it is at $m + 2 = x$. Line L8 keeps $x$, since $y = 2$, and line L9 sets $y = 1$.

In each case the new string has a pair $01$, so the invariant holds. All indices stay in $1, \ldots, n$, since $x < n$ before the pass. $\square$

**Theorem.** For $1 \le k \le n$, COOL-LEX$(n, k)$ visits each string of $B(n - k, k)$ exactly once, in cool-lex order, and then stops.

*Proof.* If $k = n$, then $x = n$ and the program visits $1^n$ once, which is all of $B(0, n)$. Let $k < n$. Line L3 visits $1^k 0^{n-k}$. By Lemma 2, each pass of the loop changes $b$ to $\sigma(b)$ and line L10 visits it, so the $i$-th visit sees $\sigma^i(1^k 0^{n-k})$. The loop goes on while the first $01$ ends before position $n$. By the remark on the shortest prefix, the first $01$ ends at position $n$ only in $1^{k-1} 0^{n-k} 1$. By the Corollary this is the last string of the list, at $i = C(n, k) - 1$, and all earlier strings are different from it. So the loop stops right after the visit of the last string, and the visits are the $C(n, k)$ strings of $B(n - k, k)$, each once. $\blacksquare$

**Cost.** Each pass of the loop does a fixed number of assignments and tests, with no inner loop, so the time between two visits is $O(1)$. Line L1 takes $\Theta(n)$ time. The total is $\Theta(n + C(n, k))$.

---
title: Bus-invert coding decodes right, toggles at most ceil(n/2) lines per transfer, and is optimal over its codewords
proves: [correctness]
status: full
---

Let $n \ge 1$. A bus state is a pair $(b, x)$ with $b \in \{0,1\}^n$ and $x \in \{0,1\}$. Write $\mathbf{1}$ for the all-ones word, $\overline{D} = D \oplus \mathbf{1}$ for the complement, and $|v|$ for the number of ones of $v$. The cost of a transfer from $(b, x)$ to $(b', x')$ is $c = |b \oplus b'| + (x \oplus x')$, the number of the $n + 1$ lines that toggle. The candidates for a word $D$ are $(D, 0)$ and $(\overline{D}, 1)$.

**Lemma 1 (decoding).** Line L7 returns $D$ for both candidates of $D$.

*Proof.* For $(D, 0)$ it returns $D \oplus 0^n = D$. For $(\overline{D}, 1)$ it returns $D \oplus \mathbf{1} \oplus \mathbf{1} = D$. $\square$

**Lemma 2 (complement).** From a state $(b, x)$, let $h = |b \oplus D| + x$. Then $(D, 0)$ costs $h$ and $(\overline{D}, 1)$ costs $n + 1 - h$.

*Proof.* The first cost is $|b \oplus D| + (x \oplus 0) = h$. For the second, $b \oplus \overline{D} = \overline{b \oplus D}$ has $n - |b \oplus D|$ ones, and $x \oplus 1 = 1 - x$. The sum is $n - |b \oplus D| + 1 - x = n + 1 - h$. $\square$

**Lemma 3 (each transfer is the cheaper candidate).** The state sent at line L4 or L5 costs $\min(h, n + 1 - h)$.

*Proof.* Line L4 sends $(\overline{D}, 1)$ when $2h > n$, that is when $h > n/2$. By Lemma 2 it costs $n + 1 - h$. Since $h$ is an integer, $h > n/2$ gives $h \ge (n+1)/2$, so $n + 1 - h \le h$. Line L5 sends $(D, 0)$ when $h \le n/2$, at cost $h$, and then $h < n + 1 - h$. $\square$

**Theorem 1 (peak bound).** Each transfer toggles at most $\lceil n/2 \rceil$ of the $n + 1$ lines, and some transfer from some state reaches this bound.

*Proof.* By Lemma 3 the cost is $\min(h, n + 1 - h)$, and the least of two integers that sum to $n + 1$ is at most $\lfloor (n+1)/2 \rfloor$. For even $n = 2k$ this is $k = n/2$. For odd $n = 2k + 1$ it is $k + 1 = (n+1)/2$. In both cases it is $\lceil n/2 \rceil$.

The bound is reached. Take $x = 0$ and a word $D$ with $|b \oplus D| = \lceil n/2 \rceil$. Then $h = \lceil n/2 \rceil$ and $n + 1 - h = \lfloor n/2 \rfloor + 1 \ge h$, so the cost is $h = \lceil n/2 \rceil$. For odd $n$ the two candidates tie at $(n+1)/2$. $\square$

**Remark (a rule that ignores INV).** Suppose that the encoder inverts when $|b \oplus D| > n/2$, without the term $x$. Take $x = 1$ and $|b \oplus D| = \lfloor n/2 \rfloor$. The rule sends $(D, 0)$, which costs $\lfloor n/2 \rfloor + 1$. For even $n$ this is $n/2 + 1 > \lceil n/2 \rceil$, so the bound of Theorem 1 fails. For odd $n$ it is $(n+1)/2 = \lceil n/2 \rceil$, and in fact the two rules then differ only where the candidates tie: with $x = 1$ they disagree only at $|b \oplus D| = (n-1)/2$, where both candidates cost $(n+1)/2$, and with $x = 0$ they agree.

**Theorem 2 (optimal over whole sequences).** Fix a start state $(b_0, x_0)$ and words $D_1, \ldots, D_T$. Among all $2^T$ sequences of choices $x_1, \ldots, x_T \in \{0, 1\}$, with state $s_t = (D_t \oplus x_t \mathbf{1}, x_t)$, the encoder of lines L1 to L6 gives the least total cost $\sum_t c(s_{t-1}, s_t)$.

*Proof.* Put $D_0 = b_0 \oplus x_0 \mathbf{1}$, so that $s_0 = (D_0 \oplus x_0 \mathbf{1}, x_0)$ has the same form as the other states. Let $y_t = x_{t-1} \oplus x_t$ for $t = 1, \ldots, T$. Then

$$ c(s_{t-1}, s_t) = |D_{t-1} \oplus D_t \oplus y_t \mathbf{1}| + y_t = \begin{cases} |D_{t-1} \oplus D_t| & \text{if } y_t = 0, \\ n + 1 - |D_{t-1} \oplus D_t| & \text{if } y_t = 1. \end{cases} $$

So the cost of transfer $t$ depends only on $y_t$. The map from $(x_1, \ldots, x_T)$ to $(y_1, \ldots, y_T)$ is a bijection of $\{0,1\}^T$, since $x_t = x_0 \oplus y_1 \oplus \cdots \oplus y_t$. So the least total is $\sum_t \min(|D_{t-1} \oplus D_t|, n + 1 - |D_{t-1} \oplus D_t|)$, reached by choosing each $y_t$ alone.

The encoder reaches this sum. At step $t$ the state is $s_{t-1}$, and $h = |b_{t-1} \oplus D_t| + x_{t-1}$, where $b_{t-1} = D_{t-1} \oplus x_{t-1} \mathbf{1}$. The candidate $(D_t, 0)$ has $y_t = x_{t-1}$, and the candidate $(\overline{D_t}, 1)$ has $y_t = 1 - x_{t-1}$, so the two candidates are the two values of $y_t$, with the two costs above. By Lemma 3 the encoder takes the cheaper one, so its cost at step $t$ is $\min(|D_{t-1} \oplus D_t|, n + 1 - |D_{t-1} \oplus D_t|)$ for every $t$. $\square$

**Corollary (mean for random words).** If the words are independent and uniform on $\{0,1\}^n$, then the mean cost of each transfer is $E[\min(B, n + 1 - B)]$ with $B$ binomial with parameters $n$ and $1/2$.

*Proof.* Given the state $s_{t-1}$, the word $D_t$ is uniform and independent of it, so $|D_{t-1} \oplus D_t|$ is binomial with parameters $n$ and $1/2$. By the proof of Theorem 2 the cost is $\min(B, n + 1 - B)$ with this $B$. $\square$

For $n = 8$ the sum $\sum_{b=0}^{8} \binom{8}{b} 2^{-8} \min(b, 9 - b)$ is $837/256 \approx 3.27$. The tests check Lemma 3 and Theorem 1 on every state and word for $n \le 6$, Theorem 2 against all $2^T$ choices on random streams, and the corollary by exhaustive averaging for $n \le 6$.

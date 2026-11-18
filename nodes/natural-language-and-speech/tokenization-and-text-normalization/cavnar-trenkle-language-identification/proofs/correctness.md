---
title: The Cavnar-Trenkle classifier returns the language with the least out-of-place distance
proves: [correctness, termination]
status: full
---

Fix the profile length $L \ge 1$ and the largest n-gram length 5. A token is a maximal run of letters and apostrophes. For a token $w$ and $1 \le n \le 5$, let $u_n(w) = w$ if $n = 1$ and $u_n(w) = \_\,w\,\_^{\,n-1}$ otherwise, where $\_$ is a symbol that is not a letter. The count $c_x(g)$ of a string $g$ of length $n$ in a text $x$ is the number of pairs (token occurrence $w$ of $x$, position $i$) with $u_n(w)[i \ldots i+n) = g$. Order strings by $g \prec h$ when $c_x(g) > c_x(h)$, or $c_x(g) = c_x(h)$ and $g$ comes before $h$ in code point order. This is a strict total order on the strings with $c_x > 0$. The profile $P_L(x)$ is the list of the first $\min(L, G)$ strings in this order, where $G$ is the number of strings with $c_x > 0$. For a list $P$ and a list $Q$ without repeats, let $\operatorname{rank}_Q(g)$ be the 0-based position of $g$ in $Q$, and let

$$\operatorname{oop}(P, Q) = \sum_{r=0}^{|P|-1} \begin{cases} |r - \operatorname{rank}_Q(P[r])| & \text{if } P[r] \in Q, \\ L & \text{otherwise.} \end{cases}$$

**Lemma 1.** After lines L10 to L14, count$[g] = c_x(g)$ for every $g$, and a missing key means $c_x(g) = 0$.

*Proof.* The loops of lines L11, L12 and L14 visit each triple (token occurrence $w$, length $n$, start $i$) with $0 \le i \le |u_n(w)| - n$ exactly once, and line L14 adds 1 to the key $u_n(w)[i \ldots i+n)$. A string of length $n$ can only equal an n-gram of length $n$, so count$[g]$ is the number of triples whose n-gram is $g$, which is $c_x(g)$. $\square$

**Lemma 2.** For a token of $k$ characters and $n \ge 2$, $u_n(w)$ has exactly $k + 1$ n-grams. For $n = 1$ it has $k$.

*Proof.* $|u_n(w)| = 1 + k + (n - 1) = k + n$, and a string of length $k + n$ has $k + n - n + 1 = k + 1$ windows of length $n$. For $n = 1$, $u_1(w) = w$ has $k$ windows. $\square$

**Lemma 3.** Lines L15 and L16 return $P_L(x)$.

*Proof.* The sort key $(-\text{count}[g], g)$ orders the keys first by decreasing count and then by the string. By Lemma 1 the keys are exactly the strings with $c_x > 0$ and the counts are $c_x$, so the sorted list is these strings in the order $\prec$. Line L16 keeps the first $L$ of them, or all of them if there are fewer. $\square$

**Lemma 4.** For a document profile $P$ and a category profile $Q$, lines L4 to L7 compute $\operatorname{oop}(P, Q)$.

*Proof.* The loop of line L5 visits $r = 0, \ldots, |P| - 1$ once each. The profile $Q$ has no repeats, so $\operatorname{rank}_Q$ is well defined. Line L6 adds the first case of the sum when $P[r] \in Q$, and line L7 adds $L$ otherwise. After the last pass, $d$ is the full sum. $\square$

**Theorem.** CT-CLASSIFY$(x, C, L)$ stops and returns the language $c$ with the least $\operatorname{oop}(P_L(x), C[c])$. If several languages share the least distance, it returns the first of them in sorted order.

*Proof.* All loops run over finite lists, so the procedure stops. By Lemma 3, line L1 sets $P = P_L(x)$. Line L3 visits the languages in sorted order $c_1, c_2, \ldots, c_K$. We show by induction on $t$ that after the pass for $c_t$, $d^*$ is $\min_{s \le t} \operatorname{oop}(P, C[c_s])$ and best is the first $c_s$, $s \le t$, that reaches it. For $t = 1$, $d^* = \infty$ before the pass, so line L8 sets best to $c_1$ and $d^*$ to its distance, by Lemma 4. For $t > 1$, line L8 replaces best only when the new distance is strictly smaller than $d^*$. If it is smaller, $c_t$ is the only language with $s \le t$ that reaches the new minimum. If it is equal or larger, the minimum and the first language that reaches it do not change. After the pass for $c_K$, line L9 returns the claimed language. $\blacksquare$

**Remarks.** The distance is not symmetric, and it is not a metric: $\operatorname{oop}(P, Q) = 0$ holds exactly when $P$ is a prefix of $Q$, because each term is 0 only when $P[r] = Q[r]$. When $|P| \le L$ and $|Q| \le L$, each term is at most $L$, because two ranks below $L$ differ by less than $L$, so $0 \le \operatorname{oop}(P, Q) \le L\,|P|$.

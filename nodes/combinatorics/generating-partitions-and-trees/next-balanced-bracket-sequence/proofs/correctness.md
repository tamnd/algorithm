---
title: The next balanced bracket sequence is the lexicographic successor
proves: [correctness]
status: full
---

Fix $n \ge 0$ and $m = 2n$. Let $D_n$ be the set of balanced words of length $m$ over $\texttt{(} < \texttt{)}$. For a word $w$ and $0 \le i \le m$, let $h_i(w)$ be the number of opening minus the number of closing brackets in $w_1 \cdots w_i$. A word $w$ of length $m$ is in $D_n$ when $h_i(w) \ge 0$ for all $i$ and $h_m(w) = 0$. For $x \ne y$ of the same length, $x < y$ when $x_k < y_k$ at the first index $k$ with $x_k \ne y_k$. We write $w$ for the input and $w'$ for the array after the call.

**Lemma 1 (completions).** Let $x$ be a word of length $i$ with $h_j(x) \ge 0$ for all $j \le i$, and let $h = h_i(x)$ and $r = m - i$. If $r \ge h$ and $r - h$ is even, the words $y$ of length $r$ with $xy \in D_n$ all contain exactly $a = (r - h)/2$ opening brackets, the least of them is $\texttt{(}^a\texttt{)}^{a+h}$, and the greatest is $\texttt{)}^h(\texttt{()})^a$.

*Proof.* If $xy \in D_n$, then $y$ has $o$ opening and $r - o$ closing brackets with $h + o - (r - o) = 0$, so $o = a$. The word $\ell = \texttt{(}^a\texttt{)}^{a+h}$ is a completion: the heights of $x\ell$ after position $i$ rise from $h$ to $h + a$ and then fall to $0$, so they stay $\ge 0$. It is the least word of length $r$ with exactly $a$ opening brackets: another such word $y \ne \ell$ differs first from $\ell$ at an index $k$, and $k \le a$ is forced (the first $a$ letters of $\ell$ hold all of its opening brackets, so agreement on them leaves only closing brackets for both words), where $\ell_k = \texttt{(}$ and $y_k = \texttt{)}$, so $\ell < y$.

Let $g = \texttt{)}^h(\texttt{()})^a$. It is a completion, since its heights are $h, h - 1, \ldots, 0$ and then alternate between 1 and 0. Let $y \ne g$ be a completion and $k$ the first index with $y_k \ne g_k$. If $k \le h$, then $g_k = \texttt{)}$, so $y_k = \texttt{(} < g_k$. If $k > h$, then $x y_1 \cdots y_{k-1} = x g_1 \cdots g_{k-1}$ has height 0 when $k - h$ is odd and height 1 when $k - h$ is even. In the first case $g_k = \texttt{(}$, and $y_k = \texttt{)}$ would give height $-1$, which is impossible. So the first case cannot occur, and in the second case $g_k = \texttt{)}$ and $y_k = \texttt{(} < g_k$. In both possible cases $y < g$. $\square$

**Lemma 2 (the scan).** Each time line L5 is reached with index $i$, $d = h_{i-1}(w)$. The loop of line L2 stops at line L10 with the largest index $i$ such that $w_i = \texttt{(}$ and $h_{i-1}(w) \ge 1$, and it reaches line L11 when there is no such index.

*Proof.* The loop does not change $s$ before line L6, so $s = w$ while it scans. After lines L3 and L4 at index $i$, $d$ equals the number of closing minus the number of opening brackets in $w_i \cdots w_m$. This holds at the first index $i = m$, because $d$ starts at 0 by line L1, and each later step adds the contribution of one more letter. Since $h_m(w) = 0$, that difference equals $h_{i-1}(w)$. Line L5 is reached only when $w_i = \texttt{(}$, and the call returns at the first such $i$, from the right, with $h_{i-1}(w) > 0$. The index $i$ drops by exactly 1 in each step, so the loop either returns or ends after $m$ steps. $\square$

**Lemma 3 (where a larger word first differs).** Let $K$ be the set of indices $k$ with $w_k = \texttt{(}$ and $h_{k-1}(w) \ge 1$. A word $v \in D_n$ with $v > w$ exists that differs first from $w$ at index $k$ if and only if $k \in K$.

*Proof.* If $v > w$ differs first at $k$, then $v_k = \texttt{)}$ and $w_k = \texttt{(}$. Then $h_k(v) = h_{k-1}(w) - 1 \ge 0$, so $h_{k-1}(w) \ge 1$ and $k \in K$. Conversely, let $k \in K$ and let $x = w_1 \cdots w_{k-1}\texttt{)}$. Its heights are $\ge 0$, and $h = h_k(x) = h_{k-1}(w) - 1 \ge 0$. The suffix $w_{k+1} \cdots w_m$ leads $w$ from height $h + 2$ to height 0, so $r = m - k \ge h + 2$ and $r - h$ is even. By Lemma 1, $x$ has a completion $y$, and $v = xy$ is in $D_n$ and differs first from $w$ at $k$ with $v_k > w_k$. $\square$

**Theorem.** If $w \ne (\texttt{()})^n$, the call returns true and $w'$ is the least word of $D_n$ greater than $w$. If $w = (\texttt{()})^n$, the call returns false, $w' = w$, and $w$ is the greatest word of $D_n$.

*Proof.* *Case $K = \varnothing$.* Every opening bracket of $w$ stands at height 0, so it is followed by a closing bracket that brings the height back to 0, and $w = (\texttt{()})^n$. By Lemma 3 no word of $D_n$ is greater than $w$. By Lemma 2 the loop reaches line L11 without a write, so the call returns false and $w' = w$.

*Case $K \ne \varnothing$.* Then $w \ne (\texttt{()})^n$, because every opening bracket of $(\texttt{()})^n$ stands at height 0. Let $i = \max K$. By Lemma 2 the loop stops at this $i$ with $d = h_{i-1}(w) \ge 1$.

Let $v \in D_n$ with $v > w$, and let $k \in K$ be its first difference with $w$ (Lemma 3). Since $i = \max K$, $k \le i$, and by Lemma 3 some $v$ has $k = i$. If $k < i$, then each word $u$ that agrees with $w$ before $i$ and has $u_i = \texttt{)}$ satisfies $u < v$: they agree before $k$, and $u_k = w_k = \texttt{(} < \texttt{)} = v_k$. So the least $v > w$ has $k = i$, that is, it has the form $w_1 \cdots w_{i-1}\texttt{)}\,y$, and it is the one with the least completion $y$.

Line L6 writes $s_i = \texttt{)}$. With $x = w_1 \cdots w_{i-1}\texttt{)}$, the height is $h = d - 1$ and $r = m - i$ cells remain. By Lemma 1 the least completion is $\texttt{(}^a\texttt{)}^{a+h}$ with $a = (r - h)/2 = (m - i - d + 1)/2$. This is the value $p$ of line L7, and lines L8 and L9 write exactly this completion. So $w'$ is the least word of $D_n$ greater than $w$, and line L10 returns true. $\blacksquare$

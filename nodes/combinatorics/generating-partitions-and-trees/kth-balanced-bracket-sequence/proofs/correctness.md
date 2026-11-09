---
title: Unranking returns the balanced bracket sequence of the given rank
proves: [correctness]
status: full
---

Fix $n \ge 0$ and $m = 2n$. Let $D_n$ be the set of balanced words of length $m$, in lexicographic order with $\texttt{(} < \texttt{)}$, and let $h_i(w)$ be the number of opening minus closing brackets in $w_1 \cdots w_i$. Let $d[i][j]$ be the table of the algorithm: $d[0][0] = 1$, $d[0][j] = 0$ for $j \ge 1$, and $d[i][j] = d[i-1][j+1] + [\,j \ge 1\,]\, d[i-1][j-1]$ for $i \ge 1$.

**Lemma 1 (the table counts completions).** $d[i][j]$ is the number of words $y$ of length $i$ such that $j + h_t(y) \ge 0$ for all $t \le i$ and $j + h_i(y) = 0$.

*Proof.* By induction on $i$. For $i = 0$ only the empty word exists, and it qualifies exactly when $j = 0$. For $i \ge 1$, the qualifying words that start with $\texttt{(}$ are $\texttt{(}y'$ with $y'$ qualifying for $(i-1, j+1)$. Those that start with $\texttt{)}$ are $\texttt{)}y'$ with $y'$ qualifying for $(i-1, j-1)$, and they exist only for $j \ge 1$, because $\texttt{)}$ at height 0 gives height $-1$. $\square$

In particular $d[m][0] = |D_n|$, so line L2 accepts exactly the integers $0 \le k < |D_n|$.

For a word $x$ of length $i - 1$, let $W(x) = \{v \in D_n : v_1 \cdots v_{i-1} = x\}$, listed in lexicographic order.

**Lemma 2 (one step).** Let $W(x) \ne \varnothing$ and $h = h_{i-1}(x)$. Then $W(x\texttt{(})$ has $c = d[m-i][h+1]$ words, every word of $W(x\texttt{(})$ is smaller than every word of $W(x\texttt{)})$, and $W(x) = W(x\texttt{(}) \cup W(x\texttt{)})$.

*Proof.* Each word of $W(x)$ has $\texttt{(}$ or $\texttt{)}$ at position $i$, which gives the union. Two words, one from each part, agree before $i$ and differ at $i$, where $\texttt{(} < \texttt{)}$. A word $x\texttt{(}y$ is in $D_n$ exactly when the heights of $x$ are $\ge 0$ and $y$ finishes from height $h + 1$ in $m - i$ cells. The heights of $x$ are $\ge 0$ because $W(x)$ is not empty, so Lemma 1 gives $|W(x\texttt{(})| = d[m-i][h+1]$. $\square$

**Theorem.** For $0 \le k < |D_n|$, UNRANK$(n, k)$ returns the word of $D_n$ at 0-based position $k$ in lexicographic order.

*Proof.* Let $k_0$ be the input value and $\sigma$ the word at position $k_0$. Let $x_i = s[1 \ldots i-1]$ be the letters written before the step for index $i$. The loop of line L4 keeps the invariant:

- $W(x_i) \ne \varnothing$ and $h = h_{i-1}(x_i)$;
- $0 \le k < |W(x_i)|$, and $\sigma$ is the word at 0-based position $k$ of $W(x_i)$.

For $i = 1$, $x_1$ is empty, $W(x_1) = D_n$, $h = 0$ by line L3, and $k = k_0 < |D_n|$ by line L2. So the invariant holds.

Assume it holds before the step for $i$. Line L5 sets $c = |W(x_i\texttt{(})|$ by Lemma 2. By Lemma 2, the list of $W(x_i)$ is the list of $W(x_i\texttt{(})$ followed by the list of $W(x_i\texttt{)})$.

- If $k < c$, then $\sigma$ is at position $k$ of $W(x_i\texttt{(})$, and this set is not empty. Line L7 writes $\texttt{(}$ and raises $h$ by 1.
- If $k \ge c$, then $\sigma$ is at position $k - c$ of $W(x_i\texttt{)})$, and $0 \le k - c < |W(x_i)| - c = |W(x_i\texttt{)})|$, so this set is not empty. Lines L8 and L9 write $\texttt{)}$, set $k$ to $k - c$ and lower $h$ by 1.

In both cases the invariant holds before the step for $i + 1$. After the step for $i = m$, $x_{m+1} = s$ has length $m$, so $W(s) = \{s\}$ because $W(s) \ne \varnothing$. Then $k = 0$ and $\sigma$ is the only word of $W(s)$, so $\sigma = s$, and line L10 returns $\sigma$. $\blacksquare$

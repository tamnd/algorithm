---
title: The rank of a balanced bracket sequence counts the smaller sequences
proves: [correctness]
status: full
---

Fix $n \ge 0$ and $m = 2n$. Let $D_n$ be the set of balanced words of length $m$ over $\texttt{(} < \texttt{)}$, ordered lexicographically: $x < y$ when $x_k < y_k$ at the first index $k$ with $x_k \ne y_k$. For a word $w$ let $h_i(w)$ be the number of opening minus closing brackets in $w_1 \cdots w_i$. The *rank* of $s \in D_n$ is $\mathrm{rank}(s) = \#\{v \in D_n : v < s\}$, its 0-based position in the sorted list.

**Lemma 1 (the table).** For $i \ge 0$ and $j \ge 0$ let $F(i, j)$ be the set of words $y$ of length $i$ such that $j + h_t(y) \ge 0$ for all $t \le i$ and $j + h_i(y) = 0$, the ways to finish from height $j$ in $i$ cells. The table of the algorithm, defined by $d[0][0] = 1$, $d[0][j] = 0$ for $j \ge 1$, and

$$d[i][j] = d[i-1][j+1] + [\,j \ge 1\,]\; d[i-1][j-1] \quad (i \ge 1),$$

satisfies $d[i][j] = |F(i, j)|$.

*Proof.* By induction on $i$. For $i = 0$, the only word is the empty word, and it finishes exactly when $j = 0$. For $i \ge 1$, split $F(i, j)$ by the first letter. The words that start with $\texttt{(}$ are $\texttt{(}y'$ with $y' \in F(i-1, j+1)$. The words that start with $\texttt{)}$ are $\texttt{)}y'$ with $y' \in F(i-1, j-1)$ when $j \ge 1$; when $j = 0$ the first letter $\texttt{)}$ gives height $-1$, so there are none. The two parts are disjoint, and the induction hypothesis gives their sizes. $\square$

**Lemma 2 (the words below a given one).** Let $s \in D_n$. For each index $i$ with $s_i = \texttt{)}$, let $A_i$ be the set of $v \in D_n$ that agree with $s$ on $1, \ldots, i-1$ and have $v_i = \texttt{(}$. Then the sets $A_i$ are pairwise disjoint, their union is $\{v \in D_n : v < s\}$, and $|A_i| = d[m-i][h_{i-1}(s) + 1]$.

*Proof.* A word $v \in D_n$ with $v < s$ has a first index $i$ with $v_i \ne s_i$, and there $v_i < s_i$, so $v_i = \texttt{(}$ and $s_i = \texttt{)}$. So $v \in A_i$ for exactly this $i$, and the sets are disjoint because the first difference is unique. Each word of $A_i$ is smaller than $s$, by the definition of the order. A word $v$ that agrees with $s$ on $1, \ldots, i-1$ and has $v_i = \texttt{(}$ is in $D_n$ exactly when its prefix heights up to $i$ are $\ge 0$ and $v_{i+1} \cdots v_m \in F(m - i, h_{i-1}(s) + 1)$. The prefix heights up to $i - 1$ are those of $s$, so they are $\ge 0$, and $h_i(v) = h_{i-1}(s) + 1 \ge 1$. So $|A_i| = |F(m-i, h_{i-1}(s)+1)|$, which is the table entry by Lemma 1. $\square$

**Theorem.** For $s \in D_n$, RANK$(s)$ returns $\mathrm{rank}(s)$. The map $s \mapsto \mathrm{rank}(s)$ is a bijection from $D_n$ onto $\{0, 1, \ldots, |D_n| - 1\}$.

*Proof.* The loop of line L3 keeps the invariant: before the step for index $i$, $h = h_{i-1}(s)$ and $r = \sum_{t < i,\ s_t = \texttt{)}} |A_t|$. It holds for $i = 1$ with $h = r = 0$ by line L2. Line L4 adds 1 to $h$ for an opening bracket. For a closing bracket, line L5 adds $d[m-i][h+1] = |A_i|$ by Lemma 2, and line L6 lowers $h$ by 1. So the invariant holds before the step for $i + 1$. The loop runs for $i = 1, \ldots, m$, so at line L7 $r = \sum_i |A_i| = \#\{v \in D_n : v < s\}$ by Lemma 2.

Lexicographic order is a total order on $D_n$, so the list of $D_n$ in increasing order is unique. The word at 0-based position $p$ of that list has exactly $p$ smaller words, so its rank is $p$. Hence the rank maps $D_n$ one to one onto $\{0, \ldots, |D_n| - 1\}$. $\blacksquare$

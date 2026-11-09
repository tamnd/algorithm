---
title: The revolving door walk visits every k-subset once with one swap per step
proves: [correctness]
status: full
---

For integers $0 \le t \le m$ let $R(m, t)$ be the list of $t$-subsets of $[m] = \{1, \ldots, m\}$ defined by $R(m, 0) = (\emptyset)$, $R(m, m) = ([m])$, and for $0 < t < m$

$$R(m, t) = R(m-1, t),\ \ R(m-1, t-1)^R \cup \{m\}.$$

Here $L^R$ is $L$ in reverse order and $L \cup \{m\}$ adds $m$ to each subset of $L$. Two subsets $S, S'$ of the same size are *adjacent* when $|S \setminus S'| = 1$, that is, $S' = S \setminus \{x\} \cup \{y\}$ for some $x \in S$, $y \notin S$. Write $F(m, t)$ and $L(m, t)$ for the first and the last subset of $R(m, t)$, and $x(m, t) = t - 1$ if $t \ge 2$ and $x(m, t) = m - 1$ if $t = 1$, the value of line L4.

**Lemma 1 (content).** $R(m, t)$ contains every $t$-subset of $[m]$ exactly once, and it has $C(m, t)$ entries.

*Proof.* Induction on $m$. The cases $t = 0$ and $t = m$ hold, since there is one such subset. For $0 < t < m$, the first part $R(m-1, t)$ holds each $t$-subset of $[m-1]$ once, which are the $t$-subsets of $[m]$ without $m$. The second part holds $T \cup \{m\}$ for each $(t-1)$-subset $T$ of $[m-1]$ once, which are the $t$-subsets of $[m]$ with $m$. Reversal does not change the content. The two parts are disjoint, and their sizes add up to $C(m-1, t) + C(m-1, t-1) = C(m, t)$. $\square$

**Lemma 2 (ends).** For $t \ge 1$ and $t \le m$: $F(m, t) = \{1, \ldots, t\}$. For $0 < t < m$: $L(m, t) = \{1, \ldots, t-1, m\}$. For $t = 0$ both ends are $\emptyset$, and for $t = m$ both are $[m]$.

*Proof.* Induction on $m$. Let $0 < t < m$. Then $F(m, t) = F(m-1, t)$, which is $\{1, \ldots, t\}$ by induction, both when $t < m - 1$ and when $t = m - 1$. The last subset of $R(m, t)$ is the first subset of $R(m-1, t-1)$ with $m$ added, so $L(m, t) = F(m-1, t-1) \cup \{m\}$. If $t \ge 2$ this is $\{1, \ldots, t-1\} \cup \{m\}$; if $t = 1$ it is $\emptyset \cup \{m\} = \{m\}$, which is the same formula. $\square$

**Lemma 3 (junction).** For $0 < t < m$, the last subset of $R(m-1, t)$ is $A = L(m-1, t)$, the first subset of $R(m-1, t-1)^R \cup \{m\}$ is $B = L(m-1, t-1) \cup \{m\}$, and $B = A \setminus \{x\} \cup \{m\}$ with $x = x(m, t) \in A$.

*Proof.* By definition, the last subset of the reversed list $R(m-1, t-1)^R$ is the first subset of the original list, so the first subset of the reversed list is $L(m-1, t-1)$. Now use Lemma 2 for each case.

- $t = 1$: $A = L(m-1, 1)$. If $m - 1 > 1$ this is $\{m-1\}$ by Lemma 2, and if $m - 1 = 1$ it is $[1] = \{1\} = \{m - 1\}$. $B = \emptyset \cup \{m\} = \{m\}$. So $x = m - 1$.
- $t \ge 2$ and $t < m - 1$: $A = \{1, \ldots, t-1, m-1\}$. $B = L(m-1, t-1) \cup \{m\}$ with $0 < t - 1 < m - 1$, so $B = \{1, \ldots, t-2, m-1, m\}$. So $x = t - 1$.
- $t \ge 2$ and $t = m - 1$: $A = [m-1] = \{1, \ldots, t\}$. $B = \{1, \ldots, t-2, m-1, m\}$ as before, and $m - 1 = t$, so $B = \{1, \ldots, t-2, t, t+1\}$. So $x = t - 1$.

In each case $x \in A$ and $m \notin A$. $\square$

**Lemma 4 (adjacency).** Consecutive subsets of $R(m, t)$ are adjacent.

*Proof.* Induction on $m$. For $t = 0$ or $t = m$ there is nothing to show. For $0 < t < m$, pairs inside $R(m-1, t)$ are adjacent by induction. Pairs inside the second part are $S \cup \{m\}$ and $S' \cup \{m\}$ where $S, S'$ are consecutive in $R(m-1, t-1)$ in one order or the other. Adjacency is symmetric, and adding $m \notin S \cup S'$ keeps it. The pair at the junction is adjacent by Lemma 3. $\square$

**Lemma 5 (the walk).** Let $0 \le t \le m \le n$. Suppose WALK$(m, t, d)$ starts when $a_1 \ldots a_m$ is the bit array of $F(m, t)$ if $d$ is forward and of $L(m, t)$ if $d$ is reverse. Then the call visits the arrays of $R(m, t)$ in order if $d$ is forward and in reverse order if $d$ is reverse, it never reads or writes $a_j$ for $j > m$, and it returns with $a_1 \ldots a_m$ equal to the other end.

*Proof.* Induction on $m$. If $t = 0$ or $t = m$, line L3 visits the single subset and returns, which is both ends. Let $0 < t < m$ and $x = x(m, t)$ from line L4; note $1 \le x \le m - 1$.

*Forward.* At the start, $a_1 \ldots a_m$ holds $F(m, t) = F(m-1, t)$ by Lemma 2, so $a_m = 0$ and $a_1 \ldots a_{m-1}$ is the first subset of $R(m-1, t)$. By induction, line L6 visits $R(m-1, t)$ with $a_m = 0$ unchanged, which is the first part of $R(m, t)$, and ends at $A = L(m-1, t)$. Line L7 clears $a_x$ and sets $a_m$, which by Lemma 3 gives $B$. Now $a_m = 1$ and $a_1 \ldots a_{m-1}$ holds $L(m-1, t-1)$, which is the last subset of $R(m-1, t-1)$. By induction, line L8 visits $R(m-1, t-1)$ in reverse with $a_m = 1$, which is the second part of $R(m, t)$, and ends at $F(m-1, t-1) \cup \{m\} = L(m, t)$.

*Reverse.* The reverse of $R(m, t)$ is $R(m-1, t-1) \cup \{m\},\ R(m-1, t)^R$. At the start $a$ holds $L(m, t) = F(m-1, t-1) \cup \{m\}$. Line L10 visits $R(m-1, t-1)$ forward with $a_m = 1$ and ends at $L(m-1, t-1) \cup \{m\} = B$. Line L11 clears $a_m$ and sets $a_x$, which by Lemma 3 gives $A = L(m-1, t)$. Line L12 visits $R(m-1, t)$ in reverse with $a_m = 0$ and ends at $F(m-1, t) = F(m, t)$.

Every call made has first argument $m - 1$, so by induction none of them touches positions above $m - 1$, and lines L7 and L11 touch only $x \le m - 1$ and $m$. $\square$

**Theorem.** For $0 \le k \le n$, REVOLVING-DOOR$(n, k)$ visits each $k$-subset of $[n]$ exactly once, in the order $R(n, k)$, and consecutive visits differ by removing one element and adding another. The walk makes $2C(n, k) - 1$ calls of WALK.

*Proof.* Line L1 sets $a$ to the array of $\{1, \ldots, k\}$, which is $F(n, k)$ by Lemma 2 (for $k = 0$ it is $\emptyset$). By Lemma 5 with $m = n$ and $d$ forward, line L2 visits $R(n, k)$ in order. By Lemma 1 this is each $k$-subset once, and by Lemma 4 consecutive ones are adjacent. For the count: each call with $0 < t < m$ makes two calls, and each of them has a nonempty list. A call with $t = 0$ or $t = m$ makes none and visits once. So the calls form a tree in which every inner node has two children and the leaves are the $C(n, k)$ visits, and such a tree has $C(n, k) - 1$ inner nodes. $\blacksquare$

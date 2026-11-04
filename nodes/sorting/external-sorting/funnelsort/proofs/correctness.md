---
title: Funnelsort returns the stable sort of its input
proves: [correctness]
status: full
---

We use the line numbers of the pseudocode. For a sequence $X$, write $\operatorname{st}(X)$ for its stable sort. For sorted sequences $X_1, \ldots, X_r$, the *stable merge* $\operatorname{mg}(X_1, \ldots, X_r)$ is $\operatorname{st}(X_1 X_2 \cdots X_r)$: the items in non-decreasing order, and equal items in the order of $X_1, \ldots, X_r$ and of their positions. The cache bound is not proved here; see the cache-oblivious model page.

## The funnel

For an inner node $v$ of a funnel, let $\sigma(v)$ be the sequence of all items that line L9 appends to the buffer of $v$, over all calls of FILL, in order. For a leaf $v$, let $\sigma(v)$ be its input, which is sorted. Let $X_1, \ldots, X_r$ be the leaves below $v$, from left to right.

**Lemma 1.** Each call FILL$(v)$ ends. At any time, the items that $v$ has appended form a prefix of $\operatorname{mg}(X_1, \ldots, X_r)$. When $v$ is marked exhausted, this prefix is all of $\operatorname{mg}(X_1, \ldots, X_r)$.

*Proof.* By induction on the height of $v$. A leaf is exhausted from the start, and its buffer holds its whole sorted input, so the claim holds.

Let $v$ be an inner node with children $c_1$ and $c_2$, and let $Y_1 = \operatorname{mg}$ of the leaves below $c_1$ and $Y_2$ the same for $c_2$. By induction, the items that $c_i$ has appended form a prefix of $Y_i$, and its buffer holds the part of this prefix that $v$ has not yet taken, in order. So at each moment, the items that $v$ has taken from $c_i$ are a prefix of $Y_i$, and the head of the buffer of $c_i$, if any, is the next item of $Y_i$.

*Termination.* Each pass of the loop of line L6 either returns at line L8 or moves one item at line L9. The number of items is finite, and each inner call of line L7 ends by induction, so FILL$(v)$ ends.

*Prefix.* Line L7 fills each child buffer that is empty and whose child is not exhausted. By induction, a call FILL$(c_i)$ ends with a full buffer or with $c_i$ exhausted. If it ends exhausted with an empty buffer, then $v$ has taken all of $Y_i$. So after line L7, for each $i$, either the buffer of $c_i$ holds the next item of $Y_i$, or $v$ has taken all of $Y_i$. Line L9 then appends the smaller of the two next items, or the left one on ties, or the only one. This is exactly the next step of the stable merge of $Y_1$ and $Y_2$, because $Y_1$ and $Y_2$ are sorted and every item of $Y_1$ comes before the equal items of $Y_2$ in $\operatorname{mg}(X_1, \ldots, X_r)$. And $\operatorname{mg}(Y_1, Y_2) = \operatorname{mg}(X_1, \ldots, X_r)$, because the leaves below $c_1$ are $X_1, \ldots, X_q$ and those below $c_2$ are $X_{q+1}, \ldots, X_r$ for some $q$.

*Exhaustion.* Line L8 marks $v$ exhausted only when both child buffers are empty after line L7. By the argument above, $v$ has then taken all of $Y_1$ and all of $Y_2$, so it has appended all of $\operatorname{mg}(Y_1, Y_2)$. $\blacksquare$

**Lemma 2.** In line L4, FILL(root) leaves in the root buffer the sequence $\operatorname{mg}(P_1, \ldots, P_k)$, where $P_1, \ldots, P_k$ are the sorted parts from left to right.

*Proof.* The empty leaves that round $k$ up to a power of 2 add no items. The root buffer holds $n$ items, the number of all items. By Lemma 1, the loop of line L6 appends a prefix of $\operatorname{mg}(P_1, \ldots, P_k)$, and it stops when the buffer is full, which is after all $n$ items, or when the root is exhausted, which by Lemma 1 is also after all items. Nothing removes items from the root buffer. $\blacksquare$

## The sort

**Theorem.** FUNNELSORT$(A)$ leaves $\operatorname{st}(A)$ in $A$.

*Proof.* By strong induction on $n$. If $n \le 8$, line L1 uses insertion sort, which is stable. Else, $k = \lceil n^{1/3} \rceil \ge 3$ and each part of line L2 has at most $\lceil n/k \rceil < n$ items, so by induction line L3 replaces the part $A_j$ by $\operatorname{st}(A_j)$. The parts are consecutive, so $\operatorname{st}(A) = \operatorname{mg}(\operatorname{st}(A_1), \ldots, \operatorname{st}(A_k))$: an item of $A_j$ comes before an equal item of $A_{j'}$ in $A$ exactly when $j < j'$. By Lemma 2, line L4 computes this sequence, and line L5 writes it to $A$. $\blacksquare$

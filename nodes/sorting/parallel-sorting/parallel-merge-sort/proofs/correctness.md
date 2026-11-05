---
title: Parallel merge sort is correct, stable, and has work Θ(n log n) and span O(log³ n)
proves: [correctness]
status: full
---

Fix the inputs of a call of P-MERGE: sorted ranges $X[a_1 \ldots a_2 - 1]$ and $Y[b_1 \ldots b_2 - 1]$, with $N = n_a + n_b$ items. Define the *stable order* on these $N$ items: $u$ comes before $v$ if $u$ has a smaller key, or the keys are equal and $u$ is in $X$ and $v$ is in $Y$, or the keys are equal, both are in the same input and $u$ has the smaller index. This is a strict total order. The stable merge of the two ranges is the list of the items in this order.

## Lemma 1. P-MERGE writes the stable merge to Z[c .. c + N − 1]

*Proof.* By induction on $N$. For $N = 0$ the call writes nothing, which is correct.

Let $N \ge 1$ and $n_a \ge n_b$, so $n_a \ge 1$. Let $x = X[q]$. Line L12 finds the least $r$ with $r = b_2$ or $Y[r] \ge x$. Since $Y$ is sorted, $Y[b_1 \ldots r-1]$ are the items of $Y$ with key less than $x$, and $Y[r \ldots b_2 - 1]$ are those with key at least $x$. The items that come before $x$ in the stable order are:

- the items $X[a_1 \ldots q-1]$, which have keys at most $x$ and smaller indices;
- the items of $Y$ with key less than $x$, which are $Y[b_1 \ldots r-1]$. An item of $Y$ with key equal to $x$ comes after $x$, because $x$ is in $X$.

No other item comes before $x$: the items $X[q+1 \ldots a_2-1]$ have keys at least $x$ and larger indices, and the items $Y[r \ldots b_2-1]$ have keys at least $x$. So exactly $(q - a_1) + (r - b_1)$ items come before $x$, and line L13 gives $x$ the position $c$ plus this number, which is its position in the stable merge.

The items before $x$ are the inputs of the call on line L15, and the items after $x$ are the inputs of the call on line L16. The stable order restricted to a subset is the stable order of that subset, because the order depends only on keys, inputs and indices. Each recursive call has fewer than $N$ items, so by induction the call on line L15 writes the items before $x$ in stable order to $Z[c \ldots t - 1]$, and the call on line L16 writes the items after $x$ in stable order to $Z[t + 1 \ldots c + N - 1]$. Together with $Z[t] = x$, this is the stable merge.

The case $n_a < n_b$ is the same with $y = Y[q]$. Line L20 finds the least $r$ with $r = a_2$ or $X[r] > y$, so $X[a_1 \ldots r-1]$ are the items of $X$ with key at most $y$. These come before $y$, because an item of $X$ with key equal to $y$ comes before $y$. The items $Y[b_1 \ldots q-1]$ also come before $y$, and no other items do. So $y$ goes to position $c + (r - a_1) + (q - b_1)$, which is line L21, and the two recursive calls handle the rest as before. $\square$

The two recursive calls of one call write the disjoint ranges $Z[c \ldots t-1]$ and $Z[t+1 \ldots c+N-1]$ and only read $X$ and $Y$. When $Z$ is not $X$ or $Y$, the parallel calls do not interfere, and every schedule gives the same result.

## Lemma 2. P-MERGE-SORT sorts A[lo .. hi − 1] stably

*Proof.* By induction on $hi - lo$. A range of at most one item is sorted. Otherwise, by induction, lines L3 to L5 sort the two halves stably. These calls work on disjoint ranges of $A$ and of $T$, so they do not interfere. Line L6 copies the range to $T$, and line L7 merges $T[lo \ldots mid-1]$ and $T[mid \ldots hi-1]$ into $A[lo \ldots hi-1]$. The items of the left half have smaller input positions than the items of the right half, so by Lemma 1 the merge puts equal keys in input order. Within each half, equal keys are already in input order. So the result is sorted, and equal keys keep their input order. $\square$

## Lemma 3. Split sizes

Let a call of P-MERGE have $N \ge 1$ items, and let its two recursive calls have $N_1$ and $N_2$ items. Then $N_1 + N_2 = N - 1$, $N_1, N_2 \le 3N/4$ and $N_1 + 1, N_2 + 1 \ge N/4$.

*Proof.* Take the case $n_a \ge n_b$, so $n_a \ge N/2 \ge n_b$. The left call gets $\lfloor n_a/2 \rfloor$ items of $X$ and $r - b_1 \le n_b$ items of $Y$, so $N_1 \le n_a/2 + n_b = N/2 + n_b/2 \le 3N/4$. The right call gets $\lceil n_a/2 \rceil - 1$ items of $X$ and at most $n_b$ items of $Y$, so $N_2 \le 3N/4$ as well. Also $N_1 \ge \lfloor n_a/2 \rfloor \ge n_a/2 - 1/2$ and $N_2 \ge \lceil n_a/2 \rceil - 1 \ge n_a/2 - 1$, so both are at least $N/4 - 1$. The other case is the same with $n_b > N/2$. $\square$

## Lemma 4. P-MERGE has span O(log² N) and work Θ(N)

Charge a call with $N$ items a cost of at most $d(1 + \lg(N+1))$ for itself, for a constant $d$. This covers lines L8 to L14, since a binary search on at most $N$ items makes at most $\lceil \lg(N+1) \rceil$ probes.

*Span.* The span satisfies $S(0) \le d$ and $S(N) \le S(\lfloor 3N/4 \rfloor) + d(1 + \lg(N+1))$ by Lemma 3. Along any chain of calls the sizes drop by a factor of at least $3/4$ at each step, so a chain has at most $\log_{4/3} N + 2$ calls, each of cost at most $d(1 + \lg(N+1))$. So $S(N) = O(\log^2 N)$.

*Work.* Let $g(N) = \lg(N + 1)$. We show $W(N) \le K(N+1) - 2d\,g(N)$ for a constant $K$. Since $W(N) \ge 0$, for each of the finitely many $N < 2^{12}$ the bound holds when $K$ is large enough, so fix such a $K$, with also $K \ge d$. Let $N \ge 2^{12}$, and assume the bound for all smaller sizes. By Lemma 3,

$$W(N) \le K(N_1 + 1) - 2d\,g(N_1) + K(N_2 + 1) - 2d\,g(N_2) + d(1 + g(N)).$$

Here $K(N_1 + 1) + K(N_2 + 1) = K(N + 1)$, and $g(N_i) \ge \lg(N/4) = \lg N - 2$. So it is enough to show $4d(\lg N - 2) \ge 2d\,g(N) + d(1 + g(N))$, that is $4 \lg N - 8 \ge 3 g(N) + 1$. Since $g(N) \le \lg N + 1$, it is enough that $\lg N \ge 12$, which holds. So $W(N) = O(N)$. Each of the $N$ items is written by its own call, so $W(N) = \Omega(N)$. $\square$

## Theorem. Work and span of P-MERGE-SORT

P-MERGE-SORT on $n$ keys has work $\Theta(n \log n)$ and span $O(\log^3 n)$ in the work-span model.

*Proof.* The copy on line L6 is a parallel loop over $hi - lo$ items, with work $\Theta(hi - lo)$ and span $O(\log(hi - lo))$. By Lemma 4 the merge on line L7 has work $\Theta(hi - lo)$ and span $O(\log^2(hi - lo))$. The two recursive calls run in parallel, so

$$W(n) = W(\lfloor n/2 \rfloor) + W(\lceil n/2 \rceil) + \Theta(n), \qquad S(n) = S(\lceil n/2 \rceil) + O(\log^2 n).$$

The first recurrence is the one of sequential merge sort, with solution $\Theta(n \log n)$. The second has $\lceil \lg n \rceil$ levels, each of span $O(\log^2 n)$, so $S(n) = O(\log^3 n)$. $\square$

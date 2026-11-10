---
title: The transposition rule is not competitive
proves: [correctness]
status: full
---

**Model.** A list holds the items $1, 2, \ldots, n$, in this order at the start, with $n \ge 2$. An access to position $i$ costs $i$, the accessed item may move forward by free exchanges, and other adjacent swaps cost $1$.

**Lemma 1 (transpose serves each request).** Each request is served: line L3 finds the item, line L4 pays its position, and line L6 swaps two adjacent items, so the list stays a permutation of the same items.

**Lemma 2 (the cost of transpose).** Let $\sigma_m$ be the sequence of $m$ requests $n, n-1, n, n-1, \ldots$ (starting with $n$). Then $\mathrm{TRANS}(\sigma_m) = nm$, and after each even number of requests the list is $1, 2, \ldots, n$ again.

*Proof.* By induction on pairs of requests. If the list is $1, \ldots, n-2, n-1, n$, the request $n$ costs $n$ and line L6 gives $1, \ldots, n-2, n, n-1$. The next request $n - 1$ is then last, costs $n$, and line L6 gives $1, \ldots, n-2, n-1, n$. If $m$ is odd, the last request costs $n$ too. $\square$

So $\sigma_m$ always requests the item that is last in the list of transpose.

**Lemma 3 (an offline schedule).** $\mathrm{OPT}(\sigma_m) \le 2n + \frac{3}{2}(m - 2) + 1$ for $m \ge 2$.

*Proof.* Consider the schedule $B$. At the first request, $n$ is at position $n$; $B$ pays $n$ and moves it to the front with free exchanges, which gives $n, 1, \ldots, n-1$. At the second request, $n - 1$ is at position $n$; $B$ pays $n$ and moves it to the front, which gives $n-1, n, 1, \ldots, n-2$. After that $B$ never moves. Each later request for $n$ costs $2$, and each later request for $n - 1$ costs $1$. Of the $m - 2$ later requests, $\lceil (m-2)/2 \rceil$ are for $n$ and $\lfloor (m-2)/2 \rfloor$ are for $n - 1$. So $B$ pays

$$2n + 2 \lceil (m-2)/2 \rceil + \lfloor (m-2)/2 \rfloor \le 2n + \tfrac{3}{2}(m-2) + 1,$$

and $\mathrm{OPT}(\sigma_m)$ is at most the cost of $B$. $\square$

**Theorem.** For each $n \ge 2$ and each $c < 2n/3$, there is no constant $b$ such that $\mathrm{TRANS}(\sigma) \le c \cdot \mathrm{OPT}(\sigma) + b$ for all sequences $\sigma$ on a list of $n$ items. So there is no constant $c$ such that transpose is $c$-competitive on lists of every length.

*Proof.* Suppose that such $c$ and $b$ exist. By Lemmas 2 and 3, for each $m \ge 2$,

$$nm \le c \bigl( 2n + \tfrac{3}{2}(m - 2) + 1 \bigr) + b .$$

Divide by $m$ and let $m \to \infty$. This gives $n \le \frac{3}{2} c$, that is $c \ge 2n/3$, which is a contradiction. For the second claim, a constant $c$ fails for each $n > 3c/2$. $\blacksquare$

**Remark (the upper bound).** On a list of $n$ items, each access costs at least $1$ for every algorithm and at most $n$ for transpose, which never pays for exchanges. So $\mathrm{TRANS}(\sigma) \le n m \le n \cdot \mathrm{OPT}(\sigma)$, and the ratio of transpose on lists of length $n$ is between $2n/3$ and $n$.

The tests reproduce Lemma 2 for $n \le 7$, compare Lemma 3 with an exact optimum (paid and free exchanges) for $n \le 5$, and check that the ratio grows with $n$.

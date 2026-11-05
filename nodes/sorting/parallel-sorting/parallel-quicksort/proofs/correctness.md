---
title: Parallel quicksort is correct and stable, with span O(log² n) with high probability
proves: [correctness]
status: full
---

## Lemma 1. PACK returns the flagged items in input order

*Proof.* Let $s[i] = f[0] + \cdots + f[i-1]$. If $f[i] = f[j] = 1$ and $i < j$, then $s[j] \ge s[i] + f[i] = s[i] + 1$, so the flagged items get distinct output indices in increasing order of their input index. The largest index used is $s[n-1] + f[n-1] - 1 = total - 1$, so the indices are exactly $0, \ldots, total - 1$. The writes of line L11 go to distinct cells, so they do not interfere. $\square$

## Lemma 2. PAR-QUICKSORT returns its input sorted and stably

Define the stable order of the input: $u$ before $v$ if $u$ has a smaller key, or the keys are equal and $u$ has the smaller input index. The claim is that the output lists the items in this order.

*Proof.* By induction on $n$. For $n \le 1$ the claim holds. For $n \ge 2$, each key of $A$ satisfies exactly one of $A[i] < x$, $A[i] = x$ and $A[i] > x$, so by Lemma 1, $L$, $E$ and $G$ split the items of $A$, and each part keeps the input order. Every item of $L$ has a smaller key than every item of $E$, which has a smaller key than every item of $G$, so in the stable order all of $L$ comes first, then all of $E$, then all of $G$. The items of $E$ have equal keys and are in input order, so $E$ is in stable order. The parts $L$ and $G$ have fewer than $n$ items, because $x$ is in $E$. The stable order of $L$ is the stable order of $A$ restricted to $L$, because PACK keeps input order, so by induction $L'$ lists $L$ in stable order, and the same holds for $G'$. So $L' \parallel E \parallel G'$ lists $A$ in stable order. The two calls of lines L6 and L7 read and write disjoint arrays, so they do not interfere. $\square$

## Lemma 3. A random pivot is good with probability at least 1/2

Consider a call on $s \ge 2$ keys. Call the pivot good if $|L| \le 3s/4$ and $|G| \le 3s/4$.

*Proof.* Sort the $s$ items of the call by the stable order, and let $u$ be the position of the pivot item in this list, from $0$ to $s - 1$. Since $i$ is uniform, $u$ is uniform. The items of $L$ come before the pivot item, so $|L| \le u$. The items of $G$ come after it, so $|G| \le s - 1 - u$. So the pivot is good when $u \le 3s/4$ and $u \ge s/4 - 1$. The integers $u$ in the interval $[s/4 - 1, 3s/4]$, which has length $s/2 + 1$, number at least $s/2$, and they all lie in $[0, s - 1]$. So the probability is at least $1/2$. $\square$

## Lemma 4. The recursion depth is O(log n) with high probability

Let $n \ge 2$, $k = \lceil \log_{4/3} n \rceil + 1$ and $D = 8k$. With probability at least $1 - n^{-2.9}$, no call is at depth more than $D$.

*Proof.* Fix one item $y$ of the input. Consider the chain of calls whose input contains $y$: the top call, then the call on $L$ or $G$ that contains $y$, and so on, until a call with $y$ in $E$ or a call on one item. If a call of this chain has $s$ items and a good pivot, the next call of the chain has at most $3s/4$ items. So after $k$ good pivots the size is at most $(3/4)^k n \le 3/4 < 1$, which is impossible, so the chain ends before the call after its $k$-th good pivot. In other words, a chain with $D$ calls of size at least 2 has fewer than $k$ good pivots among its first $D$ calls.

The pivot of each call is drawn afresh, and by Lemma 3 it is good with probability at least $1/2$ whatever happened before. So the number of good pivots among the first $D$ calls of the chain, if the chain is that long, is at least a binomial variable $X$ with $D$ trials and success probability $1/2$, in the sense of stochastic domination. Its mean is $\mu = D/2 = 4k$. By the Chernoff bound $\Pr[X < (1 - \delta)\mu] \le e^{-\delta^2 \mu / 2}$ with $\delta = 3/4$,

$$\Pr[X < k] \le e^{-(9/16)(4k)/2} = e^{-9k/8}.$$

Since $k \ge \log_{4/3} n = \ln n / \ln(4/3) \ge 3.47 \ln n$, this is at most $e^{-3.9 \ln n} = n^{-3.9}$. Every call at depth more than $D$ lies on the chain of some item, so a union bound over the $n$ items gives a failure probability of at most $n \cdot n^{-3.9} = n^{-2.9}$. $\square$

## Theorem. Span and work

In the work-span model, PAR-QUICKSORT on $n$ keys has span $O(\log^2 n)$ with probability at least $1 - n^{-2.9}$, and expected work $O(n \log n)$.

*Proof.* A call on $s$ keys does lines L1 to L5 and L9 with work $O(s)$ and span $O(\log s)$: line L4 is a parallel loop, and each PACK is a prefix sum and a parallel loop. The two recursive calls run in parallel. So the span is at most the recursion depth times $O(\log n)$, which is $O(\log^2 n)$ when the event of Lemma 4 holds.

For the work, charge the $O(s)$ work of a call to its $s$ items, $O(1)$ each. An item is charged once for each call on its chain. The chain of an item ends after at most $k$ good pivots, and each call has a good pivot with probability at least $1/2$ whatever happened before, so the expected number of calls on the chain is at most $2k$. By linearity of expectation the expected work is $O(nk) = O(n \log n)$. $\square$

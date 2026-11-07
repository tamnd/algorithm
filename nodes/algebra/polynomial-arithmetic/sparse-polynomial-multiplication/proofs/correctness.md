---
title: The heap method returns the normalized product of two sparse polynomials
proves: [correctness]
status: full
---

Let $R$ be a commutative ring and let $a = [(e_0, a_0), \ldots, (e_{s-1}, a_{s-1})]$ and $b = [(f_0, b_0), \ldots, (f_{t-1}, b_{t-1})]$ be lists that meet invariant (S): the exponents increase strictly and no coefficient is zero. The product is

$$\operatorname{val}(a) \operatorname{val}(b) = \sum_{i < s} \sum_{j < t} a_i b_j\, x^{e_i + f_j} .$$

Call $(i, j)$ a *pair* and $k(i, j) = e_i + f_j$ its *key*. If $s = 0$ or $t = 0$, the product is $0$ and line L1 returns the empty list, which is the list of $0$. Assume now $s, t \ge 1$.

**Claim 1. The heap holds at most one pair from each row.** Line L2 puts the pair $(i, 0)$ for each row $i$. Line L9 pushes $(i, j + 1)$ only right after it pops $(i, j)$. So by induction, at each test of line L4 the heap holds, for each row $i$, either nothing or the single pair $(i, j_i)$, where $j_i$ is the number of pairs of row $i$ already popped. In particular the heap never has more than $s$ entries.

**Claim 2. Every pair is popped exactly once.** By Claim 1, the pairs of row $i$ are popped in the order $(i, 0), (i, 1), \ldots$, and after $(i, j)$ is popped the pair $(i, j + 1)$ is pushed if $j + 1 < t$. So all $t$ pairs of row $i$ are popped, each once, and then the row adds nothing more. The loop stops when the heap is empty, that is after all $s t$ pairs are popped.

**Claim 3. The keys are popped in nondecreasing order.** Suppose line L5 pops a pair with key $k$. Every pair still in the heap has a key at least $k$, because the heap returns a minimum. Every pair $(i, j')$ that is pushed later comes after the pair $(i, j_i)$ that is now in the heap or was just popped, with $j' > j_i$, so $k(i, j') = e_i + f_{j'} > e_i + f_{j_i} \ge k$, because $f_0 < f_1 < \cdots$. So all later pops have keys at least $k$.

**Claim 4. Before the final filter, $c$ lists, for each key value $k$ that occurs, one pair $(k, \sum_{k(i,j) = k} a_i b_j)$, in increasing order of $k$.** By Claim 3, the pairs with the same key are popped one after the other, with no other key between them. Lines L7 and L8 start a new term when the key differs from the last exponent of $c$, and add the product to the last term when it is the same. So each block of equal keys gives one term, whose coefficient is the sum of the products $a_i b_j$ of the block, and by Claim 2 each product is counted once. The exponents of $c$ increase strictly, because the keys do not decrease and a new term starts only when the key changes.

**Conclusion.** By Claim 4, $\sum_{(k, v) \in c} v x^k$ equals the double sum above, which is $\operatorname{val}(a) \operatorname{val}(b)$. The terms of $c$ have strictly increasing exponents. Line L10 deletes the terms whose coefficient is $0$: they contribute nothing to the sum, and the deletion keeps the order. So the result is the list of nonzero terms of the product in increasing order of exponent, which is the only list that meets (S) for that polynomial. $\blacksquare$

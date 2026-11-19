---
title: Cached decoding gives the same logits as recomputation
proves: [correctness]
status: full
---

We use the notation of the page and the toy network of DECODE-STEP. Tokens $t_0, t_1, \ldots$ sit at positions $0, 1, \ldots$. Let $x^{(0)}_i = \text{embedding}(t_i) + \text{position}(i)$, and for layers $l = 1 \ldots L$ let the full forward pass compute, for every position $i$,

$$k^{(l)}_{i,j} = \text{split}(x^{(l-1)}_i W_K)_j, \quad v^{(l)}_{i,j} = \text{split}(x^{(l-1)}_i W_V)_j, \quad q^{(l)}_{i,m} = \text{split}(x^{(l-1)}_i W_Q)_m,$$

$$a^{(l)}_{i,m} = \text{attention}\big(q^{(l)}_{i,m}, (k^{(l)}_{s,j})_{s \le i}, (v^{(l)}_{s,j})_{s \le i}\big) \text{ with } j = \text{the group of } m,$$

$$y^{(l)}_i = x^{(l-1)}_i + \text{concat}(a^{(l)}_{i,1} \ldots a^{(l)}_{i,h}) W_O, \qquad x^{(l)}_i = y^{(l)}_i + \text{FFN}(y^{(l)}_i),$$

with the weights of layer $l$, and the logits $x^{(L)}_i E^T$. The causal mask is the condition $s \le i$. We assume exact arithmetic.

**Lemma 1 (dependence on the prefix).** For every layer $l$ and position $i$, the vectors $x^{(l)}_i$, $k^{(l+1)}_{i,j}$ and $v^{(l+1)}_{i,j}$ are functions of $t_0 \ldots t_i$ alone.

*Proof.* By induction on $l$. For $l = 0$, $x^{(0)}_i$ depends on $t_i$ and $i$ only. Suppose the claim holds for $l - 1$. Then $q^{(l)}_{i,m}$, $k^{(l)}_{s,j}$ and $v^{(l)}_{s,j}$ for $s \le i$ are functions of $t_0 \ldots t_s$, hence of $t_0 \ldots t_i$. The attention at position $i$ reads only positions $s \le i$, so $a^{(l)}_{i,m}$, $y^{(l)}_i$ and $x^{(l)}_i$ are functions of $t_0 \ldots t_i$. The keys and values of layer $l + 1$ are linear maps of $x^{(l)}_i$. $\square$

So appending tokens after position $i$ never changes the keys and values of position $i$; they can be computed once and kept.

**Theorem 2 (cached decoding is exact).** Call DECODE-STEP on $t_0, t_1, \ldots, t_n$ in order, at positions $0, 1, \ldots, n$, starting from an empty cache. Then, after the call for position $i$, the cache of layer $l$ and head $j$ holds exactly $k^{(l)}_{0,j} \ldots k^{(l)}_{i,j}$ and $v^{(l)}_{0,j} \ldots v^{(l)}_{i,j}$ in order, and the call returns $x^{(L)}_i E^T$.

*Proof.* By induction on $i$, and inside one call by induction on the layer. Assume that before the call for position $i$ each layer's cache holds the keys and values of positions $0 \ldots i - 1$ (true for $i = 0$, where the cache is empty). In the call, line L1 sets $x = x^{(0)}_i$. Suppose that at the start of the pass for layer $l$ we have $x = x^{(l-1)}_i$. Line L3 computes $q^{(l)}_{i,m}$, $k^{(l)}_{i,j}$ and $v^{(l)}_{i,j}$ from it, and line L4 appends the last two, so the cache of layer $l$ now holds positions $0 \ldots i$. Line L5 attends with $q^{(l)}_{i,m}$ over exactly the keys and values of positions $s \le i$ of the group of $m$, which is $a^{(l)}_{i,m}$. Lines L6 and L7 then give $y^{(l)}_i$ and $x^{(l)}_i$. After the last layer, line L8 returns $x^{(L)}_i E^T$. The stored entries of positions $s < i$ were computed in earlier calls from $x^{(l-1)}_s$ of those calls, which by the induction hypothesis equal the full pass values; by Lemma 1 these do not depend on the tokens after $s$, so they are the values of the full forward pass on $t_0 \ldots t_n$ as well. $\square$

**Corollary 3 (greedy generation).** Greedy generation with the cache emits the same tokens as greedy generation that recomputes the full forward pass at every step, when both break ties the same way.

*Proof.* By Theorem 2 the logits at each step are equal, so the argmax is equal; the next token is then the same, and induction on the steps gives the claim. $\square$

**Lemma 4 (the paged cache).** Let the block table of a sequence hold distinct physical blocks $B_0, B_1, \ldots$, and store position $p$ of a layer in slot $p \bmod b$ of block $B_{\lfloor p / b \rfloor}$. Then reading the positions $0 \ldots n - 1$ through the table returns the entries in the order they were appended, and two live sequences never share a slot.

*Proof.* The map $p \mapsto (\lfloor p / b \rfloor, p \bmod b)$ is a bijection from the positions to pairs (block index, slot), with inverse $(c, r) \mapsto c b + r$. The table maps block indices to distinct physical blocks, and a block taken from the free list belongs to no live sequence, since a block returns to the free list only on release. So each position has its own slot, and a read of position $p$ returns what was written for $p$. $\square$

With Lemma 4, Theorem 2 holds for the paged cache too, since DECODE-STEP only appends and reads keys and values in position order.

**Counting.** With the cache, the call for position $i$ (counting from 1) computes $i$ scores per query head and layer, so $n$ positions cost $\sum_{i=1}^{n} i = n(n+1)/2$ per head and layer. Without the cache, step $m$ recomputes positions $1 \ldots m$, which costs $m(m+1)/2$, and $\sum_{m=1}^{n} m(m+1)/2 = n(n+1)(n+2)/6$. For $n = 4$ these are 10 and 20.

**Floating point.** The cached pass and the full pass compute each entry by the same operations on the same inputs, so in the code, which sums with math.fsum in a fixed order, they agree; a system that batches the full pass differently may round differently, and its results then agree only to within rounding.

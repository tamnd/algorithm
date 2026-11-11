---
title: The bitonic network counts
proves: [correctness, complexity]
status: full
---

This proof follows the construction on the main page (L1 to L8) and the token code (L9 to L14), in the model of that page: an atomic TOGGLE per balancer, an atomic fetch-and-add per output, and asynchronous processes. It proves that Bitonic$[w]$ has the step property in every quiescent state, that its depth is $m(m+1)/2$ for $w = 2^m$, and that each call takes exactly that many steps plus one. That the step property gives a quiescently consistent counter is proved on the counting network page.

## Step sequences

A sequence $y_0, \ldots, y_{k-1}$ of natural numbers has the *step property* if $0 \le y_i - y_j \le 1$ for all $i < j$.

**Lemma 1.** For every $s \ge 0$ there is exactly one sequence of length $k$ with the step property and sum $s$, namely $\mathrm{step}_k(s)_i = \lceil (s - i)/k \rceil$. If $s = qk + r$ with $0 \le r < k$, it is $q + 1$ at positions $0, \ldots, r - 1$ and $q$ at positions $r, \ldots, k - 1$.

*Proof.* Let $y$ have the step property. All entries lie in $\{y_{k-1}, y_{k-1} + 1\}$, and the larger value comes first. So $y$ is $q' + 1$ at the first $r'$ positions and $q'$ after, for some $q'$ and $0 \le r' < k$, and its sum is $q'k + r'$. Division with remainder fixes $q' = q$ and $r' = r$. The formula gives the same sequence: $\lceil (qk + r - i)/k \rceil = q + \lceil (r - i)/k \rceil$, which is $q + 1$ for $i < r$ and $q$ for $r \le i < k$. ∎

**Lemma 2.** For $k$ even and $y$ with the step property, $\Sigma y^{\mathrm{even}} = \lceil \Sigma y / 2 \rceil$, $\Sigma y^{\mathrm{odd}} = \lfloor \Sigma y / 2 \rfloor$, and $y^{\mathrm{even}}$ and $y^{\mathrm{odd}}$ have the step property.

*Proof.* By Lemma 1, $y$ changes value at most once, from $q + 1$ to $q$. In each pair $(y_{2i}, y_{2i+1})$ the difference is 0 or 1, and it is 1 in at most one pair (the one that contains the change, if the change falls inside a pair). So $\Sigma y^{\mathrm{even}} - \Sigma y^{\mathrm{odd}} \in \{0, 1\}$, and since the two sums add up to $\Sigma y$ they are the ceiling and the floor of half of it. Any subsequence of $y$ keeps $0 \le y_i - y_j \le 1$ for $i < j$. ∎

**Lemma 3.** For $s \ge 0$, $\mathrm{step}_k(s + 1)$ is $\mathrm{step}_k(s)$ with the entry at position $s \bmod k$ raised by 1.

*Proof.* With $s = qk + r$, $s + 1$ is $qk + (r + 1)$ if $r + 1 < k$, which by Lemma 1 adds one $q + 1$ at position $r$; if $r + 1 = k$ it is $(q + 1)k$, all entries $q + 1$, which again raises only position $r = k - 1$. ∎

## Balancers in a quiescent state

**Lemma 4.** In any state, a balancer on which $t$ TOGGLE steps have been done has sent $\lceil t/2 \rceil$ tokens to its first wire and $\lfloor t/2 \rfloor$ to its second. In a quiescent state, $t$ is the number of tokens on its two input wires, so every wire count is a function of the input counts.

*Proof.* The toggle starts at 0 and the $i$-th TOGGLE returns $i \bmod 2$ (L11), and L12 sends the token to the first wire when that is 0. In a quiescent state every token that reached an input wire of a balancer has also passed it. Induction over the layers gives the second claim. ∎

From here on, all counts are taken in a quiescent state, and a network is identified with the map from input counts to output counts that Lemma 4 gives.

## The merger

**Theorem 1.** Let $k$ be a power of 2 and let $x$ and $x'$, each of length $k$, have the step property. Then the outputs $y_0, \ldots, y_{2k-1}$ of Merger$[2k]$ on $(x, x')$ have the step property, and $\Sigma y = \Sigma x + \Sigma x'$.

*Proof.* Balancers keep tokens, so the sums agree. The step property is by induction on $k$.

*Base, $k = 1$.* The merger is one balancer (L4) with $t = x_0 + x'_0$ tokens; its outputs are $\lceil t/2 \rceil \ge \lfloor t/2 \rfloor$, which differ by at most 1.

*Step, $k \ge 2$.* Then $k$ is even. The first Merger$[k]$ (L5) gets $x^{\mathrm{even}}$ and $x'^{\mathrm{odd}}$; both have length $k/2$ and the step property by Lemma 2. By the induction hypothesis its output $z$ has the step property, and
$$\Sigma z = \lceil \Sigma x / 2 \rceil + \lfloor \Sigma x' / 2 \rfloor.$$
The second Merger$[k]$ (L6) gets $x^{\mathrm{odd}}$ and $x'^{\mathrm{even}}$, so its output $z'$ has the step property and
$$\Sigma z' = \lfloor \Sigma x / 2 \rfloor + \lceil \Sigma x' / 2 \rceil.$$
Each of $\lceil \Sigma x/2 \rceil - \lfloor \Sigma x/2 \rfloor$ and $\lceil \Sigma x'/2 \rceil - \lfloor \Sigma x'/2 \rfloor$ is 0 or 1, so $\Sigma z - \Sigma z' \in \{-1, 0, 1\}$.

The last layer (L7) has balancer $i$ on $z_i$ and $z'_i$, with outputs $y_{2i}$ (first) and $y_{2i+1}$ (second) (L8). It gets $z_i + z'_i$ tokens.

- If $\Sigma z = \Sigma z'$, then $z = z'$ by Lemma 1. Balancer $i$ gets $2z_i$ and sends $z_i$ to each output, so $y = (z_0, z_0, z_1, z_1, \ldots)$. For $a < b$, $y_a = z_{\lfloor a/2 \rfloor}$ and $y_b = z_{\lfloor b/2 \rfloor}$ with $\lfloor a/2 \rfloor \le \lfloor b/2 \rfloor$, so $0 \le y_a - y_b \le 1$ by the step property of $z$.
- Otherwise let $u$ be the one of $z, z'$ with the smaller sum $s = qk + r$, $0 \le r < k$. By Lemma 3 the other one is $u$ with position $r$ raised by 1. For $i \ne r$, balancer $i$ gets $2u_i$ and sends $u_i$ to each output. Balancer $r$ gets $2u_r + 1 = 2q + 1$ (Lemma 1 gives $u_r = q$) and sends $q + 1$ to $y_{2r}$ and $q$ to $y_{2r+1}$. By Lemma 1, $u_i = q + 1$ for $i < r$ and $u_i = q$ for $i > r$. So $y_a = q + 1$ for $a \le 2r$ and $y_a = q$ for $a > 2r$, which has the step property. ∎

The precondition matters: Merger$[4]$ on $x = (0, 0)$, $x' = (0, 2)$ gives $(1, 0, 1, 0)$.

## The bitonic network

**Theorem 2.** For every $m \ge 0$, Bitonic$[2^m]$ has the step property in every quiescent state, for every vector of input counts.

*Proof.* By induction on $m$. Bitonic$[1]$ is one wire (L1), and a sequence of length 1 has the step property. For $w = 2k$ (L2, L3), the two copies of Bitonic$[k]$ are on disjoint wires. In a quiescent state of the whole network, by Lemma 4, the counts on the outputs of each copy are the counts that the copy alone would give for its inputs, and by the induction hypothesis they have the step property. These are the inputs $x$ and $x'$ of Merger$[2k]$, so Theorem 1 gives the step property at the outputs. ∎

With the counting network page, Theorem 2 gives a counter whose values in a quiescent state after $n$ calls are exactly $0, \ldots, n - 1$, and which is quiescently consistent.

## Depth and steps

**Theorem 3.** Merger$[2k]$ has depth $\log_2(2k)$, Bitonic$[2^m]$ has depth $D(2^m) = m(m+1)/2$, each layer of Bitonic$[2^m]$ is a perfect matching of its $2^m$ wires, and the network has $2^{m-1} \cdot m(m+1)/2$ balancers.

*Proof.* Merger$[2]$ is one layer. Merger$[2k]$ is two Merger$[k]$ on disjoint wires, which by induction have the same depth $\log_2 k$ and perfect matchings in each layer, so side by side they form $\log_2 k$ perfect matchings of the $2k$ wires; then L7 adds one more perfect matching. So the depth is $\log_2 k + 1 = \log_2(2k)$. Bitonic$[2k]$ is two Bitonic$[k]$ on disjoint wires, of equal depth by induction and with perfect matchings, followed by Merger$[2k]$; so $D(2k) = D(k) + \log_2(2k)$ with $D(1) = 0$, and $D(2^m) = 1 + 2 + \cdots + m = m(m+1)/2$. A perfect matching of $w$ wires has $w/2$ balancers, which gives the count. ∎

**Theorem 4 (wait-free).** Each call of GET-AND-INCREMENT ends after exactly $D(w) + 1$ of its own steps, whatever the other processes do.

*Proof.* By Theorem 3, every wire has exactly one balancer in each layer, so the loop L10 to L12 does exactly $D(w)$ TOGGLE steps, each a single atomic step that cannot fail. L13 is one fetch-and-add. Nothing in the code waits for another process or retries. ∎

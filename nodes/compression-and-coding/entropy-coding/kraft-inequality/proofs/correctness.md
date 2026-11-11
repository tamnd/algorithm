---
title: The Kraft inequality, its converse, and McMillan's theorem
proves: [statement]
status: full
---

We use the notation of the page. The code alphabet is $\{0, 1, \ldots, D - 1\}$ with $D \ge 2$. A code is a list of codewords $w_1, \ldots, w_m$ with lengths $\ell_1, \ldots, \ell_m \ge 1$, and its Kraft sum is $K = \sum_{i=1}^{m} D^{-\ell_i}$. For a string $w = a_1 \cdots a_\ell$ we define the number $0.w = \sum_{t=1}^{\ell} a_t D^{-t}$ and the interval $I(w) = [0.w, \, 0.w + D^{-\ell})$, a subinterval of $[0, 1)$ of length $D^{-\ell}$.

**Lemma 1.** Let $|u| \le |v|$. Then $u$ is a prefix of $v$ if and only if $I(v) \subseteq I(u)$. If $u$ is not a prefix of $v$, then $I(u)$ and $I(v)$ are disjoint.

*Proof.* The intervals $I(w)$ for the $D^\ell$ strings $w$ of a fixed length $\ell$ are the $D^\ell$ intervals $[j D^{-\ell}, (j+1) D^{-\ell})$, and they cut $[0, 1)$ into disjoint parts. A string $v$ of length $\ell' \ge \ell$ has its interval inside exactly one of them, the one of its first $\ell$ digits $v_{1..\ell}$, since $0.v_{1..\ell} \le 0.v < 0.v_{1..\ell} + D^{-\ell}$. So $I(v) \subseteq I(u)$ if $u = v_{1..\ell}$, and $I(v) \cap I(u) = \emptyset$ if $u \ne v_{1..\ell}$, because then $I(u)$ and $I(v_{1..\ell})$ are two different parts of the same cut. $\square$

**Part (a): a prefix code has $K \le 1$.** Let the code be prefix-free. For $i \ne j$, neither codeword is a prefix of the other, so by Lemma 1 the intervals $I(w_i)$ and $I(w_j)$ are disjoint. They all lie in $[0, 1)$, so the sum of their lengths is at most 1: $K = \sum_i D^{-\ell_i} \le 1$. $\square$

(The same proof in the language of trees: let $L = \max_i \ell_i$. The codeword $w_i$ has $D^{L - \ell_i}$ descendants at depth $L$ in the complete $D$-ary tree. No codeword is an ancestor of another, so these sets of descendants are disjoint, and $\sum_i D^{L - \ell_i} \le D^L$.)

**Part (b): the converse.** Let $\ell_1, \ldots, \ell_m$ be positive integers with $K \le 1$. Renumber them so that $\ell_1 \le \ell_2 \le \cdots \le \ell_m$. Let

$$c_i = \sum_{j < i} D^{-\ell_j}, \qquad i = 1, \ldots, m,$$

so $c_1 = 0$. Each term $D^{-\ell_j}$ with $j < i$ is an integer multiple of $D^{-\ell_i}$, because $\ell_j \le \ell_i$. So $c_i$ is a multiple of $D^{-\ell_i}$. Also $c_i + D^{-\ell_i} = \sum_{j \le i} D^{-\ell_j} \le K \le 1$, so $c_i < 1$. Hence $c_i = 0.w_i$ for exactly one string $w_i$ of length $\ell_i$: the first $\ell_i$ digits of $c_i$ in base $D$. Then $I(w_i) = [c_i, c_i + D^{-\ell_i})$.

For $i < j$, $c_j \ge c_i + D^{-\ell_i}$, so the intervals $I(w_i)$ and $I(w_j)$ are disjoint. In particular $I(w_j) \not\subseteq I(w_i)$, and since $\ell_i \le \ell_j$, Lemma 1 says that $w_i$ is not a prefix of $w_j$. A longer word is never a prefix of a shorter one, and two words of the same length that are prefixes of each other are equal, which disjoint intervals rule out. So no codeword is a prefix of another, and $w_1, \ldots, w_m$ is a prefix code with the given lengths. $\square$

This is the construction of the canonical code: each codeword is the previous one plus 1, padded on the right with zeros to the new length.

**Part (c): McMillan's theorem.** Let the code be uniquely decodable: no two different finite sequences of codewords have the same concatenation. Let $L = \max_i \ell_i$ and let $k \ge 1$. Expand the $k$-th power of $K$:

$$K^k = \left(\sum_{i=1}^{m} D^{-\ell_i}\right)^k = \sum_{i_1, \ldots, i_k} D^{-(\ell_{i_1} + \cdots + \ell_{i_k})} = \sum_{n = k}^{kL} a_n D^{-n},$$

where $a_n$ is the number of sequences $(i_1, \ldots, i_k)$ for which the concatenation $w_{i_1} \cdots w_{i_k}$ has length $n$. Each such sequence gives a string of length $n$, and by unique decodability different sequences give different strings. There are only $D^n$ strings of length $n$, so $a_n \le D^n$. Hence

$$K^k \le \sum_{n = k}^{kL} 1 = k(L - 1) + 1 \le kL.$$

So $K \le (kL)^{1/k}$ for every $k \ge 1$. As $k \to \infty$, $(kL)^{1/k} = e^{(\ln k + \ln L)/k} \to 1$. So $K \le 1$. $\square$

The power is the whole trick. One codeword sequence of length 1 says nothing, because short strings may be parsed in many ways, as long as the parse becomes clear later. But $K > 1$ would make $K^k$ grow exponentially in $k$, while unique decodability allows only a linear number of terms, each at most 1.

**Part (d): countable codes.** Let the code have infinitely many codewords $w_1, w_2, \ldots$.

- If it is prefix-free, every finite part of it is prefix-free, so every partial sum of $K$ is at most 1 by (a), and $K \le 1$.
- If it is uniquely decodable, every finite part of it is uniquely decodable, so every partial sum is at most 1 by (c), and $K \le 1$.
- Conversely, let $\ell_1, \ell_2, \ldots$ be positive integers with $\sum_i D^{-\ell_i} \le 1$. Each value $\ell$ occurs at most $D^\ell$ times, so the list can be sorted in non-decreasing order. Define $c_i$ as in (b). The argument of (b) uses only the codewords before $i$, so it works for each $i$ and gives an infinite prefix code with the given lengths. $\blacksquare$

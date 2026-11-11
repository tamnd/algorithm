---
title: LZ78 encoding gives the LZ78 parse, and decoding inverts it
proves: [correctness]
status: full
---

Let $T = T[1..n]$. Let $w_1, \ldots, w_c$ be the phrases of the [LZ78 parsing](/lz78-parsing/) of $T$, with $w_0 = \varepsilon$: each $w_k$ is $w_j a$, where $w_j$ ($0 \le j < k$) is the longest of $w_0, \ldots, w_{k-1}$ that is a prefix of the rest of $T$, and $a$ is the next symbol; a last phrase may be $w_j$ alone when $T$ ends inside it.

For a trie node $u$, write $\mathrm{str}(u)$ for the string on the path from the root to $u$.

**Lemma 1 (encoder invariant).** At the top of each round of line L3, with $k = next - 1$ pairs written, and $p$ the position after the last written phrase:

1. the trie has the nodes $0, 1, \ldots, k$, and $\mathrm{str}(u) = w_u$ for each $u$;
2. the pairs written so far are those of $w_1, \ldots, w_k$, and $T[1..p-1] = w_1 \cdots w_k$;
3. $p \le i$ and $\mathrm{str}(v) = T[p..i-1]$; in particular $T[p..i-1]$ is one of $w_0, \ldots, w_k$.

*Proof.* At the start, $k = 0$, $p = i = 1$, $v = 0$, and the trie has only the root, so all three hold. Assume they hold at the top of a round.

If line L4 succeeds, line L5 moves $v$ to the child for $T[i]$, so $\mathrm{str}(v) = T[p..i]$, and $i$ grows by 1. Nothing else changes.

If line L4 fails, then $T[p..i]$ is not a node of the trie, so by (1) it is not among $w_0, \ldots, w_k$. The set $\{w_0, \ldots, w_k\}$ is closed under prefixes (each $w_u$ is $w_{u'}$ plus one symbol, with $u' < u$, by induction), so no phrase that is a prefix of $T[p..n]$ is longer than $T[p..i-1]$; and $T[p..i-1] = \mathrm{str}(v)$ is a phrase by (3). So $T[p..i-1]$ is the longest phrase that is a prefix of the rest of $T$, and $w_{k+1} = T[p..i] = w_v T[i]$. Line L7 writes $(v, T[i])$, which is the pair of $w_{k+1}$. Line L8 adds node $k + 1$ under $v$ for $T[i]$, so $\mathrm{str}(k+1) = w_{k+1}$. Line L9 sets $v = 0$, and the new $p$ is $i + 1$, so after $i$ grows, (3) holds with the empty string. $\square$

**Lemma 2 (the end).** After the loop, $i = n + 1$. If $v = 0$ then $p = n + 1$ and all of $T$ is covered. If $v \ne 0$ then $T[p..n] = \mathrm{str}(v) = w_v$ is a nonempty phrase and the input ends inside it, so the last LZ78 phrase is $w_v$ alone; line L10 writes $(v, \bot)$.

*Proof.* Lemma 1(3) with $i = n + 1$. $\square$

So LZ78-ENCODE outputs exactly the pairs of the LZ78 parse of $T$, with $j < k$ in the $k$-th pair.

**Lemma 3 (decoder invariant).** After the decoder has processed $k$ pairs, $P[u] = w_u$ for $0 \le u \le k$, and the output is $w_1 \cdots w_k$.

*Proof.* By induction on $k$; for $k = 0$, $P[0] = \varepsilon$ and the output is empty. The $k$-th pair is $(j, a)$ with $j < k$, so $P[j] = w_j$ is defined. Line L14 forms $w_j a$, or $w_j$ when $a = \bot$, which is $w_k$ by the definition of the pair. Line L15 outputs it and stores it as $P[k]$. $\square$

**Theorem.** LZ78-DECODE(LZ78-ENCODE$(T)$) outputs $T$.

*Proof.* By Lemmas 1 and 2 the encoder writes the $c$ pairs of $w_1, \ldots, w_c$ and $T = w_1 \cdots w_c$. By Lemma 3 with $k = c$ the decoder outputs $w_1 \cdots w_c = T$. $\square$

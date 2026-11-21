---
title: The Bloom filter encoding keeps the shared q-grams, and the linkage returns exactly the pairs at or above the threshold
proves: [correctness]
status: full
---

Fix the keys $K_1, K_2$, the number of hash functions $k \ge 1$, the filter length $m \ge 1$ and the q-gram length $q \ge 1$. Lines L1 to L10 are those of the page. For a string $s$, let $G(s)$ be the set of q-grams of line L2, taken after normalization and padding. For a q-gram $g$, let $h_1(g) = \mathrm{HMAC\text{-}SHA1}_{K_1}(g)$ and $h_2(g) = \mathrm{HMAC\text{-}MD5}_{K_2}(g)$, read as integers, and let

$$\pi(g) = \{ (h_1(g) + i\, h_2(g)) \bmod m : 0 \le i < k \} \subseteq \{0, \ldots, m - 1\}.$$

We identify a Bloom filter with the set of positions of its 1 bits. For a set $S$ of q-grams, write $F(S) = \bigcup_{g \in S} \pi(g)$.

**Lemma 1 (the encoding).** Lines L2 to L5 produce the filter $F(G(s))$, and $|F(G(s))| \le k\, |G(s)|$. If $q \ge 2$ or $s$ is not empty, the filter is not empty.

*Proof.* Line L3 starts with the empty set. Lines L4 and L5 add the positions $\pi(g)$ for each $g \in G(s)$, and nothing else, so at the end the filter is the union $F(G(s))$. The order of the q-grams does not matter, because union is commutative and idempotent. Each $\pi(g)$ has between 1 and $k$ elements, which gives the upper bound. The padded string has length $|s| + 2(q - 1)$, which is at least $q$ if $q \ge 2$ or $|s| \ge 1$, so then $G(s)$ has at least one q-gram and the filter at least one bit. $\square$

**Theorem 1 (equal identifiers).** If two strings have the same normalized form, or more generally the same q-gram set, then their filters are equal, and if the filter is not empty, their Dice coefficient at line L8 is 1.

*Proof.* By Lemma 1 the filter depends only on $G(s)$. For a nonempty filter $A$, $\mathrm{Dice}(A, A) = 2|A| / (2|A|) = 1$. $\square$

**Theorem 2 (shared q-grams give shared bits).** For any two strings $s, t$, $F(G(s) \cap G(t)) \subseteq F(G(s)) \cap F(G(t))$. So the number of common bits is at least $|F(G(s) \cap G(t))|$.

*Proof.* $F$ is monotone: $S \subseteq T$ implies $F(S) \subseteq F(T)$. Apply it to $G(s) \cap G(t) \subseteq G(s)$ and $G(s) \cap G(t) \subseteq G(t)$. $\square$

The converse fails: a position can be in both filters because two different q-grams map to it. This is why the Dice coefficient of the filters is only an estimate of the Dice coefficient of the q-gram sets, and it is never smaller than the value from shared q-grams alone. How close the estimate is depends on $m$, $k$ and the number of q-grams, and it is a measured property.

**Theorem 3 (the linkage).** Line L10 returns exactly the pairs $(a, b) \in A \times B$ with $\mathrm{Dice}(F_a, F_b) \ge \theta$, each with its coefficient, in the order of line L7.

*Proof.* Line L1 computes the filter of every record by Lemma 1. Line L7 visits each pair once. Line L8 computes $\mathrm{Dice}(F_a, F_b) = 2 |F_a \cap F_b| / (|F_a| + |F_b|)$ exactly, with rational arithmetic in the implementation. Line L9 appends the pair if and only if the value is at least $\theta$. Nothing else changes $M$. $\square$

**Theorem 4 (what the keys give).** Assume that $h_1$ and $h_2$ under the secret keys are pseudorandom functions. Then, to a party without the keys, the map $g \mapsto \pi(g)$ is indistinguishable from a map that draws two independent uniform integers for each q-gram and applies the same double hashing. In particular, such a party cannot compute the filter of a guessed identifier and compare it with a given filter.

*Proof sketch.* A distinguisher between the two maps that makes queries on q-grams gives a distinguisher between the HMAC outputs and random functions with the same advantage, because $\pi$ is computed from $h_1$ and $h_2$ by a fixed public map. $\blacksquare$

**Remark.** Theorem 4 is about guessing single identifiers. It does not say that the filters hide the identifiers. The encoding is deterministic, so the same q-gram always sets the same bits, and the frequencies of bit patterns over many records follow the frequencies of q-grams in the population. The published attacks on Bloom filter encodings use this, as the survey of Vidanage, Ranbaduge, Christen and Schnell (2022) describes. This is why the page lists hardening methods, and why the keys alone are not a privacy guarantee.

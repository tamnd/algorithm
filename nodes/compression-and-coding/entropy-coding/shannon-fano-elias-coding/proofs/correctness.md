---
title: Correctness of Shannon-Fano-Elias coding
proves: [correctness]
status: full
---

We prove that the code is prefix-free for any order of the symbols, that the codewords are in the order of the symbols, and that $H + 1 \le L < H + 2$.

**Setup.** The symbols $1, \ldots, n$ have probabilities $p_i > 0$ with sum 1, in any order. Let $F_i = \sum_{j < i} p_j$, so symbol $i$ owns the interval $I_i = [F_i, F_i + p_i)$, and these intervals are disjoint and cover $[0, 1)$. Let $\bar F_i = F_i + p_i / 2$ be the midpoint of $I_i$ and $l_i = \lceil \log_2 (1/p_i) \rceil + 1$. The codeword $c_i$ is the first $l_i$ bits after the binary point of $\bar F_i$. Write $t_i$ for the number $0.c_i$ in binary, the truncation of $\bar F_i$ to $l_i$ bits. The set of numbers in $[0, 1)$ whose binary expansion starts with $c_i$ is the interval $J_i = [t_i, t_i + 2^{-l_i})$.

**Lemma 1.** $J_i \subseteq I_i$.

*Proof.* From $l_i - 1 \ge \log_2 (1/p_i)$ we get $2^{-l_i} \le p_i / 2$. Truncation to $l_i$ bits gives $\bar F_i - 2^{-l_i} < t_i \le \bar F_i$. So $t_i > \bar F_i - p_i / 2 = F_i$, and $t_i + 2^{-l_i} \le \bar F_i + p_i / 2 = F_i + p_i$. $\square$

**Lemma 2.** If one binary word $a$ is a prefix of another word $b$, then the interval of numbers starting with $b$ is inside the interval of numbers starting with $a$.

*Proof.* Every number whose expansion starts with $b$ also starts with $a$. $\square$

**Theorem 1 (prefix-free).** No codeword is a prefix of another.

*Proof.* Suppose $c_i$ is a prefix of $c_j$ with $i \ne j$. By Lemma 2, $J_j \subseteq J_i$, and $J_j$ is not empty. By Lemma 1, $J_i \subseteq I_i$ and $J_j \subseteq I_j$, so $I_i \cap I_j \ne \emptyset$. This is false, since the intervals of different symbols are disjoint. $\square$

The proof does not use any order of the probabilities. This is the role of the extra bit: Shannon's code uses $\lceil \log_2 (1/p_i) \rceil$ bits of the start $F_i$, and needs the symbols sorted by non-increasing probability to keep the words apart.

**Theorem 2 (order).** If $i < j$ then $c_i$ comes before $c_j$ in lexicographic order.

*Proof.* By Lemma 1, $J_i \subseteq I_i$ and $J_j \subseteq I_j$, and $I_i$ lies wholly to the left of $I_j$. So every number that starts with $c_i$ is smaller than every number that starts with $c_j$. Neither word is a prefix of the other (Theorem 1), so they differ at a first position, and there $c_i$ has the bit 0 and $c_j$ the bit 1. $\square$

**Theorem 3 (length).** $H + 1 \le L < H + 2$, where $L = \sum_i p_i l_i$ and $H = \sum_i p_i \log_2 (1/p_i)$.

*Proof.* From $\log_2 (1/p_i) + 1 \le l_i < \log_2 (1/p_i) + 2$, multiply by $p_i$ and add. $\square$

**Blocks.** Apply the same rule to the $\sigma^k$ blocks of $k$ symbols from a memoryless source, in lexicographic order. The interval of a block $x_1 \cdots x_k$ is found by starting from $[0, 1)$ and, for each symbol, keeping the part of the current interval that the symbol owns in proportion to its probability. Its width is $p(x_1) \cdots p(x_k)$, and the blocks' intervals are disjoint and cover $[0, 1)$, so Theorems 1 and 3 apply to the block alphabet. The entropy of a block is $k H$, so the mean length per symbol is below $H + 2/k$. The decoder can find the block from the number $t$ alone, because $t$ lies in the interval of the block (Lemma 1), and the nested intervals tell each symbol in turn. $\square$

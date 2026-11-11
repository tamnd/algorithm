---
title: Correctness of Shannon-Fano coding
proves: [correctness]
status: full
---

We prove that both forms give prefix codes, and that Shannon's form has expected length $L$ with $H \le L < H + 1$. We also show by an example that Fano's form is not always optimal.

**Fano's method gives a prefix code.** Each call of FANO with $m \ge 2$ symbols chooses $1 \le k < m$, so both parts are non-empty and smaller than the list, and the recursion ends. The calls form a binary tree: the call for a list is an inner node, its two subcalls are its children reached by the bits 0 and 1, and a call with one symbol is a leaf. The codeword of a symbol is the sequence of bits on the path from the root to its leaf. Two different leaves of a tree are never on one root path, so no codeword is a prefix of another. Each inner node has two children, so the tree is full and $\sum_i 2^{-l_i} = 1$. $\square$

**Shannon's method gives a prefix code.** Sort the symbols so that $p_1 \ge p_2 \ge \cdots \ge p_n > 0$, let $P_i = \sum_{j < i} p_j$, and let $l_i = \lceil \log_2 (1/p_i) \rceil$, so that $2^{-l_i} \le p_i$. The codeword $c_i$ is the first $l_i$ bits after the binary point of $P_i$. Take $i < j$. Then $l_i \le l_j$, because $p_i \ge p_j$. Also
$$ P_j - P_i = p_i + \cdots + p_{j-1} \ge p_i \ge 2^{-l_i}. $$
If $c_i$ were a prefix of $c_j$, then $P_i$ and $P_j$ would have the same first $l_i$ bits, so both would lie in one interval $[a, a + 2^{-l_i})$, and $P_j - P_i < 2^{-l_i}$, a contradiction. A longer codeword can not be a prefix of a shorter one, and two codewords of equal length are prefixes of each other only if they are equal, which the same argument excludes. So the code is prefix-free. $\square$

**Bounds for Shannon's method.** From $\log_2 (1/p_i) \le l_i < \log_2 (1/p_i) + 1$, multiplying by $p_i$ and summing gives $H \le L < H + 1$, where $H = \sum_i p_i \log_2 (1/p_i)$. The lower bound $L \ge H$ holds for every prefix code, by the Kraft inequality and Gibbs' inequality: $H - L = \sum_i p_i \log_2 (2^{-l_i} / p_i) \le \log_2 \sum_i 2^{-l_i} \le 0$ by Jensen's inequality. $\square$

**Fano's method is not always optimal.** Take the weights 15, 7, 6, 6, 5, with sum 39. The first split puts $\{15, 7\}$ against $\{6, 6, 5\}$, a difference of 5, which is better than $\{15\}$ against the rest, a difference of 9. The lengths are then 2, 2, 2, 3, 3, with cost $30 + 14 + 12 + 18 + 15 = 89$. Huffman's algorithm merges 5 and 6, then 6 and 7, then 11 and 13, and gives the lengths 1, 3, 3, 3, 3 with cost $15 + 3 \cdot 24 = 87$. Since Huffman codes are optimal, Fano's code is not. $\square$

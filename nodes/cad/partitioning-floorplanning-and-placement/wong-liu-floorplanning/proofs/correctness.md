---
title: The moves of Wong-Liu floorplanning keep the word normalized, and the search returns a valid slicing floorplan
proves: [correctness, termination]
status: full
---

We use the pseudocode and the conventions of the page. Let $E = e_1 \cdots e_{2n-1}$ be a normalized Polish expression: each block occurs one time, every prefix has more operands than operators (the balloting property), and no two equal operators are next to each other. By the [normalized Polish expression](/normalized-polish-expression/) page, these three conditions are exactly the words of the skewed slicing trees. Let $N_k$ be the number of operators in $e_1 \cdots e_k$.

**Lemma 1 (M1).** Swapping two operands that are next to each other in the operand order gives a normalized expression.

*Proof.* The positions of the operators and the operators themselves do not change. So the number of operators in each prefix, the number of operands in each prefix and every pair of neighbouring operators stay the same. The set of operands stays the same. $\square$

**Lemma 2 (M2).** Complementing one chain, a maximal run $e_s \cdots e_t$ of operators, gives a normalized expression.

*Proof.* The token types at each position do not change, so the balloting property holds. Inside the chain the operators alternate, because $E$ is normalized, and they still alternate after each one is complemented. The tokens just before $e_s$ and just after $e_t$ are operands or the ends of the word, by maximality, so no new pair of neighbouring operators appears. $\square$

**Lemma 3 (M3).** Let $e_i$ and $e_{i+1}$ be an operand and an operator, in either order, and let $E'$ be $E$ with the two swapped. Then $E'$ is normalized if and only if:

- if $e_i$ is the operand: $2 (N_{i-1} + 1) < i$ and $e_{i-1} \ne e_{i+1}$ (when $i > 1$);
- if $e_i$ is the operator: $e_{i+2} \ne e_i$ (when $i + 2 \le 2n - 1$).

The implementation tests this in $O(1)$ time with the prefix counts, with indices from 0.

*Proof.* Only the prefix of length $i$ changes its counts. In the first case, the prefix $e'_1 \cdots e'_i$ has $N_{i-1} + 1$ operators and $i - N_{i-1} - 1$ operands, and the balloting property for it is $i - N_{i-1} - 1 > N_{i-1} + 1$, which is the condition. The operator now has the neighbours $e_{i-1}$ and the operand $e_i$, so the only new pair of operators that can appear is $e_{i-1} e_{i+1}$. In the second case the prefix of length $i$ gains an operand and loses an operator, so the balloting property can only get easier. The operator now has the neighbours $e_{i+1}$, an operand, and $e_{i+2}$, so the only new pair is $e_i e_{i+2}$. All other prefixes have the same counts, and all other neighbours are the same. $\square$

**Theorem 1 (every state is a slicing floorplan).** Every word that the search visits is a normalized Polish expression of the $n$ blocks. Its cost is computed exactly, and the returned word is a visited word of least cost. If the cost is the area, the returned area is at least the least area of a slicing floorplan of the blocks, which is at least the sum of the block areas.

*Proof.* Line L1 starts with $1\,2\,V\,3\,V \cdots n\,V$, which is normalized: every operator follows an operand, and the prefix counts are $1, 2, 1, 2, 1, \ldots$. Line L6 applies M1, M2 or a checked M3, so by Lemmas 1 to 3 and induction every visited word is normalized. The cost of a word is the least area over the allowed shapes of the blocks, computed by [Stockmeyer's floorplan sizing](/stockmeyer-floorplan-sizing/), which is exact, plus $\lambda$ times the wire length of the placement that the sizing returns, computed with fractions. Line L10 keeps the best word seen. Each visited word is a slicing floorplan of the blocks, so its area is at least the least area of all slicing floorplans. The blocks do not overlap in a realization (see the normalized Polish expression page), so the area of the floorplan is at least the sum of the block areas. $\square$

**Theorem 2 (termination).** The search stops after at most $\min(s_{\max}, s_\varepsilon) \cdot (2N + 1)$ moves, where $N = k n$, $s_{\max}$ is the limit on the number of temperatures, and $s_\varepsilon = \lceil \log(\varepsilon / T_0) / \log r \rceil + 1$ for $0 < r < 1$ and $T_0 > \varepsilon$.

*Proof.* The inner loop of lines L5 to L12 counts its tries and stops when $tries > 2N$, so it runs at most $2N + 1$ times. Line L13 multiplies $T$ by $r$, so after $s$ temperatures $T = r^s T_0$, which is below $\varepsilon$ once $s \ge \log(\varepsilon / T_0) / \log r$, and line L14 then stops the outer loop. The implementation also stops after $s_{\max}$ temperatures. $\square$

**What is not proved here.** Wong and Liu prove that the three moves connect all normalized Polish expressions of $n$ blocks, so the search can reach the optimum slicing floorplan from any start. The tests check this by a breadth-first search over all normalized words for $n \le 5$. The search is a heuristic with the geometric schedule: there is no bound on the gap between the returned cost and the optimum. The convergence theorems for [simulated annealing](/simulated-annealing/) need a logarithmic schedule that is far too slow for practice. $\blacksquare$

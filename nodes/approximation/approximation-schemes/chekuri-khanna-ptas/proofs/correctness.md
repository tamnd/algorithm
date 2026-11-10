---
title: The guessing step of the Chekuri and Khanna PTAS finds a packable set of profit at least (1 − ε)·OPT among few candidates
proves: [correctness, time.worst]
status: sketch
---

We use the names of the pseudocode. The proof of the guessing step (Lemmas 1 to 6 and the theorem) is full, and it is the proof for the code on this page, where PACK is an exact search. The polynomial packing step of the paper is only sketched at the end, and this is why the status of the page is sketch.

The input has items with positive integer sizes $s_i$ and profits $p_i$, knapsacks with capacities $c_1, \ldots, c_m$, and $0 < \varepsilon \le 1$. Line L2 sets $\delta = \varepsilon / 3$, so $0 < \delta \le 1/3$. For a set $X$ of items we write $p(X) = \sum_{i \in X} p_i$ and $a(X) = \sum_{i \in X} a_i$. Let $\mathrm{OPT}$ be the optimum.

**Step 0 (the removed items).** An item larger than every capacity is in no feasible packing, so line L1 does not change $\mathrm{OPT}$. If no item is left, the empty packing is optimal. From here on $n \ge 1$ items are left, and $p_{\max}$ is their largest profit. The item with profit $p_{\max}$ fits alone in some knapsack, so $p_{\max} \le \mathrm{OPT}$. Each packing holds at most $n$ items, so $\mathrm{OPT} \le n \, p_{\max}$.

**Lemma 1 (the grid of guesses).** There is exactly one $j \in \{0, \ldots, J\}$ with $O \le \mathrm{OPT} < (1 + \delta) O$, where $O = p_{\max} (1 + \delta)^j$.

*Proof.* The intervals $[p_{\max}(1 + \delta)^j, p_{\max}(1 + \delta)^{j+1})$ for $j \ge 0$ are disjoint and cover $[p_{\max}, \infty)$. The value $\mathrm{OPT}$ is in $[p_{\max}, n p_{\max}]$, and $n p_{\max} \le p_{\max}(1 + \delta)^J$ by the choice of $J$ in line L2, so its interval has $j \le J$. $\square$

Fix this $j$ and $O$ for Lemmas 2 to 5. Fix an optimal packing, and let $U^*$ be its set of items.

**Lemma 2 (dropping small profits).** Let $T$ be the set of line L4 and $U' = U^* \cap T$. Then $U'$ fits in the knapsacks and $p(U') \ge (1 - \delta)\,\mathrm{OPT}$.

*Proof.* $U'$ is a subset of $U^*$, so the packing of $U^*$ with the other items removed packs $U'$. The items of $U^* \setminus U'$ number at most $n$, and each has profit below $\delta O / n$, so $p(U^* \setminus U') \le \delta O \le \delta \,\mathrm{OPT}$, with strict inequality when the set is not empty. $\square$

**Lemma 3 (rounding).** For each $i \in T$, $p_i / (1 + \delta) < a_i \le p_i$. Hence $a(U') > p(U')/(1 + \delta)$ when $U' \ne \emptyset$, and $a(U') \le p(U') \le \mathrm{OPT}$.

*Proof.* Let $u = \delta O / n$. Line L5 takes the largest $e_i \ge 0$ with $u (1 + \delta)^{e_i} \le p_i$; such an $e_i$ exists because $p_i \ge u$. So $a_i = u (1 + \delta)^{e_i} \le p_i < u (1 + \delta)^{e_i + 1} = (1 + \delta) a_i$. $\square$

Line L6 splits $T$ into the classes $S_1, \ldots, S_h$, one for each value of $e_i$, so all items of $S_r$ have the same rounded profit $a_r$. Each class is sorted by size, with ties broken by the item number, and "the $c$ smallest items of $S_r$" means the first $c$ items of this order. For $r = 1, \ldots, h$ let $V_r = U' \cap S_r$ and $u_r = |V_r|$, so $a(U') = \sum_r u_r a_r$.

**Lemma 4 (a tuple that the loop meets).** Let $k_r = \lfloor u_r a_r / g \rfloor$ and $c_r = \lceil k_r g / a_r \rceil$, with $g = \delta^2 O / h$ from line L7. Then $k_1 + \cdots + k_h \le D$, and $c_r \le u_r \le |S_r|$ for each $r$. So line L8 meets this tuple and line L9 does not skip it.

*Proof.* $\sum_r k_r \le \sum_r u_r a_r / g = a(U') / g \le \mathrm{OPT} / g < (1 + \delta) O \cdot h / (\delta^2 O) = (1 + \delta) h / \delta^2$, by Lemma 3 and Lemma 1. The sum is an integer below $(1 + \delta) h / \delta^2$, so it is at most $D = \lfloor (1 + \delta) h / \delta^2 \rfloor$. Next, $k_r \le u_r a_r / g$ gives $k_r g / a_r \le u_r$, and $u_r$ is an integer, so $c_r \le u_r$. Finally $V_r \subseteq S_r$. $\square$

Let $X_r$ be the $c_r$ smallest items of $S_r$, and $U = X_1 \cup \cdots \cup X_h$, the set of line L9 for this tuple.

**Lemma 5 (the exchange).** $U$ fits in the knapsacks.

*Proof.* We change the packing of $U'$ one class at a time. Fix $r$, and let $Y_r$ be the $c_r$ smallest items of $V_r$ in the same order. Since $X_r$ is a prefix of the order of $S_r$, each item of $X_r$ comes before each item of $S_r \setminus X_r$, so its size is at most theirs.

If some item $x \in X_r$ is in $V_r \setminus Y_r$, then each item of $Y_r$ comes before $x$, so it is in the prefix $X_r$. Then $Y_r \subseteq X_r$, and $|Y_r| = c_r = |X_r|$ gives $Y_r = X_r$. Otherwise $X_r \setminus Y_r$ has no item of $V_r$, and so no item of $U'$, because the classes are disjoint and $U' \cap S_r = V_r$. In both cases, $|X_r \setminus Y_r| = |Y_r \setminus X_r|$, and each item of $Y_r \setminus X_r \subseteq S_r \setminus X_r$ is at least as large as each item of $X_r \setminus Y_r$. Pair the two sets in any way, put each item of $X_r \setminus Y_r$ in the place of its partner in $Y_r \setminus X_r$, and remove the items of $V_r \setminus Y_r$. No knapsack load goes up, and the items of class $r$ in the packing are now exactly $X_r$. The change touches only items of $S_r$, so after all $h$ classes the packing holds exactly $U$, and it is feasible. $\square$

**Lemma 6 (the profit of the tuple).** $a(U) > a(U') - \delta^2 O$.

*Proof.* $a(U) = \sum_r c_r a_r \ge \sum_r k_r g > \sum_r (u_r a_r - g) = a(U') - h g = a(U') - \delta^2 O$. The first step is $c_r \ge k_r g / a_r$, and the second is $k_r > u_r a_r / g - 1$. $\square$

**Theorem.** The returned packing is feasible, and its profit is at least $(1 - 2\delta - \delta^2)\,\mathrm{OPT} \ge (1 - \varepsilon)\,\mathrm{OPT}$.

*Proof.* Line L10 keeps only packings that PACK has found, and the exact search returns a packing only when it is feasible, so the result is feasible. The empty packing is the start value, so the claim holds if $\mathrm{OPT} = 0$, which does not happen after Step 0. For the guess of Lemma 1, line L9 builds the set $U$ of Lemma 5, which fits, so PACK packs it. The result has profit at least $p(U)$, because line L10 skips a set only when its profit is not larger than the best one so far. Then, by Lemmas 3, 6 and 2, and with $O \le \mathrm{OPT}$,

$$
p(U) \ge a(U) > a(U') - \delta^2 O \ge \frac{p(U')}{1 + \delta} - \delta^2\,\mathrm{OPT} \ge \frac{1 - \delta}{1 + \delta}\,\mathrm{OPT} - \delta^2\,\mathrm{OPT} \ge (1 - 2\delta - \delta^2)\,\mathrm{OPT}.
$$

The last step is $(1 - \delta) \ge (1 - 2\delta)(1 + \delta) = 1 - \delta - 2\delta^2$. With $\delta = \varepsilon/3$, $2\delta + \delta^2 = 2\varepsilon/3 + \varepsilon^2/9 \le \varepsilon$ for $\varepsilon \le 3$. $\square$

**Lemma 7 (the number of candidates).** For one guess $O$, line L9 builds at most $\binom{D + h}{h}$ distinct sets, and

$$
\binom{D + h}{h} \le \Big(\frac{2e}{\delta^2}\Big)^{h}, \qquad h \le 1 + \frac{2 \ln(n/\delta)}{\delta}.
$$

So the number of sets for one guess is at most $(n/\delta)^{O(\log(1/\delta)/\delta)}$, and there are $J + 1 = O(\delta^{-1} \log n)$ guesses.

*Proof.* The number of tuples of $h$ non-negative integers with sum at most $D$ is $\binom{D + h}{h}$, and each set is built from at least one of them. With $\binom{N}{h} \le (eN/h)^h$ and $(D + h)/h \le 1 + (1 + \delta)/\delta^2 \le 2/\delta^2$ (true for $\delta^2 + \delta \le 1$), the first bound follows. For the second, each $i \in T$ has $u(1 + \delta)^{e_i} \le p_i \le p_{\max} \le O$ with $u = \delta O / n$, so $(1 + \delta)^{e_i} \le n / \delta$ and $e_i \le \ln(n/\delta) / \ln(1 + \delta) \le 2 \ln(n/\delta)/\delta$, using $\ln(1 + \delta) \ge \delta/2$ for $0 < \delta \le 1$. There are at most $1 + \max_i e_i$ values. Then $(2e/\delta^2)^h = (2e/\delta^2) \cdot (n/\delta)^{2\ln(2e/\delta^2)/\delta}$. Finally $J$ is the least integer with $(1 + \delta)^J \ge n$, so $J \le 1 + \ln n / \ln(1 + \delta) \le 1 + 2\ln n / \delta$. $\square$

The code builds each distinct vector $(c_1, \ldots, c_h)$ only once: for each $c_r$ it uses the least $k_r$ with $\lceil k_r g / a_r \rceil = c_r$, and it keeps the vector when these least values sum to at most $D$. This gives the same sets as the loop over all tuples, and their number is at most $\binom{D + h}{h}$ and at most $\prod_r (|S_r| + 1)$.

**Time.** For a fixed $\varepsilon$, lines L1 to L9 take polynomial time by Lemma 7. With the exact PACK of the code, line L10 can take time exponential in $|U|$, so the code is not polynomial. With the packing step of the paper in its place, each call is polynomial for a fixed $\varepsilon$.

**The packing step of the paper (sketch).** Chekuri and Khanna replace the exact search by a procedure that, for a candidate set $U$ that fits, finds a packing of a subset of $U$ of profit at least $(1 - O(\varepsilon))\,p(U)$. The argument below follows Section 2.3 of the paper. The details, in particular the counts of the guesses and Lemma 2.10, are not reproved here.

1. *Few sizes.* In each profit class, sort the items by size, split them into about $1/\varepsilon$ groups of equal count, drop one group, and round the sizes of each group up to the smallest size of the next group (the shifting of bin packing schemes). This loses a fraction $\varepsilon$ of the profit and leaves $O(\varepsilon^{-2} \log n)$ distinct sizes (Lemma 2.6).
2. *Bin blocks.* Scale so that the smallest capacity is 1, and put the knapsacks with capacity in $[(1 + \varepsilon)^i, (1 + \varepsilon)^{i+1})$ in block $B_i$. A block is small if it has at most $1/\varepsilon$ knapsacks. Only a bounded number of the small blocks with the largest capacities are kept. Among the $1/\varepsilon$ largest knapsacks of the small blocks, empty the one of least profit, which loses a fraction at most $\varepsilon$. The capacities of the small blocks fall geometrically, so the items of all the far smaller small blocks fit into this emptied knapsack (Lemma 2.8).
3. *Small blocks.* For each knapsack of a small block, guess its $1/\varepsilon$ most profitable items. The number of knapsacks in small blocks is bounded by a function of $\varepsilon$, so this is a polynomial number of guesses.
4. *Large items in large blocks.* An item is large in a knapsack if its size is at least $\varepsilon$ times the capacity, and it can be large in only $O(\varepsilon^{-1} \log(1/\varepsilon))$ blocks. For each size class and each such block, guess the number of large items up to a factor $1 - \varepsilon$. This is where the small number of sizes is used. Pack the large items of each block by a greedy step for items larger than 1 and by linear grouping and a dynamic program for the others, with at most $\varepsilon m_i$ extra knapsacks of capacity 1 (Lemmas 2.9 and 2.10).
5. *The rest by an LP.* Assign the other items by the LP of the generalized assignment problem, with the guessed items fixed, an item allowed in a large block only if it is small there, and an item allowed in a knapsack of a small block only if its profit is at most a fraction $\varepsilon/(1+\varepsilon)$ of the guessed items there. The LP is feasible if the guesses are right (Lemma 2.11). Round a basic solution by the method of Shmoys and Tardos, so that each knapsack is over its capacity by at most one item.
6. *Repair.* In a small block, drop the one extra item of each knapsack; by the profit rule of step 5 this loses a fraction at most $\varepsilon$. In a large block $B_i$, the extra items and the extra knapsacks of step 4 fit into at most $3 \varepsilon m_i$ knapsacks of capacity 1. Keep the $m_i$ most profitable of the $m_i + 3\varepsilon m_i$ knapsacks, which keeps a fraction at least $1/(1 + 3\varepsilon)$ of the profit, and their items fit into the knapsacks of $B_i$.

Each step loses a factor $1 - O(\varepsilon)$, and the number of guesses is polynomial for a fixed $\varepsilon$ (Theorem 2.12). Running the whole scheme with a suitably smaller $\varepsilon$ gives the ratio $1 - \varepsilon$.

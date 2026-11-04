---
title: The bag network sorts each input
proves: [correctness]
status: full
---

This proof follows Seiferas (Sections 4 and 5) for the case of the code, where SEPARATE in line L5 is an exact sorter, so $\varepsilon = 0$. The constants are $A = 10$, $\lambda = 1/100$ and $\nu = 13/20$. Let $n = 2^L$ and let the leaves be the bags at depth $L - 1$.

*Reduction.* The construction is a fixed list of comparators, each of which puts the minimum on a named register. By the [zero-one principle](/zero-one-principle/), which also holds for such general comparators, it is enough to show that the network sorts each input in $\{0, 1\}^n$. Each such input is $f(\pi)$ for a permutation $\pi$ of $0, \ldots, n-1$ and a non-decreasing map $f$, and the network commutes with $f$. So it is enough to show that it sorts each permutation of the ranks $0, \ldots, n-1$. From now on the items are these ranks, all different.

Write $I_X$ for the interval of a node $X$. An item $r$ in the bag of $X$ is a $j$-stranger, for $j \ge 1$, if $r \notin I_Y$ for the ancestor $Y$ of $X$ that is $j - 1$ levels up (or for the root, if there is no such ancestor). Let $b_X$ be the capacity of $X$ at the current time $t$, so a child has capacity $A b_X$ and the parent $b_X / A$.

**Invariant.** Before each stage:

1. the bags on alternate levels are empty;
2. all bags on one level hold the same number of items;
3. each bag $X$ holds at most $b_X$ items;
4. each bag $X$ holds at most $\lambda b_X$ 1-strangers and no $j$-strangers for $j \ge 2$.

Before the first stage all $n$ items are in the root, of capacity $n$, and all are native to the root. So the invariant holds with the odd levels empty.

**Lemma 1 (strangers in a bag go back).** Let $D$ be a bag that is not the root, and let the invariant hold. Then each 1-stranger of $D$ is among the items that $D$ sends to its parent in lines L6 and L7.

*Proof.* A 1-stranger of $D$ is either smaller than each item of $I_D$ or larger than each item of $I_D$. Let $s$ be the number of small ones. By part 4, $s \le \lambda b_D$, and $s$ is an integer, so $s \le \lfloor \lambda b_D \rfloor$. The exact sorter puts the $s$ small strangers in the first $s$ positions, and line L6 sends the first $\lfloor \lambda b_D \rfloor$ positions up (or all items, if there are fewer than $2 \lfloor \lambda b_D \rfloor$). The large strangers are handled in the same way at the other end. $\square$

**Parts 1 and 2.** By part 1, all items of the nonempty levels move one level up or down in a stage, so after it the nonempty levels are the ones that were empty. All bags on a level have the same capacity and, by part 2, the same number of items, so lines L6 to L8 send the same numbers of items from each of them. So the bags on each level receive the same numbers, and part 2 holds again.

**Part 3.** By part 1, a bag $B$ that holds items after the stage was empty before it, and it receives items only from its parent $D$ and its two children. Let $b = b_B$ before the stage. The parent holds at most $b/A$ items and sends at most half of them to $B$. Each child has capacity $Ab$ and sends at most $2 \lfloor \lambda A b \rfloor + 1$ items up. So $B$ receives at most $4 \lambda A b + 2 + b/(2A)$ items.

- If $b \ge A$, this is at most $b(4 \lambda A + 1/(2A) + 2/A)$.
- If $b < A$, each bag above $B$ has capacity at most $b/A < 1$, so by part 3 it is empty. The level of $B$ is empty too, so all $n$ items are in the subtrees rooted at the level of the children of $B$. By part 2 these subtrees hold the same number of items, $n$ divided by their number, which is a power of 2 and at least 2. Let $E$ be a child of $B$. The two subtrees below $E$ hold the same number of items by part 2, so $E$ itself holds an even number of items. After line L6 an even number remains, so line L7 sends nothing, and $B$ receives at most $4 \lambda A b + b/(2A)$ items.

In both cases $B$ receives at most $b(4 \lambda A + 5/(2A))$ items. For the constants above, $4 \lambda A + 5/(2A) = 2/5 + 1/4 = 13/20 = \nu$, and the new capacity of $B$ is $\nu b$. So part 3 holds again.

**Part 4, strangers of order $j \ge 2$.** Let $B$ be a bag that receives items, with parent $D$. An item that comes from a child $E$ of $B$ and is a $j$-stranger in $B$ is not native to the ancestor $j - 1$ levels above $B$, which is $j$ levels above $E$. So it was a $(j+1)$-stranger in $E$, and there are none. An item that comes from $D$ and is a $j$-stranger in $B$ was a $(j-1)$-stranger in $D$. For $j \ge 3$ there are none, and for $j = 2$ these are 1-strangers of $D$, which Lemma 1 sends to the parent of $D$, not to $B$. (If $D$ is the root, it has no strangers.) So $B$ has no $j$-strangers for $j \ge 2$.

**Part 4, 1-strangers.** The root never has strangers. Let $B$ be a bag that receives items, of capacity $b$ before the stage, with parent $D$ and sibling $C$, and let $D$ hold $d$ items. Say $B$ is the left child; the other case is symmetric. By the case $j \ge 2$, no item from a child of $B$ and no 1-stranger of $D$ is a 1-stranger in $B$ after the stage. So the only 1-strangers that $B$ gets are items of $D$ that are native to $C$.

The exact sorter puts the items of $D$ in order. Line L8 gives $B$ only positions below $d/2$, because the rest after lines L6 and L7 is symmetric around the middle. Above the items native to $C$ there are only the large 1-strangers of $D$; let $s_L$ be their number, so $s_L \le \lambda b/A$. If $c$ is the number of items of $D$ native to $C$, then those at positions below $d/2$ number at most $\max(0, c + s_L - d/2)$. So $B$ gets at most $\max(0, c - d/2) + \lambda b / A$ 1-strangers.

To bound $c - d/2$, count the items native to $C$. Let the level of $C$ have $2^i$ bags $C'$. By part 2, the subtree of each $C'$ holds the same number $m$ of items, and each parent $D'$ holds $d$ items. The bag $C$ is on the level of $B$, so it is empty by part 1. An item at depth $\delta \ge 1$ below $C$ that is not native to $C$ is a $(\delta + 1)$-stranger, and there are none. So the subtree of $C$ holds $m$ items native to $C$, and the other items of $I_C$ include the $c$ items in $D$. So

$$c \le |I_C| - m.$$

All intervals on the level of $C$ have the same length, so $|I_{C'}| - m - d/2$ is the same number for each $C'$. Their sum over the $2^i$ bags $C'$ is $n - 2^i m - 2^{i-1} d$, which is the number of items on the levels above the level of $D$. By parts 1 and 3, the levels above $D$ that hold items are $2, 4, 6, \ldots$ levels above $D$, with $2^{i-3}, 2^{i-5}, \ldots$ bags of capacity $b/A^3, b/A^5, \ldots$. So

$$c - \frac d2 \le |I_C| - m - \frac d2 \le \frac{1}{2^i} \sum_{r \ge 1} 2^{i - 2r - 1} \frac{b}{A^{2r+1}} = b \sum_{r \ge 1} \frac{1}{(2A)^{2r+1}} = \frac{b}{8A^3 - 2A}.$$

So $B$ gets at most $b \left( \frac{1}{8A^3 - 2A} + \frac{\lambda}{A} \right) = b \left( \frac{1}{7980} + \frac{1}{1000} \right) < \frac{13}{2000} b = \lambda \nu b$ 1-strangers. This is $\lambda$ times the new capacity of $B$, so part 4 holds again.

**Each stage can be done.** The only rule that can fail is line L8 at a leaf, which has no children. By part 2 the $n/2$ leaves hold the same number of items, so each holds at most 2. Line L2 runs a stage only if the leaf capacity $b$ satisfies $b \ge 1/\lambda$, so $2 \lfloor \lambda b \rfloor \ge 2$ and line L6 sends all items of a leaf up.

**The final step.** When the loop stops, the leaf capacity $b$ satisfies $b < 1/\lambda$. Let $k$ be the smallest integer with $(1/\lambda)(1/A)^{k+1} < 1$, and let $\tau = \max(L - 1 - k, 0)$ be the depth of the roots of the final subtrees. A bag at depth below $\tau$ has capacity at most $b / A^{k+1} < (1/\lambda) (1/A)^{k+1} < 1$, so by part 3 it is empty. If $\tau > 0$, a bag $R$ at depth $\tau = L - 1 - k$ has capacity $b_R = b / A^k < 1/(\lambda A^k)$, so by part 4 it holds fewer than $\lambda b_R < 1/A^k \le 1$ 1-strangers, that is none. An item in the subtree of $R$ at depth $\delta$ below $R$ that is not native to $R$ is a $(\delta + 1)$-stranger with $\delta \ge 1$, and there are none. (If $\tau = 0$, all items are native to the root.) So each item lies in the subtree of a depth-$\tau$ node to whose interval it belongs. By part 2 all these $2^\tau$ subtrees hold the same number of items, $n / 2^\tau = |I_R|$. So the subtree of $R$ holds exactly the items whose ranks are in $I_R$.

Line L10 sorts the registers of each subtree and lists the subtrees from left to right. The intervals $I_R$ are in increasing order from left to right, so the output lists the ranks $0, \ldots, n-1$ in order. $\blacksquare$

---
title: Correctness of the Garsia-Wachs algorithm
proves: [correctness]
status: sketch
---

The Garsia-Wachs algorithm has a combination phase (lines L1 to L5), a level phase (line L6) and a recombination phase (line L7). We prove the easy parts in full and give the structure of the main theorem. The original proof is by Garsia and Wachs (1977); Kingston (1988) gave a new and shorter proof, and Knuth presents the algorithm and a proof in The Art of Computer Programming, Volume 3, Section 6.2.2.

**Notation.** The list holds items with weights; at the start these are the leaves $1, \ldots, n$ with $w_i > 0$, between two sentinels of weight $\infty$. For a list $a_1, \ldots, a_m$ of items, let $\mathrm{OPT}(a_1, \ldots, a_m)$ be the least cost $\sum_i w(a_i) \, d_i$ over binary trees whose leaves, from left to right, are $a_1, \ldots, a_m$.

**Lemma 1 (the step is well defined).** While the list has $m \ge 2$ real items, there is a leftmost triple $x, y, z$ of neighbours, with $x$ and $y$ real, such that $w(x) \le w(z)$, and the move left stops.

*Proof.* The triple whose $z$ is the right sentinel has $w(z) = \infty$, so some triple qualifies. The triple that starts with the left sentinel never qualifies, because $w(z)$ is finite when $m \ge 2$; so $x$ is real. The move left stops at the latest at the left sentinel. $\square$

**Lemma 2 (the cost of the levels).** Let $d_i$ be the depth of leaf $i$ in the tree of the combination phase. Then $\sum_i w_i d_i$ is the sum of the weights of all nodes made, since leaf $i$ adds $w_i$ to each of its $d_i$ ancestors. $\square$

**Lemma 3 (recombination).** If $d_1, \ldots, d_n$ are the leaf depths of an alphabetic tree, the stack method of BUILD returns that tree. The proof is the same as for the [Hu-Tucker algorithm](/hu-tucker-algorithm/): the leftmost pair of sibling leaves are the first two neighbours of equal depth, BUILD joins them first, and induction on the tree with their parent as a leaf finishes the proof. $\square$

**Theorem (structure of the main proof).** Let $x, y, z$ be the triple chosen in line L3, let $t$ be the new item of weight $w(x) + w(y)$, and let $a'$ be the list after line L5, with $t$ moved left. The proof establishes two facts. We state them and the properties of the choice that they rest on; for the arguments see Kingston (1988) or Knuth's Section 6.2.2.

1. *Cost.* $\mathrm{OPT}(a) = w(x) + w(y) + \mathrm{OPT}(a')$, where the trees for $a'$ have $t$ as a leaf at its new place. One direction turns trees for $a'$ into trees for $a$ with $x$ and $y$ back in their old place, and the other turns an optimal tree for $a$ into a tree for $a'$; in both, the depths of the items between the new and the old place of $t$ are shifted by one place. Two properties of the choice make the shift free of loss: every item that $t$ passes is lighter than $t$, and every triple to the left of $x$ has $w(a_{j-1}) > w(a_{j+1})$, since otherwise an earlier triple would have been chosen.

2. *Feasibility.* The leaf depths of the final combination tree are the depths of some alphabetic tree for the original order, so that BUILD succeeds. This, too, comes from the shift, applied to the steps in reverse order.

By induction on the number of items, the combination phase reaches cost $\mathrm{OPT}$ for the original list, and by Lemma 2 the level phase gives depths of that cost. By fact 2 and Lemma 3, BUILD returns an alphabetic tree with these depths, which is therefore optimal.

**Evidence.** The tests run the implementation on 1500 random lists of up to 12 weights, half of them with many equal weights, and on 20 lists of 30 to 80 large weights, and compare the cost with the interval dynamic program and with the Hu-Tucker algorithm. All agree, and BUILD succeeds every time.

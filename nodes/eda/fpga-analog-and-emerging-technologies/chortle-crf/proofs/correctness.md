---
title: Chortle-crf returns a valid LUT network with the same outputs, its closing loop stops, and the cited conditions for tree optimality
proves: [correctness]
status: full
---

We use the notation of the page. The network has gates with associative and commutative operators (AND, OR, XOR). It is cut into fanout-free trees, and MAP-GATE is called on each tree root. An *item* is either a wire (size 1) or an open LUT returned by a child (size equal to the content of its last bin). A bin is a list of items, and its *content* is the sum of the sizes of its items.

**Lemma 1 (sizes bound inputs).** For every item $x$, the number of distinct signals that $x$ reads is at most its size.

*Proof.* By induction on the order in which items are made. A wire reads one signal and has size 1. An open LUT returned at line L10 is a bin whose content is the sum of the sizes of its items, and the signals it reads are the union of the signals of its items. By induction each item reads at most its size, so the union has at most the content. The output wire made at line L9 has size 1 and reads one signal. $\square$

**Lemma 2 (bins never overflow).** At every point, every bin has content at most $K$.

*Proof.* The size of a wire is $1 \le K$. The size of an open LUT is the content of a bin of a child, which is at most $K$ by induction on the depth of the tree. Line L6 puts an item into a bin only if it has room, or into a new bin, where the content is the size of the item. Line L9 does the same with a wire of size 1. Closing a bin removes it. So no step makes a content larger than $K$. $\square$

**Theorem 3 (valid LUTs).** Every LUT in the output has at most $K$ distinct inputs.

*Proof.* A LUT is a bin closed at line L8, or the last bin of a tree root at line L10. Its inputs are the signals read by its items, at most its content by Lemma 1, and the content is at most $K$ by Lemma 2. $\square$

**Lemma 4 (the closing loop stops).** Let $b$ be the number of bins after line L6. The loop at lines L7 to L9 runs at most $2b$ times, and it ends with exactly one bin.

*Proof.* A pass of the loop removes one bin at line L8. If line L9 finds a bin with room, the number of bins falls by one. If not, every remaining bin is full (content $K$), and line L9 opens a new bin with content $1 < K$, because $K \ge 2$; the number of bins stays the same. Look at the next pass, if there is one. Line L8 removes the fullest bin. If that is not the new bin, the new bin is still there with room for 1. If it is the new bin, every bin had content at most 1, so every remaining bin has room. In both cases line L9 finds room, and the number of bins falls. So two passes in a row cannot both keep the number of bins, and the number falls by at least one every two passes. The loop stops when one bin is left, after at most $2(b - 1)$ passes. If $b = 1$ the loop does not run. $\square$

**Theorem 5 (same function).** For every gate $v$, the open LUT returned for $v$, together with the LUTs closed while mapping the subtree of $v$, computes the output of $v$.

*Proof.* By induction on the subtree. Write $\circ$ for the operator of $v$ and $x_1, \ldots, x_d$ for its items. By induction each open LUT among the items computes the output of its fanin gate, and each wire is the fanin signal itself, so $v = x_1 \circ \cdots \circ x_d$. Each bin computes $\circ$ over its items. Closing a bin $B$ at line L8 makes a LUT with output $\circ B$, and line L9 puts that output, as one item, into another bin. Since $\circ$ is associative and commutative, $\circ$ over all items of all bins does not change when the items of $B$ are replaced by the single item $\circ B$. This holds before the loop (each item is in exactly one bin after line L6) and after each pass, so when one bin is left, $\circ$ over it equals $x_1 \circ \cdots \circ x_d = v$. $\square$

Applied to every tree root, Theorem 5 shows that the LUT network has the same outputs as the gate network: each tree root is a LUT with the name of the root, and other trees read it as a wire.

**Theorem 6 (the LUT count, cited).** The following two statements are from Francis, Rose and Vranesic (DAC 1991). We give them in the form of Cong and Ding's survey (ACM TODAES 1(2), 1996, Section 3.1.3), and we do not prove them here.

1. For a fanout-free tree, decomposing each gate $v$ so that (a) the number of $K$-LUTs that cover the subtree of $v$ is least, and (b) under (a), the number of inputs of the root LUT of $v$ is least, gives a mapping of the tree with the least number of $K$-LUTs.
2. First-fit decreasing, followed by the closing steps of lines L7 to L9, solves the restricted bin packing problem at a gate optimally when $K \le 5$. (Cong and Ding attribute this to Francis et al. 1991; the survey of Sangiovanni-Vincentelli, El Gamal and Rose, Proc. IEEE 1993, states the bound as $k \le 6$.)

Together they give the claim on the page: for a fanout-free tree and $K \le 5$, Chortle-crf uses the fewest LUTs over all splits of the gates into smaller gates of the same operator and all covers by LUTs.

The tests check statement 1 and statement 2 together, on random trees, against an exhaustive search that keeps, at every gate, the least number of closed LUTs for every possible size of the root LUT, and that tries every grouping of the items into LUTs. They are measurements, not a proof.

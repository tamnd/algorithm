---
title: Packet traversal returns for each ray the closest hit of single-ray traversal, and stops
proves: [correctness, termination]
status: full
---

**Setting.** The BVH is a finite rooted tree. Each leaf holds a list of primitives, each primitive is in exactly one leaf, and the box of every node contains all primitives below it. For a ray $i$ and a primitive $k$, let $\operatorname{hit}(i, k)$ be the parameter $t \in (0, t_{\max}]$ at which the ray meets $k$ first, or undefined. Pairs $(t, k)$ are ordered lexicographically, and "none" is larger than every pair. The goal for ray $i$ is
$$b_i^* = \min\{(\operatorname{hit}(i, k), k) : \operatorname{hit}(i, k) \text{ is defined}\},$$
or none if the ray hits nothing. We use exact arithmetic, and the box test of line L5 is the exact test "the ray meets the closed box for some $t \in [0, limit[i]]$".

**Lemma 1 (termination).** Each node is popped at most once, and the loop stops after at most as many passes as the tree has nodes.

*Proof.* The root is pushed once, in line L2. Any other node is pushed only in line L11, when its parent is popped. By induction on the depth, a node is pushed at most once: its parent is popped at most once, and that pop pushes each child once. So the number of pops is at most the number of nodes, and each pop removes one entry. $\square$

**Lemma 2 (the stored values are hits).** At all times, $best[i]$ is none or a pair $(\operatorname{hit}(i, k), k)$, and $limit[i]$ is $t_{\max}$ or the first component of $best[i]$. The value of $best[i]$ never increases.

*Proof.* Line L1 sets none and $t_{\max}$. Line L8 changes $best[i]$ only to a pair $(t, k)$ with $t = \operatorname{hit}(i, k)$ that is smaller than the old value, and sets $limit[i] = t$ at the same time. $\square$

**Lemma 3 (no hit is lost).** Let ray $i$ hit $k$, with $t_k = \operatorname{hit}(i, k)$, and let $N_0, \dots, N_\ell$ be the path from the root to the leaf of $k$. At the end, $best[i] \le (t_k, k)$.

*Proof.* Suppose not. By Lemma 2, $best[i] > (t_k, k)$ at all times, so $limit[i] \ge t_k$ at all times: if $best[i]$ is none, $limit[i] = t_{\max} \ge t_k$, and otherwise $best[i] = (t_b, k_b) > (t_k, k)$ gives $t_b \ge t_k$. The point $o_i + t_k d_i$ lies on $k$, hence in the box of every $N_j$, with $t_k \in [0, limit[i]]$. We show by induction on $j$ that $N_j$ is popped with $i$ in its mask after line L5. For $j = 0$, the root is pushed with all rays, it is popped by Lemma 1 before the loop ends, and line L5 keeps $i$ because the ray meets the box at $t_k$. If $N_j$, $j < \ell$, is popped with $i$ in the mask, then $M$ is not empty, $N_j$ is not a leaf, and line L11 pushes $N_{j+1}$ with a mask that contains $i$. It is popped before the stack is empty, and line L5 again keeps $i$. So the leaf $N_\ell$ is processed with $i \in M$. Line L8 then checks $k$ for ray $i$: the hit has $t_k \le limit[i]$ and $(t_k, k) < best[i]$, so $best[i]$ becomes $(t_k, k)$, a contradiction. $\square$

**Theorem.** The packet traversal stops, and for each ray $i$ it returns $b_i^*$. In particular it returns the same value as the traversal of the packet that holds only ray $i$, which is the single-ray depth-first traversal, and the same value as a linear scan over all primitives with the same tie rule.

*Proof.* Termination is Lemma 1. If ray $i$ hits nothing, line L8 never changes $best[i]$, which stays none. Otherwise, by Lemma 2 the final $best[i]$ is a pair $(\operatorname{hit}(i, k_b), k_b)$, so $best[i] \ge b_i^*$, and by Lemma 3 applied to the primitive of $b_i^*$, $best[i] \le b_i^*$. The value $b_i^*$ depends only on the ray and the primitives, not on the packet, the order of the rays or the order of the children. $\blacksquare$

**Remark (what the packet changes).** The proof uses nothing about the other rays of the packet. They change only which nodes are visited and when, and hence the counts of node visits and box tests. With floating-point box and primitive tests, the theorem holds as long as the box test never rejects a ray that meets a primitive inside the box. A conservative slab test, widened by a few units in the last place, gives this.

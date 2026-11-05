---
title: McCreight's algorithm builds the suffix tree in linear time
proves: [correctness, termination, complexity]
status: full
---

Let $t = S\$$ with $|t| = n + 1$, where $\$$ occurs only at the end, and $t_i = t[i \ldots n]$. For $i \ge 1$, $head_i$ is the longest prefix of $t_i$ that is a prefix of some $t_j$, $j < i$; $head_0$ is the empty string. Since $\$$ occurs once, no $t_i$ is a prefix of an earlier $t_j$ (its $\$$ would have to be at a position where $t_j$ has a symbol of $S$), so $|head_i| < |t_i|$. Let $\mathcal{T}_i$ be the compact trie of $t_0, \ldots, t_i$. A *place* is a node or a point inside an edge; each prefix of some $t_j$, $j \le i$, has exactly one place in $\mathcal{T}_i$.

**Lemma 1.** In $\mathcal{T}_i$, the place of $head_i$ is a node (the root, or an inner node with at least two children), and $t_i$ ends at a leaf whose parent is this node.

*Proof.* In $\mathcal{T}_{i-1}$, $t_i$ follows the path of $head_i$ and then leaves it, since the next symbol of $t_i$ does not continue $head_i$ in any earlier suffix. Adding $t_i$ adds one leaf edge at the place of $head_i$, which becomes a node with at least two children (or is the root). $\square$

**Lemma 2 (McCreight).** If $head_{i-1} = x\alpha$ with a symbol $x$, then $\alpha$ is a prefix of $head_i$.

*Proof.* $x\alpha$ is a prefix of $t_{i-1}$ and of some $t_j$, $j < i - 1$. So $\alpha$ is a prefix of $t_i$ and of $t_{j+1}$ with $j + 1 < i$. $\square$

**Lemma 3.** If $head_{i-1} = x\alpha$ is an inner node of $\mathcal{T}_{i-1}$, then $\alpha$ has a place in $\mathcal{T}_{i-1}$; if $head_{i-1}$ is an inner node of $\mathcal{T}_{i-2}$ (it existed before step $i - 1$), then $\alpha$ is a node of $\mathcal{T}_{i-2}$, hence of $\mathcal{T}_{i-1}$.

*Proof.* The first claim is Lemma 2's proof. For the second, an inner node $x\alpha$ of $\mathcal{T}_{i-2}$ has two children starting with different symbols $c \ne d$, so $x\alpha c$ and $x\alpha d$ are prefixes of two suffixes $t_j, t_k$ with $j, k \le i - 2$, and $\alpha c$, $\alpha d$ are prefixes of $t_{j+1}$ and $t_{k+1}$ with $j + 1, k + 1 \le i - 1$. So $\alpha$ branches in $\mathcal{T}_{i-1}$ and is a node there. Since nodes are never removed and edges are only split, it stays a node in later trees. $\square$

**Invariant.** Before step $i$ ($1 \le i \le n$): the tree is $\mathcal{T}_{i-1}$; $h$ is the node of $head_{i-1}$; every inner node $v \ne h$ has $link(v)$ equal to the node of its string without the first symbol; and $h$ has a link if and only if it is the root or it is an inner node of $\mathcal{T}_{i-2}$.

It holds before step 1: the tree is the root with the leaf of $t_0$, and $h$ is the root, whose link is the root.

**Step $i$.** Let $head_{i-1} = x\alpha$ when $h$ is not the root.

*Case L3, $h$ is the root.* $head_{i-1}$ is empty, and the scan starts at the root, which is the place of the empty prefix of $head_i$.

*Case L4, $h$ has a link.* By the invariant and Lemma 3, $link(h)$ is the node $\alpha$, and $\alpha$ is a prefix of $head_i$ by Lemma 2.

*Case L5 to L7, $h$ has no link.* Then $h$ was created in step $i - 1$ by a split. Let $p$ be its parent and $\beta$ the edge label, so $x\alpha = \mathrm{str}(p)\beta$. If $p$ is the root, $\alpha$ is $\beta$ without its first symbol and the rescan starts at the root. Otherwise $p \ne h$ has a link to the node of $\mathrm{str}(p)$ without its first symbol, and $\alpha$ is that string followed by $\beta$. In both cases $\alpha$ is in the tree (Lemma 3), so the rescan, which at each node takes the child whose edge starts with the next symbol of $\beta$ and skips the whole edge if it is not longer than the rest of $\beta$, reaches the place of $\alpha$ without comparing other symbols: every edge on the way is on the path of $\alpha$, and its symbols agree with $\alpha$ because $\alpha$ is in the tree. If the place is inside an edge, the split creates a node there.

Now set $link(h) = w$, the node of $\alpha$. This is the correct link. If $w$ was just created by a split, then the place of $\alpha$ had exactly one continuing symbol $c$ in $\mathcal{T}_{i-1}$. Since $h$ was created in step $i - 1$ by a split at the place where $t_{i-1}$ left the tree, $x\alpha c'$ is a prefix of an earlier suffix and $x\alpha d$ a prefix of $t_{i-1}$ for some $c' \ne d$. Then $\alpha c'$ occurs in $\mathcal{T}_{i-1}$, so $c' = c$, and $\alpha d$ is a prefix of $t_i$ with $d \ne c$. Hence $t_i$ leaves the tree right after $\alpha$, and $head_i = \alpha$.

*Line L8.* Otherwise $w$ is a node of $\alpha$, a prefix of $head_i$. The scan compares symbols of $t_i$ after $\alpha$ along the tree until the first mismatch, which exists since $|head_i| < |t_i|$; the place reached is the longest prefix of $t_i$ in $\mathcal{T}_{i-1}$, which is $head_i$. A split there makes it a node.

*Lines L9, L10.* Adding the leaf of $t_i$ at the node of $head_i$ gives $\mathcal{T}_i$ by Lemma 1. The only inner node created in step $i$ other than by the rescan split is the node of $head_i$; the rescan split node is $head_i$ itself in that case. All older inner nodes, and $h$, now have correct links. The new $h = head_i$ has a link exactly when it is the root or an old node. So the invariant holds before step $i + 1$.

After step $n$ the tree is $\mathcal{T}_n$, the compact trie of all suffixes of $S\$$, which is the suffix tree. The loop has $n$ steps, and each walk goes down a finite tree, so the algorithm terminates.

**Time.** Write $|x|$ for the string depth and $nd(x)$ for the node depth (the number of nodes on the root path, including the root) of a place $x$.

*Scans.* The scan of step $i$ starts at the node $w$ of $\alpha$, with $|\alpha| \ge |head_{i-1}| - 1$, and makes at most $|head_i| - |\alpha| + 1$ symbol comparisons. The sum over $i$ is at most $\sum_i (|head_i| - |head_{i-1}| + 2) \le |head_n| + 2n \le 3n + 1$.

*Rescans.* For a node $v$ with a link, $nd(link(v)) \ge nd(v) - 1$. Indeed, each ancestor $u$ of $v$ other than the root is an inner node with a link, and $link(u)$ is the node of $\mathrm{str}(u)$ without its first symbol, which is a prefix of the string of $link(v)$; so $link(u)$ is an ancestor of $link(v)$ or $link(v)$ itself. Distinct ancestors have distinct string depths, so their links are distinct. This gives $nd(v) - 1$ distinct nodes on the root path of $link(v)$, and $nd(link(v)) \ge nd(v) - 1$. The rescan of step $i$ starts at $v$ with $nd(v) \ge nd(p) - 1 = nd(h) - 2$ and ends at $w$, each step going down one node. The scan only goes further down, so the number of rescan steps is at most $nd(head_i) - nd(head_{i-1}) + 2$. The sum is at most $nd(head_n) + 2n \le 3n + 1$.

Each scan comparison and each rescan step costs one child lookup and $O(1)$ more work; the remaining work in a step is $O(1)$. So the total time is $O(n)$ child lookups, which is $O(n)$ for a constant alphabet or with hashing, and $O(n \log \sigma)$ with balanced child maps. $\blacksquare$

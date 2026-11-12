---
title: The tree bitmap lookup returns the longest matching prefix, and updates keep the layout
proves: [correctness]
status: full
---

We use the notation of the page. Addresses have $W$ bits, the stride is $s$ with $1 \le s \le W$, and $\mathrm{rank}(B, i)$ is the number of 1 bits of $B$ at positions below $i$. A node at depth $k$ is reached by a string $x$ of $ks$ bits (the concatenation of the child indices on its path). The *in-node prefix* of length $j$ and value $v$, with $0 \le j \le s - 1$ and $0 \le v < 2^j$, has internal bit index $2^j - 1 + v$. The indices of different pairs $(j, v)$ are different, because the indices for length $j$ fill the range $[2^j - 1, 2^{j+1} - 2]$, and these ranges are disjoint for $j = 0, 1, \ldots, s-1$ and cover $[0, 2^s - 2]$.

**The layout invariant (I).** For the table $T$ of prefixes stored in the structure:

1. A prefix $(p, \ell) \in T$ is stored at the node reached by the first $\lfloor \ell/s \rfloor s$ bits of $p$, as the in-node prefix of length $j = \ell \bmod s$ and value $v$ equal to the last $j$ bits of $p$. The internal bit $2^j - 1 + v$ of that node is 1, and no other internal bit of any node is 1.
2. In each node, `results` has one entry for each 1 bit of `internal`, in increasing order of bit index, and the entry for bit $i$ is at position $\mathrm{rank}(\mathit{internal}, i)$ and holds the next hop of the prefix of bit $i$.
3. In each node, `children` has one node for each 1 bit of `external`, in increasing order of bit index, and bit $c$ of the node reached by $x$ is 1 if and only if the node reached by $x c$ (the $s$ bits of $c$ appended) exists.
4. Each node other than the root has a 1 bit in `internal` or in `external`.

Parts 2 and 3 say that $\mathrm{rank}$ gives the array position: the entries before the one for bit $i$ are exactly those for the 1 bits below $i$.

## The lookup is correct

**Claim.** If (I) holds, TB-LOOKUP$(a)$ returns the next hop of the longest prefix of $T$ that matches $a$, or "no route" if none matches.

*Proof.* For $k \ge 0$ with $ks \le W$, let $x_k$ be the first $ks$ bits of $a$, and let $c_k$ be the next $\min(s, W - ks)$ bits of $a$, padded at the end with zeros to $s$ bits.

*Step 1: which prefixes live where.* By (I.1), a prefix $(p, \ell) \in T$ with $\lfloor \ell / s \rfloor = k$ and $j = \ell - ks$ matches $a$ if and only if it is stored in the node reached by $x_k$ and its value $v$ equals the first $j$ bits of $c_k$. The "only if" holds because a match means that the first $\ell$ bits of $p$ and of $a$ agree, so the first $ks$ bits of $p$ are $x_k$ and its last $j$ bits are the first $j$ bits of $c_k$. The "if" holds by the same equalities read the other way. Here $j \le W - ks$ because $\ell \le W$, so the first $j$ bits of $c_k$ are bits of $a$ and not padding.

*Step 2: the loop visits the nodes on the path of $a$.* We show by induction that at the start of iteration $k$, the variable $node$ is the node reached by $x_k$. This is true for $k = 0$ (line L1, the root is reached by the empty string). In iteration $k$, line L9 moves to `children`$[\mathrm{rank}(\mathit{external}, c_k)]$ only if bit $c_k$ of `external` is 1 and $(k+1)s \le W$; by (I.3) that entry is the node reached by $x_k c_k = x_{k+1}$. The loop stops at the first $k$ where $(k+1)s > W$ or the node reached by $x_{k+1}$ does not exist.

*Step 3: no matching prefix lies below the last node.* Let the loop stop at depth $K$. If $(K+1)s > W$, then a prefix at depth $K + 1$ or deeper would have length at least $(K+1)s > W$, which is impossible. Otherwise the node reached by $x_{K+1}$ does not exist. By (I.1), each prefix that matches $a$ and has length at least $(K+1)s$ is stored at a node reached by a string that starts with $x_{K+1}$. By (I.3) and induction on the depth, if the node of $x_{K+1}$ does not exist, then no node reached by a longer string that starts with $x_{K+1}$ exists. So no such prefix is in $T$.

*Step 4: the best match.* In iteration $k$, the loop of lines L5 to L7 tries $j = \min(s-1, W - ks)$ down to 0 and stops at the first $j$ whose internal bit $2^j - 1 + (\text{first } j \text{ bits of } c_k)$ is 1. By Step 1 this is the longest prefix of $T$ that matches $a$ and has length in $[ks, ks + s - 1]$, and line L7 records its node and its array position. Lengths at depth $k + 1$ are larger than all lengths at depth $k$, so after the last iteration, $best$ refers to the longest match among depths $0, \ldots, K$. By Step 3 there is none deeper. If no iteration found a bit, no prefix of $T$ matches $a$ and line L10 returns "no route". Otherwise line L11 reads `results`$[\mathrm{rank}(\mathit{internal}, i)]$ of the recorded node, which by (I.2) is the next hop of that prefix. $\square$

## Insert and delete keep the invariant

**Insert $(p, \ell, h)$.** Let $k = \lfloor \ell / s \rfloor$ and let $x$ be the first $ks$ bits of $p$, cut into the child indices $c_0, \ldots, c_{k-1}$. The walk goes down from the root. At depth $d$, if bit $c_d$ of `external` is 0, it sets the bit and inserts a new empty node into `children` at position $\mathrm{rank}(\mathit{external}, c_d)$. Before the bit is set, the children of the 1 bits below $c_d$ are the first $\mathrm{rank}(\mathit{external}, c_d)$ entries, so the new node lands in the place of bit $c_d$ in increasing bit order, and (I.3) holds again. The new node is empty only until the walk goes on below it, and at the end of the insert each new node has either a child on the path or the new internal bit, so (I.4) holds. At the last node, the insert sets internal bit $i = 2^j - 1 + v$; if it was 0, it inserts $h$ at position $\mathrm{rank}(\mathit{internal}, i)$, which by the same argument keeps (I.2); if it was 1, the prefix was already in $T$ and it overwrites the entry of bit $i$. (I.1) holds because the prefix is at the node and bit that (I.1) names.

**Delete $(p, \ell)$.** If the path or the internal bit does not exist, the prefix is not in $T$ by (I.1), and nothing changes. Else the delete removes the entry at position $\mathrm{rank}(\mathit{internal}, i)$ and then clears bit $i$, which keeps (I.1) and (I.2). Then it goes up the path. While the current node is not the root and has no 1 bit in `internal` or `external`, it removes that node from its parent: it removes the entry at position $\mathrm{rank}(\mathit{external}, c)$ and clears bit $c$, which keeps (I.3). The loop stops at the first node with a 1 bit, and every node above it on the path has a child, so each node still in the structure satisfies (I.4). A removed node held no prefix and no child, so (I.1) still holds for the remaining prefixes. $\square$

**Initial state.** The empty structure is one root with both bitmaps 0 and empty arrays. It satisfies (I) for $T = \emptyset$. By induction on the number of updates, (I) holds after any sequence of inserts and deletes, and by the claim each lookup is correct.

## Cost

The loop of TB-LOOKUP runs at most $\lfloor W/s \rfloor + 1$ times, once for each depth $0 \le k \le W/s$, and each iteration reads one node. One more read fetches the result. So a lookup makes at most $\lfloor W/s \rfloor + 2$ memory reads; for $W = 32$ and $s = 4$ that is 10. Each node other than the root lies on the path of some prefix by (I.4) and (I.1), and a prefix of length $\ell$ has $\lfloor \ell/s \rfloor$ nodes below the root on its path, so there are at most $n \lfloor W/s \rfloor + 1$ nodes for $n$ prefixes. An update walks at most $\lfloor W/s \rfloor$ nodes and changes the arrays of at most one node on the way down (insert) or of the nodes it frees and one more node (delete). An array has at most $2^s$ entries, so an update costs $O(W/s + 2^s)$ time in this array model.

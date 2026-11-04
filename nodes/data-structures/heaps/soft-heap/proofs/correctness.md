---
title: The soft heap returns an item of smallest current key and has at most 18n/2^T corrupted items
proves: [correctness]
status: full
---

We use the definitions of the page: $n$ is the number of insertions, the target sizes are $s_k = 1$ for $k \le T$ and $s_k = \lceil 3 s_{k-1}/2 \rceil$ for $k > T$, and the current key of an item in $list(x)$ is $ckey(x)$. The invariants are (I1) $ckey(x) \le ckey(c)$ for every child $c$ of $x$; (I2) $key(e) \le ckey(x)$ for every item $e$ in $list(x)$; (I3) every node that is not a leaf has a non-empty list, and every leaf in a tree has a non-empty list; (I4) each child of a node of rank $k$ has rank $k - 1$; (I5) every item that was inserted and not deleted is in exactly one list.

**Lemma 1.** SIFT$(x)$, called on a node whose children satisfy (I1) to (I4) in their subtrees, ends with (I1) to (I4) in the subtree of $x$, and with $ckey(x)$ at least its old value if $list(x)$ was not empty. It does not change any current key except by raising it.

*Proof.* By induction on the rank of $x$; the recursive call is on a child, of smaller rank. Take one pass of the loop. By (I3) the child $c$ that line L4 chooses has a non-empty list, and it has the smallest $ckey$ among the children. Line L5 sets $ckey(x) \leftarrow ckey(c)$. If $list(x)$ was not empty, the old $ckey(x)$ was at most $ckey(c)$ by (I1), so it does not decrease, and the items of $x$ get a current key that is not smaller. The items of $c$ keep their current key $ckey(c)$. So (I2) holds at $x$: old items had $key \le$ old $ckey(x) \le ckey(c)$, and the new ones had $key \le ckey(c)$. The other child $c'$ has $ckey(c') \ge ckey(c) = ckey(x)$, so (I1) holds for $c'$. Now $list(c)$ is empty. If $c$ is a leaf, line L6 removes it, and (I3) holds. Otherwise SIFT$(c)$ runs; by induction it ends with (I1) to (I4) in the subtree of $c$, its list is not empty, because $c$ is not a leaf, so the loop makes at least one pass, and each pass adds a non-empty list; and $ckey(c)$ is at least the value that $x$ took. So (I1) holds for $c$. When the loop ends, $list(x)$ is non-empty or $x$ is a leaf; $x$ started with a child, and the first pass adds a non-empty list, so $list(x)$ is not empty. Ranks do not change, so (I4) holds. $\square$

**Lemma 2.** INSERT, MELD and DELETE-MIN keep (I1) to (I5), and the suffix-min pointers point to a root of smallest $ckey$ among the roots of equal or larger rank.

*Proof.* A new node of rank 0 has one item with $ckey = key$. LINK$(x, y)$ makes a node $z$ of rank $r + 1$ with two children of rank $r$, so (I4) holds, and SIFT$(z)$ gives (I1) to (I3) by Lemma 1. Insert and meld only add roots and link them, so each item stays in one list (I5). In DELETE-MIN, line L11 removes one item, which keeps (I1), (I2) and (I5) for the others. If $x$ is not a leaf, SIFT$(x)$ restores (I3) by Lemma 1, and (I1) still holds for its parent because $x$ is a root. If $x$ is a leaf whose list is empty, line L14 removes it. The suffix-min pointers can change only for the roots whose $ckey$ changed or that were added or removed, and for the roots of smaller rank, which all come after them in the list. The code recomputes all of them from the first changed position, so they are right. $\square$

**Lemma 3.** FIND-MIN and DELETE-MIN return an item whose current key is the smallest current key of all items, and the returned current key is at least the key of the item.

*Proof.* By (I1) and induction on depth, the $ckey$ of a root is at most the $ckey$ of every node in its tree. Every root has a non-empty list by (I3), so the root $x$ of smallest $ckey$ holds an item with the current key $ckey(x)$, and every item in the heap has a current key at least $ckey(x)$. By (I2) the item has $key \le ckey(x)$. $\square$

**Lemma 4.** A node of rank $k \le T$ holds at most one item, and that item is not corrupted.

*Proof.* At creation, a node of rank 0 holds one item with its own key. A node of rank $k \ge 1$ starts with an empty list. In SIFT the loop runs only while $|list(x)| < s_k = 1$, so only when the list is empty, and then it takes the list of a child of rank $k - 1 \le T$, which by induction on $k$ and on time is at most one item that is not corrupted, and sets $ckey(x)$ to the current key of that item, which is its own key. Lists only shrink otherwise. $\square$

**Lemma 5.** For every node of rank $k$, $|list(x)| \le B_k$, where $B_k = 1$ for $k \le T$ and $B_k \le 6 (3/2)^{k - T}$ for $k > T$.

*Proof.* First, $s_{T + j} \le 2 (3/2)^j - 1$: for $j = 0$ this is $1 \le 1$, and $\lceil 3s/2 \rceil \le 3s/2 + 1/2 \le \frac32 (2 (3/2)^{j-1} - 1) + \frac12 = 2 (3/2)^j - 1$. A list grows only in line L5, while it has fewer than $s_k$ items, by one list of a child, of rank $k - 1$. So $B_k \le s_k - 1 + B_{k-1}$, with $B_k = 1$ for $k \le T$ by Lemma 4. Then for $k > T$, $B_k \le 1 + \sum_{j=1}^{k-T} (s_{T+j} - 1) \le \sum_{j=0}^{k-T} 2 (3/2)^j < 2 \cdot \frac{(3/2)^{k-T+1}}{1/2} = 6 (3/2)^{k-T}$. $\square$

**Lemma 6.** At most $n / 2^k$ nodes of rank $k$ are ever made.

*Proof.* Nodes of rank 0 are made only by insert, so there are $n$. A node of rank $k \ge 1$ is made only by LINK of two roots of rank $k - 1$, and these two nodes are no longer roots afterwards, and a node never becomes a root again. So each node of rank $k - 1$ takes part in at most one link, and the number of nodes of rank $k$ is at most half the number of rank $k - 1$. $\square$

**Theorem.** At any time the heap holds exactly the items inserted and not deleted (I5); delete-min returns an item of smallest current key (Lemma 3); current keys never decrease (Lemma 1); and the number of corrupted items is at most $18 n / 2^T$. With $T = \lceil \lg(1/\varepsilon) \rceil + 5$ this is less than $\varepsilon n$.

*Proof.* The first three claims are Lemmas 2, 3 and 1. By Lemma 4, every corrupted item is in a node of rank $k > T$. By Lemmas 5 and 6, these nodes hold at most

$$\sum_{k > T} \frac{n}{2^k} \cdot 6 \left(\frac32\right)^{k-T} = \frac{6n}{2^T} \sum_{j \ge 1} \left(\frac34\right)^j = \frac{18 n}{2^T}$$

items. If $T \ge \lg(1/\varepsilon) + 5$, then $2^T \ge 32/\varepsilon$, so the count is at most $\frac{18}{32} \varepsilon n < \varepsilon n$. $\blacksquare$

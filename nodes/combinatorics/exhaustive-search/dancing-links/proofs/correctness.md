---
title: UNCOVER undoes COVER, and COVER removes the right options
proves: [correctness]
status: full
---

We use the layout and the line numbers of the page. A *column node* is an item header or an option node; spacers and the root are not column nodes. Call an option *active* when each of its nodes is in the column list of its item.

**Lemma 1 (one deletion).** Let $x$ be a node of a circular doubly linked list with links $L$ and $R$. The deletion $R[L[x]] \gets R[x]$, $L[R[x]] \gets L[x]$ does not change $L[x]$ or $R[x]$. If the links of all nodes are exactly as right after this deletion, then $R[L[x]] \gets x$, $L[R[x]] \gets x$ gives back exactly the links before it.

*Proof.* The deletion writes only to the nodes $a = L[x]$ and $b = R[x]$; it is not a write to $x$, since $a \ne x$ and $b \ne x$ when $x$ is in a list with another node, and when $a = b = x$ both writes put $x$ in its own links, which do not change. Before it, $R[a] = x$ and $L[b] = x$, because $x$ is in the list. The undo reads $a$ and $b$ from the links of $x$, which are unchanged, and writes back $R[a] = x$ and $L[b] = x$. No other link was changed. $\square$

**Lemma 2 (reverse order).** Let $D_1, \ldots, D_k$ be deletions, each of a node that is in its list at that time, and let $U_t$ be the undo of $D_t$ as in Lemma 1. Then $D_1, \ldots, D_k, U_k, \ldots, U_1$ gives back the start state. The same holds when the lengths are decreased by $D_t$ and increased by $U_t$.

*Proof.* Let $S_0$ be the start state and $S_t$ the state after $D_t$. By induction on $r = k, k-1, \ldots, 1$: before $U_r$ the state is $S_r$, which is the state right after $D_r$ applied to $S_{r-1}$, so by Lemma 1, $U_r$ gives $S_{r-1}$. A length decreased and then increased by one is unchanged, and the counters commute with the link changes. $\square$

**Lemma 3 (walks along an option).** Let $p$ be a node of an option with nodes $y_1 < \cdots < y_r$, with $p = y_a$. HIDE$(p)$ visits, at line L5, the nodes $y_{a+1}, \ldots, y_r, y_1, \ldots, y_{a-1}$ in this order. UNHIDE$(p)$ visits, at line L17, the same nodes in the reverse order.

*Proof.* The nodes of an option are consecutive. The spacer after the option is $y_r + 1$, and its ULINK is $y_1$. So the walk $q \gets q + 1$ of HIDE goes from $y_{a+1}$ to $y_r$, meets the spacer at line L4, jumps to $y_1$, and goes on to $y_{a-1}$, then stops at $q = p$. The spacer before the option is $y_1 - 1$, and its DLINK is $y_r$, so UNHIDE goes from $y_{a-1}$ down to $y_1$, jumps to $y_r$ and goes down to $y_{a+1}$. The links of the spacers are never written by lines L5, L12, L17 or L20, because these lines write only to column nodes and headers. $\square$

**Lemma 4 (UNCOVER undoes COVER).** Assume no option names an item twice. If UNCOVER$(i)$ is called right after COVER$(i)$, or after other calls that together restore the state right after COVER$(i)$, then the state becomes exactly the state before COVER$(i)$.

*Proof.* Let $p_1, \ldots, p_h$ be the nodes of column $i$ from top to bottom when COVER$(i)$ starts. HIDE$(p_t)$ deletes only nodes of the option of $p_t$ other than $p_t$, and none of them is in column $i$, because the option has only one node in column $i$. So column $i$ does not change during COVER$(i)$, and line L10 walks $p_1, \ldots, p_h$. Each deletion of line L5 is of a node that is in its column at that time. Line L12 deletes header $i$ from its horizontal list (for a secondary item, from a list of one node, which changes nothing). So COVER$(i)$ is the sequence of deletions: those of HIDE$(p_1)$, ..., those of HIDE$(p_h)$, then header $i$.

UNCOVER$(i)$ first undoes the deletion of header $i$ at line L20. Column $i$ is still $p_1, \ldots, p_h$, because nothing deleted from or restored to it, so lines L21 to L24 walk $p_h, \ldots, p_1$. By Lemma 3, UNHIDE$(p_t)$ undoes the deletions of HIDE$(p_t)$ in the reverse order. So UNCOVER$(i)$ performs the undos of all deletions of COVER$(i)$ in exactly the reverse order, and Lemma 2 gives the claim. $\square$

**Lemma 5 (effect of COVER).** Assume (I): every option is either active, or was hidden by one HIDE$(p)$ inside a COVER$(j)$ that is not yet undone, and then all its nodes except $p$ are out of their columns, and $p$ is in column $j$. Assume also that all headers in the root list and all headers of active items have all the nodes of their active options. Let $i$ be an active item. Then COVER$(i)$ makes $i$ inactive, hides exactly the active options that contain $i$, keeps (I), and leaves column $i$ as it was.

*Proof.* Since $i$ is active, no COVER$(i)$ is pending, so by (I) every node in column $i$ belongs to an active option, and every active option that contains $i$ has its node in column $i$. COVER$(i)$ calls HIDE once on each of these nodes, which takes all other nodes of that option out of their columns and decreases their lengths. The option is then hidden by HIDE$(p)$ with $p$ in column $i$, as (I) requires. Options that do not contain $i$ are not touched. Line L12 takes $i$ out of the root list. Column $i$ is unchanged by the proof of Lemma 4. $\square$

**Theorem.** In a run where the COVER and UNCOVER calls are properly nested, that is, each UNCOVER$(i)$ undoes the last COVER that is not yet undone and that COVER is COVER$(i)$, and each COVER is of an active item:

1. after each COVER$(i)$, the active items are the old ones less $i$, and the active options are the old ones less those that contain $i$;
2. after each UNCOVER$(i)$, every link and every length is as before the matching COVER$(i)$;
3. at every moment, LEN$[x]$ is the number of nodes in column $x$, and for each active item, its column holds exactly the active options that contain it.

*Proof.* At the start, every option is active, so (I) holds, and the build makes LEN$[x]$ the length of column $x$. Proceed by induction on the number of calls. A COVER keeps (I) and has effect 1 by Lemma 5, and lines L5 and L17 change LEN by one exactly when a node leaves or enters a column, which keeps statement 3. For an UNCOVER$(i)$, the calls between the matching COVER$(i)$ and it are properly nested, so by induction they restore the state right after COVER$(i)$, and Lemma 4 then restores the state before it. That gives statement 2, and (I) and statement 3 hold because they held before the COVER. $\blacksquare$

**Running time.** Line L5 runs once for each node of each hidden option, and line L4 at most once per option, so COVER$(i)$ takes $O(1 + t)$ steps, where $t$ is the total size of the active options that contain $i$. UNCOVER$(i)$ makes the same number of steps by Lemma 4.

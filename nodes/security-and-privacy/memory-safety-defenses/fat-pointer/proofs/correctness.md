---
title: A fat pointer check passes exactly on memory-safe accesses
proves: [correctness, invariant]
status: full
---

**Setting.** The program runs a finite sequence of the operations ALLOC, ADD, LOAD, STORE and FREE of the main block, on a heap whose allocator returns disjoint blocks: a block it returns does not overlap any block that is allocated and not freed. Each allocation $j$ has a block $B_j = [b_j, e_j)$ and a capability number $c_j$; the numbers come from a counter, so they are distinct. Every pointer the program holds was returned by ALLOC or by ADD; the program cannot write the fields $\mathit{base}$, $\mathit{bound}$ or $\mathit{cap}$. For a pointer $p$ that ALLOC returned in allocation $j$, or that ADD derived from such a pointer, we say that $p$ belongs to $j$. The null pointer belongs to no allocation.

An access of $w \ge 1$ bytes through $p$ is *memory safe* if $p$ belongs to an allocation $j$, the bytes $[p.\mathit{value}, p.\mathit{value} + w)$ lie in $B_j$, and $j$ is live (not yet freed). It is a *spatial error* if $p$ is null or the bytes do not lie in $B_j$, and a *temporal error* if they lie in $B_j$ and $j$ was freed.

**Lemma 1 (invariant (F)).** After each operation: (a) every non-null pointer $p$ that belongs to allocation $j$ has $p.\mathit{base} = b_j$, $p.\mathit{bound} = e_j$ and $p.\mathit{cap} = c_j$; (b) $c \in \mathit{LIVE}$ exactly when $c = c_j$ for an allocation $j$ that is live, and then $\mathit{LIVE}[c] = B_j$.

*Proof.* By induction on the number of operations. Before the first one there is no pointer and $\mathit{LIVE}$ is empty, so (a) and (b) hold. Assume both hold before an operation.

- ALLOC$(n)$, allocation $j$. Line L1 picks $B_j = [b_j, b_j + n)$. Line L2 picks a number $c_j$ that was never issued, so it is not in $\mathit{LIVE}$ and it is distinct from the numbers of all other allocations. Line L3 adds $c_j \mapsto B_j$, which keeps (b), and line L4 returns $(b_j, b_j, e_j, c_j)$, which satisfies (a). Old pointers do not change.
- ADD$(p, k)$. If $p$ belongs to $j$, line L5 returns a pointer that belongs to $j$ and copies the three fields of $p$, which are those of $j$ by the hypothesis, so (a) holds for it. If $p$ is null, the result has the null fields $(0, 0, 0)$ and belongs to no allocation. $\mathit{LIVE}$ does not change.
- LOAD and STORE change no pointer and do not change $\mathit{LIVE}$.
- FREE$(p)$. If line L12 or line L13 reports an error, nothing changes. Otherwise $p.\mathit{value} = p.\mathit{base}$ and $p.\mathit{cap} \in \mathit{LIVE}$. By (b), $p.\mathit{cap} = c_j$ for a live $j$, and by (a) and the distinct numbers, $p$ belongs to that $j$. Line L14 deletes $c_j$ and allocation $j$ is now freed, so (b) holds again. No pointer field changes, so (a) holds. $\square$

**Theorem.** LOAD$(p, w)$ and STORE$(p, w, v)$ succeed exactly when the access is memory safe. Otherwise CHECK reports a spatial error for a spatial error and a temporal error for a temporal error.

*Proof.* Both operations run CHECK$(p, w)$ in line L10 before they touch memory in line L11.

If $p$ is null, then $p.\mathit{base} = p.\mathit{bound} = 0$, and for $w \ge 1$ either $p.\mathit{value} < 0$ or $p.\mathit{value} + w > 0$, so line L6 is true and line L7 reports a spatial error.

If $p$ belongs to $j$, Lemma 1(a) gives $[p.\mathit{base}, p.\mathit{bound}) = B_j$. Line L6 is false exactly when $b_j \le p.\mathit{value}$ and $p.\mathit{value} + w \le e_j$, that is, exactly when the $w$ bytes lie in $B_j$. So line L7 reports a spatial error exactly in the spatial case. If the bytes lie in $B_j$, line L8 tests $c_j \in \mathit{LIVE}$, which by Lemma 1(b) holds exactly when $j$ is live. So line L9 reports a temporal error exactly in the temporal case, and otherwise CHECK returns and line L11 runs. $\square$

**Corollary (FREE).** FREE$(p)$ succeeds exactly when $p$ belongs to a live allocation $j$ and $p.\mathit{value} = b_j$. A second FREE of any copy of $p$ reports a temporal error.

*Proof.* Line L12 passes exactly when $p.\mathit{value} = p.\mathit{base}$, which by Lemma 1(a) is $b_j$ for the allocation $j$ of $p$. Line L13 passes exactly when $c_j \in \mathit{LIVE}$, which by Lemma 1(b) holds exactly when $j$ is live. After a successful FREE, $c_j$ is not in $\mathit{LIVE}$ and is never issued again, so a second FREE of any pointer that belongs to $j$ fails line L13. $\blacksquare$

**Termination.** Every operation runs a bounded number of lines, except the search of the allocator in line L1, which scans a finite list of holes once.

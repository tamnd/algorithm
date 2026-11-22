---
title: Every access that SoftBound allows stays inside one object
proves: [correctness, invariant]
status: full
---

**Setting.** The program runs a finite sequence of the operations of the main block. It makes pointers only with ALLOC, ADD, FIELD, LOADPTR and INT-TO-PTR, and it cannot write the bounds of a pointer in a register. Objects are never freed, and the allocator returns blocks that do not overlap. A range $[x, y)$ is *valid* if $x = y$ (empty) or $[x, y) \subseteq O$ for the block $O = [b, b + n)$ of some object that ALLOC returned.

**Lemma 1 (invariant V).** After each operation, (a) every pointer the program holds in a register has valid bounds $[p.\mathit{base}, p.\mathit{bound})$, and (b) every entry $\mathit{META}[a] = (x, y)$ has $[x, y)$ valid.

*Proof.* By induction on the number of operations. At the start there are no pointers and $\mathit{META}$ is empty. Assume (a) and (b) before an operation.

- ALLOC returns the bounds $[b, b + n)$ of its own block in line L2, which is valid.
- ADD copies the bounds of $p$ in line L3, valid by (a).
- FIELD in line L4 returns $[\mathit{lo}, \mathit{hi})$ with $\mathit{lo} = \max(v, p.\mathit{base})$ and $\mathit{hi} = \max(\mathit{lo}, \min(v + \mathit{size}, p.\mathit{bound}))$. If $\mathit{hi} = \mathit{lo}$ the range is empty. Otherwise $p.\mathit{base} \le \mathit{lo} < \mathit{hi} \le p.\mathit{bound}$, so the range is a part of $[p.\mathit{base}, p.\mathit{bound})$, which is valid and not empty, so it lies in one block, and so does the part.
- INT-TO-PTR returns the empty bounds in line L16.
- STOREPTR$(loc, q)$ sets $\mathit{META}[loc]$ to the bounds of $q$ in line L11, valid by (a). Other entries do not change.
- LOADPTR returns the bounds of an entry of $\mathit{META}$ in line L14, valid by (b), or the empty bounds.
- LOAD and STORE do not change any bounds or any entry. $\square$

**Theorem.** If LOAD$(p, w)$, STORE$(p, w, v)$, STOREPTR$(p, q)$ or LOADPTR$(p)$ completes, with $w = W$ for the last two, then the bytes $[p, p + w)$ lie inside the block of one object.

*Proof.* Each of these runs CHECK$(p, w)$ first, in line L7, L9 or L12, and touches memory only after it. CHECK passes only if line L5 is false, that is, $p.\mathit{base} \le p$ and $p + w \le p.\mathit{bound}$. As $w \ge 1$, the range $[p.\mathit{base}, p.\mathit{bound})$ is not empty, and by Lemma 1(a) it lies in the block of one object. So $[p, p + w) \subseteq [p.\mathit{base}, p.\mathit{bound}) \subseteq O$. $\blacksquare$

**Corollary (exactness for tracked pointers).** Let $p$ be made from the block $[b, b + n)$ by ALLOC followed by ADD and FIELD steps only, possibly through STOREPTR and LOADPTR at a location whose entry was not overwritten in between. Then the bounds of $p$ are the bounds that the same steps compute on $[b, b + n)$ without the table, and CHECK passes exactly when the access lies in them.

*Proof.* ADD and FIELD compute the new bounds from the old ones only. STOREPTR at $loc$ writes the bounds of $q$ to $\mathit{META}[loc]$ and a later LOADPTR at the same $loc$, with no STOREPTR to $loc$ in between, reads them back in line L14; LOAD and STORE do not change the table. So the bounds of $p$ are the computed ones, and CHECK in line L5 is exactly the test that $[p, p + w)$ lies in them. $\square$

**Termination.** Every operation runs a bounded number of lines.

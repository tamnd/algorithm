---
title: Free nullifies every traced heap pointer that still points into the object
proves: [correctness, invariant]
status: full
---

**Setting.** The program runs a finite sequence of the operations ALLOC, FREE, STORE-PTR (which runs TRACE and then writes the word), integer STORE, and loads. Pointers are stored at word-aligned addresses, so two stored words never overlap. For a live object $o$, a location $\ell$ is *linked* to $o$ if the last STORE-PTR at $\ell$ ran while $\ell$ lay in a live heap object $s$, stored a value inside $o$, and both $s$ and $o$ have stayed live since then. Write $\mathit{rel}(\ell) = o$ in that case.

**Lemma 1 (invariant R).** After each operation, for every live object $o$ and every location $\ell$: $\ell \in o.\mathit{in}$ if and only if $\mathit{rel}(\ell) = o$; and $s.\mathit{out}[\ell] = o$ if and only if $\ell$ lies in the live object $s$ and $\mathit{rel}(\ell) = o$. No set holds a location in a freed object or names a freed target.

*Proof.* By induction on the number of operations. At the start there are no objects. Assume R before an operation.

- ALLOC. Line L6 inserts a new object with empty sets. No location was linked to it, since it was not live, and no location inside it was linked to anything, since the block was free and no live object held it. R holds.
- STORE-PTR$(\ell, v)$. If $\ell$ is in no live heap object, line L1 returns and $\mathit{rel}$ does not change, because $\ell$ was not linked (it was in no live object). Otherwise let $s$ be its object. The store replaces the old relation of $\ell$: line L2 removes $\ell$ from $s.\mathit{out}$ and from the in-set of the old target, which by R is exactly where it was. Line L3 finds the object $d$ that holds $v$. If there is none, $\ell$ is now linked to nothing, and line L4 returns. Otherwise $\mathit{rel}(\ell) = d$, and line L5 records it in both sets. Other locations do not change, because stored words do not overlap.
- Integer STORE and loads change no relation and no set. The relation is defined by the last pointer store, so an integer store does not remove it.
- FREE$(p)$ with $o$ the object at $p$. After the free, no location is linked to $o$, and no location inside $o$ is linked to anything. Lines L9 and L10 remove each $\ell \in o.\mathit{in}$ from the out-set of its source, which by R is the only other set that holds $\ell$ with target $o$. Line L12 removes each $\ell \in o.\mathit{out}$ from the in-set of its target, which by R is the only in-set that holds it. Line L13 deletes $o$ and its sets. Relations between other live objects do not change. $\square$

**Theorem.** Let FREE$(p)$ free the object $o = [b, e)$. Afterwards, every location $\ell$ with $\mathit{rel}(\ell) = o$ before the free holds NULLIFY if its word lay in $[b, e)$, and holds its old word otherwise. No other location changes, apart from the release of the block.

*Proof.* By Lemma 1, the set $o.\mathit{in}$ that line L9 visits is exactly the set of locations linked to $o$. For each of them, line L11 reads the current word and writes NULLIFY only if the word lies in $[b, e)$. Line L11 writes only to locations in $o.\mathit{in}$, and since stored words do not overlap, each write changes only its own word, so the order of the loop does not matter. Lines L10, L12 and L13 change only the sets and the tree. $\blacksquare$

**Corollary.** If the program loads a pointer from a heap location that it last wrote with a traced pointer into $o$ before $o$ was freed, it gets NULLIFY, and a load or a store through it at an offset below the size of the null page faults. A FREE through it is a free of null and does nothing. Pointers in registers, on the stack or in globals are not linked, so the theorem says nothing about them, and the tests show that such copies stay dangling.

**Termination.** TRACE and ALLOC run a bounded number of lines plus one search of a finite list. FREE runs its two loops once over finite sets, and no line adds to the set that the loop visits.

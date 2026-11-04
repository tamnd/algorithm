---
title: The real-time queue implements a persistent queue with O(1) worst-case operations
proves: [correctness]
status: full
---

**Values.** A stream denotes a finite sequence: the empty stream denotes $\langle \rangle$, and a stream whose suspension yields the cell $(x, t)$ denotes $\langle x \rangle \cdot \text{val}(t)$. Forcing a suspension does not change what it denotes, because the stored cell is the one its code yields. Write $|t|$ for the length of $\text{val}(t)$. For a list $r$ write $\text{rev}(r)$ for its items in reverse order. The items of a queue $q = (f, r, s)$ are $\text{items}(q) = \text{val}(f) \cdot \text{rev}(r)$.

**Lemma 1 (rotate).** If $|r| = |f| + 1$, then ROTATE$(f, r, a)$ denotes $\text{val}(f) \cdot \text{rev}(r) \cdot \text{val}(a)$.

*Proof.* By induction on $|f|$. If $f$ is empty, then $r = [y]$ and the result is $\langle y \rangle \cdot \text{val}(a)$, which is right. Otherwise $f$ yields $(x, f')$ with $|f'| = |f| - 1$, and $r = y :: r'$ with $|r'| = |f'| + 1$. The result is $\langle x \rangle$ followed by ROTATE$(f', r', y :: a)$, which by induction denotes $\text{val}(f') \cdot \text{rev}(r') \cdot \langle y \rangle \cdot \text{val}(a) = \text{val}(f') \cdot \text{rev}(r) \cdot \text{val}(a)$. $\square$

**Invariant.** Call $q = (f, r, s)$ *good* if (I1) $|s| = |f| - |r|$ and (I2) $s$ is a suffix of $f$ (the same stream object reached after $|f| - |s|$ tails) and every cell of $f$ before $s$ is forced.

**Lemma 2 (exec).** Let $f$ and $s$ satisfy (I2) for $f$, and let $|s| = |f| - |r| + 1$. Then EXEC$(f, r, s)$ returns a good queue with the same items as $\text{val}(f) \cdot \text{rev}(r)$.

*Proof.* If $s$ yields a cell (line L2), then the result is $(f, r, s')$ with $s'$ the tail of $s$, so $|s'| = |f| - |r|$, which is (I1). The head cell of $s$ is now forced, so every cell of $f$ before $s'$ is forced, which is (I2). The items are unchanged. If $s$ is empty (line L3), then $|f| = |r| - 1$, and by (I2) all of $f$ is forced. By Lemma 1, $f' = $ ROTATE$(f, r, \text{empty})$ denotes $\text{val}(f) \cdot \text{rev}(r)$, so the result $(f', \text{nil}, f')$ has the same items, $|s| = |f'| = |f'| - 0$, and $s = f'$ is a suffix of itself with no cells before it. $\square$

**Theorem 1 (correctness and persistence).** Every queue made by the operations is good, and its items are those that the abstract queue gives to it. FRONT and POP return the first item. No operation changes the items of an existing version.

*Proof.* The empty queue is good. Let $q = (f, r, s)$ be good. PUSH calls EXEC with $f$, $x :: r$ and $s$; then $|s| = |f| - |r| = |f| - |x :: r| + 1$, and (I2) holds for $f$ and $s$, so by Lemma 2 the result is good with items $\text{val}(f) \cdot \text{rev}(r) \cdot \langle x \rangle$, which is $\text{items}(q)$ with $x$ at the back. For FRONT and POP, if $q$ is not empty then $|f| \ge 1$, because $|f| \ge |r|$ by (I1) and $|f| + |r| \ge 1$. So $f$ yields $(x, f')$ and $x$ is the first item. POP calls EXEC with $f'$, $r$ and $s$. By (I1) and (I2), $s$ is a suffix of $f$ of length $|f| - |r|$. If $|s| < |f|$, then $s$ is also a suffix of $f'$, the cells of $f'$ before $s$ are cells of $f$ before $s$ and so are forced, and $|s| = |f'| - |r| + 1$; Lemma 2 applies. If $|s| = |f|$, then $s = f$ and $|r| = 0$; EXEC finds that $s$ yields the cell $(x, f')$ (line L2) and returns $(f', \text{nil}, f')$, which is good. The items are $\text{val}(f') \cdot \text{rev}(r)$, which is $\text{items}(q)$ without $x$. No procedure writes a cell, and forcing does not change values, so old versions keep their items. $\square$

**Theorem 2 (worst-case time).** Each operation forces at most two suspensions that were not forced before, and each such force does $O(1)$ work.

*Proof.* FRONT and POP force the head of $f$. If $|s| < |f|$, that head is before $s$ and is forced by (I2). If $s = f$, it may be unforced, and forcing it is one step. EXEC forces the head of $s$, at most one step. A step of ROTATE$(f, r, a)$ forces the head of its argument $f$ and makes $O(1)$ cells. For the outermost call made in line L3, the argument is fully forced by (I2), since $|s| = 0$ there. The inner calls receive tails of that same fully forced stream. So every step forces only cells that are already forced, which costs $O(1)$ each, and builds $O(1)$ new cells. A suspension shared by several versions is evaluated once, and later forces return the stored cell in $O(1)$. Hence each operation costs $O(1)$ in the worst case, on every version. $\blacksquare$

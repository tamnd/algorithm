---
title: Sliding mark-compact keeps exactly the reachable objects, packs them in order, and rewrites every pointer
proves: [correctness, termination]
status: full
---

**Setting.** The heap is an array of words. The objects lie one after another from address $0$ to $\mathit{top}$; an object $a$ has its size $\sigma(a) \ge 1$ in word $a$ and its fields in the words $a + 1$ to $a + \sigma(a) - 1$, each the address of an object or nil. The roots are a list of slots, each nil or the address of an object. Let $R$ be the set of objects reachable from the roots.

Let $x_1 < \cdots < x_k$ be the objects of $R$ in address order, and define $\varphi(x_i) = \sum_{j < i} \sigma(x_j)$ and $S = \sum_{j \le k} \sigma(x_j)$.

**Claim.** MARK-COMPACT terminates. At the end, for each $i$, the words $\varphi(x_i)$ to $\varphi(x_i) + \sigma(x_i) - 1$ hold $\sigma(x_i)$ and the fields of $x_i$ with each non-nil $v$ replaced by $\varphi(v)$; each root that held $x$ holds $\varphi(x)$; $\mathit{top} = S$; and no mark is set. So the graph reachable from the roots is the same up to the renaming $\varphi$, the order of the objects is kept, and the free space is the one block from $S$ up.

**Phase 1: mark (line L1).** This is the mark phase of [mark-and-sweep](/mark-and-sweep/) with an explicit stack. Each object is pushed at most once, when it is marked, so the phase ends. Every marked object is reachable, because an object is marked only as a root or as a field of a marked object. Every reachable object is marked: take a path from a root to it; the root is marked at the start, and when a marked object is popped, every field of it gets marked; each marked object is pushed and so popped before the stack is empty, so by induction along the path every object on it is marked. So the marked set is $R$. Every non-nil field of an object of $R$ is in $R$.

**Phase 2: compute locations (lines L2 to L4).** The loop visits the marked objects in address order with a running sum, so it stores $F[x_i] = \varphi(x_i)$ for each $i$ and ends with $\mathit{free} = S$. It writes only to the table $F$.

**Phase 3: update references (lines L5 and L6).** Each non-nil root is in $R$ and is replaced by $F$ of it, which is $\varphi$ of it. Each non-nil field $v$ of a marked object is in $R$ and is replaced by $\varphi(v)$. Each word is rewritten once, and the size words and the table do not change. So after phase 3 each object $x_i$ holds, at its old address, its *image*: its size and its fields mapped by $\varphi$.

**A basic fact.** $\varphi(x_i) \le x_i$, because $x_1, \ldots, x_{i-1}$ lie below $x_i$ without overlap, so their sizes add up to at most $x_i$. Also $\varphi(x_i) + \sigma(x_i) = \varphi(x_{i+1})$, so the targets $[\varphi(x_i), \varphi(x_i) + \sigma(x_i))$ are disjoint and follow each other.

**Phase 4: relocate (lines L7 and L8).** We show by induction on $i$ that, after the move of $x_i$, the target of each of $x_1, \ldots, x_i$ holds its image, and every word at or above $x_i + \sigma(x_i)$ holds its value from the end of phase 3. Before the first move, nothing has changed. Consider the move of $x_i$. The earlier moves wrote only into the targets of $x_1, \ldots, x_{i-1}$, which end at $\varphi(x_i) \le x_i$; so the words of $x_i$ still hold its image. The move copies word $x_i + t$ to $\varphi(x_i) + t$ for $t = 0, 1, \ldots$ in increasing order. A write to $\varphi(x_i) + t'$ with $t' < t$ cannot hit the word $x_i + t$ that is read later, because $\varphi(x_i) + t' < x_i + t$. So the copy places the image of $x_i$ in its target. The target of $x_i$ is disjoint from the earlier targets, so they keep their images, and it ends at $\varphi(x_i) + \sigma(x_i) \le x_i + \sigma(x_i)$, so the words from $x_i + \sigma(x_i)$ up are unchanged. Line L8 also clears the mark of $x_i$.

After the last move every target holds its image, every mark of $R$ is cleared, and no other object was marked. Line L9 sets $\mathit{top} = S$. Every loop runs over a finite list, so the algorithm terminates. $\blacksquare$

---
title: Cheney's collector copies exactly the reachable objects in breadth-first order and rewrites every pointer
proves: [correctness, termination]
status: full
---

**Setting.** At line L1 the objects of the program lie in from-space. An object $x$ has its size $\sigma(x) \ge 1$ in its header word and its fields after it, each an object of from-space or nil. Let $R$ be the set of objects reachable from the roots. To-space has $S$ words and starts at $t$; all of $R$ fits in it, because it fitted in from-space, which also has $S$ words.

Define the *breadth-first order* $q_1, q_2, \ldots, q_k$ of $R$ as follows: first the distinct non-nil roots in the order of the root slots; then, for $i = 1, 2, \ldots$, the fields of $q_i$ in order, each one appended if it is not already in the list. This is a [breadth-first search](/breadth-first-search/) from the roots with a first-in, first-out queue.

**Claim.** COLLECT terminates. At the end, the copies of $q_1, \ldots, q_k$ lie in to-space in this order, one after another from $t$ to $\mathit{free} = t + \sum_i \sigma(q_i)$. Writing $\varphi(x)$ for the address of the copy of $x$, each copy $\varphi(x)$ holds $\sigma(x)$ and $\varphi(v)$ in place of each non-nil field $v$ of $x$, and each root that held $x$ holds $\varphi(x)$.

**FORWARD.** As in the [semispace collector](/copying-collection/), FORWARD on a non-nil $p$ returns $\varphi(p)$ at once if the header of $p$ holds a forwarding address (line L6). Otherwise it copies the $\sigma(p)$ words of $p$ to $\mathit{free}$ (line L7), advances $\mathit{free}$, and writes the forwarding address into the header of $p$ (line L8). It writes nothing else in from-space, and its only write in to-space is the new copy at the old $\mathit{free}$. So each object is copied at most once, and its fields in from-space stay unchanged.

**The invariant.** At line L3, let $c_1, c_2, \ldots, c_m$ be the copies in to-space in address order. Then:

- (B1) the copies fill the words from $t$ to $\mathit{free}$ one after another, and $\mathit{scan}$ is the start of some $c_j$ or equals $\mathit{free}$;
- (B2) a copy below $\mathit{scan}$ holds the size of its original and $\varphi(v)$ for each non-nil field $v$; a copy at or above $\mathit{scan}$ holds the size and the original fields;
- (B3) the originals of $c_1, \ldots, c_m$ are $q_1, \ldots, q_m$, in this order, and every forwarded object is one of them;
- (B4) the copies below $\mathit{scan}$ are the copies of $q_1, \ldots, q_s$ for some $s$, and the list $q_1, \ldots, q_m$ is the breadth-first list built up to the end of the scan of $q_s$;
- (B5) each root that held $x$ holds $\varphi(x)$.

*Initialization.* Line L2 forwards the roots in order. A root seen for the first time is copied to $\mathit{free}$; a repeated root finds its forwarding address. So the copies are those of the distinct roots in order, which is the start of the breadth-first list, with $s = 0$ and $\mathit{scan} = t$. All facts hold.

*Maintenance.* Let $\mathit{scan} < \mathit{free}$; by (B1) and (B4) the copy at $\mathit{scan}$ is that of $q_{s+1}$, and by (B2) it holds the original fields of $q_{s+1}$. Line L4 forwards these fields in order. A field that is already forwarded is in the list, by (B3), and gets its $\varphi$. A field that is not forwarded is not in the list, by (B3), and is copied to $\mathit{free}$, which appends it to the list. This is exactly the step of the breadth-first list for $q_{s+1}$. Each field of the copy now holds $\varphi$ of the original field. Line L5 moves $\mathit{scan}$ past this copy, to the next copy or to $\mathit{free}$. So (B1) to (B4) hold with $s + 1$. Since $q_{s+1} \in R$, its fields are in $R$, so all copies are of objects in $R$. The roots are not touched, so (B5) holds.

**Termination.** Each iteration moves $\mathit{scan}$ forward by $\sigma \ge 1$ words. The value of $\mathit{free}$ grows only when an object is copied, and each of the finitely many objects is copied at most once, so $\mathit{free} \le t + \sum_{x \in R} \sigma(x)$. So $\mathit{scan}$ reaches $\mathit{free}$ after finitely many iterations.

**Proof of the claim.** At the end $\mathit{scan} = \mathit{free}$. By (B4), every copy has been scanned, so the list $q_1, \ldots, q_m$ is the breadth-first list built to its end; that list contains every reachable object, because a breadth-first search from the roots finds every object on a path from a root. So $m = k$, the forwarded objects are exactly $R$, and their copies lie in breadth-first order from $t$ to $\mathit{free}$ by (B1) and (B3). By (B2) every copy holds $\varphi$ of each field, and by (B5) every root holds $\varphi$ of its old value. $\blacksquare$

---
title: The semispace collector copies exactly the reachable objects, once each, and rewrites every pointer
proves: [correctness, termination]
status: full
---

**Setting.** Before the flip, the objects of the program lie in one semispace, which becomes from-space at line L1. An object $x$ has its size $\sigma(x) \ge 1$ in its header word and its fields after it, each an object of from-space or nil. Let $R$ be the set of objects reachable from the roots. The other semispace, to-space, is empty and has $S$ words, and $\sum_{x \in R} \sigma(x) \le S$ because all of $R$ fits in from-space, which also has $S$ words.

**Claim.** COLLECT terminates. At the end there is an injective map $\varphi$ from $R$ into to-space such that the copies $\varphi(x)$, $x \in R$, fill the words from the start of to-space to $\mathit{free}$ with no gap, the copy at $\varphi(x)$ has size $\sigma(x)$ and has $\varphi(v)$ in place of each non-nil field $v$ of $x$, and each root that held $x$ holds $\varphi(x)$. No object outside $R$ is copied.

**The invariant.** Call an object of from-space *forwarded* when its header holds a negative value $-1 - b$, and set $\varphi(x) = b$. At line L3 the following hold.

- (C1) Each from-space object is either unforwarded, with its header and fields unchanged, or forwarded; a forwarded $x$ has its fields unchanged, and the words $\varphi(x)$ to $\varphi(x) + \sigma(x) - 1$ hold $\sigma(x)$ and one value for each field $v$ of $x$, which is $v$ itself if the copy is on the stack and $\varphi(v)$ otherwise.
- (C2) The stack holds each copy that has not been scanned, exactly once.
- (C3) The copies fill the words from the start of to-space to $\mathit{free}$, one after another, each in the order of its creation.
- (C4) Every forwarded object is in $R$, and every non-nil root holds $\varphi$ of its old value.

*FORWARD keeps (C1) to (C3).* Let FORWARD be called on $p \ne$ nil. If $p$ is forwarded, line L6 returns $\varphi(p)$ and changes nothing. Otherwise, line L7 copies the $\sigma(p)$ words of $p$, which are unchanged by (C1), to $\mathit{free}$ and advances $\mathit{free}$; line L8 overwrites only the header of $p$; line L9 pushes the copy. So $p$ is now forwarded, its copy holds its original fields and is on the stack, and the copy follows the earlier ones. This is (C1) to (C3) with one more forwarded object. $\varphi$ is injective, since each copy gets a fresh range of words.

*Initialization.* At line L2, each root is replaced by the result of FORWARD on it. A root is in $R$, so the forwarded objects are in $R$, and each root holds $\varphi$ of its old value. Nothing is scanned yet, so every copy is on the stack. So (C1) to (C4) hold at line L3.

*Maintenance.* Lines L4 and L5 pop a copy $b = \varphi(x)$, which holds the original fields of $x$ by (C1), and replace each non-nil field $v$ by the result of FORWARD on $v$, which is $\varphi(v)$. Since $x \in R$, also $v \in R$, so every newly forwarded object is in $R$. Now the copy $b$ is off the stack and holds $\varphi$ of each field, as (C1) asks. FORWARD keeps (C1) to (C3) for the other objects. So the invariant holds again at line L3.

**Termination.** An object is copied only when it is unforwarded, and then it becomes forwarded, so each object of from-space is copied at most once. Each copy is pushed once (line L9) and popped once (line L4), and each pop does a finite amount of work. So the loop ends.

**Every reachable object is copied.** Take $y \in R$ and a path from a root to $y$. The first object of the path is forwarded at line L2. If an object $x$ of the path is forwarded, its copy is pushed and later popped, since the loop ends only with an empty stack; when it is popped, line L5 calls FORWARD on each field of $x$, so the next object of the path is forwarded. By induction, $y$ is forwarded.

**Proof of the claim.** At the end the stack is empty, so by (C1) and (C2) every copy $\varphi(x)$ holds $\sigma(x)$ and $\varphi(v)$ for each non-nil field $v$ of $x$. By (C4) and the last paragraph, the forwarded objects are exactly $R$. By (C3) the copies fill the words from the start of to-space to $\mathit{free}$ with no gap, so $\mathit{free}$ minus the start is $\sum_{x \in R} \sigma(x) \le S$, and the copies never pass the end of to-space. By (C4) every root holds $\varphi$ of its old value. $\blacksquare$

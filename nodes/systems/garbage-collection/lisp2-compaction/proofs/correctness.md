---
title: The LISP 2 compactor slides the live objects down in order and rewrites every pointer
proves: [correctness, termination]
status: full
---

**Setting.** The heap is an array of words. The objects lie one after another from address $0$ to $\mathit{top}$: an object at $a$ has its size $\sigma(a) \ge 2$ in word $a$, a forwarding word at $a + 1$, and its fields in the words $a + 2$ to $a + \sigma(a) - 1$. So the next object starts at $a + \sigma(a)$, and a scan that starts at $0$ and adds the sizes visits every object. Let $M$ be the set of marked objects. As in every mark-compact collector, we assume that $M$ is closed under the fields and contains every non-nil root; the mark phase gives both, with $M$ the set of reachable objects.

Let $x_1 < x_2 < \cdots < x_m$ be the objects of $M$ in address order, and define
$$\varphi(x_i) = \sum_{j < i} \sigma(x_j), \qquad S = \sum_{j \le m} \sigma(x_j).$$

**Claim.** COMPACT terminates. At the end, for each $i$, the words $\varphi(x_i)$ to $\varphi(x_i) + \sigma(x_i) - 1$ hold the object $x_i$ with each non-nil field $v$ replaced by $\varphi(v)$, each root that held $x$ holds $\varphi(x)$, $\mathit{top} = S$, and no object is marked. Since $\varphi$ is increasing and $\varphi(x_{i+1}) = \varphi(x_i) + \sigma(x_i)$, the live objects keep their order and fill the words $0$ to $S - 1$ with no gap.

**A basic fact.** For each $i$, $\varphi(x_i) \le x_i$. The objects $x_1, \ldots, x_{i-1}$ lie in the words below $x_i$ and do not overlap, so their sizes add up to at most $x_i$.

**Termination.** Each of the three loops starts at $0$ and adds $\sigma(a) \ge 2$ to $a$ until $a \ge \mathit{top}$. It reads the size of $a$ from word $a$. Lemmas 1 to 3 show that this word still holds $\sigma(a)$ when it is read, so each loop visits exactly the objects, in address order, and stops.

**Lemma 1 (pass 1, lines L1 to L4).** After pass 1, the forwarding word of each $x_i$ holds $\varphi(x_i)$, and $\mathit{free} = S$.

*Proof.* Pass 1 writes only forwarding words, so the size words stay correct and the scan visits every object. The invariant is: when the scan is at the object $a$, the value of $\mathit{free}$ is the sum of the sizes of the marked objects below $a$. It holds at $a = 0$ with $\mathit{free} = 0$. If $a = x_i$ is marked, $\mathit{free} = \varphi(x_i)$ by the invariant and the definition of $\varphi$; line L4 stores this value and adds $\sigma(x_i)$, which keeps the invariant at the next object. If $a$ is not marked, nothing changes and the invariant holds at the next object too. At the end, $\mathit{free}$ is the sum of the sizes of all marked objects, $S$. $\square$

**Lemma 2 (pass 2, lines L5 to L7).** After pass 2, each root that held $x$ holds $\varphi(x)$, and each non-nil field $v$ of each marked object holds $\varphi(v)$. The size words and the forwarding words do not change.

*Proof.* Pass 2 writes only roots and the field words of marked objects, never a size word or a forwarding word. So the scan still visits every object, and the forwarding words still hold the values of Lemma 1. A non-nil root or field $v$ is in $M$ by the closure assumption, so line L5 or L7 reads the forwarding word of $v$, which is $\varphi(v)$ by Lemma 1. Each field word is visited once, so it is rewritten once. $\square$

**Lemma 3 (pass 3, lines L8 to L10).** Call the words $\varphi(x_i)$ to $\varphi(x_i) + \sigma(x_i) - 1$ the *target* of $x_i$, and call the content of the words of $x_i$ after pass 2 the *image* of $x_i$. When the scan of pass 3 is at the object $a$:

- (P1) for every marked $x_i < a$, the target of $x_i$ holds the image of $x_i$;
- (P2) every word at or above $a$ holds its value from the end of pass 2.

*Proof.* At $a = 0$ no word has changed. Suppose (P1) and (P2) hold at $a$. By (P2) the word $a$ still holds $\sigma(a)$, so the scan finds the next object correctly. If $a$ is not marked, pass 3 writes nothing, and both facts hold at $a + \sigma(a)$. If $a = x_i$ is marked, the forwarding word $a + 1$ still holds $\varphi(x_i)$ by (P2), and line L10 copies the words $a + t$ to $\varphi(x_i) + t$ for $t = 0, 1, \ldots, \sigma(x_i) - 1$ in this order.

- *The copy reads the image.* When word $a + t$ is read, the earlier writes of this copy went to $\varphi(x_i) + t'$ with $t' < t$, and $\varphi(x_i) + t' < x_i + t$ by the basic fact. All writes of earlier copies went to targets of earlier objects, which end at $\varphi(x_i) \le x_i$. So the word $a + t$ still holds its value from the end of pass 2.
- *The copy keeps the earlier targets.* The targets of $x_1, \ldots, x_i$ are disjoint, because each one ends where the next one starts. So the copy of $x_i$ does not change the target of an earlier object, and (P1) holds for $x_1, \ldots, x_i$.
- *The copy keeps the words above.* The copy writes only below $\varphi(x_i) + \sigma(x_i) \le x_i + \sigma(x_i)$, the start of the next object. So (P2) holds there.

$\square$

**Proof of the claim.** At the end of pass 3, (P1) holds for every marked object, so the target of each $x_i$ holds its image: the size $\sigma(x_i)$, a forwarding word, and by Lemma 2 the fields with each non-nil $v$ replaced by $\varphi(v)$. The roots hold $\varphi$ of their old values by Lemma 2, and pass 3 does not touch them. Line L9 clears the mark of each marked object, and no other object was marked, so no mark is left. Line L11 sets $\mathit{top} = \mathit{free} = S$ by Lemma 1. $\blacksquare$

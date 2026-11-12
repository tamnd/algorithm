---
title: Garbage-First keeps complete remembered sets, keeps every reachable object across pauses and markings, and its greedy choice loses at most one region of garbage
proves: [correctness]
status: full
---

We use the heap model and the procedures of the page, with the restriction of the model: a pause does not overlap a marking (a pause first finishes the marking). Each mutator operation with its barriers is one atomic step, and so is each marking step. Objects are named by identity; a copy has the identity of its original.

**Invariant H.** At the end of every step: (a) every root and every field of every object in the heap is nil or the address of an object in the heap; (b) for every object $x$ and field $f$ with $y = x.f$ in a region other than that of $x$, the slot $(x, f)$ is in $\textit{RS}(\text{region}(y))$.

**Lemma 1 (the mutator keeps H).** A load and a register copy change only roots, with values taken from roots or fields, so (a) holds. A store writes a root value, so (a) holds, and line L3 adds the slot when it crosses regions, so (b) holds. A new object has nil fields. $\square$

**Lemma 2 (a pause keeps H and the graph).** Let $\textit{CS}$ be the collection set. After the pause, H holds and the graph reachable from the roots is the same, by identity, as before it.

*Proof.* Call a pointer *external* if it is held by a root or by an object outside $\textit{CS}$, and points into $\textit{CS}$. Line L9 replaces every external root pointer by the address of a copy. By H(b) before the pause, every external field pointer is a slot in the remembered set of its target region; line L10 visits that slot, line L11 finds that it points into $c$, and replaces it by the address of a copy. Every copy is put on the queue once (line L16), and line L13 replaces each of its fields that points into $\textit{CS}$ by a copy. EVACUATE copies each object at most once (line L15), with the same identity and the same fields. So after line L13 no root and no field of an object outside $\textit{CS}$ or of a copy points into $\textit{CS}$, and line L14 frees only objects that nothing points to: H(a) holds. Every pointer was replaced by the address of a copy of the same object, so the graph is the same. For H(b): the slots of objects outside $\textit{CS}$ whose target moved get an entry for the new region at line L11; the fields of copies get entries at line L13; other slots did not change, and their entries are in remembered sets of regions outside $\textit{CS}$, which are kept. Freeing a region removes only entries whose source or target is gone. $\square$

**Lemma 3 (the snapshot).** Let $G_0$ be the set of objects reachable when marking starts. When the queues are empty at the end of marking, every object of $G_0$ is marked.

*Proof.* This is the argument of [snapshot-at-the-beginning](/snapshot-at-the-beginning/). Take $z \in G_0$ and a path from a snapshot root to $z$ as it was at the start. Every object on the path is below TAMS. Each pointer of the path is either still in the heap, or was overwritten by a store; that store ran line L1 while marking, and logged the old target. So the first unmarked object on the path is on the mark stack or in the SATB queue, or is the target of a pointer that was overwritten and logged, or of a pointer of a marked object; a marked object pushed all its fields when it was marked (line L4), as they were then, and a later change of such a field was logged. Marking only ends when the stack and the queue are empty, so the path is marked to its end. $\square$

**Lemma 4 (cleanup frees no reachable object).** At the end of marking, every object reachable from the roots is marked or above TAMS.

*Proof.* Take a reachable object $z$ below TAMS. It existed at the start of marking. A path from a root to $z$ at the end goes through objects that are either in $G_0$, or were allocated during marking (above TAMS). A pointer from an object above TAMS, or from a register, was copied from a register at some time during marking. Follow the path back from $z$ to its last object $w$ that was reachable at the start: by induction on the time of the stores, the value of each pointer stored during marking was reachable when it was stored, and an object below TAMS that is reachable at any time during marking was reachable at the start (no allocation can make an old object reachable). So $z \in G_0$, and by Lemma 3 it is marked. $\square$

So cleanup removes only unreachable objects. Every object that remains was marked or new, and a marked or new object points only to marked or new objects (its fields hold values that were reachable when stored), so H(a) still holds; cleanup removes the slots of removed objects from the remembered sets, and H(b) still holds.

**Theorem.** In every run, H holds after every step, and the graph reachable from the roots is the same, by identity, as in a heap with no collector.

*Proof.* By induction on the steps, with Lemmas 1, 2 and 4. Marking steps change no root and no field. $\blacksquare$

**The choice of the collection set.** Let the old candidates have garbage $g_i$ and cost $c_i$, with budget $b$, and let lines L6 to L8 take the regions $1, \ldots, k$ in ratio order and stop at region $k + 1$. Then $\textit{OPT} \le \sum_{i \le k} g_i + g_{k+1}$.

*Proof.* The fractional knapsack with the same data has an optimum at least $\textit{OPT}$, and the greedy rule by ratio is optimal for it: it takes $1, \ldots, k$ and the fraction $(b - \sum_{i \le k} c_i)/c_{k+1} < 1$ of region $k + 1$. So $\textit{OPT} \le \sum_{i \le k} g_i + g_{k+1}$. $\square$

The bound does not give a constant factor: in the page's example, $g_{k+1} = 90$ and the greedy set reclaims 10. The greedy rule is a heuristic for an NP-hard choice, and the page makes no claim that it is optimal.

---
tag: 21VA27
kind: definition
slug: tp1-tp2-conditions
name: TP1 and TP2 conditions
aliases:
- transformation property 1
- transformation property 2
area: distributed/replication-and-crdts
level: research
summary: Two conditions on an OT transformation function. TP1 makes two concurrent edits end in one state, and TP2 makes a third edit transform the same way along both paths.
prereqs: [operational-transformation, happened-before]
see_also: [operational-transformation, collaborative-text-editing, rga, crdt, strong-eventual-consistency, total-order-broadcast]
sources:
  - paper: doi:10.1145/240080.240305
    title: Matthias Ressel, Doris Nitsche-Ruhland and Rul Gunzenhäuser, An integrating, transformation-oriented approach to concurrency control and undo in group editors, CSCW 1996
    locator: pages 288 to 297, the transformation properties TP1 and TP2, the adOPTed algorithm, and its convergence when the transformation function meets both
  - paper: doi:10.1007/978-94-010-0068-0_15
    title: Abdessamad Imine, Pascal Molli, Gérald Oster and Michaël Rusinowitch, Proving correctness of transformation functions in real-time groupware, ECSCW 2003
    locator: pages 277 to 293, the check of published transformation functions against TP1 and TP2 with the SPIKE theorem prover, the counterexamples, and the new functions
  - paper: doi:10.4204/EPTCS.107.5
    title: Aurel Randolph, Hanifa Boucheneb, Abdessamad Imine and Alejandro Quintero, On consistency of operational transformation approach, EPTCS 107, 2013
    locator: pages 45 to 59, which known functions meet TP1 and TP2 (Figures 11 and 12 for the TP2 counterexamples), and the controller synthesis result
  - paper: doi:10.1145/274444.274447
    title: Chengzheng Sun, Xiaohua Jia, Yanchun Zhang, Yun Yang and David Chen, Achieving convergence, causality preservation, and intention preservation in real-time cooperative editing systems, ACM TOCHI 5(1), 1998
    locator: pages 63 to 108, the GOT algorithm, which transforms in one total order with undo and redo, and the exclusion transformation
  - paper: doi:10.1145/289444.289469
    title: Chengzheng Sun and Clarence Ellis, Operational transformation in real-time group editors, issues, algorithms, and achievements, CSCW 1998
    locator: the GOTO algorithm and the role of the two transformation properties in it
  - paper: doi:10.1145/215585.215706
    title: David A. Nichols, Pavel Curtis, Michael Dixon and John Lamping, High-latency, low-bandwidth windowing in the Jupiter collaboration system, UIST 1995
    locator: pages 111 to 120, the two-party protocol with a central server, which transforms edits only in a two-dimensional state space
---

TP1 and TP2 are two conditions on the transformation function $T$ of [operational transformation](/operational-transformation/). Ressel, Nitsche-Ruhland and Gunzenhäuser stated them in 1996. TP1 says that two concurrent edits, each applied after the other has been transformed against it, give the same state in either order. TP2 says that a third concurrent edit, transformed along the two orders, becomes the same edit. A control algorithm that may transform an edit along any path through the concurrent edits, such as their adOPTed, converges when $T$ meets both. TP1 is easy to meet for text. TP2 is not: Imine, Molli, Oster and Rusinowitch (2003) checked published functions with a theorem prover and found counterexamples, and Randolph, Boucheneb, Imine and Quintero (2013) showed that no function of the usual form meets both conditions.

## Definition

**Setting.** There is a set of states and a set of edits, with $s \cdot o$ the state after edit $o$ runs on state $s$, and $s \cdot o_1 \cdot o_2$ for two edits in a row. Two edits are *defined on the same state* if they were made on that state. For edits $a$ and $b$ defined on the same state $s$, the transformation $T(a, b)$ is an edit defined on $s \cdot b$ that has the effect of $a$ there. For a list of edits, transform one at a time: $T(c, [x, y]) = T(T(c, x), y)$.

**TP1.** For every state $s$ and all edits $a$ and $b$ defined on $s$:
$$s \cdot a \cdot T(b, a) = s \cdot b \cdot T(a, b).$$

**TP2.** For every state $s$ and all edits $a$, $b$ and $c$ defined on $s$:
$$T(c, [a, T(b, a)]) = T(c, [b, T(a, b)]).$$

TP1 is an equation between states. TP2 is an equation between edits: both sides are edits defined on the state of TP1, and they must be the same edit, not only have the same effect on that state. The checks below, for a given $T$, are what the tests run.

```pseudo id=main
TP1(T, s, a, b)                                       ▷ a and b made on state s
L1  return s · a · T(b, a) = s · b · T(a, b)
TP2(T, a, b, c)                                       ▷ a, b and c made on the same state
L2  left ← T(T(c, a), T(b, a))
L3  right ← T(T(c, b), T(a, b))
L4  return left = right
```

**Why both are needed.** Draw the states as points and the edits as arrows. Two concurrent edits $a$ and $b$ on $s$ give a square, with $a$ then $T(b, a)$ on one side and $b$ then $T(a, b)$ on the other, and TP1 says the square closes (line L1). A third edit $c$ must then be carried to the far corner of the square. One site, which applied $a$ first, carries it along the first side, and another site along the second side (lines L2 and L3). If the two results differ, the sites apply different edits from the same state and diverge. TP2 says the two results are equal (line L4). Ressel et al. use TP1 and TP2 to show that transforming an edit along any path to the current state gives the same edit, which makes adOPTed converge.

**When TP2 is not needed.** A control algorithm can avoid TP2 by never carrying an edit along two different paths. In Jupiter (Nichols et al. 1995), all edits pass through one server, each link has two parties, and every transformation closes a square in a two-dimensional grid, so TP1 is enough. GOT (Sun et al. 1998) transforms every edit in one total order, with undo and redo. GOTO (Sun and Ellis 1998) works peer to peer without a fixed order and needs both conditions.

## Examples and non-examples

The examples use edits on strings: ins$(p, c, u)$ puts character $c$ at 0-based index $p$ and was made by user $u$, del$(p)$ removes the character at $p$, and nop does nothing. The first two counterexamples below are the first ones found by a search over small documents and edits, in a fixed order, so the tests reproduce them. The third is from Randolph et al. (2013).

**A function that fails TP1.** Let two inserts at one index move the second one right in both orders: $T(a, b)$ shifts $a$ right whenever $p(a) \ge p(b)$. On the empty string with $a = $ ins$(0, x, 1)$ and $b = $ ins$(0, y, 2)$:

| order | first edit | transformed second edit | state |
| --- | --- | --- | --- |
| $a$ then $T(b, a)$ | "x" | ins$(1, y)$ | "xy" |
| $b$ then $T(a, b)$ | "y" | ins$(1, x)$ | "yx" |

The fix of Ressel et al. orders two inserts at one index by user id, as in lines L2 and L3 of the [OT](/operational-transformation/) page. With it, the tests find no TP1 counterexample on any document over a two-letter alphabet of length at most 4.

**Ressel's function fails TP2.** The search finds this case on the document "a", with $a = $ ins$(1, x, 1)$, $b = $ del$(0)$ and $c = $ ins$(0, z, 3)$. Both orders of $a$ and $b$ reach the state "x", as TP1 asks.

| path | $c$ after the first edit | $c$ after the second edit | text |
| --- | --- | --- | --- |
| $a$, then $T(b, a) = $ del$(0)$ | ins$(0, z)$ | ins$(0, z)$ | "zx" |
| $b$, then $T(a, b) = $ ins$(0, x, 1)$ | ins$(0, z)$ | ins$(1, z)$, by the user id tie | "xz" |

The trouble is that after the delete, "z" and "x" are both inserts at index 0, so the tie rule decides by user id, while on the other path "z" was before "x" all along. The function has lost the fact that "x" was after the deleted "a".

**The counterexample of Randolph et al.** Their Figure 11 gives a TP2 counterexample for Ressel's function. In 0-based form on "xy": $o_1 = $ del$(0)$, $o_2 = $ ins$(1, c, 2)$ and $o_3 = $ ins$(0, e, 3)$. Both orders of $o_1$ and $o_2$ give "cy". Along the path through $o_1$, $o_3$ becomes ins$(1, e)$ and the text is "cey". Along the path through $o_2$, $o_3$ stays ins$(0, e)$ and the text is "ecy". The tests check both results.

**What Imine et al. (2003) show.** They wrote the transformation functions of the literature as rewrite rules and used the SPIKE theorem prover to check TP1 and TP2. For the published functions they examined, the prover found counterexamples, and they proposed new functions for which it found none.

**What Randolph et al. (2013) show.** With model checking, they test the known functions: those of Ellis and Gibbs and of Sun et al. fail TP1, Suleiman's fails both, and those of Ressel et al. and of Imine et al. meet TP1 but fail TP2 (their Figures 11 and 12). By controller synthesis they then show that no inclusion transformation function built on the classical parameters of an edit (its kind, its index and its character, with a user id for ties) meets both TP1 and TP2.

**A non-example of difficulty.** If all edits commute, for example increments of a counter, then $T(a, b) = a$ meets TP1 and TP2 at once. The conditions bite only when edits use positions that other edits move.

## Related definitions

- [Operational transformation](/operational-transformation/) gives the transformation function and the control algorithms, dOPT, Jupiter, adOPTed, GOT and GOTO, that rely on these conditions.
- [Collaborative text editing](/collaborative-text-editing/) is the problem these conditions serve, with its convergence requirement.
- Sequence [CRDTs](/crdt/), such as [RGA](/rga/), avoid the conditions: an edit names characters by unique ids, not by index, so no transformation is needed and [strong eventual consistency](/strong-eventual-consistency/) follows from commutativity.
- A server that orders all edits, as in [total order broadcast](/total-order-broadcast/), removes the need for TP2 but not for TP1, since a client must still transform its unconfirmed edits.
- The exclusion transformation of GOT, the inverse of inclusion, has its own conditions for undo, which this page does not cover.

## References

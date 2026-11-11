---
title: Correctness of the non-blocking binary search tree
proves: [correctness, linearizability, progress]
status: sketch
---

This is a sketch. It follows the pseudocode on the main page, with the line labels L1 to L41, in the model of that page: sequential consistency, atomic read and CAS on one word, and no reuse of addresses. Ellen, Fatourou, Ruppert and van Breugel give a full proof in their technical report; the structure of this sketch follows theirs, but the details are ours.

## Lemmas on the update field

**Lemma 1 (fresh values).** Each Info record $op$ is written into update fields only as $(\mathrm{IFLAG}, op)$, $(\mathrm{DFLAG}, op)$, $(\mathrm{MARK}, op)$ or $(\mathrm{CLEAN}, op)$, and each of these values is written into at most one field, at most once.

*Proof sketch.* A new $op$ is made at L14 or L24 for each try. The flag CAS at L15 or L25 writes it into one field. The mark at L29 writes $(\mathrm{MARK}, op)$ into $op.p$ only. The unflag CAS steps at L19, L32 and L36 expect the flagged value with the same $op$, so only the first of them can succeed, and only on the field that $op$ flagged. ∎

So a CAS that expects a value $(s, op)$ that it read earlier succeeds only if the field has not changed since then: there is no ABA on update fields.

**Lemma 2 (marks are permanent).** A field that holds $(\mathrm{MARK}, op)$ never changes again.

*Proof sketch.* Every CAS on an update field expects a CLEAN value (L15, L25, L29) or a flagged value (L19, L32, L36). None expects a MARK value. ∎

**Lemma 3 (child CAS steps).** A child field of $x$ changes only by a successful CAS at L18 or L35 for a record $op$ that flagged $x$, while $x$ is flagged by $op$, and for each $op$ only the first such CAS succeeds.

*Proof sketch.* L18 and L35 run only in HELPINSERT and HELPMARKED, which are called only after the flag of $op$ succeeded (and, for a delete, the mark too). Before $op$'s flag is removed, the flag CAS must have been followed by the child CAS of the owner or of a helper, because the unflag steps L19 and L36 come after L18 and L35 in program order, and L32 runs only when the mark failed, in which case no child CAS for $op$ is ever made. The expected old child ($op.l$ or $op.p$) is replaced by a new node or by a node that was below it, and since addresses are not reused and a removed node is never put back, the old value never comes back. So only the first child CAS for $op$ succeeds, and it happens while $x$ is flagged by $op$ (the flag stays until the unflag, which comes after the first child CAS in any process that does both). ∎

**Lemma 4 (a marked node is fixed and removed once).** After $p$ is marked by a DInfo $op$, the children of $p$ never change, and the first dchild CAS for $op$ replaces $p$ by its sibling of $op.l$ under $op.gp$.

*Proof sketch.* A child of $p$ changes only while $p$ is flagged (Lemma 3), and a marked field is never flagged (Lemma 2). So L34 reads the true sibling. When the mark succeeded, $op.gp$ was flagged by $op$ and $op.p$ was still a child of $op.gp$: the child of $gp$ could change only while $gp$ is flagged, which it has been since the dflag, and the dflag succeeded only if $gp.\mathit{update}$ was still the value read at L4 during the search, after the child read that led to $p$. The same holds for $p$ and $l$ with $\mathit{pupdate}$. ∎

## Theorem 1 (the tree stays a search tree)

The invariant of the main page holds in every state.

*Proof sketch.* By induction on the successful child CAS steps. An ichild replaces a leaf $l$ under $p$ by an internal node whose key is $\max(k, l.\mathit{key})$, with leaves $k$ and $l.\mathit{key}$ on the correct sides. Since the search for $k$ reached $l$ through $p$ and $p$ has not changed since its update field was read (Lemma 1 and Lemma 3), $k$ lies in the key range of $l$'s position. A dchild replaces $p$ by one of its own children, whose subtree already lies in the range of $p$'s position. ∎

## Theorem 2 (linearizability)

Take as linearization points: for an insert that returns true, the first ichild CAS of its record; for a delete that returns true, the first dchild CAS of its record; for a find and for updates that return false, a moment during the search at which the leaf $l$ it returns was in the tree.

*Proof sketch.* By Lemma 3 and Lemma 4, each successful update has exactly one point at which its leaf enters or leaves the tree, and the point lies between the operation's flag and its return, so inside the operation. A delete that returns true has its mark succeed (L30), and then its dchild CAS is done by itself or by a helper before it returns. At that moment the leaf $k$ leaves the tree and no other leaf changes. At an insert's point, leaf $k$ enters and no leaf leaves. For searches, Ellen et al. prove that each node a search visits was on the search path for $k$ at some moment after the search started; this is their key lemma, and it uses that a node, once removed, keeps the child pointers it had when it was marked (Lemma 4). At such a moment for the final leaf $l$, the set contains $k$ exactly when $l.\mathit{key} = k$, which gives the result of a find and of an update that returns false. Ordering all points gives a sequential history of a set with the same results. ∎

## Theorem 3 (lock-freedom)

*Proof sketch.* Suppose that after some time no operation completes but some process takes infinitely many steps. Searches are finite, since the tree is finite and paths go down. So updates retry for ever. A retry happens only when an update field read by the search is not CLEAN, or a flag or a mark CAS fails; in both cases another update has written a flag or a mark. Each flagged or marked node is helped: a process that sees $(\mathrm{IFLAG}, op)$ completes $op$; one that sees $(\mathrm{MARK}, op)$ completes the delete; one that sees $(\mathrm{DFLAG}, op)$ tries the mark, and either completes the delete or backtracks it. A backtrack happens only if $op.p$ was flagged or marked by another update $op'$, which the helper helps first. Ellen et al. show that the chain of such helping cannot be a cycle: a delete's flag is on a node above its mark, so following the blocking relation goes strictly down the tree, and the bottom update in a chain can finish. Each completed ichild or dchild completes an insert or a delete that returns true. So some operation completes, which contradicts the assumption. ∎

## Theorem 4 (solo cost)

Run alone, a find takes exactly $2d$ steps and an insert or a delete at most $2d + 7$ steps, where $d$ is the number of internal nodes on the search path.

*Proof.* SEARCH does two reads (L4, and L5 or L6) per internal node and stops at the leaf. Alone, every update field is CLEAN, so an update tries once. An insert then does four allocations (L12 to L14), the flag (L15), the child CAS (L18) and the unflag (L19): seven steps, or none if the key is present. A delete does one allocation (L24), the flag (L25), the mark (L29), one or two reads (L34), the child CAS (L35) and the unflag (L36): at most seven steps. ∎

The test `test_solo_cost_is_two_steps_per_level_plus_seven` checks this on balanced trees of 7, 31 and 127 keys.

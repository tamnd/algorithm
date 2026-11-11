---
title: The lock-free skip list is a linearizable lock-free set with a wait-free contains
proves: [correctness, linearizability, progress]
status: sketch
---

We use the pseudocode and the model of the page. Lemmas 2 and 3 and Theorem 3 are proved in full; Lemma 1 uses Lemma 4 for one case. The linearizability argument for contains is given as an outline that follows the textbook proof, so the proof as a whole is a sketch.

Call a write to a word of node $x$ at level $i$ a *level-$i$ pointer* from $x$. The CAS steps of the code are: the link at L14 and L17, the reset of the new node's own word at L16, the unlink at L6, and the marks at L23 and L25.

**Lemma 1 (pointers go up).** Every level-$i$ pointer from $x$ points to a node whose key is strictly larger than the key of $x$.

*Proof.* At the start, head points to the nodes in sorted order and the last node to tail. Induction over the CAS steps. A mark keeps the pointer. At L13 and L16, the new node $v$ with key $k$ gets succs[i], whose key FIND saw as at least $k$ and not equal to $k$ (at level 0 the key is not $k$ since found is false, and at level $i > 0$ FIND stops at the first key not below $k$, and the node with key $k$ at level $i$ could only be $v$ itself, which is not yet linked at $i$; so the key is larger). At L14 and L17 the CAS writes $v$ into preds[i], whose key FIND saw below $k$. At L6 the CAS replaces $\mathit{curr}$ by $\mathit{succ}$, the pointer read from $\mathit{curr}$, whose key is larger than that of $\mathit{curr}$ by induction, which is larger than that of pred. ∎

So from any node, reachable or not, each level is a strictly increasing chain that ends at tail.

**Lemma 2 (marks are permanent).** Once the word of $x$ at level $i$ is marked, it never changes.

*Proof.* Every CAS in the code has an unmarked expected value: (curr, 0), (succs[i], 0), (s, 0) or (succ, 0). A marked word never equals it. ∎

**Lemma 3 (unlinking).** A node is removed from the chain of reachable nodes at level $i$ only by the CAS at L6, and only when it is marked at level $i$. In particular a node that was linked at level 0 and is not marked there is reachable at level 0.

*Proof.* The only CAS steps that change which nodes are reachable are the links, which add a node, and L6, which moves pred past $\mathit{curr}$. L6 runs only after the read at L4 or L7 saw $\mathit{curr}$ marked, and by Lemma 2 it is still marked. The CAS at L6 succeeds only if pred still points to $\mathit{curr}$ unmarked, so pred is not marked, and $\mathit{succ}$ is the frozen successor of $\mathit{curr}$, so the nodes after $\mathit{curr}$ stay reachable. ∎

**Lemma 4 (one present node per key).** At any time, at most one node with key $k$ is present.

*Proof sketch.* A node becomes present only at a successful CAS at L14, which writes $v$ between preds[0] and succs[0] when preds[0] points to succs[0] unmarked. By Lemma 3, preds[0] is reachable then, and by Lemma 1 its chain is sorted, so no node with key between preds[0].key and succs[0].key is reachable at level 0, and in particular no present node with key $k$. ∎

**Theorem 1 (linearizability).** Each history is linearizable to the sequential set, with the linearization points of the page.

*Proof sketch.* Define the abstract set at each time as the keys of the present nodes. By Lemma 4 this is a set. It changes only at a successful CAS at L14 (a key is added, by the add whose CAS it is) and at a successful CAS at L25 (a key is removed, by the remove whose CAS it is): marks at upper levels and unlinks at L6 do not change which nodes are present, by Lemma 3 and since present is defined at level 0. By Lemma 2 at most one CAS at L25 succeeds for each node, so one remove returns true per present node.

An add that returns false and a remove that returns false at L21 are linearized at the read in FIND that saw, at level 0, an unmarked node with key $k$, or a pair (pred, curr) with keys below and above $k$ and pred unmarked. In the first case the node is present then (Lemma 3); in the second no node with key $k$ is present then (Lemma 1 and Lemma 3). A remove that returns false at L27 saw its own CAS fail and the word marked; by Lemma 2 another remove's CAS at L25 succeeded between the FIND of this remove and L27, and the key was not present just after it.

For contains, a true answer is linearized at the read of the unmarked level 0 word of the returned node. For a false answer: if no node with key $k$ was present at the start of the call, linearize there. Otherwise let $x$ be that node. Contains walks level 0 along a strictly increasing chain (Lemma 1), and it starts level 0 at a node whose key is below $k$. The textbook shows that the walk either reaches $x$ or skips past it, and that it can skip past $x$ only if $x$ was marked at level 0 at that time; so $x$ was marked during the call, and contains is linearized just after that mark, when no node with key $k$ is present, because a new node with key $k$ can only become present after a FIND that sees $x$ marked. We do not repeat that case analysis here. ∎

**Theorem 2 (lock-freedom).** In every infinite run, infinitely many operations finish.

*Proof sketch.* Suppose that from some time on no operation finishes. Then a fixed finite set of operations runs forever. A CAS fails only if its word changed after it was read, which needs a successful CAS of another step. Count the successful CAS steps after that time. Each add links its node at level 0 at most once (it leaves the loop at L14) and at each upper level at most once (it leaves the loop at L17); the nodes made at L13 in failed tries are never linked, so they are never reached. Each node is marked at most once per level (Lemma 2). Each unlink at L6 removes one link of a marked node from the chain, and a node is linked at a level only by its own add, at most once, so the unlinks are bounded by the links. A reset at L16 succeeds at most once per failed CAS at L17. So only finitely many CAS steps succeed, and after the last one every CAS succeeds. Then a FIND does not restart, so it finishes in a bounded number of reads (Lemma 1, finitely many nodes), each loop at L23 or L25 ends after one more CAS, and the loop at L15 to L18 ends after one more try. So an operation finishes, which is a contradiction. ∎

**Theorem 3 (contains is wait-free for a finite key range).** If all keys are integers in a range of size $R$, a contains reads at most $L(R + 2)$ words.

*Proof.* At each level, contains first reads pred's word, then follows pointers. Each pointer it follows goes to a strictly larger key (Lemma 1), and it stops at the first key that is not below $k$, or at tail. So at each level it visits at most $R + 1$ nodes after pred, and reads one word of each, plus the first read. It never writes and never restarts. ∎

The bound depends on $R$, not on $n$; with real-valued keys a contains can be kept walking by adds in front of it, as long as new keys keep appearing between its position and $k$.

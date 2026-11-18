---
title: Semistructured merge keeps the work of a side that alone changed the program, and orders no members by place
proves: [correctness]
status: full
---

We use the pseudocode of the page. A tree is a node with a kind and a name; its *key* is the pair of the two. A nonterminal node has a list of children with distinct keys, and a terminal node has a body, a list of lines. Two trees are *equal up to order* if they become equal when the children of every nonterminal node are sorted by key. MERGE$(a, o, b)$ takes two nodes $a$ and $b$ with the same key and their base $o$, which is absent when both sides added the node. LINE-MERGE is the chunk rule of [diff3](/diff3/) on two longest matchings, $o$ with $a$ and $o$ with $b$: between two lines of $o$ that are matched on both sides, it takes the piece of $a$ if the pieces of $o$ and $b$ are equal or the pieces of $a$ and $b$ are equal, else the piece of $b$ if the pieces of $o$ and $a$ are equal, else it writes a conflict.

**Lemma 1 (the line merge with one side unchanged).** LINE-MERGE$(a, o, o)$ is $a$ and LINE-MERGE$(o, o, b)$ is $b$, both without a conflict.

*Proof.* A longest matching of $o$ with itself has $|o|$ pairs and is increasing, so it is the identity. Take LINE-MERGE$(a, o, o)$. The partner of each line $x$ of $o$ in the copy is $x$ itself, so at each step the start in the copy is the start in $o$, and the pieces of $o$ and of the copy are equal. The first case of the rule applies at every step, and the output is the pieces of $a$, joined by the lines $o[x] = a[a(x)]$ between them, which is $a$. For LINE-MERGE$(o, o, b)$ the pieces of $a$ and $o$ are equal at every step. If the piece of $b$ is equal to them too, the rule takes the piece of $a$, which is the same; otherwise it takes the piece of $b$. So the output is $b$. $\square$

**Lemma 2 (the line merge is symmetric without conflicts).** If LINE-MERGE$(a, o, b)$ has no conflict, then LINE-MERGE$(b, o, a)$ has the same lines.

*Proof.* The lines of $o$ that are matched on both sides are the same for the two calls, and the pieces of each step are the same with $a$ and $b$ swapped. Write $p_A$, $p_O$ and $p_B$ for the pieces of one step. If $p_A = p_B$, both calls take that piece. If $p_O = p_B \ne p_A$, the first call takes $p_A$; in the second call $p_O \ne p_A$ and $p_A \ne p_B$, so it reaches the case $p_O = p_B$ and takes $p_A$ too. If $p_O = p_A \ne p_B$, both calls take $p_B$ in the same way. These are all the steps without a conflict. $\square$

**Lemma 3 (the members of a merged node).** Let $a$ and $b$ be nonterminal nodes with base $o$. For each key $k$ of a child, the merged node has a child with key $k$ exactly in these cases, and the conflicts of line L6 are the only ones made at this level:

1. $k$ is in $a$ and in $b$: the child is the merge of the two children and the child of $o$ (line L4);
2. $k$ is in exactly one of $a$ and $b$, and not in $o$: the child is that one (line L5);
3. $k$ is in exactly one of $a$ and $b$, and in $o$, and that child differs from the child of $o$: the child is kept, and a conflict is reported (line L6).

If $k$ is in exactly one of $a$ and $b$, in $o$, and unchanged there, or in neither $a$ nor $b$, the merged node has no child with key $k$. The children with a key in $a$ come first, in the order of $a$, and then the others, in the order of $b$.

*Proof.* Line L2 lists each key of $a$ or $b$ once, the keys of $a$ in their order and then the new keys of $b$ in theirs, so a key that is in neither does not appear. Line L3 takes the children $x$, $y$ and $z$ of $a$, $o$ and $b$ with the key; a key has at most one child in each node. The three branches of lines L4 to L6 are the cases of the lemma. $\square$

**Theorem 1 (one side unchanged).** MERGE$(a, o, o)$ is $a$, and MERGE$(o, o, b)$ is equal to $b$ up to order, both without a conflict.

*Proof.* By induction on the height of the trees. If the nodes are terminal, line L1 returns LINE-MERGE of the bodies, which is the body of $a$ or of $b$ without a conflict by Lemma 1. Otherwise use Lemma 3. In MERGE$(a, o, o)$, a key of $a$ that is in $o$ is in both sides, and its child is MERGE$(x, y, y) = x$ by induction. A key of $a$ that is not in $o$ is not in the copy of $o$ either, so its child is $x$ by case 2. A key of $o$ that is not in $a$ is in the copy of $o$ unchanged, so it is dropped. So the merged children are those of $a$, in the order of $a$, and the node is $a$. In MERGE$(o, o, b)$, in the same way, a key in $o$ and $b$ gives a child equal to that of $b$ up to order, a key only in $b$ gives the child of $b$, and a key of $o$ that is not in $b$ is dropped, because the first side has it unchanged. So the merged node has the children of $b$, up to order. No case is case 3, so there is no conflict. $\square$

**Theorem 2 (no ordering conflicts).** Two members that the two sides add to the same node with different keys never conflict, wherever they are placed, and a member that one side moves among its siblings and the other side changes is merged as if it had not moved.

*Proof.* Lemma 3 matches children by key only, never by place. Two added members with different keys fall under case 2 each, without a conflict. A moved member is in $a$, $o$ and $b$ with the same key, so case 1 merges it with its base like any other member; the move changes only the order of the children, which no case of Lemma 3 tests. $\square$

**Theorem 3 (symmetric without conflicts).** If MERGE$(a, o, b)$ has no conflict, then MERGE$(b, o, a)$ has no conflict either, and the two results are equal up to order.

*Proof.* By induction on the height. For terminal nodes, Lemma 2 applies to the bodies, with an empty base if $o$ is absent, and a conflict of one call is a conflict of the other because the pieces are only swapped. For nonterminal nodes, the set of keys at line L2 is the union of the keys of $a$ and $b$ in both calls, and each case of Lemma 3 is symmetric in $a$ and $b$: case 1 by induction, case 2 takes the same child, and in the last case the child is dropped in both calls. Case 3 is excluded, since it reports a conflict. Only the order of the children can differ. $\square$

**Renaming.** A member that one side renames has a new key. By Lemma 3 the old key is in $o$ and on one side only, and the new key is on one side only and not in $o$. If the other side changed the member, the result keeps both versions and reports a conflict of case 3; if not, the old member is dropped and the renamed one is kept. This is the weakness that Apel et al. found in their study.

**Termination and cost.** Each call of MERGE recurses only on children, so the calls follow the nodes of the trees, and each node of $a$ or $b$ is in at most one call. With hash maps for the children, one nonterminal costs expected time linear in its number of children, so the tree part is expected linear in the size of the trees. A terminal costs the two longest matchings of its bodies, $O(|o| (|a| + |b|))$ with the dynamic program, so the total time is $O(n^2)$ for versions with $n$ lines and nodes in total.

---
title: Searches in the B^ε-tree return the newest value and updates keep the invariants
proves: [correctness, termination]
status: full
---

We use the pseudocode of the page, with $F \ge 3$, $C \ge 2$ and $L \ge 2$. The *range* of the root is all keys, and the range of the child $c_i$ of $x$ is the part of the range of $x$ between the pivots $p_{i-1}$ and $p_i$, closed on the left and open on the right, with $p_0 = -\infty$ and $p_f = +\infty$. For a key $k$ and a node $x$ whose range holds $k$, define the *state* of $k$ at $x$:

- if $x$ is a leaf, $k$ is present with value $v$ when the pair $(k, v)$ is in $x$, and absent otherwise;
- if $x$ is internal and $x.buf$ has a message on $k$, the state is that of the message: present with $v$ for `PUT(v)`, absent for `DEL`;
- otherwise, the state of $k$ at the child of $x$ whose range holds $k$.

Let $\sigma(k)$ be the state of $k$ after all updates so far, in the abstract dictionary. We prove that between operations:

- (E1) the pivots of each node are increasing and inside its range, all leaves are at one depth, each internal node has between 2 and $F$ children, and each leaf has at most $L$ keys, all in its range;
- (E2) each message in $x.buf$ is on a key in the range of $x$;
- (E4) every buffer has at most $C$ messages;
- (S) for every key $k$, the state of $k$ at the root is $\sigma(k)$.

Property (E3) of the page is what makes (S) survive a flush; we use it in the form of the definition of state, which looks at the highest message first.

**Base.** The tree is one empty leaf, and every key is absent in the dictionary and at the root.

**GET.** Lines L1 to L5 follow the definition of state: at each internal node, line L3 returns the state of the message on $k$ if there is one, and line L4 goes to the child whose range holds $k$, which exists and is unique by (E1). At the leaf, line L5 returns the state there. So GET returns the state of $k$ at the root, which is $\sigma(k)$ by (S). It ends because the height is finite, and it changes nothing.

**UPSERT, line L6.** If the root is a leaf, applying the message makes $k$ present with $v$ or absent, which is the new $\sigma(k)$; other keys keep their state. The leaf stays sorted. It may have $L + 1$ keys, which line L8 handles.

**UPSERT, line L7.** The message goes into the root buffer and replaces any older message on $k$. Now the state of $k$ at the root is that of the new message, which is the new $\sigma(k)$. Other keys are not affected. Since the range of the root is all keys, (E2) holds. The buffer may have $C + 1$ messages, and FLUSH is called.

**FLUSH(x).** We show: if, when FLUSH$(x)$ is called, (E1) and (E2) hold except that $x.buf$ may have more than $C$ messages and the states at $x$ of all keys are given, then when it returns, $x.buf$ has at most $C$ messages, every buffer below $x$ has at most $C$, every child of $x$ satisfies (E1) but $x$ itself may have more than $F$ children, and the state of every key at $x$ is unchanged.

*Lines L10 and L11.* Let $c$ be the chosen child and $G$ the set of messages on keys in the range of $c$, all moved to $c$. For a key $k$ with a message in $G$: before the move, its state at $x$ was given by that message. After the move, $x$ has no message on $k$, so the state at $x$ is the state at $c$. If $c$ is a leaf, line L11 applied the message to $k$ in the leaf, so the state at $c$ is that of the message. If $c$ is internal, the message is now in $c.buf$, having replaced any older message on $k$ there, so again the state at $c$ is that of the message. For a key with no message in $G$, nothing on its path changed. So the state of every key at $x$ is unchanged. The moved messages are on keys in the range of $c$, so (E2) holds for $c$.

*Line L12.* If $c.buf$ now has more than $C$ messages, the recursive call FLUSH$(c)$ keeps the states at $c$, so also at $x$, and returns with the buffers of $c$ and below at most $C$.

*Line L13.* If $c$ has more than $L$ keys or more than $F$ children, SPLIT cuts it.

*SPLIT (line L14).* Let $c$ be a leaf with keys $k_1 < \cdots < k_s$, $s > L$, and $h = \lfloor s/2 \rfloor \ge 1$. The left half keeps $k_1, \ldots, k_h$, the right half gets $k_{h+1}, \ldots, k_s$, and $k_{h+1}$ becomes a pivot of the parent, between the pivots around $c$. Since $k_1 < k_{h+1}$ and all keys of $c$ are in its range, the new pivot is strictly inside the range of $c$, so the pivots of the parent stay increasing, and each key is in the range of its new leaf. If $c$ is internal with $f > F$ children, $h = \lfloor f/2 \rfloor \ge 2$, the left half keeps the children $1..h$ and their pivots, the right half the others, and the pivot $p_h$ between them goes up. Each message of $c.buf$ goes to the half whose range holds its key. Then each key has, in the half that holds it, the same message and the same subtree as before, so its state is unchanged. Each half has between 2 and $F$ children if $f \le 2F$, and the repeat in line L14 splits halves that are still too big, which happens a finite number of times since each split makes the halves smaller. The new nodes are at the depth of $c$, so all leaves stay at one depth. The parent gains children, which is allowed during FLUSH.

*Line L9.* The loop ends: each pass moves a nonempty group of messages out of $x.buf$, since $|x.buf| > C \ge 1$, and nothing is added to $x.buf$ during the loop. When it ends, $|x.buf| \le C$.

**UPSERT, line L8.** After line L6 or L7, only the root may be too big: every other node satisfies (E1) by the claim on FLUSH. While the root is too big, line L8 puts a new root with one child above it and splits that child, as in line L14. The new root has an empty buffer and its range is all keys, so all states are kept; the depth of all leaves grows by one at once; and after the split, every child of the new root satisfies (E1), because SPLIT repeats on each half that is still too big. The new root has at least 2 children. If it has more than $F$, the loop runs again with it. Each round adds a level above nodes of at most $F$ children and replaces a root of $f$ children by one of about $f/F$ or fewer, so the loop ends, and then (E1) holds.

**Deletes and the rebuild.** A delete is an update with the message `DEL`, covered above. The rebuild computes, for each key, its state at the root, by resolving each buffer over the content of its subtree from the bottom up, which is the definition of state; it then builds a tree with empty buffers from the present keys, with leaves of at most $L$ keys and nodes of 2 to $F$ children. So (S) and (E1) to (E4) hold after it.

**Termination.** GET follows one path. FLUSH$(x)$ recurses only into children of $x$, so the depth of the recursion is at most the height, and each loop ends as shown. SPLIT recurses only on smaller nodes. So every operation ends.

Hence every GET returns the value of the newest update of its key, or "absent", and all invariants hold between operations. $\blacksquare$

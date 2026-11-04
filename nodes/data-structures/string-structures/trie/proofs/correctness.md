---
title: The trie operations keep the invariant and answer the string symbol table queries
proves: [correctness]
status: full
---

We use the pseudocode of the page. For a node $x$, $str(x)$ is the string spelled by the path from the root to $x$. The invariant is:

> **(T1)** $s$ is a key with value $v$ if and only if some node $x$ has $str(x) = s$ and $x.val = v \ne$ NIL. **(T2)** Each node other than the root has a value or a child. **(T3)** $T.n$ is the number of nodes with a value.

The edges out of one node carry distinct symbols, because $x.next$ is a function from symbols to nodes. This structural fact holds for each trie, and no operation can break it: a link is only written at an index $c$ where it was NIL (line L8), or removed (line L21).

**Lemma 1 (walk).** For a string $s$, let $d$ be the largest $i \le |s|$ such that some node $y$ has $str(y) = s[0 \ldots i-1]$. Then this node $y$ is unique, and a walk from the root that follows $s[0], s[1], \ldots$ visits the nodes of $s[0 \ldots i-1]$ for $i = 0, \ldots, d$ and then stops (it finds a NIL link at step $d + 1$ if $d < |s|$).

*Proof.* By induction on $i$. For $i = 0$ the walk is at the root, and the root is the only node with $str = \varepsilon$. Assume the walk is at the unique node $y_i$ with $str(y_i) = s[0 \ldots i-1]$, and $i < |s|$. A node $z$ with $str(z) = s[0 \ldots i]$ has a parent $p$ with $str(p) = s[0 \ldots i-1]$, so $p = y_i$ by uniqueness, and the edge from $y_i$ to $z$ carries $s[i]$. The edges out of $y_i$ carry distinct symbols, so there is at most one such $z$, and it is $y_i.next[s[i]]$. If it exists, the walk moves to it; if not, the link is NIL and no node of $s[0 \ldots i]$ exists, so $d = i$. $\square$

**GET.** By Lemma 1, lines L1 to L4 return NIL exactly when no node $x$ has $str(x) = s$, and then $s$ is not a key by (T1). Else the loop ends at the unique node $x$ with $str(x) = s$, and line L5 returns $x.val$. By (T1) this is the value of $s$ if $s$ is a key, and NIL if it is not. GET changes nothing.

**PUT.** Lines L6 to L9 visit, by Lemma 1, the nodes of the prefixes of $s$ that exist, and line L8 creates the missing ones, each as the only child for its symbol. At the end $x$ is the unique node with $str(x) = s$. New nodes have no value, and only the value of $x$ is changed. So (T1) holds: the keys other than $s$ keep their nodes and values, and $s$ now has the value $v \ne$ NIL. Line L10 adds one to $T.n$ exactly when $x$ had no value, so (T3) holds. For (T2), each new node lies on the path from the root to $x$, so it has a child on that path or it is $x$, which has a value.

**DELETE.** If lines L13 to L17 return, then by Lemma 1 and (T1) $s$ is not a key, and nothing changed. Else the list $path$ holds the nodes $path[i]$ with $str(path[i]) = s[0 \ldots i-1]$ for $i = 0, \ldots, |s|$, and $path[|s|]$ has a value. Line L18 removes that value and subtracts one from $T.n$, so (T1) and (T3) hold for the set of keys without $s$. Now (T2) can fail only at nodes of $path$. We show that the loop of lines L19 to L21 restores it. The loop keeps this claim, for the current $i$: (T2) holds at each node except possibly $path[i]$, and the nodes $path[i+1 \ldots |s|]$ that were cut had no value. At the start, $i = |s|$ and only $path[|s|]$ changed. If line L20 finds that $path[i]$ has a value or a child, (T2) holds everywhere and the loop returns. Else $path[i]$ has no value and no child, so cutting the link to it removes one node and no key, and its parent $path[i-1]$ is the only node whose children changed. So the claim holds for $i - 1$. If the loop reaches $i = 0$, it stops at the root, for which (T2) asks nothing. Cutting a node with no value keeps (T1) and (T3).

**KEYS-WITH-PREFIX.** Let $x$ be the node of $p$ found in line L22. If there is none, then by Lemma 1 no node has a string that starts with $p$, because the node of each such string would have the node of $p$ as an ancestor. So no key starts with $p$, and the empty list is right. Else, the stack always holds pairs $(y, str(y))$: this holds for $(x, p)$, and line L28 pushes $(y.next[c], str(y) \cdot c)$. Each node of the subtree of $x$ is pushed exactly one time, because each node has one parent. Each node $y$ of the subtree has $str(y)$ that starts with $p$, and each node with such a string is in the subtree of $x$. So by (T1), line L27 appends exactly the keys that start with $p$, each one time.

*Order.* The loop is a preorder walk with the children of each node visited in increasing order of their symbols, because they are pushed in decreasing order onto a stack. In this order, $str(y)$ comes before the strings of its subtree, which it is a proper prefix of, and for two children $c < c'$ of a node, each string below $c$ comes before each string below $c'$. These are the two rules of lexicographic order, so the output is sorted.

**LONGEST-PREFIX-OF.** By Lemma 1, the loop visits the node of $s[0 \ldots i-1]$ for each $i = 0, \ldots, d$, where $d$ is as in the lemma, and stops after $i = d$ (by line L33 or line L35). The prefixes $s[0 \ldots i-1]$ with $i > d$ have no node, so by (T1) they are not keys. For $i \le d$, line L32 sets $best = i$ exactly when $s[0 \ldots i-1]$ is a key. Since $i$ increases, at the end $best$ is the largest such $i$, or $-1$ if there is none. Line L36 returns the longest prefix of $s$ that is a key, or NIL. $\blacksquare$

**Termination and cost.** Each loop of GET, PUT, DELETE and LONGEST-PREFIX-OF runs at most $|s| + 1$ times. The loop of KEYS-WITH-PREFIX pops one node of the subtree of $x$ in each round and pushes each node one time, so it runs exactly $t$ times, where $t$ is the number of nodes of the subtree.

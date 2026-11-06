---
title: Discrimination tree retrieval returns exactly the patterns whose linear form matches the query
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the term rewriting pages: a signature $\Sigma$, variables $V$, terms $T(\Sigma, V)$, and substitutions $\sigma$. A function symbol $f$ of arity $k$ is written $f/k$ when it is a symbol of a key. For a pattern $l$, $key(l)$ is its preorder sequence of symbols with each variable replaced by $*$. For a term $l$, $lin(l)$ is $l$ with each occurrence of a variable replaced by a new variable, all distinct. A term $p$ **matches** $t$ if $p\sigma = t$ for some $\sigma$; the variables of $t$ are treated as constants.

For a node $x$ of the tree, $str(x)$ is the sequence of edge symbols on the path from the root to $x$. The edges out of a node carry distinct symbols, because $x.next$ is a map. The tree stores the entry $(l, v)$ at a node $x$ with $str(x) = key(l)$.

**Invariant.** (D1) An entry $(l, v)$ is in the set if and only if it is in $x.vals$ for the node $x$ with $str(x) = key(l)$. (D2) Each node other than the root has an entry or a child. (D3) $D.n$ is the number of entries.

## Insert and delete keep the invariant

INSERT walks from the root along $key(l)$, creates each missing node as the only child for its symbol (line L3), and adds the entry at the last node $x$, which has $str(x) = key(l)$ (line L5). Other nodes keep their entries, so (D1) holds. Each new node is on the path to $x$, so it has a child on that path or it is $x$, which has an entry, and (D2) holds.

DELETE walks along $key(l)$ (lines L18 to L20). If an edge is missing, no node has $str = key(l)$, so by (D1) the entry is not in the set, and DELETE returns false without a change. Else it reaches the node $x$ with $str(x) = key(l)$, and by (D1) the entry is in the set iff it is in $x.vals$; line L21 removes one copy, or returns false. Lines L22 to L24 then go up from $x$ and remove each node that has no entry and no child, and stop at the first node that has one. A removed node has no entry, so (D1) still holds. A node that stays either was not changed, or is the node where the loop stopped, which has an entry or a child, so (D2) holds. (D3) is kept by the counter. $\blacksquare$

## Retrieval

Let $t$ be the query, with preorder symbols $a_0, \ldots, a_{n-1}$ (line L6). Each $a_i$ starts one subterm $t_i$ of $t$, and the subterm ends just before $skip[i]$; a variable $y$ of $t$ gives the symbol $?y$, which is not $*$ and not a function symbol. If $a_i = f/k$, then $t_i = f(u_1, \ldots, u_k)$, $u_1$ starts at $i + 1$, and $u_{j+1}$ starts at the end of $u_j$, the last one ending at $skip[i]$. This is the definition of preorder.

**Walk.** For a sequence $w$ of key symbols and an index $i \le n$, define the walk of $w$ from $i$: start at $i$; for each symbol $c$ of $w$ in turn, if $i < n$ and $c = *$, set $i \leftarrow skip[i]$; if $i < n$ and $c = a_i$ is a function symbol, set $i \leftarrow i + 1$; else the walk fails. The walk is deterministic, so it fails or ends at one index.

**Lemma 1 (forest).** Let $l_1, \ldots, l_m$ be terms, and let $w = key(l_1) \cdots key(l_m)$. Let $i_0 = i$ be an index. The walk of $w$ from $i$ ends at $j$ if and only if there are indices $i_0, i_1, \ldots, i_m$ with $i_{r} = skip[i_{r-1}]$ and $i_r \le n$ for $r = 1, \ldots, m$, such that $lin(l_r)$ matches $t_{i_{r-1}}$ for each $r$, and $j = i_m$. (The term $t_{i_{r-1}}$ must exist, so $i_{r-1} < n$, and $i_m \le skip[i_{m-1}]$ is part of the claim.)

*Proof.* Induction on the total size $|l_1| + \cdots + |l_m|$. If $m = 0$, $w$ is empty and the walk ends at $i$; take $j = i_0$. Let $m \ge 1$.

- If $l_1$ is a variable, $key(l_1) = *$. The walk does its first step iff $i < n$, and then it moves to $skip[i]$. The term $lin(l_1)$ is a variable, which matches $t_i$. The claim follows from the induction hypothesis for $l_2, \ldots, l_m$ from $skip[i]$.
- If $l_1 = f(s_1, \ldots, s_k)$, $key(l_1) = f/k\ key(s_1) \cdots key(s_k)$. The first step succeeds iff $i < n$ and $a_i = f/k$, that is, $t_i = f(u_1, \ldots, u_k)$, and then the walk continues from $i + 1$ with $key(s_1) \cdots key(s_k)\ key(l_2) \cdots key(l_m)$, a forest of smaller total size. By the induction hypothesis, this walk ends at $j$ iff $lin(s_1), \ldots, lin(s_k)$ match the consecutive subterms starting at $i + 1$, which are $u_1, \ldots, u_k$ and end at $skip[i]$, and then $lin(l_2), \ldots, lin(l_m)$ match consecutive subterms from $skip[i]$, ending at $j$. Because $lin(l_1)$ has distinct variables, the variables of $lin(s_1), \ldots, lin(s_k)$ are disjoint, so the matchers combine into one, and $lin(l_1) = f(lin(s_1), \ldots, lin(s_k))$ up to renaming matches $f(u_1, \ldots, u_k) = t_i$ iff each $lin(s_r)$ matches $u_r$. If $a_i$ is another function symbol or a query variable, the walk fails, and $lin(l_1)$, whose root is $f$, does not match $t_i$, whose root is not $f/k$. $\blacksquare$

**Lemma 2 (search).** The loop of lines L8 to L12 pops the pair $(x, i)$ if and only if the walk of $str(x)$ from $0$ ends at $i$. Each node is popped at most once.

*Proof.* If: induction on the length of $str(x)$. The root is pushed with $0$ at line L7. Let $x$ be a child of $y$ by the symbol $c$, and let the walk of $str(x)$ end at $i$. Then the walk of $str(y)$ ends at some $i' < n$, so by the induction hypothesis $(y, i')$ is popped, and $i' \ne n$, so lines L11 and L12 run. If $c = *$, line L11 pushes $(x, skip[i'])$ and $skip[i'] = i$. If $c$ is a function symbol, then $c = a_{i'}$, line L12 pushes $(x, i' + 1)$ and $i' + 1 = i$. Every pushed pair is popped, since the loop runs until the stack is empty.

Only if: each push at lines L11 and L12 extends the walk by one step of its definition, so by induction on the number of pushes, every pushed $(x, i)$ has a walk of $str(x)$ that ends at $i$. The walk is deterministic, and each node has one parent, so each node is pushed at most once. $\blacksquare$

**Theorem.** RETRIEVE$(D, t)$ returns each entry $(l, v)$ of $D$ such that $lin(l)$ matches $t$, once, and no other entry. MATCH$(D, t)$ returns each entry $(l, v)$ such that $l$ matches $t$, once, with its matcher.

*Proof.* Line L10 outputs the entries of $x$ when $(x, i)$ is popped with $i = n$. Let $(l, v)$ be an entry and $x$ its node, $str(x) = key(l)$ by (D1). By Lemma 2, $(x, n)$ is popped iff the walk of $key(l)$ from $0$ ends at $n$. By Lemma 1 with $m = 1$, this holds iff $lin(l)$ matches $t_0 = t$ and $skip[0] = n$, and $skip[0] = n$ is always true. Lemma 2 also says that $x$ is popped at most once, so the entry is output at most once.

For MATCH: if $l$ matches $t$ with $l\sigma = t$, then $lin(l)$ matches $t$ (map each new variable to the image of its old variable), so the entry is a candidate, and line L16 accepts it. Line L16 rejects every candidate that $l$ does not match. $\blacksquare$

**Remark.** The converse of "$l$ matches $t$ implies $lin(l)$ matches $t$" is false for non-linear $l$: $f(x, x)$ is a candidate for $f(g(a), b)$, but it does not match. For linear $l$, $lin(l)$ is $l$ up to renaming, so RETRIEVE alone is exact.

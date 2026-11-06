---
title: The preorder search finds the leftmost-outermost redex
proves: [correctness]
status: full
---

We use the pseudocode of the page and the notation of the term rewriting pages. $R$ is a list of rules $l_1 \to r_1, \ldots, l_m \to r_m$ with $l_j \notin V$ and $\mathrm{Var}(r_j) \subseteq \mathrm{Var}(l_j)$. A position $p$ of $t$ is a **redex** if $t|_p = l_j\tau$ for some $j$ and $\tau$; it is **outermost** if no proper prefix of $p$ is a redex. Two distinct outermost redexes are not prefixes of each other, so they are ordered from left to right by the lexicographic order $<_{\mathrm{lex}}$ of positions. The **leftmost-outermost step** contracts the least outermost redex in this order, with the first rule of the list that matches there.

**Preorder.** The preorder of the positions of $t$ is defined by: $p$ comes before $q$ iff $p$ is a proper prefix of $q$, or $p = u\,i\,v$ and $q = u\,j\,w$ with $i < j$. This is the lexicographic order on positions with a prefix coming first, and it is a strict total order on $\mathrm{Pos}(t)$.

**Lemma 1 (the search visits positions in preorder).** Line L3 pops the positions of $t$ in preorder, and checks the rules at each of them, until it finds a redex.

*Proof.* The search keeps a stack of positions, starting with $\varepsilon$. When it pops $p$ and finds no rule, it pushes $p\,n, \ldots, p\,1$, so $p\,1$ is on top. We show by induction on the size of $t|_p$ that, from the moment $p$ is on top of the stack, the search pops exactly the positions of the subtree at $p$, in preorder, before it pops any position that was below $p$ on the stack (unless it stops at a redex). For a leaf this is immediate. Otherwise it pops $p$, pushes the children with $p\,1$ on top, and by induction finishes the subtree of $p\,1$ in preorder before $p\,2$ comes to the top, and so on. The concatenation $p$, subtree of $p\,1$, ..., subtree of $p\,n$ is the preorder of the subtree at $p$. Applied to $\varepsilon$, the search visits all of $\mathrm{Pos}(t)$ in preorder. $\square$

**Lemma 2 (the first redex in preorder is the leftmost-outermost redex).** If $t$ has a redex, the least redex $p$ in preorder is outermost, and it is $<_{\mathrm{lex}}$-least among the outermost redexes.

*Proof.* Each proper prefix of $p$ comes before $p$ in preorder, so it is not a redex, by the choice of $p$. Hence $p$ is outermost. Let $q \ne p$ be another outermost redex. Neither is a prefix of the other. Since $p$ comes before $q$ in preorder and is not a prefix of $q$, the two positions first differ at some index where $p$ has the smaller number, so $p <_{\mathrm{lex}} q$. $\square$

**Lemma 3 (one step).** If line L3 returns the path to $p$, the rule index $j$ and $v = r_j\tau$, then after line L6 the current term is $t[r_j\tau]_p$, the result of the leftmost-outermost step.

*Proof.* By Lemmas 1 and 2, $p$ is the leftmost-outermost redex, and the search tries the rules at $p$ in list order, so $j$ is the first rule that matches $t|_p$, with the match $\tau$; matching returns the unique $\tau$ on $\mathrm{Var}(l_j)$ with $l_j\tau = t|_p$, and the substitution function builds $r_j\tau$. The path lists the pairs $(t|_{p'}, i)$ for each proper prefix $p'$ with $p'\,i$ a prefix of $p$, from the root down. Line L6 goes up the path and replaces argument $i$ of $t|_{p'}$ by the current value. By induction on the number of pairs processed, after processing the pair of $p'$ the value is $t|_{p'}[r_j\tau]_{q}$, where $p = p'\,q$. After the root pair it is $t[r_j\tau]_p$. $\square$

**Theorem.** On input $t$ and $R$, the algorithm makes exactly the leftmost-outermost steps from $t$, in order. If this sequence is finite with $k$ steps, it returns its last term, which is a normal form, together with $k$. If it is infinite, the algorithm does not stop. With a bound $B$, it returns $\bot$ exactly when the sequence has more than $B$ steps.

*Proof.* By induction on the number of iterations of the loop of line L2, using Lemma 3: after $i$ iterations that did not return, the current term is the $i$-th term of the leftmost-outermost sequence and the counter is $i$. In an iteration, if line L3 finds no redex, Lemma 1 says that every position was checked, so the current term is a normal form and line L4 returns it. Otherwise, with a bound, line L5 returns $\bot$ when $i = B$, that is, when a $(B+1)$-st step is about to be made. Every step is a step of $\to_R$, so the returned term $v$ satisfies $t \to_R^* v$. $\blacksquare$

**Remark.** The theorem says nothing about whether the sequence is finite. That depends on the system. For left-normal orthogonal systems, the leftmost-outermost sequence is finite whenever $t$ has a normal form (O'Donnell 1977); the page states this result and gives a counterexample without left-normality.

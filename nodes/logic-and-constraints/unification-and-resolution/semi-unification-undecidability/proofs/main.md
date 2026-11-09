---
title: Undecidability of semi-unification, with the reduction from Turing machine boundedness in outline
proves: [statement]
status: sketch
---

The full reduction of Kfoury, Tiuryn and Urzyczyn (1993) takes most of their paper, and it is not given here. This file proves in full the parts that frame it: semi-unification is semi-decidable, the boundedness problem for Turing machines is equivalent to the absence of immortal configurations, and boundedness is semi-decidable. With Hooper's theorem, which is cited, this gives the undecidability of boundedness. The file then outlines the reduction from boundedness to semi-unification and shows how the pieces give the theorem. So the file has the status of a sketch.

## Part 1: semi-unification is semi-decidable

**Claim.** There is an algorithm that halts on a finite system $\Gamma = \{s_1 \le t_1, \ldots, s_n \le t_n\}$ exactly when $\Gamma$ has a semi-unifier.

*Proof.* Fix a countable set of function symbols that contains the symbols of $\Gamma$, and a countable set of variables. A tuple $(\sigma, \rho_1, \ldots, \rho_n)$ of substitutions with finite domains is a finite object, so the set of all such tuples can be listed as $T_1, T_2, \ldots$. For each $T_k$, the test $s_i\sigma\rho_i = t_i\sigma$ for all $i$ compares finite terms, so it halts. The algorithm tests $T_1, T_2, \ldots$ in order and halts at the first tuple that passes. If $\Gamma$ has a semi-unifier $\sigma$ with residual substitutions $\rho_i$, then the restrictions of $\sigma$ to $\mathrm{Var}(\Gamma)$ and of each $\rho_i$ to $\mathrm{Var}(s_i\sigma)$ also pass the test, and this tuple appears in the list, so the algorithm halts. If it halts, the tuple it found is a witness. $\square$

So the set of semi-unifiable systems is recursively enumerable. If it were decidable, its complement would also be recursively enumerable.

## Part 2: boundedness of Turing machines

Let $M$ be a deterministic Turing machine with a finite set $Q$ of states, a finite tape alphabet $\Sigma$, and a partial transition function. A **configuration** is a state $q$ and a tape $c : \mathbb{Z} \to \Sigma$, with the head on cell $0$. The tape may have infinitely many non-blank cells. $M$ **halts** in a configuration when no transition applies. A configuration is **immortal** if $M$ never halts when it starts from it. $M$ is **bounded** if there is an $n$ such that $M$ halts within $n$ steps from every configuration.

**Lemma A (locality).** Whether $M$ halts within $k$ steps from $(q, c)$, and the first $k$ steps themselves, depend only on $q$ and on the restriction of $c$ to the cells $-k$ to $k$.

*Proof.* The head starts on cell $0$ and moves by one cell in each step. Before step $j$ it is on a cell in $[-(j-1), j-1]$. So the first $k$ steps read only cells in $[-(k-1), k-1]$, and the cells they write are in the same range. By induction on $j$, two configurations with the same state that agree on $[-k, k]$ make the same first $k$ steps. $\square$

**Lemma B.** $M$ is bounded if and only if $M$ has no immortal configuration.

*Proof.* If $M$ is bounded by $n$, every configuration halts within $n$ steps, so none is immortal.

Now suppose $M$ is not bounded. For $n \ge 0$, let $W_n$ be the set of pairs $(q, w)$ with $w : [-n, n] \to \Sigma$ such that $M$ does not halt within $n$ steps from $q$ on a tape that agrees with $w$ on $[-n, n]$. By Lemma A this does not depend on the rest of the tape. $W_n$ is not empty, because some configuration does not halt within $n$ steps, and its restriction is in $W_n$. If $(q, w) \in W_{n+1}$, then $(q, w|_{[-n, n]}) \in W_n$, because a run that does not halt within $n + 1$ steps does not halt within $n$ steps.

Make a forest whose nodes are the elements of all the $W_n$, where the parent of $(q, w) \in W_{n+1}$ is $(q, w|_{[-n, n]}) \in W_n$. There are at most $|Q| \cdot |\Sigma|$ roots in $W_0$, each node has at most $|\Sigma|^2$ children, and there are infinitely many nodes, since each $W_n$ is not empty. By König's lemma, applied to the tree that has a new root above the roots of the forest, there is an infinite path $(q, w_0), (q, w_1), (q, w_2), \ldots$ with $w_{n+1}$ extending $w_n$. Let $c$ be the union of the $w_n$, a tape on all of $\mathbb{Z}$. For each $n$, $c$ agrees with $w_n$ on $[-n, n]$, so $M$ does not halt within $n$ steps from $(q, c)$. So $(q, c)$ is immortal. $\square$

**Lemma C.** Boundedness is semi-decidable.

*Proof.* For $n = 1, 2, \ldots$, test every pair $(q, w)$ with $w : [-n, n] \to \Sigma$, of which there are finitely many, and run $M$ for $n$ steps on each. By Lemma A this decides whether $M$ halts within $n$ steps from every configuration. Halt at the first $n$ for which all pairs halt. This happens exactly when $M$ is bounded. $\square$

**Hooper's theorem (1966).** It is undecidable whether a given Turing machine has an immortal configuration.

**Corollary.** Boundedness is undecidable. By Lemma B, a decision procedure for boundedness would decide immortality.

## Part 3: the reduction, in outline

**Theorem (Kfoury, Tiuryn and Urzyczyn).** There is a computable map $M \mapsto \Gamma_M$ from Turing machines to finite systems of inequalities such that $M$ is bounded if and only if $\Gamma_M$ is semi-unifiable.

The direction of the reduction is forced by Parts 1 and 2: both boundedness and semi-unifiability are recursively enumerable, and the map must send the bounded machines, not the immortal ones, to the semi-unifiable systems.

The intuition behind the construction, in simplified form, is as follows. The actual systems and their proofs are more involved.

1. A configuration of $M$ is coded by a term. The tape to the left of the head and the tape to the right of the head are coded as nested terms, like two stacks, and the state is coded by the choice of symbols.
2. Each transition of $M$ moves one symbol from one stack to the other. The inequalities of $\Gamma_M$ say that the term for a configuration and the term for its successor are related by instantiation. The residual substitutions $\rho_i$ play the role of the moves: applying $\rho_i$ to a term follows one transition.
3. The semi-unifier $\sigma$ is shared by all inequalities. Its terms must therefore contain, as subterms, a record of every run that the inequalities can start, from every configuration and not only from one input.
4. If every run halts within $n$ steps, then this record has bounded depth, and a semi-unifier with finite terms exists. If some configuration is immortal, the record of its run never ends, and the inequalities would force an infinite term, so no semi-unifier exists.

Kfoury, Tiuryn and Urzyczyn carry out this plan with intermediate problems on machines, and prove both directions in detail. Dudenhefner (2020) gave a shorter chain of reductions, through simple stack machines, and checked it in the Coq proof assistant.

## Part 4: the theorem

Suppose that semi-unifiability were decidable. Then, for a Turing machine $M$, compute $\Gamma_M$ by Part 3 and decide whether it is semi-unifiable. By Part 3, this decides whether $M$ is bounded, which contradicts the corollary of Part 2. So semi-unifiability is undecidable. By Part 1 it is recursively enumerable, so its complement is not recursively enumerable. $\blacksquare$

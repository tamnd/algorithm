---
title: The basic DPLL(T) strategy is sound, complete and terminating
proves: [correctness, termination]
status: full
---

We prove the claims for the strategy in the pseudocode, with a theory solver that meets (S1), (S2) and (S3) of the page. Let $F_0$ be the input clause set, and $n$ the number of its variables. $F$ is the clause set during the run, $M$ the trail. For a set of literals $\mu$, $\mu \models_T \varphi$ means every $T$-model of $\mu$ is a model of $\varphi$; a propositional variable that is not a theory atom is treated as an atom that the theory does not restrict. A clause is read as the disjunction of its literals.

## Invariants

At the start of each pass of the loop, and at each return:

- **(A)** $M$ has no repeated variable, and each variable of $M$ occurs in $F_0$.
- **(B)** $F_0 \models_T C$ for each clause $C$ of $F$. Also $F \supseteq F_0$.
- **(C)** For each literal $l$ of $M$ that is not a decision, $F_0 \cup \{d : d$ a decision before $l$ in $M\} \models_T l$.

*Initialization.* $M$ is empty and $F = F_0$.

*Line L3 (Propagate).* It adds the only undefined literal $l$ of a clause $C \vee l$ of $F$ whose other literals are false in $M$. So $l$ is new, which keeps (A). Each false literal $\neg l_i$ of $C$ is in $M$, so by (C) it follows from $F_0$ and the decisions before it, which are among the decisions before $l$. With $F_0 \models_T C \vee l$ from (B), this gives (C) for $l$.

*Line L6 (T-Backjump).* Let $M = M_1\, d^\bullet M_2$ with $d$ the last decision. The clause $C$ of $F$ is false in $M$. Let $D$ be the set of decisions of $M_1$. Every literal of $M$ follows from $F_0 \cup D \cup \{d\}$, by (C) and by induction along $M$. So $F_0 \cup D \cup \{d\} \models_T \neg C$, and with $F_0 \models_T C$ from (B), $F_0 \cup D \cup \{d\}$ is $T$-unsatisfiable. So $F_0 \cup D \models_T \neg d$. The new literal $\neg d$ has exactly the decisions $D$ before it, which gives (C). The variable of $d$ was removed with $M_2$, so (A) holds. This is a T-Backjump step with conflicting clause $C$ and backjump clause $\neg D \vee \neg d$.

*Line L7 (T-Forget).* Removing a lemma keeps (B), since $F \supseteq F_0$ still holds.

*Line L9 (T-Learn).* By (S1), $\eta$ is $T$-unsatisfiable, so $\models_T \neg \eta$, and the lemma $\neg \eta$ meets (B). Its atoms are in $M$.

*Line L10 (T-Propagate).* By (S3), each new $l$ has $\mu \models_T l$ for the theory literals $\mu$ of $M$. Each literal of $\mu$ follows from $F_0$ and the decisions before it, all of which come before $l$. So (C) holds. The literals are undefined and their atoms occur in $F_0$ (the strategy only asks about atoms of $F_0$), so (A) holds.

*Line L12 (Decide).* A decision literal needs nothing for (C), and it is a new variable of $F_0$.

## Soundness of UNSAT

Line L5 returns UNSAT when a clause $C$ of $F$ is false in $M$ and $M$ has no decision. By (C) with no decisions, $F_0 \models_T l$ for each $l$ of $M$, so $F_0 \models_T \neg C$. By (B), $F_0 \models_T C$. So $F_0$ has no $T$-model. $\square$

## Soundness of SAT

Line L11 returns $M$ when every variable of $F$ is defined, so $M$ is a total assignment of the variables of $F_0$ by (A). Under a total assignment each clause is true or false, and line L4 found no false clause, so each clause of $F \supseteq F_0$ is true in $M$. Line L8 found no conflict in the theory literals $\mu$ of $M$, so by (S2) $\mu$ is $T$-satisfiable. Take a $T$-model $\mathcal{A}$ of $\mu$, and give each plain propositional variable its value in $M$. Each atom of $F_0$ has the truth value of $M$ in $\mathcal{A}$, so $\mathcal{A}$ satisfies every clause of $F_0$. $\square$

## Termination

Write $M = M_0\, d_1^\bullet M_1\, d_2^\bullet \cdots d_k^\bullet M_k$, where the $d_i$ are the decisions. Let $\tau(M) = (|M_0|, |M_1| + 1, \ldots, |M_k| + 1)$, so that a decision counts in its own segment, and compare such tuples in lexicographic order, where a proper prefix is smaller than its extensions.

- Line L3, line L10 and line L12 append literals at the end of $M$, so $\tau(M)$ grows: the last entry grows, or a new entry is added.
- Line L6 replaces $M_1\, d^\bullet M_2$ with $M_1\, \neg d$. If $d = d_j$, entries $0$ to $j - 2$ do not change, entry $j - 1$ grows by one, and the later entries are dropped. So $\tau(M)$ grows.
- Line L7 and line L9 do not change $M$. Line L9 adds a lemma that is false in $M$, because $\eta \subseteq M$. The next pass of line L3 adds nothing from this clause, so line L4 then finds a false clause, and line L5 or line L6 follows. Line L7 always follows line L6. So between two changes of $\tau(M)$ there are at most two passes of the loop.

Each tuple has at most $n + 1$ entries, each at most $n + 1$, by (A). So $\tau(M)$ takes finitely many values, and since it grows at each change and never repeats, the run is finite. Each pass of line L3 stops, because each step adds a new variable to $M$. Every run ends at line L5 or line L11, and both answers are correct by the two parts above. $\blacksquare$

## The bound on the steps

Consider the binary tree whose nodes are the sequences of decisions with their values. Each decision goes one level down, and each backjump of line L6 moves from the subtree of $d$ to the subtree of $\neg d$, where $\neg d$ is not a decision. A decision at a level of the tree is never made again in the same context, because after the backjump the variable of $d$ is defined at that level until a backjump to a lower level. So each node of the tree is visited at most once. The tree has depth at most $n$, so there are at most $2^n$ backjumps and at most $2^n$ decisions. Each is followed by at most $n$ appended literals, and each T-Learn by a backjump or Fail. This gives $O(2^n n)$ rule applications. $\blacksquare$

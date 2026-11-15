---
title: Houdini returns the largest inductive subset with at most c + 1 prover calls
proves: [correctness]
status: full
---

**Setting.** A loop has a set of initial states $\mathit{Init}$, a guard $b$ and a body. For a state $s$ that satisfies $b$, $\mathrm{post}(s)$ is the set of states that one turn of the body can reach from $s$; the body may be nondeterministic, and the proof does not need it to be deterministic. Fix a set of states $B$, the *domain of the check*: all states for a real prover, or a box of integers for the prover of the page. $C$ is a finite set of $c$ candidate formulas. For $H \subseteq C$, write $\bigwedge H$ for the conjunction, which is true everywhere when $H$ is empty.

$H$ is *inductive on $B$* when

1. every $s \in B \cap \mathit{Init}$ satisfies $\bigwedge H$, and
2. for every $s \in B$ with $s \models \bigwedge H \wedge b$ and every $t \in \mathrm{post}(s)$, $t \models \bigwedge H$.

PROVE is *exact on $B$*: it returns "none" when $H$ is inductive on $B$, and otherwise a counterexample, either an initial state $s \in B \cap \mathit{Init}$ with $s \not\models \bigwedge H$, or a step $(s, t)$ with $s \in B$, $s \models \bigwedge H \wedge b$, $t \in \mathrm{post}(s)$ and $t \not\models \bigwedge H$.

## Lemma 1: a largest inductive subset exists

**Claim.** If $H_1$ and $H_2$ are inductive on $B$, so is $H_1 \cup H_2$. Hence the union $H^\ast$ of all subsets of $C$ that are inductive on $B$ is itself inductive on $B$, and it contains every inductive subset.

**Proof.** Condition 1: a state of $B \cap \mathit{Init}$ satisfies $\bigwedge H_1$ and $\bigwedge H_2$, so it satisfies $\bigwedge (H_1 \cup H_2)$, the conjunction of the two. Condition 2: let $s \in B$ satisfy $\bigwedge (H_1 \cup H_2) \wedge b$ and let $t \in \mathrm{post}(s)$. Then $s \models \bigwedge H_1 \wedge b$, so $t \models \bigwedge H_1$ because $H_1$ is inductive, and in the same way $t \models \bigwedge H_2$. So $t \models \bigwedge (H_1 \cup H_2)$. The empty set is inductive, because condition 1 asks nothing of the empty conjunction and condition 2 asks only that $t$ satisfies $\mathit{true}$. $C$ has finitely many subsets, so $H^\ast$ is a finite union of inductive sets and is inductive by the first part. $\square$

Note that the union of candidate sets is the conjunction of more formulas, that is, a stronger invariant. "Largest" means the strongest inductive invariant that is a conjunction of candidates.

## Lemma 2: Houdini never removes a candidate of $H^\ast$

**Claim.** At every call of PROVE, $H^\ast \subseteq H$.

**Proof.** At the first call $H = C$. Suppose $H^\ast \subseteq H$ and PROVE returns a counterexample.

- An initial state $s \in B \cap \mathit{Init}$. Line L5 removes the candidates false in $s$. By condition 1 for $H^\ast$, every candidate of $H^\ast$ is true in $s$, so none of them is removed.
- A step $(s, t)$ with $s \in B$ and $s \models \bigwedge H \wedge b$. Since $H^\ast \subseteq H$, $s \models \bigwedge H^\ast \wedge b$, and by condition 2 for $H^\ast$, $t \models \bigwedge H^\ast$. Line L6 removes the candidates false in $t$, so none of $H^\ast$ is removed. $\square$

## Lemma 3: every failed call removes a candidate

**Claim.** When PROVE returns a counterexample, the next $H$ is strictly smaller.

**Proof.** An initial counterexample $s$ falsifies $\bigwedge H$, so some candidate of $H$ is false in $s$ and line L5 removes it. A step counterexample $(s, t)$ has $t \not\models \bigwedge H$, so some candidate of $H$ is false in $t$ and line L6 removes it. $\square$

## Theorem

**Claim.** HOUDINI stops after at most $c + 1$ calls of PROVE and returns $H^\ast$, the largest subset of $C$ that is inductive on $B$.

**Proof.** By Lemma 3, each call that returns a counterexample makes $|H|$ smaller by at least one. $|H|$ starts at $c$ and cannot go below 0, so at most $c$ calls fail, and the next call returns "none". That is at most $c + 1$ calls. When PROVE returns "none", $H$ is inductive on $B$ because PROVE is exact, so $H \subseteq H^\ast$ by Lemma 1. By Lemma 2, $H^\ast \subseteq H$. So $H = H^\ast$. $\square$

**The bound is tight.** For the loop $x := x + 1$ from $x = 0$ with guard $\mathit{true}$ and the candidates $x \le 0, x \le 1, \dots, x \le c - 1$, checked on a box that contains $-1, 0, \dots, c$, the first counterexample in increasing order of $x$ is the step $c' \to c' + 1$ for the smallest bound $c'$ still present, and it falsifies only $x \le c'$. So each failed call removes one candidate, and Houdini makes exactly $c + 1$ calls. The tests check this for $c = 3$.

**Weaker provers.** If PROVE is sound but may return a spurious counterexample, Lemma 2 can fail and Houdini can return a smaller set; the result is still inductive, since the last call said "none". If PROVE may say "none" for a set that is not inductive, the result need not be inductive. $\blacksquare$

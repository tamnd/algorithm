---
title: Forward chaining computes the least model of a definite rule set
proves: [correctness]
status: full
---

Let $P$ be a finite set of safe definite rules $h \leftarrow b_1, \ldots, b_m$ over a finite set of constants, and let $F$ be a finite set of ground facts. A ground instance $\rho\theta$ of a rule $\rho$ replaces each variable by a constant. The immediate consequence operator is $T(I) = F \cup \{ h\theta : (h \leftarrow b_1, \ldots, b_m) \in P,\ b_1\theta, \ldots, b_m\theta \in I \}$. A set $I$ of ground atoms is a *model* when $T(I) \subseteq I$. The *least model* $M$ is the intersection of all models; by the [Knaster-Tarski theorem](/knaster-tarski-theorem/) it is the least fixed point of $T$, and $M = \bigcup_{k \ge 0} T^k(\emptyset)$ because $T$ is monotone and the set of ground atoms is finite.

We use the procedure FORWARD-CHAIN of the page. $W$ is the working memory and $Q$ is the agenda. The procedure adds a fact to $W$ and to the end of $Q$ in one step (line L4 or L11), and only when the fact is not in $W$ yet. Nothing is ever removed from $W$.

## Lemma 1 (soundness)

At every moment, $W \subseteq M$.

*Proof.* By induction on the order in which facts enter $W$. A fact of $F$, or the head of a rule with an empty body, is in $T(\emptyset) \subseteq M$. Any other fact enters $W$ at line L11 as $h\theta$, where $\theta$ matches every body pattern $b_j$ to a fact $b_j\theta$ that is in $W$ at that moment. By the induction hypothesis each $b_j\theta \in M$, so $h\theta \in T(M) = M$. $\square$

## Lemma 2 (termination)

The procedure stops after at most $|M|$ iterations of the main loop.

*Proof.* Each fact enters $Q$ only when it enters $W$, and so at most once. Each iteration removes one fact from $Q$. By Lemma 1 at most $|M|$ facts enter $W$, and $M$ is finite because a safe rule only puts constants of its body facts or of the rule itself into its head. Each iteration does finite work, because the join at line L9 ranges over the finite set $W$. $\square$

## Lemma 3 (closure)

If the main loop ends because $Q$ is empty, then $T(W) \subseteq W$.

*Proof.* $F \subseteq W$ by line L4. Take a rule $\rho = (h \leftarrow b_1, \ldots, b_m)$ and a ground instance $\theta$ with $b_1\theta, \ldots, b_m\theta \in W$. If $m = 0$, then $h$ is ground and line L4 put it in $W$. Otherwise each $b_j\theta$ entered $Q$ when it entered $W$, and since $Q$ is now empty, each was removed from $Q$ at line L6. Let $f$ be the one of these facts that was removed last, and let $i$ be an index with $b_i\theta = f$. When $f$ was removed, every other $b_j\theta$ was either removed earlier, and so already in $W$, or equal to $f$, which entered $W$ before it entered $Q$. Since $W$ only grows, all of them stay in $W$ during that iteration. The pattern $b_i$ matches $f$ with the restriction of $\theta$ to the variables of $b_i$ (line L8), and the join at line L9 enumerates every extension of this binding that matches the other patterns to facts of $W$, so it reaches $\theta$ restricted to the variables of $\rho$. Line L11 then puts $h\theta$ in $W$, or $h\theta$ was in $W$ already. $\square$

## Theorem

FORWARD-CHAIN$(P, F, g)$ stops. It returns *true* exactly when $g \in M$. When it returns *false*, the final $W$ equals $M$.

*Proof.* The procedure stops by Lemma 2. If it returns *true*, then $g \in W \subseteq M$ by Lemma 1. Otherwise the loop ended with $Q$ empty, so $W$ is a model by Lemma 3. Since $M$ is the least model, $M \subseteq W$, and with Lemma 1, $W = M$. The procedure checks every fact as it enters $W$ (lines L4 and L11), so $g \notin W = M$. $\blacksquare$

## Remark on the order of the agenda

The proof uses only the facts that each fact enters $Q$ once and that the loop runs until $Q$ is empty. So the result is the same for a queue, a stack or any other order of $Q$, and for any order of the rules. This is the reason why conflict resolution does not change the result of a production system whose rules only add facts. It changes the result as soon as rules can delete facts or stop the run, as in the [production system](/production-system/) model.

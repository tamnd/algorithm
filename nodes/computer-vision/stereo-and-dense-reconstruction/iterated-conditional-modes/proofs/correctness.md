---
title: Correctness of iterated conditional modes
proves: [correctness]
status: full
---

The energy is $E(f) = \sum_p D_p(f_p) + \sum_{(p,q) \in \mathcal{N}} w_{pq} V(f_p, f_q)$ with real costs; $V$ is any table. We prove that ICM never raises the energy, that it stops after finitely many sweeps, and that the output is a local minimum for changes of one site: no labeling that differs from it at one site has smaller energy.

## Lemma (local costs)

Fix $f$ and a site $p$. For a label $\ell$ let $f^{p \to \ell}$ be $f$ with $f_p$ replaced by $\ell$, and let

$$c(\ell) = D_p(\ell) + \sum_{(p,q) \in \mathcal{N}} w_{pq} V(\ell, f_q) + \sum_{(q,p) \in \mathcal{N}} w_{qp} V(f_q, \ell),$$

the cost of line L4. Then $E(f^{p \to \ell}) - E(f) = c(\ell) - c(f_p)$.

*Proof.* $f^{p \to \ell}$ and $f$ differ only at $p$. The terms of $E$ that do not contain $p$ are equal in both and cancel. The terms that contain $p$ are the data term of $p$ and the pair terms of $p$, and their sum is $c(\ell)$ for $f^{p \to \ell}$ and $c(f_p)$ for $f$. $\square$

## The energy does not rise

Line L6 changes $f_p$ only if $c(\ell) < c(f_p)$. By the lemma, the energy then drops by $c(f_p) - c(\ell) > 0$. All other steps leave $f$ unchanged. So the energy after each step is at most the energy before it, and it drops strictly at each change.

## Termination

There are $L^n$ labelings. The energy drops strictly at each change, so no labeling occurs twice, and there are at most $L^n - 1$ changes. Each sweep that does not stop at line L7 makes at least one change, so there are at most $L^n$ sweeps. With integer costs each change lowers the energy by at least 1, so the number of changes is also at most $E(f_0) - \min E$.

## Local minimality

The loop stops after a sweep with no change. During that sweep $f$ stayed the same, so for every site $p$ line L6 found $c(\ell) \ge c(f_p)$ for the least $c(\ell)$, and therefore for every label $\ell$. By the lemma, $E(f^{p \to \ell}) \ge E(f)$ for every site $p$ and label $\ell$. $\square$

## What is not claimed

The output need not be a global minimum, and it depends on the start and on the order of the sites; the worked example on the page has two orders with energies 10 and 7. The proof uses that sites are updated one at a time. If all sites are updated at once from the old labeling, the lemma no longer applies to the joint change, and the energy can rise or cycle.

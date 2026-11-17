---
title: Conservative advancement never steps past the first contact, and stops when the gap is at most the tolerance
proves: [correctness, termination]
status: full
---

Let $A$ and $B$ be convex polygons that move over $[0, T]$. A point with local coordinates $p$ of body $A$ is at $x_p(t) = c_A + v_A t + R(\theta_A + \omega_A t)\, p$, and the same holds for $B$. Let $r_A = \max |p|$ over the vertices of $A$, which is also the maximum over all points of $A$, and the same for $r_B$. Let $d(t)$ be the distance between $A(t)$ and $B(t)$, and let $t^* = \min \{ t \in [0, T] : d(t) = 0 \}$ be the first contact, if there is one. Use exact arithmetic, and let $\mathrm{tol} > 0$.

**Lemma 1 (the rotation part).** For all $t, s$ and $p$, $|R(\theta + \omega s)\,p - R(\theta + \omega t)\,p| \le |\omega|\,|s - t|\,|p|$.

*Proof.* The two points are on the circle of radius $|p|$, at the angle $|\omega|\,|s - t|$ apart. A chord is at most the arc, which is $|\omega|\,|s - t|\,|p|$. $\square$

**Lemma 2 (the step is safe).** Let $t_0 \in [0, T]$ with $d_0 = d(t_0) > 0$. Let $p_A$ and $p_B$ be a closest pair, $n = (p_A - p_B) / d_0$, and $\mu = -n \cdot (v_A - v_B) + |\omega_A|\, r_A + |\omega_B|\, r_B$. Then for all $t \ge t_0$,
$$d(t) \ge d_0 - (t - t_0)\,\mu.$$

*Proof.* Because $A(t_0)$ and $B(t_0)$ are convex and $p_A, p_B$ is a closest pair, the line through $p_B$ with normal $n$ separates them: $n \cdot x \ge n \cdot p_A$ for $x \in A(t_0)$ and $n \cdot y \le n \cdot p_B$ for $y \in B(t_0)$. So $n \cdot (x - y) \ge d_0$ for every pair. Now take a point $p$ of $A$ and a point $q$ of $B$, and let $h = t - t_0 \ge 0$. Then
$$x_p(t) - x_p(t_0) = v_A h + \big(R(\theta_A + \omega_A t) - R(\theta_A + \omega_A t_0)\big) p,$$
and by Lemma 1, $n \cdot (x_p(t) - x_p(t_0)) \ge h\, n \cdot v_A - h\, |\omega_A|\, r_A$. In the same way, $n \cdot (y_q(t) - y_q(t_0)) \le h\, n \cdot v_B + h\, |\omega_B|\, r_B$. Subtract:
$$n \cdot (x_p(t) - y_q(t)) \ge d_0 + h\, n \cdot (v_A - v_B) - h\,(|\omega_A| r_A + |\omega_B| r_B) = d_0 - h \mu.$$
For a unit vector $n$, $|x - y| \ge n \cdot (x - y)$, so every pair of points is at least $d_0 - h\mu$ apart, and $d(t) \ge d_0 - h\mu$. $\square$

**Theorem.** Let $t_0 = 0 < t_1 < t_2 < \dots$ be the times of the loop. If there is a first contact $t^*$, then every $t_k \le t^*$. If the loop returns a time $t$, then $d(t) \le \mathrm{tol}$ and $t \le t^*$ when $t^*$ exists. If it returns NO-CONTACT, there is no contact in $[0, T]$.

*Proof.* By induction, $t_k \le t^*$, with $t_0 = 0$. A new time $t_{k+1}$ is made only if $d(t_k) > \mathrm{tol} > 0$, so $t_k < t^*$. If $\mu \le 0$, Lemma 2 gives $d(t) \ge d(t_k) > 0$ for all $t \ge t_k$, so there is no contact after $t_k$ and none before it by the induction, and the answer NO-CONTACT of line L7 is right. If $\mu > 0$, Lemma 2 gives $d(t) > 0$ for $t \in [t_k, t_k + d(t_k)/\mu)$, so $t^* \ge t_k + d(t_k)/\mu = t_{k+1}$. If $t_{k+1} > T$, then $t^* > T$, and the answer NO-CONTACT of line L9 is right. A time returned by line L4 is some $t_k$ with $d(t_k) \le \mathrm{tol}$. $\square$

**Termination.** Let $L = |v_A - v_B| + |\omega_A| r_A + |\omega_B| r_B$. Each $\mu$ is at most $L$, so each step that does not stop is at least $d(t_k)/L > \mathrm{tol}/L$. The times grow by more than $\mathrm{tol}/L$ in each step and the loop stops when they pass $T$, so there are at most $\lceil T L / \mathrm{tol} \rceil + 1$ steps. If $L = 0$, the first $\mu$ is 0 and the loop stops at once. $\blacksquare$

**Remarks.** The bound $T L / \mathrm{tol}$ grows without limit as the tolerance goes to 0, and the tests of this page show a grazing motion where the step count grows as the gap shrinks. For a head-on approach without rotation, $\mu$ is exact and one step reaches the contact. For a contact at a positive angle the distance decreases at a rate bounded away from 0 near $t^*$, and the gap then shrinks at least by a constant factor in each step, so the count grows like $\log(1/\mathrm{tol})$. This last claim needs a transversal contact and is not proved here. In floating point the computed distance and the bound have rounding errors, so a step can pass the contact by a few ulps. A small safety margin in the distance, for example using $d - \mathrm{tol}/2$ for the step, prevents this.

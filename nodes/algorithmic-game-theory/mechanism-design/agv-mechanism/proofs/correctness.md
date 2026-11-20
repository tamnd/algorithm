---
title: The AGV mechanism is efficient, strongly budget balanced and Bayesian incentive compatible
proves: [correctness]
status: full
---

The setting has $n \ge 2$ agents and a finite set $O$ of outcomes. Agent $i$ has a type $t_i$ in a finite set $T_i$, drawn from a prior $f_i$, and the types of different agents are independent. The value of agent $i$ of type $t_i$ for outcome $o$ is $v_i(t_i, o)$. The utility is quasilinear: an agent who gets outcome $o$ and pays $p_i$ has utility $v_i(t_i, o) - p_i$. For a profile $t$, write $W(t, o) = \sum_j v_j(t_j, o)$.

## What the code computes

Let $x^*(t)$ be the first outcome in the list $O$ that maximizes $W(t, o)$. Line L3 and line L6 both use this rule. Line L5 adds, for each profile $t$ and each agent $i$, the term $\Pr[t_{-i}] \sum_{j \ne i} v_j(t_j, x^*(t))$ to $h_i(t_i)$, where $\Pr[t_{-i}] = \prod_{j \ne i} f_j(t_j)$. Each profile $t$ with $t_i = s$ is visited once by line L2, so after the loop

$$h_i(s) = \sum_{t_{-i}} \Pr[t_{-i}] \sum_{j \ne i} v_j\big(t_j, x^*(s, t_{-i})\big) = \mathbb{E}_{t_{-i}}\Big[\sum_{j \ne i} v_j\big(t_j, x^*(s, t_{-i})\big)\Big].$$

So $h_i(s)$ is the expected welfare of the other agents when agent $i$ reports $s$ and the others report their true types. Line L8 sets, for the reports $b$,

$$p_i(b) = \frac{1}{n - 1} \sum_{j \ne i} h_j(b_j) - h_i(b_i).$$

## Efficiency

Line L6 returns $x^*(b)$, which maximizes $W(b, o)$ over $O$ by definition. When all agents report their true types, the outcome maximizes the true welfare. This holds at every profile, not only in expectation.

## Strong budget balance

At every profile $b$,

$$\sum_{i} p_i(b) = \frac{1}{n - 1} \sum_{i} \sum_{j \ne i} h_j(b_j) - \sum_i h_i(b_i).$$

In the double sum each index $j$ appears once for each $i \ne j$, that is $n - 1$ times. So the first term is $\sum_j h_j(b_j)$, and the total is $0$. The mechanism pays out exactly what it collects, at every profile and for any reports, true or not.

## Bayesian incentive compatibility

Fix an agent $i$ with true type $t_i$, and let the others report their true types $t_{-i}$, drawn from the prior. If agent $i$ reports $r$, its expected utility is

$$U_i(r \mid t_i) = \mathbb{E}_{t_{-i}}\big[v_i(t_i, x^*(r, t_{-i}))\big] + h_i(r) - \frac{1}{n - 1} \sum_{j \ne i} \mathbb{E}_{t_j}\big[h_j(t_j)\big].$$

The expectation over $t_{-i}$ does not depend on $t_i$, because the types are independent. This is where independence is used. The last term does not depend on $r$. Call it $C_i$. Put in the formula for $h_i(r)$:

$$U_i(r \mid t_i) = \mathbb{E}_{t_{-i}}\Big[v_i(t_i, x^*(r, t_{-i})) + \sum_{j \ne i} v_j(t_j, x^*(r, t_{-i}))\Big] - C_i = \mathbb{E}_{t_{-i}}\big[W((t_i, t_{-i}), x^*(r, t_{-i}))\big] - C_i.$$

For each fixed $t_{-i}$, the outcome $x^*(t_i, t_{-i})$ maximizes $W((t_i, t_{-i}), \cdot)$ over all of $O$, and $x^*(r, t_{-i})$ is one element of $O$. So the term inside the expectation is at least as large for $r = t_i$ as for any other $r$, pointwise in $t_{-i}$. Taking expectations, $U_i(t_i \mid t_i) \ge U_i(r \mid t_i)$ for every $r$. Truth telling is a Bayes-Nash equilibrium, which is the definition of BIC.

The argument uses that $h_i$ was computed with the same outcome rule $x^*$, tie rule included, that the mechanism applies. If line L3 and line L6 broke ties in different ways, the identity above would fail at the tie profiles.

## What is not claimed

The proof gives a Bayes-Nash equilibrium, not a dominant strategy. If the others lie, $h_j(b_j)$ is not the expectation that the formula needs, and a lie of agent $i$ can pay. The node page shows a profile of the public project example where a lie gains $5/2$ ex post. The mechanism is also not individually rational in general. In the same example the low type has interim utility $-15/4$ under truth telling. Adding constants $K_i$ to the payments keeps BIC, and keeps budget balance only if $\sum_i K_i = 0$, so constants cannot always repair interim IR; the Myerson-Satterthwaite theorem shows that in bilateral trade no BIC, budget balanced and efficient mechanism is interim IR.

## Cost

Line L2 visits $\prod_i |T_i|$ profiles, which is $k^n$ when each agent has $k$ types. For each profile line L3 scans $m = |O|$ outcomes at $O(n)$ each, and lines L4 and L5 take $O(n)$ more work if the probability $\Pr[t_{-i}]$ is obtained as $\Pr[t] / f_i(t_i)$ (for positive $f_i$) or as a product of prefix and suffix products. The table $h$ costs $O(n m k^n)$ time and $O(n k)$ space. After that, one run of lines L6 to L9 costs $O(n m + n)$.

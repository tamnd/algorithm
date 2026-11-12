---
title: Termination, the split distribution, the score range and the fit of extremely randomized trees
proves: [correctness]
status: full
---

We use the pseudocode of the page. A node holds a multiset $S$ of examples. An attribute $a$ is constant in $S$ when all its values in $S$ are equal. The split $[a < c]$ sends the examples with $x_a < c$ to the left child.

### Claim 1: each split makes two nonempty children, and BUILD terminates

At line L6 the attribute $a$ is not constant in $S$, so $\min_S a < \max_S a$, and the cut point $c$ lies in $(\min_S a, \max_S a]$. The example with the smallest value of $a$ has $x_a < c$ and goes left. The example with the largest value has $x_a = \max_S a \ge c$ and goes right. So both children are nonempty and strictly smaller than $S$. Each call of BUILD on a node with $|S|$ examples makes at most two calls on smaller nodes, so the recursion ends, and a tree has at most $|S|$ leaves. $\square$

(A uniform draw in the closed interval $[\min_S a, \max_S a]$, as in the paper, equals $\min_S a$ with probability 0. The code draws again in that case.)

### Claim 2: the distribution of the split on one attribute

Let the distinct values of $a$ in $S$ be $v_1 < v_2 < \ldots < v_r$ with $r \ge 2$. The split puts exactly the examples with values $v_1, \ldots, v_j$ on the left when $v_j < c \le v_{j+1}$. Since $c$ is uniform on $(v_1, v_r]$, this happens with probability

$$\frac{v_{j+1} - v_j}{v_r - v_1}, \qquad j = 1, \ldots, r - 1.$$

So the split does not depend on the outputs, and a large gap between two values is cut more often than a small one. Unlike CART, the method depends on the actual values of an attribute, not only on their order. $\square$

### Claim 3: the classification score lies in $[0, 1]$

Let $C$ be the class and $T$ the side of the split of a random example of $S$, and let $H_c = H(C)$, $H_s = H(T)$ and $I = H(C) - H(C \mid T)$, the mutual information. Mutual information is not negative, and $I = H(C) - H(C \mid T) \le H_c$ and $I = H(T) - H(T \mid C) \le H_s$, because conditional entropies are not negative. Hence $0 \le 2I \le H_c + H_s$. Both children are nonempty, so $H_s > 0$, and the score $2I/(H_c + H_s)$ is well defined and in $[0, 1]$. It is 1 exactly when $I = H_c = H_s$, that is when the side of the split determines the class and the class determines the side. It is 0 exactly when the side and the class are independent in $S$. $\square$

### Claim 4: the regression score lies in $[0, 1]$

The score is $\big(\mathrm{var}(S) - \frac{|S_l|}{|S|} \mathrm{var}(S_l) - \frac{|S_r|}{|S|} \mathrm{var}(S_r)\big) / \mathrm{var}(S)$. Line L4 stops when the output is constant, so $\mathrm{var}(S) > 0$. By the law of total variance, $\mathrm{var}(S)$ equals the weighted mean of the variances of the children plus the variance of the two child means, which is not negative. So the numerator is between 0 and $\mathrm{var}(S)$. $\square$

### Claim 5: with $n_{\min} = 2$ and distinct inputs, each tree fits the training set

Let a leaf hold the set $S$. By line L4, $|S| < 2$, or all attributes are constant in $S$, or the output is constant in $S$. If $|S| = 1$, the leaf predicts the output of its example. If all attributes are constant, all examples of $S$ have the same input, so $|S| = 1$ when the inputs are distinct. If the output is constant, the leaf predicts it. In each case the leaf predicts the output of each of its examples, and each training example reaches the leaf that holds it. So each tree has zero training error, and so does the ensemble. This is why the method needs the averaging over $M$ trees to control the variance. $\square$

### Claim 6: the randomization part of the variance falls like $1/M$

Fix the training set. The trees are built with independent random draws, so given the training set, the predictions $t_1(x), \ldots, t_M(x)$ of the trees at a point $x$ are independent and identically distributed. For regression, the variance of their average over the draws is therefore $\mathrm{var}(t_1(x) \mid S)/M$. Over random training sets, the variance of an average of identically distributed predictions with variance $\sigma^2$ and pairwise correlation $\rho$ is $\rho \sigma^2 + (1 - \rho)\sigma^2 / M$, as on the page of [ensemble learning](/ensemble-learning/). Random cut points lower $\rho$, and since the whole sample is used, they do it without the loss of data that a bootstrap sample causes. $\square$

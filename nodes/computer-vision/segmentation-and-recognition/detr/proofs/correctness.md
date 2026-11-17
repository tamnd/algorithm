---
title: The Hungarian algorithm of the code finds a one-to-one matching of least cost, the set loss does not depend on the order of queries or truths when that matching is unique, and the generalized IoU lies in (-1, 1]
proves: [correctness]
status: full
---

The backbone and the transformer are learned and outside the claims. The claims are about the steps of the page that are not learned, as the Python code does them. The cost matrix $c$ has a row for each of the $M$ truths and a column for each of the $N \ge M$ queries.

**Claim 1 (optimal matching).** The function `hungarian` returns a map $\sigma$ of the rows to distinct columns that minimizes $\sum_j c_{j\sigma(j)}$ over all such maps.

*Proof.* The code keeps a potential $u_j$ for each row and $v_i$ for each column, and a partial matching $p$ from columns to rows. Call $\bar c_{ji} = c_{ji} - u_j - v_i$ the reduced cost. The rows are added one at a time. We show three invariants at the end of each phase, for the rows added so far:

- (a) $\bar c_{ji} \ge 0$ for every added row $j$ and every column $i$;
- (b) $\bar c_{ji} = 0$ when row $j$ is matched to column $i$;
- (c) $v_i \le 0$ for every column, and $v_i = 0$ for every column that is not matched.

In the phase of row $r$, the code keeps a set of used columns, starting with a dummy column 0 matched to $r$. The used rows are the rows matched to used columns. For each unused column $i$, the value $\mathit{minv}_i$ is the least reduced cost from a used row to $i$, and $\mathit{way}_i$ is the used column whose row gives it. Each round takes $\delta = \min_i \mathit{minv}_i$ over the unused columns, adds $\delta$ to $u$ of the used rows and subtracts it from $v$ of the used real columns, and makes the column $i^*$ of least $\mathit{minv}$ used.

In the first round, the only used row is $r$ and the only used column is the dummy. So the update changes only $u_r$, to the least reduced cost in row $r$. After it, every reduced cost of row $r$ is non-negative, and those of the other rows are unchanged. In later rounds every used row is an added row or $r$, so all their reduced costs are non-negative, and $\delta \ge 0$. The update does not change $\bar c$ between a used row and a used column. It lowers $\bar c$ by $\delta$ between a used row and an unused column, which stays non-negative by the choice of $\delta$. It raises $\bar c$ by $\delta$ between an unused row and a used column. So (a) holds through the phase, also for row $r$. Every matched pair has both ends used or both unused, so (b) is kept. $v$ only falls, and only for used columns. A used real column is matched, or it is the last column of the phase, which the augmentation matches. So (c) is kept.

The round makes $\bar c$ zero on the edge from the row of $\mathit{way}_{i^*}$ to $i^*$. Both ends are used from then on, so the edge stays at zero. If $i^*$ is matched, its row becomes used and the rounds go on. If $i^*$ is free, the phase ends: the code walks back along $\mathit{way}$ and moves each column on the path to the row of the column before it. Every new matched edge is one of these zero edges, which keeps (b). The old matched edges off the path are not changed, and each row on the path changes its column. So after the phase, $r$ and all earlier rows are matched to distinct columns. A free column always exists, since fewer than $M \le N$ rows are matched during the phase. Each round uses one more column, so a phase has at most $N$ rounds.

At the end every row is matched. By (b), the cost of $\sigma$ is $\sum_j u_j + \sum_{i \text{ matched}} v_i$, which by (c) is $\sum_j u_j + \sum_i v_i$. For any other map $\tau$ of the rows to distinct columns, (a) gives $\sum_j c_{j\tau(j)} \ge \sum_j u_j + \sum_j v_{\tau(j)} \ge \sum_j u_j + \sum_i v_i$, where the last step uses $v_i \le 0$ for the columns that $\tau$ leaves out. So no map costs less than $\sigma$. $\square$

The tests compare the cost of the result with the least cost over all one-to-one maps, on random matrices of up to $5 \times 6$, half of them with integer costs and many ties.

**Claim 2 (order).** Let the matching of least cost be unique. If the queries or the truths are listed in another order, the set loss does not change.

*Proof.* A reordering of the queries permutes the columns of the cost matrix, and a reordering of the truths permutes its rows, with the same entries. One-to-one maps of the two matrices correspond, with the same costs, so the unique optimal maps correspond. Under that map, each query has the same target as before, and the loss is a sum over the queries of a term that depends only on the output of the query and its target. The weights and the box sum over the matched pairs are also the same. So the loss is the same. $\square$

If two matchings tie for the least cost, they can give different losses, since the loss uses $-\log \hat p$ and the cost uses $-\hat p$. Ties then decide which one the solver returns. For outputs with random real values, ties have probability zero, as in the test.

**Claim 3 (generalized IoU).** For boxes $A$ and $B$ of positive area, $\text{GIoU}(A, B) \in (-1, 1]$. It is symmetric, and it equals 1 if and only if $A = B$.

*Proof.* Let $U = |A \cup B| > 0$ and let $H$ be the area of the smallest box that holds both, so $H \ge U$. Then $\text{GIoU} = \text{IoU} - (H - U)/H$, with $0 \le \text{IoU} \le 1$ and $0 \le (H - U)/H < 1$. So $-1 < \text{GIoU} \le 1$. Both parts are symmetric in $A$ and $B$. $\text{GIoU} = 1$ needs $\text{IoU} = 1$, so $|A \cap B| = |A \cup B|$ and $A = B$. Conversely $A = B$ gives $\text{IoU} = 1$ and $H = U$. $\square$

**Claim 4 (loss).** The code returns $\frac{\sum_i w_i(-\log \hat p_i(t_i))}{\sum_i w_i} + \frac{1}{\max(1, M)}\sum_j L_{box}(\hat b_{\sigma(j)}, b_j)$. Here $t_i$ is the class of the truth matched to query $i$, or $\varnothing$, and $w_i$ is 0.1 for $\varnothing$ and 1 otherwise. Each truth gives exactly one query its class, and every other query has the target $\varnothing$. With no truths, the loss is the mean of $-\log \hat p_i(\varnothing)$.

*Proof.* Lines L4 to L7 of the code compute exactly these sums from the map of Claim 1, which is one to one. With $M = 0$, every target is $\varnothing$, all weights are 0.1 and cancel in the mean, and the box sum is empty. $\square$

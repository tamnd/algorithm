---
tag: 37H975
kind: problem
slug: role-mining-problem
name: Role mining problem
aliases:
- basic role mining problem
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Given a user-permission matrix, find the fewest roles whose Boolean product with a user-role matrix gives it exactly. Its decision version is NP-complete.
prereqs: [role-based-access-control, np-complete]
see_also: [role-based-access-control, set-cover, greedy-set-cover, bipartite-graph, edge-clique-cover, garey-johnson-compendium, principle-of-least-privilege, np-complete]
sources:
  - paper: doi:10.1145/1266840.1266870
    title: "Jaideep Vaidya, Vijayalakshmi Atluri and Qi Guo, The role mining problem: finding a minimal descriptive set of roles, Proceedings of the 12th ACM Symposium on Access Control Models and Technologies (SACMAT), 2007, pages 175 to 184"
    locator: "the basic role mining problem, the delta-approx and MinNoise variants, and the proof of NP-completeness by the set basis problem"
  - paper: doi:10.1145/1805974.1805983
    title: "Jaideep Vaidya, Vijayalakshmi Atluri and Qi Guo, The role mining problem: a formal perspective, ACM Transactions on Information and System Security 13(3), 2010"
    locator: the journal version, with the variants and their relation to known problems
  - paper: doi:10.1109/ACSAC.2008.38
    title: "Qi Guo, Jaideep Vaidya and Vijayalakshmi Atluri, The role hierarchy mining problem: discovery of optimal role hierarchies, Annual Computer Security Applications Conference (ACSAC), 2008, pages 237 to 246"
    locator: the role hierarchy mining problem
---

The role mining problem asks for the smallest set of roles that explains an existing assignment of permissions to users. The input is the user-permission matrix of a system, as it is before the move to [role-based access control](/role-based-access-control/). The output is a set of roles, each a set of permissions, and an assignment of roles to users, such that each user gets exactly the permissions he has now, no more and no fewer. Vaidya, Atluri and Guo stated it in 2007 and showed that its decision version is NP-complete. The problem is the same as the Boolean rank of a 0-1 matrix and as the minimum biclique cover of a bipartite graph.

## In plain words

A company has many users and many permissions, and a big table that says which user has which permission. It wants to replace the table with roles, such as "clerk" or "auditor": each role is a bundle of permissions, and each user gets some roles. The goal is to use as few roles as possible, under one strict condition: after the change, every user must have exactly the same permissions as before. A user may not lose a permission he needs, and he may not gain one he did not have. Finding the smallest number of roles is hard in general, so tools use fast methods that find a good set of roles but not always the best one. Some versions of the problem allow a small number of errors in return for fewer roles.

## Definition

Let $U$ be a set of $u$ users and $P$ a set of $p$ permissions. On this page $u$ is the number of users, $p$ the number of permissions and $k$ the number of roles. The input is a 0-1 matrix $\mathit{UPA}$ of size $u \times p$, with $\mathit{UPA}[i, j] = 1$ if user $i$ has permission $j$.

A *role set* of size $k$ is a pair of 0-1 matrices: $\mathit{UA}$ of size $u \times k$ (users to roles) and $\mathit{PA}$ of size $k \times p$ (roles to permissions). Their Boolean product is

$$(\mathit{UA} \otimes \mathit{PA})[i, j] = \bigvee_{l=1}^{k} \bigl(\mathit{UA}[i, l] \wedge \mathit{PA}[l, j]\bigr).$$

**Basic role mining problem.** Given $\mathit{UPA}$, find $\mathit{UA}$ and $\mathit{PA}$ with $\mathit{UA} \otimes \mathit{PA} = \mathit{UPA}$ and $k$ as small as possible.

**Decision version.** Given $\mathit{UPA}$ and an integer $k$, is there a role set of size at most $k$ with $\mathit{UA} \otimes \mathit{PA} = \mathit{UPA}$?

The minimum $k$ is the *Boolean rank* of $\mathit{UPA}$. In graph terms, let $G$ be the [bipartite graph](/bipartite-graph/) with users on one side, permissions on the other, and an edge for each 1 of $\mathit{UPA}$. A role $l$ is a complete bipartite subgraph (a biclique) between the users that have it and its permissions. The product equals $\mathit{UPA}$ exactly when every biclique uses only edges of $G$ and every edge is in some biclique. So the minimum $k$ is the minimum number of bicliques that cover the edges of $G$.

## Variants

- **Delta-approx role mining** (Vaidya, Atluri and Guo 2007). Given $\delta$, find the smallest $k$ with $\lVert \mathit{UA} \otimes \mathit{PA} - \mathit{UPA} \rVert_1 \le \delta$, where the norm counts the cells that differ. The basic problem is the case $\delta = 0$.
- **MinNoise role mining** (Vaidya, Atluri and Guo 2007). Given $k$, find a role set of size $k$ that minimizes the number of cells that differ.
- **Fewest assignments.** Minimize $|\mathit{UA}| + |\mathit{PA}|$, the number of 1s in the two matrices, instead of $k$. This measures the work of the administrators more closely than the number of roles.
- **Role hierarchy mining** (Guo, Vaidya and Atluri 2008). Find roles together with a hierarchy among them, so that a role inherits the permissions of the roles below it, and minimize the size of the hierarchy.

The approximate variants have a security cost. A cell with 1 in the product and 0 in $\mathit{UPA}$ gives a user a permission he did not have. If the adversary is a user who uses every permission he holds, such a cell is a real gain for him and a break of the [principle of least privilege](/principle-of-least-privilege/). A cell with 0 in the product and 1 in $\mathit{UPA}$ only blocks his work. So tools often allow only the second kind of error.

## Examples

Take four users and five permissions:

| user | permissions |
|---|---|
| $u_1$ | $p_1, p_2, p_3$ |
| $u_2$ | $p_1, p_2$ |
| $u_3$ | $p_3, p_4, p_5$ |
| $u_4$ | $p_1, p_2, p_3, p_4, p_5$ |

Three roles suffice: $r_1 = \{p_1, p_2\}$, $r_2 = \{p_3\}$ and $r_3 = \{p_4, p_5\}$, with $u_1 \mapsto \{r_1, r_2\}$, $u_2 \mapsto \{r_1\}$, $u_3 \mapsto \{r_2, r_3\}$ and $u_4 \mapsto \{r_1, r_2, r_3\}$. A search over all role sets shows that there are five optimal role sets of size 3.

Two roles are not enough, for two separate reasons. First, the four users have four different nonempty permission sets, and with $k$ roles there are at most $2^k - 1$ different nonempty unions of roles, which is 3 for $k = 2$. Second, the three cells $(u_2, p_1)$, $(u_3, p_4)$ and $(u_1, p_3)$ are pairwise *isolated*: no role can contain two of them, because a role that gives $p_1$ to $u_2$ and $p_4$ to $u_3$ would also give $p_4$ to $u_2$, which is 0 in $\mathit{UPA}$, and the other two pairs fail at $(u_2, p_3)$ and $(u_1, p_4)$. Each of the three cells needs its own role.

## Known algorithms

- **Remove duplicates** (exact). Users with equal rows can share one role set, and permissions with equal columns can be merged into one. This never changes the minimum $k$.
- **Kernel and exact search** (theorem). After duplicates are removed, a matrix with Boolean rank at most $k$ has at most $2^k$ different rows and at most $2^k$ different columns, since each row is a union of a subset of the $k$ roles and each column is the set of users of a subset of the roles. So if there are more than $2^k$ distinct rows, the answer is no. Otherwise the reduced matrix has size at most $2^k \times 2^k$, and an exhaustive search over the roles, each a subset of the at most $2^k$ columns, decides the instance. The total time is polynomial in $u$ and $p$ plus a function of $k$ alone, so the decision problem is fixed-parameter tractable in $k$. The function of $k$ is doubly exponential, so this is useful only for very small $k$.
- **Greedy cover by maximal bicliques** (theorem for the ratio). Every role of an optimal solution can be grown to a maximal biclique of $G$ without breaking exactness, so there is an optimal solution made of maximal bicliques. Running [greedy set cover](/greedy-set-cover/) with the edges as elements and the maximal bicliques as sets gives at most $H(e) \le 1 + \ln e$ times the minimum number of roles, where $e$ is the number of 1s in $\mathit{UPA}$. The weak point is that $G$ can have exponentially many maximal bicliques.
- **Candidate roles from intersections** (heuristic). Practical tools build candidate roles from the permission sets of the users and their pairwise intersections, which are polynomially many, and then pick roles from the candidates greedily. This keeps the result exact but gives no bound on its size.
- **Integer programming and SAT** (exact). The decision version for a given $k$ is a [SAT](/sat/) instance with $k(u + p)$ main variables, one for each cell of $\mathit{UA}$ and $\mathit{PA}$. How large a matrix a solver handles in practice is a matter of measurement, not of a proven bound.

## Bounds

Each item is a theorem.

- **Upper bound.** $k \le \min(u, p)$: one role per user (its row) or one role per permission (assigned to the users of its column) is always exact.
- **Counting lower bound.** If $\mathit{UPA}$ has $d$ distinct nonempty rows, then $k \ge \lceil \log_2(d + 1) \rceil$.
- **Isolated set lower bound.** A set of 1 cells such that for any two of them, $(i, j)$ and $(i', j')$, one of $\mathit{UPA}[i, j']$ and $\mathit{UPA}[i', j]$ is 0, needs one role per cell. So $k$ is at least the size of the largest such set.
- **Hardness.** The decision version is NP-complete (Vaidya, Atluri and Guo 2007). It is in NP because a role set of size $k \le \min(u, p)$ is a certificate of polynomial size that is checked by one Boolean matrix product.

## Reductions

- **Set basis.** In the set basis problem (problem SP7 in the [Garey and Johnson compendium](/garey-johnson-compendium/)), the input is a collection $C$ of subsets of a finite set and an integer $k$, and the question is whether there are $k$ sets such that each member of $C$ is a union of some of them. Take $C$ to be the set of rows of $\mathit{UPA}$: the basic role mining problem with bound $k$ is then exactly set basis with bound $k$. Since set basis is NP-complete, so is role mining. Vaidya, Atluri and Guo use this reduction.
- **Biclique cover.** As in the definition, role mining is the minimum cover of the edges of a bipartite graph by bicliques. The covering form is close to [edge clique cover](/edge-clique-cover/), where the graph is general and the covering sets are cliques.
- **Set cover.** Once a family of candidate roles is fixed, choosing the fewest of them is an instance of [set cover](/set-cover/) on the 1 cells of $\mathit{UPA}$.
- **Boolean matrix factorization.** Role mining is exact factorization of a 0-1 matrix over the Boolean semiring with the smallest inner dimension. The MinNoise variant is the approximate factorization studied in data mining.

## Applications

- **Role engineering.** Moving a large organization to role-based access control needs an initial set of roles. Bottom-up role mining finds them from the current permissions; top-down role engineering starts from job functions. Most projects use both.
- **Access review.** Users whose permissions are far from every mined role are candidates for review, since their access may be a leftover of earlier jobs.
- **Separation of duty.** Mined roles must still be checked against [separation of duty](/separation-of-duty/) constraints, which a pure minimization ignores.

## References

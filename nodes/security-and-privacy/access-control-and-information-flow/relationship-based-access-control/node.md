---
tag: R6C5QA
kind: model
slug: relationship-based-access-control
name: Relationship-based access control
aliases:
- ReBAC
area: security-and-privacy/access-control-and-information-flow
level: advanced
summary: Decides access by the paths of relations between the requester and the resource or its owner in a social or organizational graph.
model: word-ram
prereqs: [access-control-matrix, breadth-first-search, nondeterministic-finite-automaton]
see_also: [regular-path-query, attribute-based-access-control, role-based-access-control, access-control-list, graph-reachability, datalog, transitive-closure, authorization-logic]
sources:
  - paper: doi:10.1145/1943513.1943539
    title: Philip W. L. Fong, Relationship-based access control, protection model and policy language, ACM Conference on Data and Application Security and Privacy (CODASPY), 2011
    locator: pages 191 to 202 (the protection model with a social network as protection state, and a modal logic for policies)
  - url: "https://www.usenix.org/conference/atc19/presentation/pang"
    title: Ruoming Pang and others, Zanzibar, Google's consistent, global authorization system, USENIX ATC 2019
    locator: pages 33 to 46 (relation tuples, usersets and rewrite rules in namespace configurations, the check as a graph search, and the snapshot tokens that keep checks consistent)
  - paper: doi:10.1109/2.485845
    title: Ravi S. Sandhu, Edward J. Coyne, Hal L. Feinstein and Charles E. Youman, Role-based access control models, IEEE Computer 29(2), 1996
    locator: pages 38 to 47 (roles as the fixed relation between users and permissions that ReBAC generalizes)
---

Relationship-based access control (ReBAC) decides a request by the relations between the requester and the resource in a graph: "friends of the owner may see this photo", "the members of a group that is a viewer of this folder may read the files in it", "the doctor of this patient may write this record". The protection state is a labeled graph of users, resources and other entities, and a policy says which paths in the graph give a right. Fong (2011) gave a protection model with a social network as its state and a modal logic as its policy language, and Google's Zanzibar (2019) stores the relations as tuples and answers access checks by graph search for many services. ReBAC differs from [RBAC](/role-based-access-control/), where the relation between users and permissions passes through a fixed set of roles, and from [ABAC](/attribute-based-access-control/), where each rule tests the attributes of single entities, not paths between them.

## The machine

**State.** A finite directed graph $G = (V, E)$ with edge labels from a finite set $\Sigma$ of relation names. The vertices are users and resources, and also groups, folders or organizations. An edge $(x, \ell, y)$ says that $x$ stands in relation $\ell$ to $y$: alice *friend* bob, bob *member* eng, eng *viewer* readme. Write $n = |V|$ and $m = |E|$.

**Policy.** For each resource type and action, a set of allowed paths, given as a regular expression or an automaton over $\Sigma$; a reverse edge $\ell^{-1}$ lets a path follow $\ell$ backwards. A request "may $u$ do $a$ to $v$?" is allowed when the graph has a path from $u$ to $v$ (or from the owner of $v$ to $u$, by the policy) whose labels spell a word of the language for $a$. Fong's model states policies in a modal logic whose formulas talk about the neighbours of the owner and of the requester; Zanzibar states them as rewrite rules over relations, such as "every editor is a viewer" and "the viewers of a document include the viewers of its parent folder".

**Decision.** The check is a [regular path query](/regular-path-query/): a search of the product of the graph with an automaton $(Q, \Sigma, \delta, q_0, F)$ for the policy, as in [breadth-first search](/breadth-first-search/):

```pseudo id=main
CHECK(G, A, u, v)
L1  seen ← {(u, q0)}; queue ← [(u, q0)]
L2  while queue is not empty do
L3      (x, q) ← remove the first pair of queue
L4      if x = v and q ∈ F then return true
L5      for each edge (x, l, y) of G and each q' ∈ δ(q, l) do
L6          if (y, q') ∉ seen then add (y, q') to seen and to queue
L7  return false
```

Each pair (vertex, state) enters the queue at most once, so the search ends. It returns true exactly when some path from $u$ to $v$ spells a word that the automaton accepts.

**Transitions.** Users change the graph: they add or remove friends, join groups, share a folder with a group, create resources. Each change of an edge can change many cells of the implied [access control matrix](/access-control-matrix/) at once. The policies are usually fixed by the service.

**Example.** A social network has friend edges in both directions: alice and bob, bob and carol, carol and dave. Alice shares a photo with "friends of friends", the language $\mathit{friend} \cdot (\epsilon \mid \mathit{friend})$ of paths of length 1 or 2 from alice. A request by carol is allowed: alice, bob, carol is a path of two friend edges. A request by dave is denied: the shortest path has three edges. If bob and carol stop being friends, carol loses access with no change to the photo.

In the Zanzibar style, the tuples (readme, viewer, group eng as a set of members) and (eng, member, alice) say that the members of eng may view readme and that alice is a member. A check for alice and readme follows the two tuples and allows the request. Adding (eng, member, erin) gives erin access to every resource shared with eng.

## What it counts

**The access decision.** The product search of lines L1 to L7 has at most $|Q| \cdot n$ pairs. For each pair $(x, q)$ it reads the edges out of $x$ and, for each, at most $|Q|$ next states, so it takes $O(|Q| \cdot n + |Q|^2 \cdot m)$ time in the worst case. For a fixed policy this is linear in the size of the graph, $O(n + m)$. A policy with a bounded path length, such as "friends of friends", needs only the neighbours within that distance, which is how large services keep checks fast.

**What the matrix would cost.** The implied matrix has a cell for each user and resource, and one new edge can change a whole block of it. ReBAC stores the graph, of size $O(n + m)$, and computes cells on demand; storing the matrix, or the [transitive closure](/transitive-closure/) of the group relations, trades space and the cost of updates for faster checks.

## Relation to other models

- **Access lists.** A relation tuple (object, relation, user) is an entry of an [access control list](/access-control-list/). When the user can be a set given by another tuple, the lists point into each other and a check becomes a search; this is how Zanzibar extends ACLs.
- **RBAC.** A role is a vertex with *member* edges from users and *grants* edges to permissions; the RBAC check is the regular path query $\mathit{member} \cdot \mathit{senior}^* \cdot \mathit{grants}$. ReBAC lets the path pass through any relation, and lets the relation depend on the resource, as in "the owner's friends".
- **ABAC.** An attribute is a relation to a value. ReBAC adds paths of any length; ABAC adds arithmetic and comparisons on values.
- **Logic.** A regular path query is a recursive query, so ReBAC policies can be written in [Datalog](/datalog/), as can the policies of [authorization logics](/authorization-logic/).

## Known results in the model

- **Decision.** With policies given as regular expressions or finite automata over relation names, a check is a regular path query, decidable in time $O(|Q| \cdot n + |Q|^2 \cdot m)$ by the product construction above.
- **Policies as modal formulas.** In Fong's model (2011) a policy is a formula of a modal logic that is evaluated on the social graph, with the owner and the requester as the two points of view; it can state conditions such as "the requester is a friend of a friend of the owner".
- **Consistency at scale.** Zanzibar (2019) keeps checks consistent with the order of changes: a client gets a snapshot token when it changes content, and a later check is evaluated at a snapshot at least as new. This prevents the case where a user removed from a list still sees content added after the removal.

## References

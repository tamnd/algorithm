# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/potential-based-reward-shaping/. The authors are listed in prov/C2XHTJ.jsonl.

"""Potential-based reward shaping (Ng, Harada and Russell, 1999).

The shaped reward of a transition (s, a, s') is r + F(s, s') with
F(s, s') = gamma * Phi(s') - Phi(s), and Phi = 0 on terminal states.

An MDP here is a dict mdp[(s, a)] = list of (prob, r, s2, done). Values are
exact when the inputs are Fractions: optimal_q uses policy iteration with
exact linear solves. Cost of optimal_q: O(I * S^3) for I improvement rounds.
"""


def shaping_term(phi, s, s2, done: bool, gamma):
    """F(s, s') = gamma Phi(s') - Phi(s), with Phi(terminal) = 0."""
    phi_next = 0 if done else phi[s2]  # @line L1
    return gamma * phi_next - phi[s]  # @line L3


def shape_mdp(mdp, phi, gamma):
    """The shaped MDP M' with rewards r + F(s, s')."""
    out = {}
    for (s, a), outcomes in mdp.items():  # @line L2
        out[(s, a)] = [(p, r + shaping_term(phi, s, s2, done, gamma), s2, done)  # @line L4
                       for p, r, s2, done in outcomes]  # @line L5
    return out


def shaped_q_learning(transitions, q0, phi, gamma, lr):
    """Tabular Q-learning on a fixed sequence of transitions (s, a, r, s2, done),
    with the shaped reward r + F(s, s2). q0 is the initial table (dict of lists)."""
    q = {s: list(row) for s, row in q0.items()}
    for s, a, r, s2, done in transitions:
        r2 = r + shaping_term(phi, s, s2, done, gamma)  # @line L4
        target = r2 if done else r2 + gamma * max(q[s2])  # @line L5
        q[s][a] += lr * (target - q[s][a])
    return q


def recover_q(q_shaped, phi):
    """Q_M(s, a) = Q_M'(s, a) + Phi(s)."""
    return {s: [x + phi[s] for x in row] for s, row in q_shaped.items()}  # @line L6


def states_actions(mdp):
    states = sorted({s for s, _ in mdp})
    actions = {s: sorted(a for t, a in mdp if t == s) for s in states}
    return states, actions


def solve(mat, rhs):
    """Solve mat x = rhs by Gauss-Jordan elimination (exact with Fractions)."""
    k = len(rhs)
    m = [list(mat[i]) + [rhs[i]] for i in range(k)]
    for c in range(k):
        p = next(i for i in range(c, k) if m[i][c] != 0)
        m[c], m[p] = m[p], m[c]
        for i in range(k):
            if i != c and m[i][c] != 0:
                f = m[i][c] / m[c][c]
                m[i] = [x - f * y for x, y in zip(m[i], m[c])]
    return [m[i][k] / m[i][i] for i in range(k)]


def q_of_policy(mdp, policy, gamma):
    """Exact Q^pi of a deterministic policy {s: a}."""
    states, actions = states_actions(mdp)
    idx = {s: i for i, s in enumerate(states)}
    n = len(states)
    mat = [[0] * n for _ in range(n)]
    rhs = [0] * n
    for s in states:
        i = idx[s]
        mat[i][i] += 1
        for p, r, s2, done in mdp[(s, policy[s])]:
            rhs[i] += p * r
            if not done:
                mat[i][idx[s2]] -= gamma * p
    v = solve(mat, rhs)
    q = {}
    for s in states:
        q[s] = []
        for a in actions[s]:
            q[s].append(sum(p * (r if done else r + gamma * v[idx[s2]])
                            for p, r, s2, done in mdp[(s, a)]))
    return q


def optimal_q(mdp, gamma):
    """Exact Q* by policy iteration; returns (Q*, a greedy optimal policy)."""
    states, actions = states_actions(mdp)
    policy = {s: actions[s][0] for s in states}
    while True:
        q = q_of_policy(mdp, policy, gamma)
        changed = False
        for s in states:
            best = max(q[s])
            cur = q[s][actions[s].index(policy[s])]
            if cur < best:
                policy[s] = actions[s][q[s].index(best)]
                changed = True
        if not changed:
            return q, policy


def optimal_action_sets(q):
    return {s: {a for a, x in enumerate(row) if x == max(row)} for s, row in q.items()}

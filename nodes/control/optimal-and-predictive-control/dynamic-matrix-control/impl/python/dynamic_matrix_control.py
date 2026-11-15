# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/dynamic-matrix-control/. The authors are listed in prov/078WY3.jsonl.

"""Dynamic matrix control (DMC) for a single input and a single output.

The model is the truncated step response s_1, ..., s_Ns of the plant: s_i is
the output i samples after a unit step of the input, and s_i = s_Ns for
i >= Ns. With the input moves du(k) = u(k) - u(k-1), the model output is

    yhat(k) = sum_(j >= 1) s_min(j, Ns) du(k - j).

At each sample the controller:

1. compares the measured output with the model output and takes the
   difference d(k) = y(k) - yhat(k) as a constant output disturbance over
   the horizon;
2. computes the free response f_i, i = 1..P: the predicted output if no
   more moves are made, plus d(k);
3. chooses the next M moves to minimize
       sum_(i=1)^P (r - f_i - (S du)_i)^2 + lam sum_(j=0)^(M-1) du(k+j)^2,
   where S is the P x M dynamic matrix, S_ij = s_(i-j+1) for i >= j and 0
   otherwise; the minimizer is du = (S^T S + lam I)^-1 S^T (r - f);
4. applies only the first move.

Without constraints the first row of (S^T S + lam I)^-1 S^T is a constant
vector, so DMC is a linear time-invariant controller.
"""

__all__ = ["dynamic_matrix", "dmc_gain", "DMC", "step_response"]


def _solve(a, b):
    n = len(a)
    m = [list(map(float, r)) + [float(v)] for r, v in zip(a, b)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        if m[p][c] == 0.0:
            raise ValueError("singular matrix")
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[r][c] != 0.0:
                f = m[r][c] / m[c][c]
                m[r] = [x - f * y for x, y in zip(m[r], m[c])]
    return [m[i][n] / m[i][i] for i in range(n)]


def step_response(plant_step, Ns):
    """Return [s_1, ..., s_Ns] by running plant_step(u) from rest with u = 1.

    plant_step takes the input of sample k and returns the output of sample
    k + 1; it must start at rest.
    """
    return [plant_step(1.0) for _ in range(Ns)]


def dynamic_matrix(s, P, M):
    """Return the P x M dynamic matrix S_ij = s_(i-j+1) (0 above the diagonal)."""
    Ns = len(s)
    return [[s[min(i - j, Ns - 1)] if i >= j else 0.0 for j in range(M)] for i in range(P)]


def dmc_gain(s, P, M, lam):
    """Return all M rows of (S^T S + lam I)^-1 S^T, as a list of rows of length P."""
    S = dynamic_matrix(s, P, M)  # @line L1
    StS = [[sum(S[i][a] * S[i][b] for i in range(P)) + (lam if a == b else 0.0) for b in range(M)]
           for a in range(M)]
    cols = []
    for i in range(P):  # column i of the gain solves (S^T S + lam I) g = S^T e_i
        cols.append(_solve(StS, [S[i][a] for a in range(M)]))  # @line L2
    return [[cols[i][a] for i in range(P)] for a in range(M)]


class DMC:
    """Unconstrained DMC controller with the step model s and the tuning P, M, lam."""

    def __init__(self, s, P, M, lam, u0=0.0):
        if P > len(s) - 1:
            raise ValueError("the step model must be longer than the prediction horizon")
        self.s, self.P, self.M, self.lam = [float(v) for v in s], P, M, lam
        self.Ns = len(s)
        self.K = dmc_gain(self.s, P, M, lam)[0]
        self.u = float(u0)
        self.moves = [0.0] * self.Ns  # du(k-1), ..., du(k-Ns)
        self.older = 0.0  # sum of the moves older than Ns samples
        self.d = 0.0

    def _s(self, i):
        return self.s[min(i, self.Ns) - 1]

    def model_output(self, ahead=0):
        """Model output at k + ahead with no future moves (without d)."""
        y = sum(self._s(ahead + j) * dj for j, dj in enumerate(self.moves, start=1))
        return y + self.s[-1] * self.older

    def free_response(self, y_meas):
        """Return f_1..f_P and set d(k) = y_meas - yhat(k)."""
        self.d = y_meas - self.model_output(0)  # @line L4
        return [self.model_output(i) + self.d for i in range(1, self.P + 1)]  # @line L5

    def step(self, y_meas, r):
        """Return the input u(k) for the measured y(k) and the setpoint r."""
        f = self.free_response(y_meas)  # @line L3
        rr = r if isinstance(r, list) else [r] * self.P
        du = sum(k * (ri - fi) for k, ri, fi in zip(self.K, rr, f))  # @line L6
        self.older += self.moves[-1]  # @line L7
        self.moves = [du] + self.moves[:-1]
        self.u += du
        return self.u

    def predict(self, y_meas, du_future):
        """Predicted outputs y(k+1..k+P) for the future moves du_future (length M)."""
        f = self.free_response(y_meas)
        S = dynamic_matrix(self.s, self.P, self.M)
        return [fi + sum(S[i][j] * du_future[j] for j in range(self.M)) for i, fi in enumerate(f)]

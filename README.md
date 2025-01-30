# Enhanced-Portfolio-Optimization
Enhanced Portfolio Optimization (EPO)

Refactoring original R repository https://github.com/Reckziegel/epo

The Enhanced Portfolio Optimization (EPO) method, described in Pedersen,
Babu and Levine (2021), proposes a unifying theory on portfolio
optimization. Employing Principal Component Analysis (PCA), the EPO
method ranks portfolios based on their variance, from the most to the
least important principal components. Notably, the least important
principal components emerge as “problem portfolios”, primarily due to
their low *estimated* risk, leading to the underestimation of their
*true* risks. These portfolios offer high expected returns (*ex-ante*)
and low realized Sharpe Ratios (*ex-post*), underscoring the challenges
faced when using them through standard approaches.

To fix this issue, EPO introduces a straightforward yet powerful
strategy: it shrinks correlations! The key insight from Pedersen, Babu,
and Levine (2021) is that by reducing correlations close to zero, the
volatilities of these “problem portfolios” are effectively increased.
Consequently, the EPO method stabilizes Mean-Variance Optimization (MVO)
by adjusting downward the Sharpe-Ratios of the least important
components.

The elegance of the EPO approach lies in its connection to three leading
methods: MVO, Bayesian Optimization, and Robust Optimization. By
incorporating a closed-form solution with a single shrinkage parameter,
denoted as $w \in \{0, 1\}$, the investor can seamlessly navigate
through the optimization process. In the “Simple EPO”, a $w=0$ coincides
with the classical MVO. Conversely, a $w=1$ completely disregards
correlations, resulting in a portfolio allocation that do not optimize.

In real-world applications, it is crucial to consider the potential
deviation from a reference point or benchmark. EPO effectively handles
this concern through the “Anchored EPO”. When a anchor needs to be
considered, a $w=0$ aligns with the classical MVO, while a $w=1$
precisely matches the benchmark. The most interesting outcome arise when
$0 < w < 1$, leading to portfolios resembling the Black-Litterman model.
Here, the shrinking parameter, $w$, tunes the confidence in the *prior*,
offering a flexible and dynamic optimization process. However, unlike
Black-Litterman, the “Anchored EPO” does not restrict the reference
point to the “Market Portfolio,” making it more general and widely
applicable.

Overall, the Enhanced Portfolio Optimization (EPO) method presents a
novel, efficient, and adaptable framework for portfolio optimization.
Its ability to address the limitations of traditional methods while
incorporating various optimization approaches through a single parameter
makes it a compelling tool for investors seeking more stable and
well-tailored portfolios.

## References

- Pedersen, Lasse Heje and Babu, Abhilash and Levine, Ari, Enhanced
  Portfolio Optimization (January 2, 2020). Lasse Heje Pedersen,
  Abhilash Babu, and Ari Levine (2021), Enhanced Portfolio Optimization,
  Financial Analysts Journal, 77:2, 124-151, DOI:
  10.1080/0015198X.2020.1854543 , Available at
  SSRN: <https://www.ssrn.com/abstract=3530390> or [http://dx.doi.org/10.2139/ssrn.3530390](https://dx.doi.org/10.2139/ssrn.3530390)

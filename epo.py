import numpy as np
import pandas as pd

def epo(x, signal, lambda_, method='simple', w=0, anchor=None, normalize=True, endogenous=True):
    """
    Enhanced Portfolio Optimization (EPO)

    Computes the optimal portfolio allocation using the EPO method.

    Parameters:
    ----------
    x : np.ndarray or pd.DataFrame
        A dataset with asset returns. It should be a 2D array (matrix) or a pandas DataFrame.
    
    signal : np.ndarray
        A 1D array (vector) containing the investor's beliefs (signals or forecasts) regarding asset returns.
    
    lambda_ : float
        A scalar representing the investor's risk-aversion preference. Higher values indicate greater risk aversion.
    
    method : str, optional
        A string specifying the method to use for optimization. It can be one of the following:
        - "simple": Traditional Mean-Variance Analysis.
        - "anchored": Anchored EPO, which considers a benchmark allocation.
        Default is "simple".
    
    w : float, optional
        A scalar between 0 and 1 representing the shrinkage level. This parameter controls the weight given to the 
        classical mean-variance optimization versus the shrunk estimates. Default is 0.
    
    anchor : np.ndarray, optional
        A 1D array (vector) representing the anchor (benchmark) allocation. This parameter is only used when 
        `method` is set to "anchored". It specifies the allocation that the optimized portfolio should not deviate 
        too much from. Default is None.
    
    normalize : bool, optional
        A boolean indicating whether the allocation should be normalized to sum to 1 (full-investment constraint).
        Default is True.
    
    endogenous : bool, optional
        A boolean indicating whether the risk-aversion parameter should be considered endogenous. This parameter is 
        only used when `method` is set to "anchored". Default is True.

    Returns:
    -------
    np.ndarray
        The optimal allocation vector, which represents the weights of the assets in the portfolio.

    Examples:
    --------
    # Example usage with simulated data
    import numpy as np
    import pandas as pd

    np.random.seed(123)
    log_ret = np.random.normal(0, 1, (100, 4)) / 10  # Simulated log returns
    sigma = np.cov(log_ret, rowvar=False)  # Covariance matrix
    signal = np.mean(log_ret, axis=0)  # Example signal (mean returns)

    # 1/N reference
    b = np.repeat(1 / log_ret.shape[1], log_ret.shape[1])

    # Simple EPO
    optimal_allocation_simple = epo(x=log_ret, signal=signal, lambda_=10, method="simple", w=0)

    # Anchored EPO
    optimal_allocation_anchored = epo(x=log_ret, signal=signal, lambda_=10, method="anchored", w=0.5, anchor=b)
    """
    if not isinstance(x, (pd.DataFrame, np.ndarray)):
        raise ValueError("`x` must be a DataFrame or a numpy array.")
    
    if method not in ['simple', 'anchored']:
        raise ValueError("`method` not accepted. Try `simple` or `anchored` instead.")
    
    if anchor is None and method == 'anchored':
        raise ValueError("When the `anchored` method is chosen the `anchor` can't be `None`.")

    # Convert to numpy array if x is a DataFrame
    if isinstance(x, pd.DataFrame):
        x = x.to_numpy()
    
    # Ensure signal is a 1D array
    signal = np.asarray(signal).flatten()
    
    # Ensure anchor is a 1D array if provided
    if anchor is not None:
        anchor = np.asarray(anchor).flatten()

    # Begin Computation
    n = x.shape[1]
    vcov = np.cov(x, rowvar=False)
    corr = np.corrcoef(x, rowvar=False)
    I = np.eye(n)
    V = np.zeros((n, n))
    np.fill_diagonal(V, np.diag(vcov))
    std = np.sqrt(np.diag(V))
    
    shrunk_cor = (1 - w) * I @ corr + w * I  # equation 7
    cov_tilde = std[:, None] * shrunk_cor * std  # topic 2.II: page 11
    inv_shrunk_cov = np.linalg.inv(cov_tilde)

    # The simple EPO
    if method == "simple":
        epo_result = (1 / lambda_) * inv_shrunk_cov @ signal  # equation 16

    # The anchored EPO
    elif method == "anchored":
        if endogenous:
            gamma = np.sqrt(anchor @ cov_tilde @ anchor) / np.sqrt(signal @ inv_shrunk_cov @ cov_tilde @ inv_shrunk_cov @ signal)
            epo_result = inv_shrunk_cov @ ((1 - w) * gamma * signal + w * I @ V @ anchor)  # equation 17
        else:
            epo_result = inv_shrunk_cov @ ((1 - w) * (1 / lambda_) * signal + w * I @ V @ anchor)

    # Normalize if required
    if normalize:
        epo_result = epo_result / np.sum(epo_result)

    return epo_result
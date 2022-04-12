import numpy as np
from numpy import random as rng
from numpy import linalg as la
from scipy import optimize
from scipy.stats import norm
from scipy.stats import genextreme
from tabulate import tabulate




def estimate(
        func: object, 
        theta0: list, 
        y: np.array, 
        x: np.array, 
        cov_type='Outer Product',
        disp = True,
        **kwargs
    ):
    """Takes a function and returns the minimum, given start values and 
    variables to calculate the residuals.

    Args:
        func (object): The function to minimize
        theta0 (list): A list with starting values.
        y (np.array): Array of dependent variable.
        x (np.array): Array of independent variables.
        cov_type (str, optional): String for which type of variances to 
        calculate. Defaults to 'Outer Product'.
        disp (bool, optional): To display extra information after the 
        optimize.minimize function is finished. Defaults to True.

    Returns:
        dict: Returns a dictionary with results from the estimation.
    """
    
    # The minimzer can't handle 2-D arrays, so we flatten them to 1-D.
    theta0 = theta0.flatten()
    y = y.flatten()
    n = y.size

    # Objective function must return a single number, so we sum it. 
    # We also scale the sum, as the optimizer is sensitive to large scales.
    obj_func = lambda theta: -(1/n)*np.sum(func(theta, y, x))
    result = optimize.minimize(
        obj_func, theta0, options={'disp': disp},  **kwargs
        )
    
    cov, se = variance(func, y, x, result, cov_type)   
    names = ['b_hat', 'se', 't_values', 'cov', 'iter', 'fiter']
    results = [result.x, se, result.x/se, cov, result.nit, result.nfev]
    return dict(zip(names, results))


def clogit(theta: np.array, y: np.array, x: np.array):
    """Inputs data and coefficients, and outputs a vector with
    log choice probabilities dependent on actual choice from y vector.

    Args:
        theta (np.array): Coefficients, or weights for the x array.
        y (np.array): Dependent variable
        x (np.array): Independent variable

    Returns:
        np.array: Log choice probabilities with dimensions (n, 1)
    """
    n, _, _ = x.shape
    
    ccp, logccp = choice_prob(theta, x)
    
    # We create the row and column indexes as a array.
    # The row needs to be the person, the column we take
    # the choice they made.
    
    idx = np.column_stack((np.arange(0, n), y))
    return np.array([logccp[row[0], row[1]] for row in idx])


def choice_prob(theta: np.array, x: np.array):
    """Takes the coefficients and covariates and outputs choice probabilites 
    and log choice probabilites. The utilities are max rescaled before
    choice probabilities are calculated.

    Args:
        theta (np.array): Coefficients, or weights for the x array
        x (np.array): Dependent variables.

    Returns:
        (tuple): Returns choice probabilities and log choice probabilities,
            both are np.array. 
    """
    n, j, k = x.shape
    
    u = x @ theta
    max_u = u.max(axis=1).reshape(-1, 1)

    # Substract maximum for numerical stability
    u = u.reshape(n, j)  # Make sure u has correct shape
    u -= max_u
    denom = np.sum(np.exp(u), axis=1).reshape(-1, 1)
    
    # Conditional choice probabilites
    ccp = np.exp(u) / denom
    logccp = u - np.log(denom)
    
    return ccp, logccp


def sim_data(n: int, j: int, theta: np.array):
    """Takes input values n and j to specify the shape of the output data. The
    k dimension is inferred from the length of theta. Creates a y column vector
    that are the choice that maximises utility, and a x matrix that are the 
    covariates, drawn from a random normal distribution.

    Args:
        n (int): Number of households.'
        j (int): Number of choices.
        theta (np.array): The true value of the coefficients.

    Returns:
        dict: Returns a dict with keys "y" and "x".
    """
    k = theta.size
    
    x = rng.normal(size=(n, j, k))
    v = x @ theta
    e = genextreme.ppf(rng.uniform(size=(n, j)), c=0)
    u = v + e
    
    # Find which choice that maximises value.
    u_index = u.argmax(axis=1)
    
    label = ['y', 'x']
    return dict(zip(label, [u_index, x]))


def variance(
        func: object, 
        y: np.array, 
        x: np.array, 
        result: dict, 
        cov_type: str
    ):
    """Calculates the variance for the likelihood function.

    Args:
        >> func (object): Function to be minimized.
        >> y (np.array): Dependent variable.
        >> x (np.array): Independent variables.
        >> result (dict): Results from minimization.
        >> cov_type (str): Type of calculation to use in estimation.

    Returns:
        tuple: Returns the variance-covariance matrix and standard errors.
    """
    n = y.size
    s = centered_grad(lambda theta: func(theta, y, x), result.x)
    b = (s.T@s)/n
    
    if cov_type == 'Hessian':
        hess_inv = result.hess_inv
        cov = 1/n * hess_inv
    elif cov_type == 'Outer Product':
        cov = 1/n * la.inv(b)
    elif cov_type == 'Sandwich':
        hess_inv = result.hess_inv
        cov = 1/n * (hess_inv @ b @ hess_inv)
    else:
        raise ValueError("Invalid covariance type given.")
    se = np.sqrt(np.diag(cov))
    return cov, se


def centered_grad(func, x0, h=1.49e-08):
    # Make sure we have a 2-D array:
    if len(x0.shape) == 1:
        x0 = x0.reshape(-1, 1)
    
    f0 = func(x0)
    grad = np.zeros((f0.size, x0.size))
    for i, val in enumerate(x0):
        x1 = x0.copy()
        x_1 = x0.copy()
        # If not 0, take relative step. Else absolute step.
        if val != 0:
            x1[i] = val*(1 + h)
            x_1[i] = val*(1 - h)
        else:
            x1[i] = h
            x_1[i] = -h
        
        step = x1[i] - x_1[i]
        grad[:, i] = -((func(x1) - func(x_1))/step).flatten()
    return grad


def print_table(
        labels: tuple,
        results: dict,
        headers=["", "Beta", "Se", "t-values"],
        title="Results",
        _lambda:float=None,
        **kwargs
    ):
    """Prints a nice looking table, must at least have coefficients, 
    standard errors and t-values. The number of coefficients must be the
    same length as the labels.

    Args:
        >> theta_label (list): List of labels for estimated parameters
        >> results (dict): The results from a regression. Needs to be in a 
        dictionary with at least the following keys:
            'b_hat', 'se', 't_values'
        >> headers (list, optional): Column headers. Defaults to 
        ["", "Beta", "Se", "t-values"].
        >> title (str, optional): Table title. Defaults to "Results".
    """
    # Unpack the labels
    label_y, label_x = labels
    
    # Create table, using the label for x to get a variable's coefficient,
    # standard error and t_value.
    table = []
    for i, name in enumerate(label_x):
        row = [
            name, 
            results.get('b_hat')[i], 
            results.get('se')[i], 
            results.get('t_values')[i]
        ]
        table.append(row)
    
    # Print the table
    print(title)
    print(f"Dependent variable: {label_y}\n")
    print(tabulate(table, headers, **kwargs))
    print(f"In {results.get('iter')} iterations and {results.get('fiter')} function evaluations.")
    
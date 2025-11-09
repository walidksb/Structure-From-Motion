from scipy.optimize import least_squares

def bundle_adjustment(initial_params, reprojection_function):
    """Run bundle adjustment optimization."""
    result = least_squares(reprojection_function, initial_params, method="lm")
    return result.x

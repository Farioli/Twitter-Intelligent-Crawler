from sklearn.feature_selection import mutual_info_classif

# Estimate mutual information for a discrete target variable.

# Mutual information(MI)[1] between two random variables is a non-negative value, which measures the dependency between the variables.
# It is equal to zero if and only if two random variables are independent, and higher values mean higher dependency.

# The function relies on nonparametric methods based on entropy estimation from k-nearest neighbors distances as described in [2] and [3].
# Both methods are based on the idea originally proposed in [4].

sklearn.feature_selection.mutual_info_classif(X, y, *, discrete_features='auto', n_neighbors=3, copy=True, random_state=None)

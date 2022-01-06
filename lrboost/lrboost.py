from typing import Dict

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.linear_model import RidgeCV
from sklearn.utils.validation import check_is_fitted


class LRBoostRegressor(RegressorMixin, BaseEstimator):
    def __init__(self, linear_model=None, non_linear_model=None):
        if linear_model is None:
            linear_model = RidgeCV()

        if non_linear_model is None:
            non_linear_model = HistGradientBoostingRegressor()

        self.linear_model = linear_model
        self.non_linear_model = non_linear_model

    def __sklearn_is_fitted__(self):
        """Internal sklearn helper that indicates the object has been fitted

        Returns:
            bool: True
        """
        return True

    def fit(self, X, y, sample_weight=None):
        """[summary]

        Args:
            X ([type]): [description]
            y ([type]): [description]
            sample_weight ([type], optional): [description]. Defaults to None.

        Returns:
            self: [description]
        """
        self.linear_model.fit(X, y, sample_weight=sample_weight)
        self.linear_predicted = self.linear_model.predict(X)
        self.linear_residual = np.subtract(self.linear_predicted, y)
        self.non_linear_model.fit(
            X, y=self.linear_residual, sample_weight=sample_weight
        )

        return self

    def predict(self, X) -> np.array:
        """[summary]

        Args:
            X ([type]): [description]

        Returns:
            np.array: [description]
        """
        check_is_fitted(self)
        non_linear_predicted = self.non_linear_model.predict(X)

        return np.add(non_linear_predicted, self.linear_predicted)

    def predict_detail(self, X) -> Dict:
        """[summary]

        Args:
            X ([type]): [description]

        Returns:
            Dict: [description]
        """
        check_is_fitted(self)
        non_linear_prediction = self.non_linear_model.predict(X)

        res = {
            "linear_prediction": self.linear_predicted,
            "non_linear_prediction": non_linear_prediction,
            "prediction": np.add(non_linear_prediction, self.linear_predicted),
        }

        return res

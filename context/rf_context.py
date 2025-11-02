from pandas import DataFrame

from core.strategies.random_forest import RandomForestAnalysis


class RfContext:
    def __init__(self, linear_regression_analysis: RandomForestAnalysis, data: DataFrame):
        self.linearRegressionAnalysis = linear_regression_analysis
        self.data: DataFrame = data


    def run(self, features, targets):
        return self.linearRegressionAnalysis.analyze(data=self.data, features=features, targets=targets)

    def visualize_importance(self, regression_results, features):
        self.linearRegressionAnalysis.visualize_importance(results=regression_results, features=features)

    def visualize_prediction_fit(self, regression_results):
        self.linearRegressionAnalysis.visualize_prediction_fit(results=regression_results)

    def visualize_residuals(self, regression_results):
        self.linearRegressionAnalysis.visualize_residuals(results=regression_results)

from core.strategies.anova import ANOVAAnalysis
from core.strategies.pca import PCAAnalysis
from core.strategies.pearson_spearman import PearsonSpearmanCorrelation
from core.strategies.linear_regression import LinearRegressionAnalysis
from core.strategies.random_forest import RandomForestAnalysis
from typing import Any


class AnalysisFactory:
    @staticmethod
    def get_analysis(strategy_type) -> Any:
        strategies = {
            "pearson_spearman": PearsonSpearmanCorrelation(),
            "pca": PCAAnalysis(),
            "anova": ANOVAAnalysis(),
            "linear_regression": LinearRegressionAnalysis(),
            "random_forest": RandomForestAnalysis()
        }
        return strategies.get(strategy_type, ValueError("Unsupported analysis strategy"))

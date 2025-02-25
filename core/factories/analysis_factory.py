from core.strategies.anova import ANOVAAnalysis
from core.strategies.pca import PCAAnalysis
from core.strategies.pearson_spearman import PearsonSpearmanCorrelation


class AnalysisFactory:
    @staticmethod
    def get_analysis(strategy_type):
        strategies = {
            "pearson_spearman": PearsonSpearmanCorrelation(),
            "pca": PCAAnalysis(),
            "anova": ANOVAAnalysis()
        }
        return strategies.get(strategy_type, ValueError("Unsupported analysis strategy"))

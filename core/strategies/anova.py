from core.correlation_analysis_factory import AnalysisStrategy
from scipy.stats import f_oneway
import numpy as np


class ANOVAAnalysis(AnalysisStrategy):
    def analyze(self, data, features, targets):
        anova_results = {}
        for target in targets:
            anova_results[target] = {}
            for feature in features:
                groups = [data[data[feature] == val][target].dropna() for val in np.unique(data[feature]) if
                          len(data[data[feature] == val][target].dropna()) > 1]
                if len(groups) > 1:
                    f_stat, p_value = f_oneway(*groups)
                    anova_results[target][feature] = {"f_stat": f_stat, "p_value": p_value}

        return anova_results
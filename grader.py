"""
Autograding System for Assignment 3
This file contains the grading logic and be protected in GitHub Classroom
"""
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import quantstats as qs
from Markowitz import EqualWeightPortfolio, RiskParityPortfolio, MeanVariancePortfolio, df_returns


"""
Helper Function:

The following functions will help check your solution,
Please see the following "Performance Check" section
"""


class Helper:
    def __init__(self):
        self.eqw = EqualWeightPortfolio("SPY").get_results()
        self.rp = RiskParityPortfolio("SPY").get_results()
        self.mv_list = [
            MeanVariancePortfolio("SPY").get_results(),
            MeanVariancePortfolio("SPY", gamma=100).get_results(),
            MeanVariancePortfolio("SPY", lookback=100).get_results(),
            MeanVariancePortfolio("SPY", lookback=100, gamma=100).get_results(),
        ]

    def plot_performance(self, strategy_list=None):
        # Plot cumulative returns
        _, ax = plt.subplots()

        (1 + df_returns["SPY"]).cumprod().plot(ax=ax, label="SPY")
        (1 + self.eqw[1]["Portfolio"]).cumprod().plot(ax=ax, label="equal_weight")
        (1 + self.rp[1]["Portfolio"]).cumprod().plot(ax=ax, label="risk_parity")

        if strategy_list != None:
            for i, strategy in enumerate(strategy_list):
                (1 + strategy[1]["Portfolio"]).cumprod().plot(
                    ax=ax, label=f"strategy {i+1}"
                )

        ax.set_title("Cumulative Returns")
        ax.set_xlabel("Date")
        ax.set_ylabel("Cumulative Returns")
        ax.legend()
        plt.show()
        return None

    def plot_allocation(self, df_weights):
        df_weights = df_weights.fillna(0).ffill()

        # long only
        df_weights[df_weights < 0] = 0

        # Plotting
        _, ax = plt.subplots()
        df_weights.plot.area(ax=ax)
        ax.set_xlabel("Date")
        ax.set_ylabel("Allocation")
        ax.set_title("Asset Allocation Over Time")
        plt.show()
        return None

    def report_metrics(self):
        df_bl = pd.DataFrame()
        df_bl["EQW"] = pd.to_numeric(self.eqw[1]["Portfolio"], errors="coerce")
        df_bl["RP"] = pd.to_numeric(self.rp[1]["Portfolio"], errors="coerce")
        df_bl["SPY"] = df_returns["SPY"]
        for i, strategy in enumerate(self.mv_list):
            df_bl[f"MV {i+1}"] = pd.to_numeric(
                strategy[1]["Portfolio"], errors="coerce"
            )
            """
            NOTE: You can add your strategy here.
            """

        qs.reports.metrics(df_bl, mode="full", display=True)

    def plot_mean_variance_portfolio_performance(self):
        self.plot_performance(self.mv_list)

    def plot_eqw_allocation(self):
        self.plot_allocation(self.eqw[0])

    def plot_rp_allocation(self):
        self.plot_allocation(self.rp[0])

    def plot_mean_variance_allocation(self):
        self.plot_allocation(self.mv_list[0][0])
        self.plot_allocation(self.mv_list[1][0])

    def plot_report_metrics(self):
        self.report_metrics()


"""
Assignment Judge
"""


class AssignmentJudge:
    def __init__(self):
        self.eqw_path = "./Answer/eqw.pkl"
        self.rp_path = "./Answer/rp.pkl"
        self.mv_list_0_path = "./Answer/mv_list_0.pkl"
        self.mv_list_1_path = "./Answer/mv_list_1.pkl"
        self.mv_list_2_path = "./Answer/mv_list_2.pkl"
        self.mv_list_3_path = "./Answer/mv_list_3.pkl"

        self.eqw = EqualWeightPortfolio("SPY").get_results()[0]
        self.rp = RiskParityPortfolio("SPY").get_results()[0]
        self.mv_list = [
            MeanVariancePortfolio("SPY").get_results()[0],
            MeanVariancePortfolio("SPY", gamma=100).get_results()[0],
            MeanVariancePortfolio("SPY", lookback=100).get_results()[0],
            MeanVariancePortfolio("SPY", lookback=100, gamma=100).get_results()[0],
        ]

    def check_dataframe_similarity(self, df1, df2, tolerance=0.01):
        # Check if the shape, index, and columns of both DataFrames are the same
        if (
            df1.shape != df2.shape
            or not df1.index.equals(df2.index)
            or not df1.columns.equals(df2.columns)
        ):
            return False

        # Compare values with allowed relative difference
        for column in df1.columns:
            if (
                df1[column].dtype.kind in "bifc" and df2[column].dtype.kind in "bifc"
            ):  # Check only numeric types
                if not np.isclose(df1[column], df2[column], atol=tolerance).all():
                    return False
            else:
                if not (df1[column] == df2[column]).all():
                    return False

        return True

    def compare_dataframe_list(self, std_ans_list, ans_list, tolerance=0.01):
        if len(std_ans_list) != len(ans_list):
            raise ValueError("Both lists must have the same number of DataFrames.")

        results = []
        for df1, df2 in zip(std_ans_list, ans_list):
            result = self.check_dataframe_similarity(df1, df2, tolerance)
            results.append(result)

        return results == [True] * len(results)

    def compare_dataframe(self, df1, df2, tolerance=0.01):
        return self.check_dataframe_similarity(df1, df2, tolerance)

    def check_answer_eqw(self, eqw_dataframe):
        answer_dataframe = pd.read_pickle(self.eqw_path)
        if self.compare_dataframe(answer_dataframe, eqw_dataframe):
            print("Problem 1 Complete - Get 20 Points")
            return 20
        else:
            print("Problem 1 Fail")
        return 0

    def check_answer_rp(self, rp_dataframe):
        answer_dataframe = pd.read_pickle(self.rp_path)
        if self.compare_dataframe(answer_dataframe, rp_dataframe):
            print("Problem 2 Complete - Get 20 Points")
            return 20
        else:
            print("Problem 2 Fail")
        return 0

    def check_answer_mv_list(self, mv_list):
        mv_list_0 = pd.read_pickle(self.mv_list_0_path)
        mv_list_1 = pd.read_pickle(self.mv_list_1_path)
        mv_list_2 = pd.read_pickle(self.mv_list_2_path)
        mv_list_3 = pd.read_pickle(self.mv_list_3_path)
        answer_list = [mv_list_0, mv_list_1, mv_list_2, mv_list_3]
        if self.compare_dataframe_list(answer_list, mv_list):
            print("Problem 3 Complete - Get 30 points")
            return 30
        else:
            print("Problem 3 Fail")
        return 0

    def check_all_answer(self):
        score = 0
        score += self.check_answer_eqw(eqw_dataframe=self.eqw)
        score += self.check_answer_rp(self.rp)
        score += self.check_answer_mv_list(self.mv_list)
        return score

    def run_grading(self, args):
        """
        Main grading function with exit code logic (protected from student modification)
        """
        if args.score:
            if ("eqw" in args.score) or ("rp" in args.score) or ("mv" in args.score):
                # 這一段保留給你自己在本機測 eqw / rp / mv 用,
                # 不會被 GitHub Classroom 的 workflow 用到
                if "eqw" in args.score:
                    self.check_answer_eqw(self.eqw)
                if "rp" in args.score:
                    self.check_answer_rp(self.rp)
                if "mv" in args.score:
                    self.check_answer_mv_list(self.mv_list)

            elif "all" in args.score:
                # GitHub Classroom autograding 用的情境：python Markowitz.py --score all
                total_score = self.check_all_answer()
                print(f"==> total Score = {total_score} <==")

                # 這裡決定 exit code：
                # 你的滿分是 20 + 20 + 30 = 70
                FULL_SCORE = 70
                if total_score == FULL_SCORE:
                    # 三題都對 → exit code 0 → autograder 給 70/70
                    sys.exit(0)
                else:
                    # 只要有題目錯 → exit code 1 → autograder 給 0/70
                    sys.exit(1)

        if args.allocation:
            helper = Helper()
            if "eqw" in args.allocation:
                helper.plot_eqw_allocation()
            if "rp" in args.allocation:
                helper.plot_rp_allocation()
            if "mv" in args.allocation:
                helper.plot_mean_variance_allocation()

        if args.performance:
            helper = Helper()
            if "mv" in args.performance:
                helper.plot_mean_variance_portfolio_performance()

        if args.report:
            helper = Helper()
            if "mv" in args.report:
                helper.plot_report_metrics()
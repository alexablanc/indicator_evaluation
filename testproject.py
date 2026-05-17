import TheoreticallyOptimalStrategy as tos
from marketsimcode import compute_portvals
import indicators as ind
import matplotlib.pyplot as plt
import pandas as pd

def author():
    return "ablanc6"

def study_group():
    return "ablanc6"

df_trades = tos.testPolicy()
benchmark_trades = pd.DataFrame(index=df_trades.index, columns=["JPM"], data=0)
benchmark_trades.iloc[0, 0] = 1000
tos_portvals = compute_portvals(df_trades, sv=100000, commission=0.0, impact=0.0)
benchmark_portvals = compute_portvals(benchmark_trades, sv=100000, commission=0.0, impact=0.0)

#normalize portvals
tos_norm = tos_portvals / tos_portvals.iloc[0]
benchmark_norm = benchmark_portvals / benchmark_portvals.iloc[0]

def plot_tos_vs_benchmark(benchmark_norm, tos_norm, filename="tos_vsbenchmark.png"):
    plt.figure(figsize=(10,6))

    # Handle Series or one-column DataFrame
    if isinstance(benchmark_norm, pd.DataFrame):
        benchmark_series = benchmark_norm.iloc[:,0]
    else:
        benchmark_series = benchmark_norm
    if isinstance(tos_norm, pd.DataFrame):
        tos_series = tos_norm.iloc[:,0]
    else:
        tos_series = tos_norm
    plt.plot(benchmark_series.index, benchmark_series.values, color="purple", label="Benchmark")
    plt.plot(tos_series.index, tos_series.values, color="red", label="Theoretically Optimal Portfolio")
    plt.title("Benchmark vs Theoretically Optimal Strategy")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)

def compute_stats(portvals):
    """
    portvals: Series or one column DataFrame of portfolio values
    returns: cumulative return, std daily return, mean daily return
    """
    if isinstance(portvals, pd.DataFrame):
        portvals = portvals.iloc[:, 0]

    daily_ret = portvals.pct_change().dropna()
    cum_ret = (portvals.iloc[-1] / portvals.iloc[0]) - 1
    std_daily_ret = daily_ret.std()
    mean_daily_ret = daily_ret.mean()

    return cum_ret, std_daily_ret, mean_daily_ret

def save_table_figure(stats_df, filename="tos_stats_table.png"):
    fig, ax = plt.subplots(figsize=(9, 2.5))
    ax.axis("off")

    table = ax.table(
        cellText=stats_df.values,
        rowLabels=stats_df.index,
        colLabels=stats_df.columns,
        cellLoc="center",
        loc="center"
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.5)

    plt.tight_layout()
    plt.savefig(filename, bbox_inches="tight")

bench_cum_ret, bench_std_daily_ret, bench_mean_daily_ret = compute_stats(benchmark_portvals)
tos_cum_ret, tos_std_daily_ret, tos_mean_daily_ret = compute_stats(tos_portvals)

stats_df = pd.DataFrame({
    "Benchmark": [
        bench_cum_ret,
        bench_std_daily_ret,
        bench_mean_daily_ret
    ],
    "Theoretically Optimal": [
        tos_cum_ret,
        tos_std_daily_ret,
        tos_mean_daily_ret
    ]
}, index=[
    "Cumulative Return",
    "Std Dev of Daily Return",
    "Mean of Daily Return"
])

plot_tos_vs_benchmark(benchmark_norm, tos_norm)

# Format to 6 digits to the right of the decimal
stats_df = stats_df.applymap(lambda x: f"{x:.6f}")

save_table_figure(stats_df)

ind.run()
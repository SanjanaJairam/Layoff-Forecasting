import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from prophet import Prophet
from pathlib import Path
from sklearn.metrics import mean_squared_error
from math import sqrt


def forecast_layoffs(file_path, output_subdir):
    df = pd.read_excel(file_path, na_values='-')
    df.fillna(df.mean(numeric_only=True), inplace=True)
    df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m', errors='coerce')
    df = df.dropna(subset=['Month'])

    all_rmse = []
    output_dir = Path("outputs") / output_subdir
    output_dir.mkdir(parents=True, exist_ok=True)

    for char in df['Characteristic'].unique():
        df_new = df[df['Characteristic'] == char]

        if df_new['TotalEmpLaidOff'].dropna().shape[0] < 10:
            continue  # Skip sparse data

        df_prophet = df_new[['Month', 'TotalEmpLaidOff']].rename(columns={'Month': 'ds', 'TotalEmpLaidOff': 'y'})
        df_prophet = df_prophet.sort_values('ds')

        # Last 4 months = test, rest = train
        df_train = df_prophet.iloc[:-4]
        df_test = df_prophet.iloc[-4:]

        if df_test.empty or df_train.empty:
            continue  # Skip if no test or train data

        model = Prophet(seasonality_mode='multiplicative')
        model.fit(df_train)

        future = df_test[['ds']].copy()
        forecast = model.predict(future)

        mse = mean_squared_error(df_test['y'], forecast['yhat_upper'])
        rmse = sqrt(mse)
        all_rmse.append(rmse)

        # Plotting
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(df_prophet['ds'], df_prophet['y'], label='Actuals', linewidth=2, color='royalblue')

        # Plot confidence interval as shaded area
        ax.fill_between(forecast['ds'], forecast['yhat_lower'], forecast['yhat_upper'],
                        color='orange', alpha=0.3, label='Forecast Range')
        ax.plot(forecast['ds'], forecast['yhat'], linestyle='--', color='darkorange', linewidth=2, label='Forecast')

        ax.set_title(f"{char} Employees Laid Off Forecast ({output_subdir.upper()})", fontsize=14, fontweight='bold')
        ax.set_xlabel("Date", fontsize=12)
        ax.set_ylabel("Number of Employees", fontsize=12)

        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.legend(fontsize=10)

        plt.tight_layout()
        filename = f"{output_subdir.upper()} - {char} employees laid off.png".replace("/", "-")
        plt.savefig(output_dir / filename, dpi=300)
        plt.close()

    print(f"{output_subdir} - Average RMSE:", sum(all_rmse)/len(all_rmse) if all_rmse else 'N/A')


# Run forecasts for both T3 and T7
datasets = {
    "t3": "data/bls-T3.xlsx",
    "t7": "data/bls-T7.xlsx"
}

for key, path in datasets.items():
    forecast_layoffs(path, key)

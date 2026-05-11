# Investment Notes - Project Guidelines

## データソース戦略

| 対象 | ツール | 備考 |
|---|---|---|
| 日本株 | JPX CLI | stock-dashboardプロジェクトのCLI経由 |
| 米国主要銘柄（大型株） | MCP (financial-datasets) | S&P500・NASDAQ100構成銘柄など。フリー枠で取得可能 |
| 米国ニッチ株（小型・中型） | yfinance | POET・RKLBなど。stock-dashboardの.venvを使用 |

## 環境

- Python仮想環境: `/home/bluefelix/my-apps/stock-dashboard/.venv`（yfinance使用時はこちらをactivate）
- 日本株データはstock-dashboardプロジェクトとは別に管理する

## サイト構成方針

- トップページ・Macroセクション：マクロトレンドを前面に出す
- 個別銘柄（stocks/）：深い階層に配置、メインには出さない
- 定性分析：Markdownで記述
- 定量分析：Jupyter Notebookで記述（stocks/<TICKER>/analysis.ipynb）

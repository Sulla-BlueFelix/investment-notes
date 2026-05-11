# Investment Notes - Project Guidelines

## データソース戦略

| 対象 | ツール | 備考 |
|---|---|---|
| 日本株 | JPX CLI | stock-dashboardプロジェクトのCLI経由 |
| 米国主要銘柄（大型株） | MCP (financial-datasets) | S&P500・NASDAQ100構成銘柄など。フリー枠で取得可能 |
| 米国ニッチ株（小型・中型） | yfinance | POET・RKLBなど |

## Python環境

- **パッケージ管理**: `uv`（`pyproject.toml` + `uv.lock`でバージョン固定）
- **仮想環境**: `investment-notes/.venv`（gitignore済み）
- **環境再現**: 別PCでclone後に `uv sync` するだけで同じ環境が作られる
- **stock-dashboardの`.venv`は使わない**（このプロジェクトは独立した環境）

### パッケージ追加方法
```bash
cd ~/my-apps/investment-notes
uv add <package-name>
```

## Quartoコード実行

- `_quarto.yml`に`execute: freeze: auto`を設定済み
- コードチャンクはローカルで実行し、結果を`_freeze/`にキャッシュしてgit管理
- GitHub Actions上ではPythonを実行しない（キャッシュを使う）
- ローカルでレンダリング: `quarto render`

## サイト構成方針

- トップページ・Macroセクション：マクロトレンドを前面に出す
- 個別銘柄（stocks/）：深い階層に配置、メインには出さない
- 定性分析：Markdownで記述（.qmdファイル）
- 定量分析：Pythonコードチャンクで記述（同じ.qmdに埋め込み）

## デプロイフロー

1. ローカルで分析・執筆
2. `quarto render`でビルド（コードチャンクが実行され`_freeze/`に保存）
3. `git add . && git commit && git push origin main`
4. GitHub Actionsが`gh-pages`ブランチを更新
5. GitHub Pagesに自動反映（数分）

# Note PC Handoff

このリポジトリは、Quarto website と Jupyter notebook で投資メモを管理するためのものです。

## 現在の状態

- GitHub: `https://github.com/Sulla-BlueFelix/investment-notes.git`
- Branch: `main`
- Python package manager: `uv`
- Python requirement: `>=3.13`
- Quarto project: `_quarto.yml`
- GitHub Pages deploy: `main` に push すると GitHub Actions が `gh-pages` を更新

## Note PC 初回セットアップ

Windows note PC なら、WSL Ubuntu 上で作業するのが今の環境に近いです。

1. 必要ツールを入れる

   - Git
   - VS Code
   - WSL Ubuntu
   - Quarto
   - `uv`

2. GitHub にログインする

   HTTPS remote なので、Git Credential Manager または GitHub CLI で認証します。

   ```bash
   gh auth login
   ```

3. リポジトリを clone する

   ```bash
   mkdir -p ~/my-apps
   cd ~/my-apps
   git clone https://github.com/Sulla-BlueFelix/investment-notes.git
   cd investment-notes
   ```

4. Python 環境を再現する

   ```bash
   uv sync
   ```

5. サイトを確認する

   ```bash
   quarto preview
   ```

6. 全体をビルドする

   ```bash
   quarto render
   ```

## 日々の作業フロー

作業開始時:

```bash
cd ~/my-apps/investment-notes
git pull origin main
```

分析やメモ作成後:

```bash
quarto render
git status
git add .
git commit -m "Update investment notes"
git push origin main
```

Jupyter notebook を使う場合:

```bash
uv run jupyter lab
```

テーマ別スナップショット例:

```bash
uv run python scripts/theme_snapshot.py --preset ai_infra
uv run python scripts/theme_snapshot.py --preset ai_memory
uv run python scripts/theme_snapshot.py --preset japan_memory
uv run python scripts/theme_snapshot.py --preset hyperscaler_capex
```

## GitHub に載らないもの

`.gitignore` により、以下は GitHub に push されません。

- `.venv/`
- `.quarto/`
- `__pycache__/`
- `**/*.quarto_ipynb`
- `analysis/crystal_timing_and_holdings.ipynb`

`analysis/crystal_timing_and_holdings.ipynb` は保有・取得単価など個人情報を含む想定なので、公開リポジトリには載せません。note PCでも必要なら、USB、Dropbox、private vault などで別途移してください。

## Obsidian vault

一次記憶は GitHub ではなく、以下の Obsidian vault です。

```text
/mnt/c/Users/BlueF/Dropbox/obsidian1/10_Investment/投資分析 with Claude/
```

note PC で同じ運用にするには、Dropbox と Obsidian を入れて、同じパスか、それに近いパスで vault を開けるようにします。パスが変わる場合は `CLAUDE.md` の vault path を更新してください。

## トラブル時

依存関係が壊れた場合:

```bash
rm -rf .venv
uv sync
```

GitHub Pages が更新されない場合:

- GitHub の Actions タブで `Publish to GitHub Pages` の失敗ログを見る
- ローカルで `quarto render` が通るか確認する
- `main` に push できているか `git status --branch` で確認する


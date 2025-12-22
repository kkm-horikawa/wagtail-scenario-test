# CLAUDE.md

Claude Code 用のプロジェクト固有ガイド。

## 開発サイクル

Issue に取り組む際は以下の順序で進める:

1. `/feasibility <issue-number>` - 公式ドキュメント・実装調査、結果を Issue にコメント
2. `/implement <issue-number>` - CONTRIBUTING.md に完全準拠して実装、Draft PR 作成
3. `/review` - コードレビュー、問題なければ Ready for Review に変更
4. 他のWagtailライブラリ（wagtail-reusable-blocks等）で動作確認後、マージ

## 動作確認

このライブラリはWagtail向けE2Eテストライブラリなので、他のWagtailライブラリ（wagtail-reusable-blocks, wagtail-html-editor等）のE2Eテストで動作確認する。

```bash
# wagtail-reusable-blocks で動作確認
cd ../wagtail-reusable-blocks
uv pip install -e ../wagtail-scenario-test
uv run pytest tests/e2e/ -v
```

## コマンド

```bash
# テスト
uv run pytest

# リント
uv run ruff check .
uv run ruff format --check .

# 型チェック
uv run mypy src/
```

## ブランチ命名

- `feature/<issue-number>-<description>`
- `fix/<issue-number>-<description>`

## コミットメッセージ

- Claude Code の署名（🤖 Generated with...）を含めない
- Co-Authored-By を含めない
- Conventional Commits 形式を使用（feat:, fix:, docs:, etc.）

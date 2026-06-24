#!/usr/bin/env python3
"""Print a compact market snapshot for thematic watchlists.

Usage:
  uv run python scripts/theme_snapshot.py --preset ai_memory
  uv run python scripts/theme_snapshot.py --tickers MU,NVDA,AVGO
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime

import yfinance as yf


PRESETS: dict[str, dict[str, str]] = {
    "ai_memory": {
        "MU": "Micron / HBM DRAM",
        "WDC": "Western Digital / storage",
        "STX": "Seagate / HDD storage",
        "NVDA": "NVIDIA / GPU platform",
        "AVGO": "Broadcom / ASIC networking",
        "SOXX": "Semiconductor ETF",
        "SMH": "Semiconductor ETF",
        "285A.T": "Kioxia JP",
        "005930.KS": "Samsung Electronics",
        "000660.KS": "SK Hynix",
    },
    "data_center_water": {
        "XYL": "Xylem / water infra",
        "VLTO": "Veralto / water quality",
        "PNR": "Pentair / water treatment",
        "BMI": "Badger Meter / smart water",
        "ERII": "Energy Recovery / desalination",
        "TTEK": "Tetra Tech / water engineering",
        "6370.T": "Kurita / water treatment JP",
        "6368.T": "Organo / ultrapure water JP",
        "6361.T": "Ebara / pumps JP",
    },
    "ai_infra": {
        "NVDA": "NVIDIA / GPU platform",
        "AVGO": "Broadcom / ASIC networking",
        "MU": "Micron / HBM DRAM",
        "VRT": "Vertiv / power cooling",
        "MOD": "Modine / liquid cooling",
        "ETN": "Eaton / electrical infra",
        "GEV": "GE Vernova / grid power",
        "LITE": "Lumentum / optics",
        "AMKR": "Amkor / advanced packaging",
        "SOXX": "Semiconductor ETF",
        "SMH": "Semiconductor ETF",
    },
}


@dataclass
class Snapshot:
    ticker: str
    label: str
    last: float
    day_pct: float
    one_month_pct: float
    three_month_pct: float
    from_52w_high_pct: float
    low_52w: float
    high_52w: float


def pct(now: float, then: float) -> float:
    return (now / then - 1.0) * 100.0 if then else 0.0


def fetch_snapshot(ticker: str, label: str) -> Snapshot | None:
    hist = yf.Ticker(ticker).history(period="1y", interval="1d", auto_adjust=False)
    if hist.empty or len(hist["Close"]) < 2:
        return None

    close = hist["Close"].dropna()
    last = float(close.iloc[-1])
    prev = float(close.iloc[-2])
    one_month = float(close.iloc[-22]) if len(close) > 22 else float(close.iloc[0])
    three_month = float(close.iloc[-66]) if len(close) > 66 else float(close.iloc[0])
    high_52w = float(close.max())
    low_52w = float(close.min())

    return Snapshot(
        ticker=ticker,
        label=label,
        last=last,
        day_pct=pct(last, prev),
        one_month_pct=pct(last, one_month),
        three_month_pct=pct(last, three_month),
        from_52w_high_pct=pct(last, high_52w),
        low_52w=low_52w,
        high_52w=high_52w,
    )


def format_markdown(rows: list[Snapshot], title: str) -> str:
    lines = [
        f"# Theme Snapshot: {title}",
        "",
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        "",
        "| ticker | label | last | 1d% | 1m% | 3m% | from 52w high | 52w low | 52w high |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in rows:
        lines.append(
            "| "
            f"{r.ticker} | {r.label} | {r.last:.2f} | {r.day_pct:.2f} | "
            f"{r.one_month_pct:.1f} | {r.three_month_pct:.1f} | "
            f"{r.from_52w_high_pct:.1f} | {r.low_52w:.2f} | {r.high_52w:.2f} |"
        )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--preset", choices=sorted(PRESETS), default="ai_infra")
    parser.add_argument("--tickers", help="Comma-separated tickers. Overrides --preset.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.tickers:
        universe = {ticker.strip(): ticker.strip() for ticker in args.tickers.split(",") if ticker.strip()}
        title = "custom"
    else:
        universe = PRESETS[args.preset]
        title = args.preset

    rows = []
    for ticker, label in universe.items():
        row = fetch_snapshot(ticker, label)
        if row:
            rows.append(row)

    print(format_markdown(rows, title))


if __name__ == "__main__":
    main()

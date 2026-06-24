#!/usr/bin/env python3
"""Print a compact market snapshot for thematic watchlists.

Usage:
  uv run python scripts/theme_snapshot.py --preset ai_memory
  uv run python scripts/theme_snapshot.py --preset japan_memory
  uv run python scripts/theme_snapshot.py --preset hyperscaler_capex
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
    "japan_memory": {
        "285A.T": "Kioxia / NAND SSD",
        "6146.T": "Disco / dicing grinding packaging",
        "6857.T": "Advantest / memory logic test",
        "8035.T": "Tokyo Electron / WFE",
        "7735.T": "Screen / WFE cleaning",
        "6920.T": "Lasertec / inspection",
        "6525.T": "Kokusai Electric / deposition",
        "3436.T": "Sumco / silicon wafer",
        "4063.T": "Shin-Etsu / wafer materials",
        "4062.T": "Ibiden / package substrate",
        "6315.T": "Towa / molding packaging",
        "6779.T": "Nihon Dempa / timing component",
        "5803.T": "Fujikura / fiber cable power",
        "MU": "Micron / HBM DRAM NAND",
        "WDC": "Western Digital / NAND storage",
        "STX": "Seagate / HDD storage",
        "SOXX": "Semiconductor ETF",
        "SMH": "Semiconductor ETF",
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
    "hyperscaler_capex": {
        "MSFT": "Microsoft / Azure OpenAI",
        "GOOGL": "Alphabet / Google Cloud TPU",
        "AMZN": "Amazon / AWS Trainium",
        "META": "Meta / AI ads infra",
        "ORCL": "Oracle / OCI AI infra",
        "NVDA": "NVIDIA / GPU supplier",
        "AVGO": "Broadcom / custom ASIC networking",
        "MU": "Micron / memory supplier",
        "VRT": "Vertiv / power cooling",
        "ETN": "Eaton / electrical infra",
        "GEV": "GE Vernova / grid power",
        "COHR": "Coherent / optics",
        "LITE": "Lumentum / optics",
        "DLR": "Digital Realty / data center REIT",
    },
    "ai_networking": {
        "AVGO": "Broadcom / Ethernet ASIC CPO",
        "MRVL": "Marvell / custom silicon optical DSP",
        "ANET": "Arista / AI Ethernet switching",
        "COHR": "Coherent / optics lasers",
        "LITE": "Lumentum / optics lasers",
        "CRDO": "Credo / AEC SerDes",
        "ALAB": "Astera Labs / PCIe CXL connectivity",
        "FN": "Fabrinet / optical manufacturing",
        "CLS": "Celestica / AI network hardware",
        "POET": "POET / optical interposer",
        "GLW": "Corning / fiber glass",
        "NVDA": "NVIDIA / networking platform",
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


def format_markdown(rows: list[Snapshot], title: str, missing: list[str]) -> str:
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
    if missing:
        lines.extend(
            [
                "",
                "## Missing",
                "",
                "No price data was returned for: " + ", ".join(missing),
            ]
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
    missing = []
    for ticker, label in universe.items():
        row = fetch_snapshot(ticker, label)
        if row:
            rows.append(row)
        else:
            missing.append(ticker)

    print(format_markdown(rows, title, missing))


if __name__ == "__main__":
    main()

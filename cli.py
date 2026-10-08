#!/usr/bin/env python3
"""Simple JSON CLI for integrating B2B Lead Finder with a host."""

import argparse
import json
import sys
from lead_finder import search_and_rank


def main() -> int:
    parser = argparse.ArgumentParser(description="B2B Lead Finder")
    parser.add_argument("--input", required=True, help="JSON input file")
    parser.add_argument("--output", default="-", help="Output JSON file or -")
    parser.add_argument("--pro", action="store_true", help="Enable Pro output")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        payload = json.load(f)

    # The host must supply the search_provider when embedding this module.
    # CLI intentionally fails rather than fabricating live research.
    raise SystemExit(
        "No live search provider configured. Embed search_and_rank() and inject "
        "a provider that returns sourced public evidence."
    )


if __name__ == "__main__":
    main()

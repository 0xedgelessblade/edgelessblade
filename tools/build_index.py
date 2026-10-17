#!/usr/bin/env python3
"""Build llms-full.txt and the topic index (README.md, llms.txt). No dependencies."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
T, R, U, A, L = ("Tesla and TSLA", "US Treasury yields and interest rates",
                 "US stocks and valuation", "AI tools and agents", "Life and mindset")
TOPIC_ORDER = [T, R, U, A, L]
FOLDER_FALLBACK = {"tesla": [T], "markets": [U], "ai": [A], "life": [L]}

# Filled by reading each article (title + opening lines). Keyed by relative path.
TOPICS = {
    "articles/markets/2026-06-02-another-night-picking-up-the-tab.md": [A, U],
    "articles/markets/2026-06-03-did-i-invent-a-time-machine.md": [U],
    "articles/markets/2026-06-02-racing-to-the-bottom-faster.md": [U],
    "articles/life/2026-05-31-buy-the-swiss-magic-pass-now.md": [L],
    "articles/markets/2026-05-30-only-blockchain-goes-to-space.md": [U, L],
    "articles/ai/2026-10-16-four-business-seats-taipei-tokyo-in-five-minutes.md": [A, L],
    "articles/life/2026-06-09-book-swiss-christmas-hotels-early.md": [L],
    "articles/markets/2026-06-08-what-goes-around-comes-around-germany-bitcoin.md": [U],
    "articles/tesla/2026-06-06-rock-bottom-of-the-passionless-valley.md": [T, L],
    "articles/markets/2026-06-05-hang-in-there-brothers.md": [U, L],
    "articles/markets/2026-06-11-investing-in-spacex-unlock-dates.md": [U],
    "articles/markets/2026-06-10-fed-qt-first-then-cuts.md": [R, U],
    "articles/markets/2026-06-06-caught-100000-of-bitcoin-at-200-week-ma.md": [U],
    "articles/markets/2026-06-04-the-time-machine-has-been-invented.md": [U],
    "articles/tesla/2026-10-16-kept-adding-tsll-sell-puts.md": [T, U],
    "articles/life/2026-06-14-thought-it-was-mildly-enlarged-adenoids.md": [L],
    "articles/markets/2026-06-13-zero-spacex-ipo-shares-still-made-22000.md": [U],
    "articles/markets/2026-06-12-spacex-ipo-1000-shares-at-150.md": [U],
    "articles/markets/2026-06-12-results-are-in-spacex-ipo-zero.md": [U],
    "articles/markets/2026-06-12-applied-4500-spacex-ipo-shares-got-0.md": [U],
    "articles/tesla/2026-10-15-plan-your-trade-trade-your-plan.md": [T, U],
    "articles/life/2026-07-10-if-you-rent-cars-abroad-often.md": [L],
    "articles/tesla/2026-07-06-can-you-feel-it-higher-lows.md": [T, U],
    "articles/life/2026-06-20-discovering-fire-apple-pay-cards.md": [L],
    "articles/markets/2026-06-17-spcx-options-are-open.md": [U],
    "articles/markets/2026-06-18-spcx-pulled-back-still-cashing-in.md": [U],
    "articles/ai/2026-10-15-alaska-search-adds-4-destinations.md": [A, L],
    "articles/markets/2026-06-15-flipping-spcx-ipo-10000-profit.md": [U],
    "articles/tesla/2026-07-23-tesla-flattened-me-after-i-bought.md": [T, U],
    "articles/tesla/2026-07-21-grilling-tsll-120-puts.md": [T, U],
    "articles/markets/2026-07-18-spcx-assigned-at-ipo-price.md": [U],
    "articles/life/2026-07-15-how-do-i-comfort-the-teacher.md": [L],
    "articles/tesla/2026-10-14-tesla-and-spacex-will-merge.md": [T, U],
    "articles/markets/2026-07-28-mstr-buys-back-strc.md": [U],
    "articles/markets/2026-07-27-qqq-top-divergence.md": [U, R],
    "articles/markets/2026-07-27-bitcoin-along-the-200-week-ma.md": [U],
    "articles/markets/2026-07-14-spcx-puts-still-on.md": [U],
    "articles/markets/2026-07-15-two-days-left-spcx-assignment.md": [U],
    "articles/markets/2026-07-17-spcx-stuck-at-ipo-price.md": [U],
    "articles/life/2026-07-25-which-floor-you-live-on.md": [L],
    "articles/life/2026-07-29-craving-sashimi-abroad.md": [L],
    "articles/tesla/2026-07-28-assigned-another-2000-shares.md": [T, U],
    "articles/tesla/2026-07-24-cover-fire-bought-10000-tsll.md": [T, U],
    "articles/tesla/2026-07-23-another-5000-tsll-at-8-86.md": [T, U],
    "articles/tesla/2026-07-30-hell-train-boarding.md": [T],
    "articles/tesla/2026-08-03-spcx-wheel-and-spotting-scams.md": [T, U],
    "articles/tesla/2026-08-04-hell-train-tsll-last-4000-shares.md": [T, U],
    "articles/markets/2026-08-05-clarity-act-odds-ibit-ethb-and-spcx.md": [U],
    "articles/markets/2026-08-06-clarity-act-this-week-ibit-long-strangle.md": [U],
    "articles/markets/2026-08-07-clarity-act-delayed-bitcoin-and-ibit.md": [U],
    "articles/tesla/2026-08-09-why-tsll-can-decouple-on-a-huge-up-day.md": [T, U],
    "articles/tesla/2026-08-13-spcx-about-to-get-called-away.md": [T, U],
    "articles/tesla/2026-08-12-tsll-assigned-another-8000-shares.md": [T, U],
    "articles/tesla/2026-08-11-my-1000-shares-of-boundless-ocean.md": [T, U],
    "articles/life/2026-08-10-tuna-belly-at-the-market.md": [L],
    "articles/life/2026-08-06-focusing-on-monthly-salary.md": [L, U],
    "articles/tesla/2026-08-08-spcx-1000-shares-cost-135.md": [T, U],
    "articles/ai/2026-10-13-alaska-miles-too-easy-eight-business-awards.md": [A, L],
    "articles/markets/2026-08-21-where-does-the-money-come-from.md": [R, U],
    "articles/markets/2026-08-21-half-a-day-of-bitcoin.md": [U],
    "articles/markets/2026-08-19-btc-at-68000.md": [U],
    "articles/tesla/2026-08-18-my-answer-key-for-this-ai-cycle.md": [T, A],
    "articles/markets/2026-10-13-investing-is-like-baseball.md": [U, L],
    "articles/tesla/2026-08-22-riding-tesla-and-bitcoins-breakout.md": [T, U],
    "articles/markets/2026-08-20-the-market-is-short-on-cash.md": [R, U],
    "articles/tesla/2026-08-15-spcx-called-away-at-135.md": [T, U],
    "articles/tesla/2026-08-14-nevada-permit-for-ten-cars.md": [T],
    "articles/ai/2026-10-12-i-built-an-alaska-miles-award-finder.md": [A, L],
    "articles/life/2026-08-31-they-choose-to-trust-themselves.md": [L],
    "articles/tesla/2026-08-28-texas-robotaxi-fleet-hits-270.md": [T],
    "articles/markets/2026-09-02-standing-with-bessent-on-rates-and-ai.md": [R, U],
    "articles/markets/2026-08-27-on-collateral.md": [R, U],
    "articles/markets/2026-08-26-credit-is-a-divine-weapon.md": [U, L],
    "articles/markets/2026-08-25-stop-measuring-assets-by-your-salary.md": [U, L],
    "articles/markets/2026-08-24-intervening-in-the-30-year-is-a-great-signal.md": [R, U],
    "articles/markets/2026-08-23-options-many-plays-same-premise.md": [U],
    "articles/tesla/2026-09-07-teslas-odds-finally-line-up.md": [T],
    "articles/markets/2026-09-06-maybe-the-weather-is-turning.md": [U],
    "articles/tesla/2026-09-05-nhtsa-looks-like-the-real-bull.md": [T],
    "articles/markets/2026-09-04-bitcoins-200-day-ma-turns-up.md": [U],
    "articles/markets/2026-09-03-the-casino-whose-chips-are-metal.md": [U],
    "articles/life/2026-10-11-one-ticket-turned-into-a-years-holidays.md": [L],
    "articles/life/2026-09-12-hede-fashion-outlet-bone-breaking-discounts.md": [L],
    "articles/markets/2026-09-11-the-cost-of-every-kind-of-leverage.md": [R, U],
    "articles/markets/2026-09-10-four-fed-bank-tools-before-cpi.md": [R, U],
    "articles/life/2026-09-09-get-a-food-waste-processor.md": [L],
    "articles/markets/2026-09-08-bitcoin-seller-exhaustion.md": [U],
    "articles/tesla/2026-10-10-covering-the-retreat-then-trimming-tsll.md": [T],
    "articles/tesla/2026-10-09-tesla-fleet-daily.md": [T],
    "articles/tesla/2026-10-09-tsla-spcx-relative-strength-index.md": [T],
    "articles/tesla/2026-10-08-tesla-fleet-status.md": [T],
    "articles/tesla/2026-09-09-why-tesla-doesnt-need-to-buy-uber.md": [T],
    "articles/tesla/2026-09-01-carried-by-my-good-for-nothing-son.md": [T],
    "articles/markets/2026-10-05-30-year-yield-and-the-treasury-toolbox.md": [R],
    "articles/markets/2026-10-02-ai-price-comparison-erodes-the-hassle-moat.md": [U, A],
    "articles/markets/2026-10-01-introduction.md": [R, U],
    "articles/markets/2026-09-30-adding-goog-waiting-for-meta-at-640.md": [R, U],
    "articles/markets/2026-09-22-time-in-the-market.md": [U],
    "articles/markets/2026-09-19-wait-rate-hikes-make-stocks-go-up.md": [R, U],
    "articles/markets/2026-09-18-nt-100-million-lifes-escape-velocity.md": [U, L],
    "articles/markets/2026-09-18-rates-went-up-and-so-did-the-market.md": [T, R, U],
    "articles/markets/2026-09-17-find-the-camp-that-is-your-calling.md": [U, L],
    "articles/markets/2026-09-16-clarity-act-stalls-bitcoin-bottom-near.md": [R, U],
    "articles/markets/2026-09-14-maybe-today-is-the-starting-gun.md": [U, A],
    "articles/markets/2026-09-13-good-product-good-business-good-stock.md": [U],
    "articles/ai/2026-10-06-eva-award-tickets-via-live-text-chat.md": [A],
    "articles/ai/2026-10-02-metas-muse-buys-your-inbox-with-tokens.md": [A],
    "articles/ai/2026-09-27-muse-and-prompt-injection.md": [A],
    "articles/ai/2026-09-26-muse-handled-my-lululemon-return.md": [A],
    "articles/ai/2026-09-23-the-real-agi-era-is-here.md": [A],
    "articles/ai/2026-09-20-for-anyone-who-doesnt-know-what-ai-can-do.md": [A],
    "articles/life/2026-10-03-for-people-just-starting-out.md": [L],
    "articles/life/2026-09-30-easy-wins-in-life.md": [L],
    "articles/life/2026-09-29-how-ordinary-people-turn-things-around.md": [L, U],
    "articles/life/2026-09-28-turning-a-four-bedroom-into-a-two-bedroom.md": [L],
    "articles/life/2026-09-21-permanent-residency-is-not-a-passport.md": [L],
    "articles/life/2026-09-19-inawashiro-and-nekoma.md": [L],
    "articles/ai/2026-10-17-alaska-us-routes-live.md": [A, L],
    "articles/tesla/2026-10-17-not-2022-anymore-tsll.md": [T, R, U],
    "articles/markets/2026-05-29-cme-bitcoin-gap-ends.md": [U],
    "articles/markets/2026-05-28-spacex-ipo-520k-wired.md": [U],
    "articles/life/2026-05-27-hsbc-singapore-premier-test.md": [L],
    "articles/markets/2026-05-26-bksy-blacksky-technology.md": [U, A],
    "articles/markets/2026-05-25-spacex-ipo-taiwan-subscription.md": [U],
    "articles/life/2026-05-25-still-respect-money.md": [L, U],
}


def load():
    items = []
    for p in sorted((ROOT / "articles").rglob("*.md")):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        m = re.search(r"^# (.+)$", text, re.M)
        title = m.group(1).strip() if m else p.stem
        date = re.match(r"(\d{4}-\d{2}-\d{2})", p.name)
        date = date.group(1) if date else ""
        items.append({"rel": rel, "text": text, "title": title, "date": date,
                      "folder": p.parent.name})
    items.sort(key=lambda a: (a["date"], a["rel"]), reverse=True)
    return items


def topic_block(items):
    out = ["## Topic index", ""]
    for topic in TOPIC_ORDER:
        rows = [a for a in items
                if topic in TOPICS.get(a["rel"], FOLDER_FALLBACK.get(a["folder"], [L]))]
        if not rows:
            continue
        out += [f"### {topic}", ""]
        out += [f"- {a['date']} | {a['title']} | {a['rel']}" for a in rows]
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def insert(path, block):
    s, e = "<!-- topics:start -->", "<!-- topics:end -->"
    text = path.read_text(encoding="utf-8")
    new = f"{s}\n{block}{e}"
    if s in text and e in text:
        text = re.sub(re.escape(s) + r".*?" + re.escape(e), lambda m: new, text, flags=re.S)
    else:
        m = re.search(r"^## Articles.*$", text, re.M)
        pos = m.start() if m else len(text)
        text = text[:pos] + new + "\n\n" + text[pos:]
    path.write_text(text, encoding="utf-8")


def identity_header():
    lines = (ROOT / "llms.txt").read_text(encoding="utf-8").split("\n")
    out = []
    for ln in lines:
        if ln.startswith("## ") and not ln.startswith("## Who I am"):
            if out and any(x.startswith("## Who I am") for x in out):
                break
        out.append(ln)
    return "\n".join(out).rstrip() + "\n"


def main():
    items = load()
    insert(ROOT / "README.md", topic_block(items))
    insert(ROOT / "llms.txt", topic_block(items))
    parts = [identity_header()]
    for a in items:
        parts.append(f"=====\nFile: {a['rel']}\n\n{a['text'].rstrip()}\n")
    (ROOT / "llms-full.txt").write_text("\n".join(parts), encoding="utf-8")
    print(f"{len(items)} articles")


if __name__ == "__main__":
    main()

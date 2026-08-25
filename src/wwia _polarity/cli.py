import click
import json
from .formula import compute_country_bias
from .multipolar import compute_directed_bias, build_multipolar_matrix
from .multipolar_range import multipolar_range
from .ranking import rank_by_multipolarity_range
from .threshold import apply_threshold_vector, rank_countries_by_risk
from .network import multipolar_metrics
from .gamification import GamificationEngine
from .intelligence_tokenizer import tokenize_intelligence
from .config import load_config

@click.command()
@click.option("--country", default=None)
@click.option("--pair", nargs=2, type=str)
@click.option("--matrix", is_flag=True)
@click.option("--countries", default=None)
@click.option("--range-rank", is_flag=True)
@click.option("--cluster-range", default=None, help="Comma-separated countries, e.g. US,IR,SA")
@click.option("--threshold", is_flag=True)
@click.option("--rank", is_flag=True)
@click.option("--gamify", type=click.Choice(["award", "leaderboard"]))
@click.option("--user", default="analyst1")
@click.option("--challenge", default="range_detector")
@click.option("--tokenize", is_flag=True)
def main(country, pair, matrix, countries, range_rank, cluster_range, threshold, rank, gamify, user, challenge, tokenize):
    cfg = load_config()
    clist = [c.strip() for c in (countries or cfg.get("default_countries", "US,IL,IR,SA")).split(",") if c.strip()]

    if pair:
        res = compute_directed_bias(pair[0], pair[1])
        click.echo(json.dumps(res, indent=2))
    elif matrix:
        M = build_multipolar_matrix(clist)
        click.echo(M.round(3).to_string())
        click.echo(json.dumps(multipolar_metrics(M), indent=2, default=str))
    elif range_rank:
        ranked = rank_by_multipolarity_range(clist)
        click.echo(json.dumps(ranked, indent=2))
    elif cluster_range:
        countries_c = [c.strip() for c in cluster_range.split(",")]
        M = build_multipolar_matrix(countries_c)
        r = multipolar_range(M, countries_c)
        click.echo(json.dumps({"cluster": countries_c, "R(S)": round(r, 3)}, indent=2))
    elif threshold:
        flags = apply_threshold_vector(clist)
        click.echo(json.dumps(flags, indent=2))
    elif rank:
        ranked = rank_countries_by_risk(clist)
        click.echo(json.dumps(ranked, indent=2))
    elif gamify == "award":
        engine = GamificationEngine()
        res = engine.award(user, challenge)
        click.echo(json.dumps(res, indent=2))
    elif gamify == "leaderboard":
        engine = GamificationEngine()
        click.echo(json.dumps(engine.leaderboard(), indent=2))
    elif country:
        res = compute_country_bias(country)
        click.echo(json.dumps(res, indent=2))
    elif tokenize:
        ranked = rank_by_multipolarity_range(clist)
        intel = {"range_ranking": ranked}
        tok = tokenize_intelligence(intel)
        click.echo(f"Token count: {tok['token_count']}")
        click.echo(tok["raw_text"][:1500] + "...")
    else:
        click.echo("Use --country, --pair, --matrix, --range-rank, --cluster-range, --threshold, --rank, --gamify or --tokenize")

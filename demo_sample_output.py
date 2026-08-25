#!/usr/bin/env python3
"""
Demo script to showcase WWIA Polarity Bias sample output.
Run this to generate sample JSON output for all major CLI operations.
"""

import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from wwia_polarity.formula import compute_country_bias
from wwia_polarity.multipolar import build_multipolar_matrix, compute_directed_bias
from wwia_polarity.multipolar_range import multipolar_range, compute_all_country_ranges
from wwia_polarity.ranking import rank_by_multipolarity_range
from wwia_polarity.threshold import apply_threshold_vector
from wwia_polarity.network import multipolar_metrics
from wwia_polarity.gamification import GamificationEngine
from wwia_polarity.config import load_config

def demo_range_ranking():
    """Demo: --range-rank"""
    print("\n" + "="*70)
    print("DEMO 1: Range Ranking (--range-rank)")
    print("="*70)
    
    cfg = load_config()
    countries = [c.strip() for c in cfg.get("default_countries", "US,IL,IR,SA").split(",")]
    
    result = rank_by_multipolarity_range(countries)
    print(json.dumps(result[:5], indent=2))
    print(f"\n... (showing first 5 of {len(result)} countries)")

def demo_cluster_range():
    """Demo: --cluster-range"""
    print("\n" + "="*70)
    print("DEMO 2: Cluster Range (--cluster-range US,IR,SA,TR,PK)")
    print("="*70)
    
    countries = ["US", "IR", "SA", "TR", "PK"]
    M = build_multipolar_matrix(countries)
    r = multipolar_range(M, countries)
    
    result = {
        "cluster": countries,
        "R(S)": round(r, 3)
    }
    print(json.dumps(result, indent=2))

def demo_directed_pair():
    """Demo: --pair"""
    print("\n" + "="*70)
    print("DEMO 3: Directed Bias Pair (--pair US IR)")
    print("="*70)
    
    result = compute_directed_bias("US", "IR")
    print(json.dumps(result, indent=2))

def demo_threshold_vector():
    """Demo: --threshold"""
    print("\n" + "="*70)
    print("DEMO 4: Threshold Vector Flags (--threshold)")
    print("="*70)
    
    cfg = load_config()
    countries = [c.strip() for c in cfg.get("default_countries", "US,IL,IR,SA").split(",")]
    
    result = apply_threshold_vector(countries)
    print(json.dumps(result, indent=2))

def demo_matrix():
    """Demo: --matrix"""
    print("\n" + "="*70)
    print("DEMO 5: Full Multipolar Matrix (--matrix)")
    print("="*70)
    
    countries = ["US", "IR", "IL", "SA"]
    M = build_multipolar_matrix(countries)
    print("\nDirected Multipolar Bias Matrix B_{i→j}:")
    print(M.round(3).to_string())
    
    print("\nNetwork Metrics:")
    metrics = multipolar_metrics(M)
    print(json.dumps(metrics, indent=2, default=str))

def demo_country_bias():
    """Demo: --country"""
    print("\n" + "="*70)
    print("DEMO 6: Single Country Bias (--country US)")
    print("="*70)
    
    result = compute_country_bias("US")
    print(json.dumps(result, indent=2))

def demo_gamification():
    """Demo: --gamify"""
    print("\n" + "="*70)
    print("DEMO 7: Gamification (--gamify award/leaderboard)")
    print("="*70)
    
    engine = GamificationEngine()
    
    # Award XP
    award_result = engine.award("analyst1", "range_detector")
    print("\nAward Challenge:")
    print(json.dumps(award_result, indent=2))
    
    # Leaderboard
    lb = engine.leaderboard()
    print("\nLeaderboard:")
    print(json.dumps(lb, indent=2))

def main():
    """Run all demos."""
    print("\n" + "█"*70)
    print("█ WWIA POLARITY BIAS - SAMPLE OUTPUT DEMO")
    print("█ v0.4.0 – Range of Multipolarity Release")
    print("█"*70)
    
    try:
        demo_range_ranking()
        demo_cluster_range()
        demo_directed_pair()
        demo_threshold_vector()
        demo_matrix()
        demo_country_bias()
        demo_gamification()
        
        print("\n" + "█"*70)
        print("█ All demos completed successfully!")
        print("█"*70 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

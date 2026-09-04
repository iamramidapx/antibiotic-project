import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# --------------------------------------------------------------------------
# CONFIGURATION
# --------------------------------------------------------------------------

SUMMARY_CSV = Path("growth_curve.csv")
OUTPUT_DIR = Path("figures")

STRAIN_COLORS = {
    "PY012": "#e2761b",  # wild-type - ส้ม
    "PY001": "#2b7fc9",  # recA- - ฟ้า
    "MA012": "#3f9e4d",  # addA- - เขียว
}
STRAIN_LABELS = {
    "PY012": "PY012 (wild-type)",
    "PY001": "PY001 (recA\u207b)",
    "MA012": "MA012 (addA\u207b)",
}


# --------------------------------------------------------------------------
# PLOTTING FROM SUMMARY DATA
# --------------------------------------------------------------------------

def plot_summary_metrics(df: pd.DataFrame, out_dir: Path):
    out_dir.mkdir(exist_ok=True)
    
    experiments = df["experiment"].unique()
    
    for exp in experiments:
        sub_df = df[df["experiment"] == exp]
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        strains = sub_df["strain"].unique()
        x = range(len(strains))
        width = 0.35
        
        # กราฟที่ 1: Growth Rate (mu per min)
        treatments = sub_df["treatment"].unique()
        
        # จัดการพล็อตแบบเปรียบเทียบ Control และ Treated (ถ้ามี)
        for i, trt in enumerate(treatments):
            trt_data = sub_df[sub_df["treatment"] == trt]
            mu_vals = [trt_data[trt_data["strain"] == s]["growth_rate_mu_per_min"].values[0] if not trt_data[trt_data["strain"] == s].empty else 0 for s in strains]
            
            offset = (i - 0.5) * width if len(treatments) > 1 else 0
            ax1.bar([pos + offset for pos in x], mu_vals, width=width, label=f"Treatment: {trt}")
            
        ax1.set_xticks(list(x))
        ax1.set_xticklabels([STRAIN_LABELS.get(s, s) for s in strains])
        ax1.set_ylabel("Growth Rate ($\mu$ / min)")
        ax1.set_title(f"Growth Rate - {exp}")
        ax1.legend()
        ax1.grid(alpha=0.3, axis="y")
        
        # กราฟที่ 2: Doubling Time (min)
        for i, trt in enumerate(treatments):
            trt_data = sub_df[sub_df["treatment"] == trt]
            dt_vals = [trt_data[trt_data["strain"] == s]["doubling_time_min"].values[0] if not trt_data[trt_data["strain"] == s].empty else 0 for s in strains]
            
            offset = (i - 0.5) * width if len(treatments) > 1 else 0
            ax2.bar([pos + offset for pos in x], dt_vals, width=width, label=f"Treatment: {trt}")
            
        ax2.set_xticks(list(x))
        ax2.set_xticklabels([STRAIN_LABELS.get(s, s) for s in strains])
        ax2.set_ylabel("Doubling Time (min)")
        ax2.set_title(f"Doubling Time - {exp}")
        ax2.legend()
        ax2.grid(alpha=0.3, axis="y")
        
        fig.tight_layout()
        out_path = out_dir / f"summary_{exp}.png"
        fig.savefig(out_path, dpi=200)
        plt.close(fig)
        print(f"Saved summary plot: {out_path}")


def main():
    if not SUMMARY_CSV.exists():
        sys.exit(f"ERROR: Could not find '{SUMMARY_CSV}'")
        
    df = pd.read_csv(SUMMARY_CSV)
    print(f"Successfully loaded summary CSV with {len(df)} rows.")
    
    plot_summary_metrics(df, OUTPUT_DIR)
    print("\nAll summary charts generated successfully!")


if __name__ == "__main__":
    main()

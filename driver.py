import subprocess
import numpy as np
import matplotlib.pyplot as plt

def run_experiment(d, r, N):
    """
    Run the Monte Carlo hypersphere volume program with given d, r, N.
    Returns the relative error (float).
    """
    # Call the other program as a subprocess
    result = subprocess.run(
        ["python3", "ndsphere.py", str(d), str(N), str(r)],
        capture_output=True,
        text=True,
        check=True
    )

    # Parse output lines
    rel_error = None
    stdev = None
    for line in result.stdout.splitlines():
        if line.startswith("relative error:"):
            rel_error = float(line.split(":")[1].strip())
        elif line.startswith("stat uncertainty:"):
            stdev = float(line.split(":")[1].strip())

    return rel_error, stdev

def main():
    dims = [10, 5, 3]   # dimensions to test
    r = 1.0
    ks = range(6, 25)  # 6 to 24 inclusive
    Ns = [2**k for k in ks]

    all_data = {}

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    for d in dims:
        errors = []
        errors_std = []
        sqrtN = []

        for N in Ns:
            rel_error, stdev = run_experiment(d, r, N)
            errors.append(rel_error)
            errors_std.append(stdev)
            sqrtN.append(np.sqrt(N))
            print(f"d={d}, N={N}, rel_error={rel_error}, stdev={stdev}")

        all_data[d] = (np.array(sqrtN), np.array(errors), np.array(errors_std))

        # Log-log plot
        ax1.errorbar(sqrtN, errors, yerr=errors_std, fmt='o-', capsize=3, label=f"d={d}")

        # Linear plot
        ax2.errorbar(sqrtN, errors, yerr=errors_std, fmt='o-', capsize=3, label=f"d={d}")

    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_xlabel(r"$\sqrt{N}$")
    ax1.set_ylabel("Relative Error")
    ax1.set_title("Log–Log Scale")
    ax1.grid(True, which="both", ls="--")
    ax1.legend()

    # Right: linear scaling
    ax2.set_xlabel(r"$\sqrt{N}$")
    ax2.set_title("Linear Scale (supposed to see the error bars better but they get very small)")
    ax2.grid(True, ls="--")
    ax2.legend()

    plt.suptitle("Relative Error vs √N for Monte Carlo Hypersphere Volume", fontsize=14)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig("convergence.png", dpi=300)

    #Plot of only 10D error

    sqrtN_10, errors_10, _ = all_data[10]

    plt.figure(figsize=(7,6))
    plt.loglog(sqrtN_10, errors_10, 'o-', label="d = 10", color='tab:blue')
    plt.xlabel(r"$\sqrt{N}$")
    plt.ylabel("Relative Error")
    plt.title("Monte Carlo Relative Error vs √N (10D only)")
    plt.grid(True, which="both", ls="--")
    plt.legend()
    plt.tight_layout()
    plt.savefig("10Dconvergence.png", dpi=300)

if __name__ == "__main__":
    main()


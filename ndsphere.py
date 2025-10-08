import sys
import numpy as np
from scipy.special import gamma

def main():
    # Check if the user provided the correct number of arguments
    if len(sys.argv) != 4:
        print(f"Usage: {sys.argv[0]} <int1> <int2> <double>")
        sys.exit(1)  # Exit with error code

    # Parse the command-line arguments
    try:
        d = int(sys.argv[1])         # First integer
        N = int(sys.argv[2])         # Second integer
        r = float(sys.argv[3])       # First double

    except ValueError:
        print("Error: Please provide valid integers and doubles as arguments.")
        sys.exit(1)  # Exit with error code

    # ******* Add your code here
    points = (np.random.rand(N,d)-0.5)*2*r
    distances = np.linalg.norm(points, axis=1)
    #print(distances)
    #print(d)
    counter = 0
    for g in distances:
        if g<=r:
            counter+=1
    volume = counter/N*(2*r)**(d)
    realVolume = (np.pi ** (d / 2) / gamma(d / 2 + 1)) * (r ** d)
    e1 = np.sqrt((counter - (counter**2)/N)/(N-1))
    stdev = e1*((2*r)**(d))/np.sqrt(N)
    relerror=np.abs((realVolume-volume)/realVolume)
    

    # *******

    # Do not change the format below
    print(f"(r): {r}")
    print(f"(d,N): {d} {N}")
    print(f"volume: {volume}")
    print(f"stat uncertainty: {stdev}")
    print(f"relative error: {relerror}")

if __name__ == "__main__":
    main()

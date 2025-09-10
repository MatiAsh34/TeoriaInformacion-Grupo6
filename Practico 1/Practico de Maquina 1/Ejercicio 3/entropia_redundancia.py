import os
import math
from array import array
from typing import Dict, Any

class calculo_entropia_redundancia:
    def __init__(self, alphabet_size: int = 256, chunk_size: int = 1 << 20):
        self.A = alphabet_size
        self.chunk = chunk_size

    def analizar_stream(self, path: str) -> Dict[str, Any]:
        counts = array('Q', [0]) * self.A
        pair_counts = array('Q', [0]) * (self.A * self.A)
        N = 0
        Npairs = 0
        prev = None

        with open(path, 'rb') as f:
            while True:
                block = f.read(self.chunk)
                if not block:
                    break
                for b in block:
                    counts[b] += 1
                    N += 1
                    if prev is not None:
                        pair_counts[prev * self.A + b] += 1
                        Npairs += 1
                    prev = b

        return {
            "counts": counts,
            "pair_counts": pair_counts,
            "N": N,
            "Npairs": Npairs
        }

    def entropia_orden0(self, counts: array, N: int) -> float:
        if N == 0:
            return 0.0
        H = 0.0
        for c in counts:
            if c:
                p = c / N
                H -= p * math.log2(p)
        return H

    def entropia_orden1(self, counts: array, pair_counts: array, Npairs: int) -> float:
        if Npairs == 0:
            return 0.0
        A = self.A
        H = 0.0
        for x in range(A):
            row_start = x * A
            c_x = 0
            for y in range(A):
                c_x += pair_counts[row_start + y]
            if c_x == 0:
                continue
            inv_cx = 1.0 / c_x
            for y in range(A):
                c_xy = pair_counts[row_start + y]
                if c_xy:
                    p_xy = c_xy / Npairs
                    p_y_given_x = c_xy * inv_cx
                    H -= p_xy * math.log2(p_y_given_x)
        return H

    def analizar(self, filename: str) -> Dict[str, Any]:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(path)

        data = self.analizar_stream(path)
        counts = data["counts"]
        pair_counts = data["pair_counts"]
        N = data["N"]
        Npairs = data["Npairs"]

        H0 = self.entropia_orden0(counts, N)
        H1 = self.entropia_orden1(counts, pair_counts, Npairs)

        logA = math.log2(self.A) if self.A > 1 else 1.0
        R0 = 0.0 if logA == 0 else max(0.0, 1.0 - H0 / logA)
        R1 = 0.0 if logA == 0 else max(0.0, 1.0 - H1 / logA)

        return {
            "Entropia Independiente": H0,
            "Entropia Dependiente": H1,
            "Redundancia Independiente": R0,
            "Redundancia Dependiente": R1,
        }


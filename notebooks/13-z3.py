from z3 import *
from collections import namedtuple
import re
import pandas as pd

with open("13-input", "r") as file:
    lines = file.readlines()
data_raw = "".join(lines)

Claw = namedtuple("Claw", ["XA", "YA", "XB", "YB", "X", "Y"])

def preprocess_data (data):
    def prep_setup(a):
        XA, YA = re.findall(r'\d+', a[0])
        XB, YB = re.findall(r'\d+', a[1])
        X, Y = re.findall(r'\d+', a[2])
        # YA = int(a[0].split("+")[-1])
        # XA = int(a[0].split("+")[-2].split(",")[0])
        # YB = int(a[1].split("+")[-1])
        # XB = int(a[1].split("+")[-2].split(",")[0])
        
        return Claw(XA=int(XA), YA=int(YA), XB=int(XB), YB=int(YB), X=int(X), Y=int(Y))
    
    rows = [prep_setup(row.split("\n")) for row in data.split("\n\n")]
    return rows

full_data = preprocess_data(data_raw)
total = 0
solutions = pd.DataFrame()

for claw in full_data:
    s = Solver()

    a = Int("A")
    b = Int("B")
    # Claw(XA=22, YA=36, XB=49, YB=21, X=8122, Y=6806)
    s.add(a * claw.XA + b * claw.XB == claw.X + 10000000000000, 
          a * claw.YA + b * claw.YB == claw.Y + 10000000000000,
          0 < a, 
        #   a <= 100, 
          0 < b, 
        #   b <= 100 
          )
    
    print(claw)
    print(s)
    # Check if system is satisfiable
    sat = s.check()
    print(sat)
    
    # We say the solution is a model for the set of asserted constraints. A model is an interpretation that makes each asserted constraint true
    
    if str(sat) == 'sat':
        m = s.model()
        print(m.eval(a), m.eval(b))
        
        total += 3*m.eval(a).as_long()+m.eval(b).as_long()
        solutions = pd.concat([solutions, pd.DataFrame({"Sat": ["sat"], "A": [m.eval(a).as_long()], "B": [m.eval(b).as_long()]})])
    else:
        solutions = pd.concat([solutions, pd.DataFrame({"Sat": ["unsat"]})])
    
  
    print("\n")
solutions.to_csv("solutions.csv", index=False)
print(total)
    
import pandas as pd

for i in range(103, 108):
    df = pd.read_csv(f"csv/{i}_student.csv")
    df["學年度"] = i
    df.to_csv(f"csv/{i}_student_mod.csv")

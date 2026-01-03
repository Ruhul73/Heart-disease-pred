import argparse
import pickle
import os
import sys

MODEL_PATH = "heart_model.pkl"


def load_model(path=MODEL_PATH):
    if not os.path.exists(path):
        print(f"Model file '{path}' not found. Run train_model.py first.", file=sys.stderr)
        sys.exit(2)
    with open(path, "rb") as f:
        return pickle.load(f)


def parse_values(s):
    parts = [p.strip() for p in s.split(",") if p.strip()!='']
    if len(parts) != 13:
        raise argparse.ArgumentTypeError("--values must contain 13 comma-separated values in order: age,sex,cp,bp,chol,sugar,ecg,hr,angina,oldpeak,slope,vessels,thal")
    # convert numeric types
    out = []
    for i, p in enumerate(parts):
        try:
            if i == 9:  # oldpeak float
                out.append(float(p))
            else:
                out.append(int(float(p)))
        except Exception:
            raise argparse.ArgumentTypeError(f"Invalid numeric value: {p}")
    return out


def main():
    p = argparse.ArgumentParser(description="Headless predictor for Heart Disease model")
    p.add_argument("--values", type=parse_values,
                   help="Comma-separated 13 values: age,sex,cp,bp,chol,sugar,ecg,hr,angina,oldpeak,slope,vessels,thal")
    p.add_argument("--interactive", action="store_true", help="Prompt for values interactively")
    args = p.parse_args()

    model = load_model()

    if args.interactive:
        vals = []
        prompts = [
            "age","sex (1=male,0=female)","cp","bp","chol","sugar (fbs)","ecg (restecg)","hr (thalach)","angina (exang)","oldpeak","slope","vessels (ca)","thal"
        ]
        for pr in prompts:
            v = input(f"{pr}: ")
            if pr == "oldpeak":
                vals.append(float(v))
            else:
                vals.append(int(float(v)))
    elif args.values:
        vals = args.values
    else:
        p.print_help()
        sys.exit(1)

    data = [vals]
    prob = model.predict_proba(data)[0][1] * 100
    result = model.predict(data)[0]

    if result == 1:
        print(f"HIGH RISK OF HEART DISEASE — Confidence: {prob:.2f}%")
        sys.exit(0)
    else:
        print(f"LOW RISK — Confidence: {100-prob:.2f}%")
        sys.exit(0)


if __name__ == '__main__':
    main()

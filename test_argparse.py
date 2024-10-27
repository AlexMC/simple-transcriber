import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Test argparse")
    parser.add_argument("input", help="Test input")
    return parser.parse_args()

def main():
    args = parse_args()
    print(f"Input argument: {args.input}")

if __name__ == "__main__":
    main()


import argparse
import json
from pathlib import Path

from .data import audit, download
from .experiments import develop, dry_run, evaluate, load_config, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description="ME276DS gas turbine NOx project")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("download", help="Restore pinned raw CSVs; no training")
    qa = commands.add_parser("audit", help="Data integrity and training-only summary; no fitting")
    qa.add_argument("--output", type=Path)
    for name in ["dry-run", "develop"]:
        command = commands.add_parser(name)
        command.add_argument("--config", type=Path, default=Path("configs/experiments.json"))
        if name == "develop":
            command.add_argument("--run", type=Path, required=True)
            command.add_argument(
                "--execute", action="store_true", help="Explicitly enable model fitting"
            )
    final = commands.add_parser("evaluate", help="Refit frozen models and evaluate test once")
    final.add_argument("--run", type=Path, required=True)
    final.add_argument("--execute", action="store_true")
    report = commands.add_parser("report", help="Render saved results; no fitting")
    report.add_argument("--run", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    if args.command in {"develop", "evaluate"} and not args.execute:
        parser.error("Model fitting is disabled without --execute. Use dry-run for preparation.")
    if args.command == "download":
        result = download(root)
    elif args.command == "audit":
        result = audit(root)
        if args.output:
            output = root / args.output
            output.parent.mkdir(parents=True, exist_ok=True)
            write_json(output, result)
    elif args.command in {"develop", "dry-run"}:
        config = load_config(root / args.config)
        result = (
            dry_run(root, config)
            if args.command == "dry-run"
            else develop(root, config, root / args.run)
        )
    elif args.command == "evaluate":
        result = evaluate(root, root / args.run)
    else:
        from .reporting import make_report

        result = make_report(root / args.run)
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()

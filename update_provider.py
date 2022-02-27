import argparse

from gaqqie_rainbow import Gaqqie
from gaqqie_rainbow.rest import Provider


if __name__ == "__main__":
    # build parser
    parser = argparse.ArgumentParser(description="update provider for gaqqie cloud")
    parser.add_argument(
        "--region", required=True, help="the region name of gaqqie provider API"
    )
    parser.add_argument(
        "--api_id", required=True, help="the API ID of gaqqie provider API"
    )
    parser.add_argument("--name", required=True, help="provider name")
    parser.add_argument(
        "--status", choices=["ACTIVE", "INACTIVE"], help="status of provider"
    )
    parser.add_argument("--description", help="description of provider")
    parser.add_argument("--details", help="details of provider")

    # parse args
    args = parser.parse_args()
    args_dict = {"name": args.name}
    if args.status:
        args_dict["status"] = args.status
    if args.description:
        args_dict["description"] = args.description
    if args.details:
        args_dict["details"] = args.details

    # execute command
    url = f"https://{args.api_id}.execute-api.{args.region}.amazonaws.com/dev"
    app = Gaqqie(url)
    provider = Provider(**args_dict)
    app.provider_api.update_provider(provider, args.name)

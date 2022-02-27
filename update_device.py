import argparse

from gaqqie_rainbow import Gaqqie
from gaqqie_rainbow.rest import Device


if __name__ == "__main__":
    # build parser
    parser = argparse.ArgumentParser(description="update device for gaqqie cloud")
    parser.add_argument(
        "--region", required=True, help="the region name of gaqqie provider API"
    )
    parser.add_argument(
        "--api_id", required=True, help="the API ID of gaqqie provider API"
    )
    parser.add_argument("--name", required=True, help="device name")
    parser.add_argument("--provider_name", help="provider name")
    parser.add_argument(
        "--status",
        choices=["ACTIVE", "SUBMITTABLE", "UNSUBMITTABLE"],
        help="status of device",
    )
    parser.add_argument("--num_qubits", type=int, help="number of qubits")
    parser.add_argument("--max_shots", type=int, help="max shots")
    parser.add_argument("--description", help="description of device")
    parser.add_argument("--details", help="details of device")

    # parse args
    args = parser.parse_args()
    args_dict = {"name": args.name}
    if args.provider_name:
        args_dict["provider_name"] = args.provider_name
    if args.status:
        args_dict["status"] = args.status
    if args.num_qubits:
        args_dict["num_qubits"] = args.num_qubits
    if args.max_shots:
        args_dict["max_shots"] = args.max_shots
    if args.description:
        args_dict["description"] = args.description
    if args.details:
        args_dict["details"] = args.details

    # execute command
    url = f"https://{args.api_id}.execute-api.{args.region}.amazonaws.com/dev"
    app = Gaqqie(url)
    device = Device(**args_dict)
    app.device_api.update_device(device, args.name)

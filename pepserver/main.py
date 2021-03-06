import sys

import logmuse
import uvicorn
from fastapi import FastAPI

from ._version import __version__ as server_v
from .const import LOG_FORMAT, PKG_NAME
from .helpers import build_parser

app = FastAPI(
    title=PKG_NAME,
    description="a web interface and RESTful API for PEPs",
    version=server_v,
)


def main():
    global _LOGGER
    parser = build_parser()
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        print("No subcommand given")
        sys.exit(1)
    logger_args = (
        dict(name=PKG_NAME, fmt=LOG_FORMAT, level=5)
        if args.debug
        else dict(name=PKG_NAME, fmt=LOG_FORMAT)
    )
    _LOGGER = logmuse.setup_logger(**logger_args)
    if args.command == "serve":
        from .routers import validate, version1

        app.include_router(validate.router, prefix="/validate")
        app.include_router(version1.router)
        app.include_router(version1.router, prefix="/v1")

        uvicorn.run(app, host="0.0.0.0", port=args.port)
    else:
        _LOGGER.error(f"unknown command: {args.command}")
        sys.exit(1)

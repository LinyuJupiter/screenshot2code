import uvicorn
import os
import traceback
import json
import time
import datetime
import httpx
import jwt
import zhipuai
import fastapi

from fastapi.middleware.cors import CORSMiddleware
import asyncio
import re
import typing
import bs4

if __name__ == "__main__":
    log_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.FileHandler",
                "formatter": "default",
                "filename": "app.log",
            },
        },
        "loggers": {
            "": {
                "handlers": ["file"],
                "level": "INFO",
            },
        },
    }
    uvicorn.run("main:app", port=7001, reload=False, log_config=log_config)

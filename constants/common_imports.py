import json
import requests
import uuid
import base64
import ast
import io
import jwt
import re
import pypdf
import pytz
import imghdr
import img2pdf
import hashlib
import boto3
import hmac
import pillow_heif
from Crypto.Util.Padding import pad, unpad
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from dateutil import parser
import botocore.session
import random
from time import gmtime, strftime
from typing import *
from PIL import Image
from io import BytesIO
from Crypto import Random
from Crypto.Cipher import AES
from pathlib import Path
from requests.auth import HTTPBasicAuth
from functools import wraps
from bson import ObjectId
from secrets import token_bytes
from starlette.middleware.base import BaseHTTPMiddleware

"""FastAPI"""
from fastapi.security import OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Request, Response, File, UploadFile, Form, Header, Depends, HTTPException, status

"""pydantic"""
from dotenv import load_dotenv
from pydantic import BaseModel, constr, validator

"""date"""
from datetime import datetime, timezone, timedelta
from dateutil.parser import parse

tags_metadata = []

app = FastAPI(openapi_tags=tags_metadata, )  # docs_url=None, redoc_url=None # For production

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
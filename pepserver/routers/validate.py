import tempfile
from typing import List
import os
import shutil

# fastapi imports
from fastapi import APIRouter, File, UploadFile

# exceptions
from jsonschema.exceptions import ValidationError

# eido & peppy
import eido
from peppy import Project

# helpers
from ..utils import TEST_SCHEMA

# router setup
router = APIRouter(
    prefix="/validate"
)

@router.post("/project")
async def validate_project(files: List[UploadFile] = File(...)):
    _tmpdirpath = tempfile.mkdtemp()
    for file in files:
        # read and write to tmp file
        contents = await file.read()
        with open(os.path.join(_tmpdirpath, file.filename), 'w+b') as f:
            f.write(contents)
        
        # detect yaml file
        _, ext = os.path.splitext(file.filename)
        if ext == '.yaml' or ext == '.yml':
            # config file found -- store
            cfg_file = os.path.join(_tmpdirpath, file.filename)

    # instantiate Project() from known cfg file
    prj = Project(cfg=cfg_file)
    results = []
    for s_name, s_src in TEST_SCHEMA.items():
        print(f"----> Testing: {s_name}")
        try:
            eido.validate_project(
                project=prj,
                schema=s_src
            )
            # if no error thrown, SUCCESS
            results.append({
                "schema": s_name,
                "result": "PASS"
            })
        except ValidationError as e:
            # else FAIL
            results.append({
                "schema": s_name,
                "result": "FAIL",
                "reason": f"{e}"
            })
            
    # remove tmp dir
    shutil.rmtree(_tmpdirpath)
    
    # return
    return results
            
        
        
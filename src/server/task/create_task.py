#!/usr/bin/env python
import os
import sys

# import framework
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from starlette.requests import Request

# import tools
from src.tools.config_tools import ConfigTools
from src.tools.io_tools.io_tools import IOTools

# import other server
from src.server.task.select_task import select_all_task_name_core

# from pathlib import Path

# import logging

# from settings import app_root_path
# from settings import upload_folder
# from settings import log_file_path


router = APIRouter()


@router.post("/create")
def create(request: Request):

    task_name = "test004"
    config = ConfigTools()
    source_folder_path = config.get_source_folder_path()
    all_task_names = select_all_task_name_core()
    log_info = f"all task names: {all_task_names}"
    print(log_info)
    resout_code = 1 # 0: success, 1: failed
    if task_name in all_task_names:
        log_info = f"task name: {task_name} already exists!"
        print(log_info)
    else:
        log_info = f"task name: {task_name} not exists!"
        print(log_info)
        io_tools = IOTools()
        task_dir = os.path.join(source_folder_path, task_name)
        resout = io_tools.create_target_folder(task_dir)
        resout_code = resout.get("return_value", 1)
        if resout_code == 0:
            log_info = f"create task folder success!"
            task_index_json_file = os.path.join(source_folder_path, task_name, "task_index.json")
            resout = io_tools.create_target_file(task_index_json_file)
            resout_code = resout.get("return_value", 1)
            if resout_code == 0:
                log_info = f"create task index json file success!"
            else:
                log_info = f"create task index json file failed!"
            print(log_info)
        else:
            log_info = f"create task folder failed!"
            print(log_info)
    return {"message": log_info, "resout": resout_code}


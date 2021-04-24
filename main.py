# -*- coding: utf-8 -*-
import time
import pybase64
import json
import numpy as np
import cv2
from typing import Optional
from fastapi import FastAPI, Response, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from utils.base import load_image, ocr_result, pprint
from api.paddleOCR import OCR

app = FastAPI()
OCR = OCR()
"""uvicorn main:app --host 127.0.0.1 --port 8766 --reload"""

@app.get("/")
def read_root():
    return {"Hello": "World"}


class paddleOCR_item(BaseModel):
    image: Optional[str] = None  # base64编码
    lang: Optional[str] = 'en' # 默认识别语言


@app.post("/ocr/paddle/general_basic")
def paddleOCR_general_basic(item: paddleOCR_item, response: Response):
    """基础识别, 不包含检测位置, 只识别. det=False, res=True, cls=False"""
    start_time = time.time()
    item_dict = item.dict()
    img, lang = load_image(item_dict['image']), item_dict['lang']
    result = OCR.ocr(image=img, det=False, lang=lang)
    txts = result[0][0]
    scores = result[0][1]
    if txts:
        result = ocr_result({
            'text': txts,
            'scores': float(scores)
        }, item_dict['lang'], time.time() - start_time)
    else:
        result = ocr_result(None, item_dict['lang'], time.time() - start_time)
    return result


@app.post("/ocr/paddle/general")
def paddleOCR_general(item: paddleOCR_item, response: Response):
    start_time = time.time()
    item_dict = item.dict()
    img, lang = load_image(item_dict['image']), item_dict['lang']
    result = OCR.ocr(image=img, det=True, rec=True, lang=lang)
    if result:
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        ret = []
        for index in range(len(result)):
            ret.append({
                'boxes': boxes[index],
                'txts': txts[index],
                'scores': float(scores[index])
            })
        result = ocr_result(ret, item_dict['lang'], time.time() - start_time)
    else:
        result = ocr_result(None, item_dict['lang'], time.time() - start_time)
    return result

# -*- coding: utf-8 -*-
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.50.104", port=8766, log_level="info")
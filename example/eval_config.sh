#!/bin/bash

CUDA_VISIBLE_DEVICES=5 mace_eval_configs \ 
    --configs="test.xyz" \
    --model="model_stagetwo.model" \
    --output="./test_out.xyz" \
    --default_dtype="float64" \
    --device="cuda" \
    --batch_size=5

CUDA_VISIBLE_DEVICES=5 mace_eval_configs --config ./test.xyz --model model_stagetwo.model --output test_out.xyz


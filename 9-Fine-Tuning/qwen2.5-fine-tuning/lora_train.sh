#! /usr/bin/env bash

set -ex

LR=1e-4
MAX_SEQ_LEN=384
MAX_SOURCE_LEN=128
MAX_TARGET_LEN=256

BASE_MODEL_PATH=model/qwen/Qwen2___5-1___5B-Instruct

DATESTR=`date +%Y%m%d-%H%M%S`
RUN_NAME=qwen2.5-1.5B-Instruct-lora
OUTPUT_DIR=output/${RUN_NAME}-${DATESTR}
mkdir -p $OUTPUT_DIR


CUDA_VISIBLE_DEVICES=0 python train.py \
    --do_train \
    --do_eval \
    --train_file data/train.json \
    --validation_file data/val.json \
    --max_seq_length $MAX_SEQ_LEN \
    --max_source_length $MAX_SOURCE_LEN \
    --max_target_length $MAX_TARGET_LEN \
    --preprocessing_num_workers 1 \
    --model_name_or_path $BASE_MODEL_PATH \
    --output_dir $OUTPUT_DIR \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --num_train_epochs 4 \
    --gradient_accumulation_steps 4\
    --evaluation_strategy steps \
    --eval_steps 1000 \
    --logging_steps 10 \
    --logging_dir $OUTPUT_DIR/logs \
    --save_steps 1000 \
    --learning_rate $LR \
    --lora_rank 8 \
    --lora_alpha 32 \
    --lora_dropout 0.1 2>&1 | tee ${OUTPUT_DIR}/train.log

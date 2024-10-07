from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    DataCollatorForSeq2Seq,
    HfArgumentParser,
    TrainingArguments,
    Trainer,
)

from qwen_dataset import QwenDataset
from arguments import ModelArguments, DataTrainingArguments, PeftArguments
from peft import get_peft_model, LoraConfig, TaskType


def load_lora_model(model_args, peft_args):
    # 加载预训练的tokenizer和model
    tokenizer = AutoTokenizer.from_pretrained(model_args.model_name_or_path, use_fast=False, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model_args.model_name_or_path, device_map='auto', torch_dtype='auto')
    print("torch_dtype", model.dtype)
    print("device", model.device)

    # 使用peft库配置lora参数
    peft_config = LoraConfig(
        task_type=TaskType.CAUSAL_LM,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        inference_mode=False,
        r=peft_args.lora_rank,  # Lora 秩
        lora_alpha=peft_args.lora_alpha,
        lora_dropout=peft_args.lora_dropout  # Dropout 比例
    )
    model = get_peft_model(model, peft_config)

    model.enable_input_require_grads()
    model.is_parallelizable = True
    model.model_parallel = True
    model.config.use_cache = False

    # 打印可训练的参数量
    model.print_trainable_parameters()

    return tokenizer, model


def main():
    # 解析传入的命令行参数
    parser = HfArgumentParser((ModelArguments, DataTrainingArguments, PeftArguments, TrainingArguments))
    model_args, data_args, peft_args, training_args = parser.parse_args_into_dataclasses()
    # 设备
    tokenizer, model = load_lora_model(model_args, peft_args)

    # 准备训练数据集并处理成所需格式
    if training_args.do_train:
        train_dataset = QwenDataset(
            data_args.train_file,
            tokenizer,
            data_args.max_source_length,
            data_args.max_target_length
        )

    if training_args.do_eval:
        eval_dataset = QwenDataset(
            data_args.validation_file,
            tokenizer,
            data_args.max_source_length,
            data_args.max_target_length
        )
    # 配置训练参数
    args = TrainingArguments(
        output_dir=training_args.output_dir,
        per_device_train_batch_size=training_args.per_device_train_batch_size,
        gradient_accumulation_steps=training_args.gradient_accumulation_steps,
        logging_steps=training_args.logging_steps,
        num_train_epochs=training_args.num_train_epochs,
        save_steps=training_args.save_steps,
        learning_rate=training_args.learning_rate,
        save_on_each_node=True,
        gradient_checkpointing=True
    )

    # 配置trainer
    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
        data_collator=DataCollatorForSeq2Seq(tokenizer=tokenizer, padding=True),
    )

    # 开始训练
    if training_args.do_train:
        model.gradient_checkpointing_enable()
        model.enable_input_require_grads()
        trainer.train()
        trainer.save_model()  # Saves the tokenizer too for easy upload
        trainer.save_state()

    if training_args.do_eval:
        trainer.evaluate()


if __name__ == "__main__":
    main()

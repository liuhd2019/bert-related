export CUDA_VISIBLE_DEVICES=2
python run_nq.py \
	--do_predict true \
	--predict_file models/tiny-train/nq-dev-sample.jsonl.gz \
	--train_precomputed_file outputs/model.ckpt-600 \
	--vocab_file models/bert-joint-baseline/vocab-nq.txt \
	--bert_config_file models/bert-joint-baseline/bert_config.json \
	--predict_batch_size 1 \
	--output_dir ./outputs \
	--output_prediction_file ./outputs/pred.txt


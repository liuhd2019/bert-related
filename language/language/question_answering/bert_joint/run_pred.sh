python run_nq.py \
	--do_predict true \
	--predict_file one.jsonl.gz \
	--train_precomputed_file models/bert-joint-baseline/bert_joint.ckpt \
	--vocab_file models/bert-joint-baseline/vocab-nq.txt \
	--bert_config_file models/bert-joint-baseline/bert_config.json \
	--predict_batch_size 1 \
	--output_dir ./outputs \
	--output_prediction_file ./outputs/pred.txt


export CUDA_VISIBLE_DEVICES=1
python run_nq.py \
	--do_train true \
	--bert_config_file models/bert-joint-baseline/bert_config.json \
	--output_dir ./outputs \
	--train_num_precomputed 200 \
	--train_precomputed_file models/tiny-train/nq-dev-sample.tf_record \
	--vocab_file models/bert-joint-baseline/vocab-nq.txt \
	--init_checkpoint models/bert-joint-baseline/bert_joint.ckpt \
	--train_batch_size 1 \
	--num_train_epochs 5



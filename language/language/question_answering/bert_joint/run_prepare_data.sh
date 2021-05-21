# 用于为训练过程做数据预处理，将数据处理成tf_record格式
python prepare_nq_data.py \
	--input_jsonl models/tiny-train/nq-dev-sample.jsonl.gz \
	--output_tfrecord models/tiny-train/nq-dev-sample.tf_record \
	--vocab_file models/bert-joint-baseline/vocab-nq.txt

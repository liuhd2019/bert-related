CUDA_VISIBLE_DEVICES='0' nohup python3 -u run_kbert_ner.py \
    --pretrained_model_path ./models/google_model.bin \
    --config_path ./models/google_config.json \
    --vocab_path ./models/google_vocab.txt \
    --train_path ./datasets/msra_ner/train.tsv \
    --dev_path ./datasets/msra_ner/dev.tsv \
    --test_path ./datasets/msra_ner/test.tsv \
    --epochs_num 5 --batch_size 16 --kg_name CnDbpedia \
    --output_model_path ./outputs/kbert_msraner_CnDbpedia.bin \
    > ./outputs/kbert_msraner_CnDbpedia.log &

#useage: [--pretrained_model_path] - Path to the pre-trained model parameters.
#        [--config_path] - Path to the model configuration file.
#        [--vocab_path] - Path to the vocabulary file.
#        --train_path - Path to the training dataset.
#        --dev_path - Path to the validating dataset.
#        --test_path - Path to the testing dataset.
#        [--epochs_num] - The number of training epoches.
#        [--batch_size] - Batch size of the training process.
#        [--kg_name] - The name of knowledge graph.
#        [--output_model_path] - Path to the output model.

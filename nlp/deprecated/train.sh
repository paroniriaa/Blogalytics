for SPLIT in train test
do
  for LANG in src tgt
  do
    python -m fairseq.examples.roberta.multiprocessing_bpe_encoder \
    --encoder-json encoder.json \
    --vocab-bpe vocab.bpe \
    --inputs "data/mask/$SPLIT.mask.$LANG" \
    --outputs "data/bpe/$SPLIT.bpe.$LANG" \
    --workers 60 \
    --keep-empty;
  done
done


fairseq-preprocess \
  --source-lang "src" \
  --target-lang "tgt" \
  --trainpref "data/bpe/train.bpe" \
  --validpref "data/bpe/test.bpe" \
  --destdir data/bin/ \
  --workers 60 \
  --srcdict dict.txt \
  --tgtdict dict.txt


  TOTAL_NUM_UPDATES=20000
  WARMUP_UPDATES=500
  LR=3e-05
  MAX_TOKENS=2048
  UPDATE_FREQ=4
  BART_PATH=model/bart.large/model.pt

  CUDA_VISIBLE_DEVICES=2,3 fairseq-train data/bin \
      --restore-file $BART_PATH \
      --max-tokens $MAX_TOKENS \
      --task translation \
      --source-lang src --target-lang tgt \
      --truncate-source \
      --layernorm-embedding \
      --share-all-embeddings \
      --share-decoder-input-output-embed \
      --reset-optimizer --reset-dataloader --reset-meters \
      --required-batch-size-multiple 1 \
      --arch bart_large \
      --criterion label_smoothed_cross_entropy \
      --label-smoothing 0.1 \
      --dropout 0.1 --attention-dropout 0.1 \
      --weight-decay 0.01 --optimizer adam --adam-betas "(0.9, 0.999)" --adam-eps 1e-08 \
      --clip-norm 0.1 \
      --lr-scheduler polynomial_decay --lr $LR --total-num-update $TOTAL_NUM_UPDATES --warmup-updates $WARMUP_UPDATES \
      --fp16 --update-freq $UPDATE_FREQ \
      --skip-invalid-size-inputs-valid-test \
      --find-unused-parameters > logs/bart_large.log 2>&1 &

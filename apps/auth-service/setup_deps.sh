if ! test -d ./python/; then
  mkdir -p python/lib/python3.10/site-packages
  pip install -r r.txt -t python/lib/python3.10/site-packages/
fi

zip -r deps.layer.zip python

aws lambda publish-layer-version \
  --layer-name deps-layer \
  --zip-file fileb://deps.layer.zip \
  --compatible-runtimes python3.10

rm -rf deps.layer.zip python

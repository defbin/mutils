## prepare env
```bash
python3 -m venv ./venv              && \
source ./venv/bin/activate          && \
pip install -Ur requirements.txt
```

## examples
### mlog: collect "cluster" oplog
```bash
# set MONGODB_URI to not specify --uri
export MONGODB_URI=user:pass@host:27017
# CSV by default subset of oplog record fields
mlog > oplog.csv

# MongoDB Extended JSON v2 output with all oplog record fields
mlog --json > oplog.json

# limit oplog range ('123.456' -> Timestamp({t: 123, i: 456}))
mlog --start='1.1' --end='123.456' > oplog.csv
```

### mtake: snapshot of cluster for testing/debugging
```bash
mtake > snap.json

# include user documents
mtake --with-docs > snap.json
```

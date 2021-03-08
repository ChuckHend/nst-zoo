# Batch Processing
- You can invoke the batch processing utilities via the `nst-processor` command.
- This requires additional requirements (`pip install -r requirements/batch_processing.txt`)
- This serves as a simple redis interface:
    -  `send-to-queue` will send the parameter grid (inspired by [sklearn](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterGrid.html)) of a given file to Redis. See `data/config.json` for an example.
    - `process-from-queue` will iterate over a given queue (using `Redis.lpop()`) until the queue is empty
- I plan to eventually add an interface for S3 storage, as batch processing typically results in a ton of files.
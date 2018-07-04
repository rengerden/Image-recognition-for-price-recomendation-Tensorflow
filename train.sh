#!/bin/bash
python retrain.py --bottleneck_dir=tmp/bottlenecks --model_dir=tmp/inception --output_graph=output/retrained_graph.pb --output_labels=output/retrained_labels.txt --image_dir=dataset/training_set/

python retrain.py --bottleneck_dir=tmp/bottlenecks --model_dir=tmp/inception --output_graph=output/retrained_graph.pb --output_labels=output/retrained_labels.txt --image_dir=Imagenes

%PYTHONPATH%
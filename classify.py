import tensorflow as tf
import sys
import os
import numpy as np
from PIL import Image
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def analyse(imageObj):
    # Resize image to 299x299 (what Inception v3 expects)
    img = Image.open(imageObj).convert('RGB')
    img = img.resize((299, 299))
    img.save("temp_resized.png")

    # Read resized image
    image_data = tf.io.gfile.GFile("temp_resized.png", 'rb').read()

    # Load labels
    label_lines = [line.rstrip() for line
                   in tf.io.gfile.GFile("tf_files/retrained_labels.txt")]

    # Load graph
    with tf.io.gfile.GFile("tf_files/retrained_graph.pb", 'rb') as f:
        graph_def = tf.compat.v1.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.compat.v1.Session() as sess:
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                    {'DecodeJpeg/contents:0': image_data})
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        obj = {}
        for node_id in top_k:
            obj[label_lines[node_id]] = float(predictions[0][node_id])
        return obj

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 classify.py <image>")
        sys.exit(1)
    result = analyse(sys.argv[1])
    for label, score in sorted(result.items(), key=lambda x: x[1], reverse=True):
        print(f"{label}: {score:.4f}")
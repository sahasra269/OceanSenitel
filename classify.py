import tensorflow as tf
import sys
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def analyse(imageObj):
    # Read the image data
    image_data = tf.io.gfile.GFile(imageObj, 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                   in tf.io.gfile.GFile("/tmp/output_labels.txt")]

    # Unpersists graph from file
    with tf.io.gfile.GFile("/tmp/output_graph.pb", 'rb') as f:
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
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
            obj[human_string] = float(score)

        return obj

# Run directly from terminal with an image path
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 classify.py <path_to_image>")
        sys.exit(1)
    image_path = sys.argv[1]
    result = analyse(image_path)
    for label, score in sorted(result.items(), key=lambda x: x[1], reverse=True):
        print(f"{label}: {score:.4f}")
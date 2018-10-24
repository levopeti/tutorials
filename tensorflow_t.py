import tensorflow as tf
import time
import os

#os.environ['CUDA_VISIBLE_DEVICES'] = ''

l1 = [x for x in range(10000000)]
l2 = [x + 1 for x in range(10000000)]

print('tf')

x1 = tf.constant(l1)
x2 = tf.constant(l2)

result = tf.multiply(x1, x2)
print(666)

sess = tf.Session()

config = tf.ConfigProto(allow_soft_placement=True, log_device_placement=True)

start = time.time()

sess.run(result)

end = time.time()
print(end - start)
# print(sess.run(result))

sess.close()


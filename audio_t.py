from pydub import AudioSegment
from pydub.utils import which
import matplotlib.pyplot as plt
import numpy as np
import scipy.io.wavfile

#AudioSegment.converter = which("ffmpeg")

#sound = AudioSegment.from_mp3("/home/biot/Downloads/Beatman _Ludmilla-Maldova_(DaVIP_Remix).mp3")
sound = AudioSegment.from_wav("/home/biot/projects/audio_generator/generated_music/1_gen.wav")
print(666)
rate = sound.frame_rate
print(rate)

# sound._data is a bytestring
raw_data = sound.get_array_of_samples()
sound_array = np.array(raw_data)
sound_array = sound_array.reshape(sound.channels, -1, order='F')
#cut = sound_array[0, 1000000:2000000]

print(sound_array.shape)
#f, axarr = plt.subplots(2)
#axarr[0] = plt.plot(sound_array[0, :1000000])
# axarr[1] = plt.plot(sound_array[1, :1000000])
plt.plot(sound_array[0, :])
plt.show()
#print(cut.shape)
#scipy.io.wavfile.write('/home/biot/Downloads/Beatman_and_Ludmilla-Live_at_Normafa_Open_Air_Festival_2016_2.wav', rate, cut.T)



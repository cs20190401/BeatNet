from BeatNet.BeatNet import BeatNet

#estimator = BeatNet(1, mode='stream', inference_model='PF', plot=[], thread=False)
estimator = BeatNet(1, mode='realtime', inference_model='PF', plot=['beat_particles', 'activations'], thread=False)
#estimator = BeatNet(1, mode='online', inference_model='PF', plot=['activations'], thread=False)
#estimator = BeatNet(1, mode='offline', inference_model='PF', plot=['activations'], thread=False)

Output = estimator.process("./test/test_data/808kick120bpm.mp3")
#Output = estimator.process()
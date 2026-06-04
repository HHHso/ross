import torch
import openvino as ov
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from pygame import mixer
from openvoice.api import OpenVoiceBaseClass,BaseSpeakerTTS

class OVOpenVoiceBase(torch.nn.Module):
    """
    Base class for both TTS and voice tone conversion model: constructor is same for both of them.
    """
    def __init__(self, voice_model: OpenVoiceBaseClass):
        super().__init__()
        self.voice_model = voice_model
        for par in voice_model.model.parameters():
            par.requires_grad = False

class OVOpenVoiceTTS(OVOpenVoiceBase):
    """
    Constructor of this class accepts BaseSpeakerTTS object for speech generation and wraps it's 'infer' method with forward.
    """
    def get_example_input(self):
        stn_tst = self.voice_model.get_text('this is original text', self.voice_model.hps, False)
        x_tst = stn_tst.unsqueeze(0)
        x_tst_lengths = torch.LongTensor([stn_tst.size(0)])
        speaker_id = torch.LongTensor([1])
        noise_scale = torch.tensor(0.667)
        length_scale = torch.tensor(1.0)
        noise_scale_w = torch.tensor(0.6)
        return (x_tst, x_tst_lengths, speaker_id, noise_scale, length_scale, noise_scale_w)

    def forward(self, x, x_lengths, sid, noise_scale, length_scale, noise_scale_w):
        return self.voice_model.model.infer(x, x_lengths, sid, noise_scale, length_scale, noise_scale_w)

def get_pathched_infer(ov_model: ov.Model, device: str) -> callable:
    compiled_model = core.compile_model(ov_model, device)
    def infer_impl(x, x_lengths, sid, noise_scale, length_scale, noise_scale_w):
        ov_output = compiled_model((x, x_lengths, sid, noise_scale, length_scale, noise_scale_w))
        return (torch.tensor(ov_output[0]), )
    return infer_impl

core = ov.Core()
zh_suffix = f'checkpoints/base_speakers/ZH'
ZH_TTS_IR = f'openvino_irs/openvoice_zh_tts.xml'
save_path = f'output_chinese.wav'

ov_zh_tts = core.read_model(ZH_TTS_IR)
zh_base_speaker_tts = BaseSpeakerTTS(f'{zh_suffix}/config.json', device="cpu")
zh_base_speaker_tts.load_ckpt(f'{zh_suffix}/checkpoint.pth')
zh_base_speaker_tts.model.infer = get_pathched_infer(ov_zh_tts, "CPU")

def TTS(text):
    zh_base_speaker_tts.tts(text, 'tmp.wav', speaker='default', language='Chinese')
    mixer.init()
    mixer.music.load('tmp.wav')
    mixer.music.play()
    while mixer.music.get_busy() == True:continue
    mixer.music.stop()
    mixer.quit()

# ROS2 服務
class TTS_node(Node):
    def __init__(self):
        super().__init__('tts_service_node')
        # 訂閱
        self.subscription = self.create_subscription(String,"speak_text",self.listener_callback,10) 
        
    def listener_callback(self, msg):
        # 在服務中調用 TTS 函數，並將請求中的字串傳入
        self.get_logger().info(f"Received request to speak: {msg.data}")
        TTS(msg.data)  # 使用請求中的字串作為TTS的輸入
        
def main(args=None):
    rclpy.init(args=args)
    node = TTS_node()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()


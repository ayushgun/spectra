from optimum.exporters.onnx import main_export
from optimum.exporters.onnx.model_configs import OwlViTOnnxConfig
from transformers import AutoConfig

from optimum.exporters.onnx.base import ConfigBehavior
from typing import Dict

class OwlV2OnnxConfig(OwlViTOnnxConfig):
    pass

model_id = "google/owlv2-base-patch16-ensemble"
config = AutoConfig.from_pretrained(model_id)

owl_v2_onnx_config = OwlV2OnnxConfig(
    config=config,
    task="zero-shot-object-detection",
)

# encoder_config = owl_v2_onnx_config.with_behavior("encoder")
# decoder_config = owl_v2_onnx_config.with_behavior("decoder", use_past=False)
# decoder_with_past_config = owl_v2_onnx_config.with_behavior("decoder", use_past=True)

custom_onnx_configs={
    "encoder_model": owl_v2_onnx_config,
    "decoder_model": owl_v2_onnx_config,
    "decoder_with_past_model": owl_v2_onnx_config,
}

# custom_onnx_configs = {
    
# }

main_export(
    model_id,
    output="owlv2-onnx",
    task="zero-shot-object-detection",
    # no_post_process=True,
    # model_kwargs={"output_attentions": True},
    custom_onnx_configs=custom_onnx_configs
)
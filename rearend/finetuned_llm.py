from transformers import AutoModelForCausalLM, AutoTokenizer, TextStreamer
from tokens import HF_TOKEN

model_id = "google/gemma-2b"
peft_model_id = "apfurman/gemma-dolly-agriculture"

model = AutoModelForCausalLM.from_pretrained(model_id, token=HF_TOKEN)
model.load_adapter(peft_model_id)
tokenizer = AutoTokenizer.from_pretrained(model_id, token=HF_TOKEN)

#note this code will only work on the intel compute
import intel_extension_for_pytorch as ipex
import torch

qconfig = ipex.quantization.get_weight_only_quant_qconfig_mapping(
  weight_dtype=torch.quint4x2, # or torch.qint8
  lowp_mode=ipex.quantization.WoqLowpMode.NONE, # or FP16, BF16, INT8
)
checkpoint = None # optionally load int4 or int8 checkpoint

# PART 3: Model optimization and quantization
model_ipex = ipex.llm.optimize(model, quantization_config=qconfig, low_precision_checkpoint=checkpoint)

del model 

# user = "\n\n Give 5 facts about peach leaf curling."


def ask(prompt):
    print("prompting: ", prompt)
    inputs = tokenizer(prompt, return_tensors="pt").input_ids
    with torch.inference_mode():
        tokens = model_ipex.generate(
            inputs,
            pad_token_id=128001,
            eos_token_id=128001,
            max_new_tokens=100,
            repetition_penalty=1.5,
        )
        
    return tokenizer.decode(tokens[0], skip_special_tokens=True)

if __name__ == '__main__':
    print("prompting...")
    user= "\n\n Winter slows down many garden pest problems, but it is also a key time for gardeners to take actions to prevent certain pest problems next spring. One of the most important of these preventive practices is application of dormant treatments for peach leaf curl. Caused by the fungus Taphrina deformans, peach leaf curl is a very serious disease, which affects only peach and nectarine trees. Its most distinctive symptom is distortion, thickening, and reddening of foliage as trees leaf out in the spring. Damaged leaves often die and fall off trees but will be replaced with new, usually healthy leaves once the weather turns dry and warmer. A leaf curl infection that continues untreated over several years will contribute to a tree’s decline and reduce fruit production. To prevent peach leaf curl, peach and nectarine trees must be treated with preventive fungicides during the dormant season. The best time is after leaves have fallen, usually in December. In wet climates or during a wet winter, a second application can be made in late winter or early spring just before buds swell. If the December treatment wasn’t made, it can be applied in January or February as buds begin to expand. Although gardeners won’t notice the symptoms until spring, there is little that they can do at that time to reduce leaf curl. Treatment applied after trees leaf out or after symptoms appear won’t be effective. Removing affected leaves or shoots will not reduce the problem. There are a few peach varieties that are resistant or partially resistant to leaf curl. These are Frost, Indian Free, Muir, and Q-1-8. Your local nurseries may feature these varieties for customers who prefer not to apply the dormant spray. Dormant Treatment Materials Recently Discontinued Two important fungicides traditionally used to treat peach leaf curl were withdrawn from the market in the last year. Lime sulfur (calcium polysulfide) was cancelled for backyard uses by the U.S. EPA, effective Dec. 31, 2010. Tribasic copper sulfate (sold as Microcop by Lilly Miller) has been discontinued by the manufacturer, although existing supplies can be sold and used. As a result, the options for dormant treatments for preventing peach leaf curl in backyard trees are limited and less than ideal. Copper ammonium complex is still available but is only 8% copper. It can be made more effective by applying it with 1% oil in the solution. The fungicide chlorothalonil is effective, and several trade named products are available. However, care must be taken in handling chlorothalonil, since it is listed as a likely carcinogen and can also cause severe eye or skin irritation if applied improperly or proper protective clothing and equipment isn’t worn. Bordeaux mixture, which gardeners can mix up themselves by following the directions in the UC IPM publication Pest Note: Bordeaux Mixture (http://www.ipm.ucdavis.edu/PMG/PESTNOTES/pn7481.html), is also effective, but most gardeners will find the process of finding the ingredients and mixing up Bordeaux more work than they are willing to do to protect one or two backyard trees. For gardeners wishing to take the extra time to make Bordeaux mixture, be sure to have goggles, gloves, and a dust and mist-filtering respirator when working with hydrated lime and mixing up the solution. Five facts about peach leaf curling are:"
    response = ask(user)
    print(response)

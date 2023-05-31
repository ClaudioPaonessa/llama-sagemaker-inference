from pathlib import Path
import random
import flask
import json
from llama_cpp import Llama

prefix = "/opt/ml/"
model_path = Path(prefix, "model")


# A singleton for holding the model. This simply loads the model and holds it.
# It has a predict function that does a prediction based on the model and the input data.
class LlamaLLM(object):
    llm = None

    @classmethod
    def get_model(cls):
        if cls.llm == None:
            cls.llm = Llama(
                model_path=str(Path(model_path, "modelfile.bin")),
                seed=random.randint(0, 65535),
            )
        return cls.llm

    @classmethod
    def predict(
        cls,
        text: str,
        prior_output: str = "",
        penalty: float = 1.1,
        token_count: int = 50,
    ):
        returndict = {}
        
        model_instance = cls.get_model()
        print(f"Start generation. input: {text}")
        '''
        output = model_instance(
            "Below is an instruction that describes a task, as well as any previous text you have generated. You must continue where you left off if there is text following Previous Output. Write a response that appropriately completes the request. When you are finished, write [[COMPLETE]].\n\n Instruction: "
            + text
            + " Previous output: "
            + prior_output
            + " Response:",
            repeat_penalty=penalty,
            echo=False,
            max_tokens=token_count,
        )
        '''
        output = model_instance(
            " Question"
            + text
            + " Response:",
            repeat_penalty=penalty,
            echo=False,
            max_tokens=token_count,
        )
        print(output)
        returndict["response"] = output["choices"][0]["text"]
        return returndict


# The flask app for serving predictions
app = flask.Flask(__name__)


@app.route("/ping", methods=["GET"])
def ping():
    # In this container, we declare it healthy if we can load the model successfully.
    health = LlamaLLM.get_model() is not None
    status = 200 if health else 404
    return flask.Response(response="\n", status=status, mimetype="application/json")


@app.route("/invocations", methods=["POST"])
def transformation():
    data = flask.request.get_json()
    text = data["text"]
    prior_output = data.get("prior_output", "")
    penalty = float(data.get("penalty", 1.1))
    token_count = int(data.get("token_count", 50))

    result = LlamaLLM.predict(
        text=text, prior_output=prior_output, penalty=penalty, token_count=token_count
    )

    return flask.Response(response=json.dumps(result), status=200, mimetype="application/json")

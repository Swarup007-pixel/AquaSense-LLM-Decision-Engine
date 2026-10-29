import importlib
import model





model = importlib.reload(model)
llm = model.get_llm()
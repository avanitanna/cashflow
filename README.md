## Escaping the Ratrace with LLMs

This repo contains a simple AI workflow that models a player in Robert Kiyosaki's Cashflow game.

### Setup

1. Install [Ollama](https://ollama.com/)
2. Pick the model you want to run and download it. By default, the workflow uses Llama3.2 3B. Make sure everything works by chatting with the model:
```
ollama run <modelname>
```
3. Only if you picked a different model than Llama 3.2 3B, update the model in `ratrace_workflow.py` in line 353.
4. Install dependencies:
```
pip install -r requirements.txt
```

You can now run the workflow and play the game!
```
python3 ratrace_workflow.py
```

### Test suite

This repo also contains a small test suite/benchmark for the workflow. You can run it after the setup as
```
python3 test_suite.py
```

You can use the test suite to test out with model works best for you.

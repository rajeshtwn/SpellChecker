- **Run Ollama3 locally:**
  1. Step 1: Install Ollama (if not already): 
  
     https://ollama.com/download

  2. Step 2: Pull a LLaMA Model

     ```ollama pull llama3```

     To reduce latency, consider:
     
      ```ollama pull mistral```
	
     Use mistral or quantized llama3 (like llama3:8b-q4) for better speed.
  
  3. Step 3: Start Ollama Server
  
     ```ollama run llama3```


- **Run FastAPI server:**
   
  ```$ uvicorn main:app --reload```


- **API call request (cURL):**
  1. $ curl -X POST "http://localhost:8000/spell-correct/" -F "Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain."
  2. $ curl -X POST "http://localhost:8000/spell-correct-ollama/" -F "Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain."
  3. $ curl -X POST "http://localhost:8000/wer/" -F "reference=Patient suffers from hypertension and diabetes. He was admitted to the hospital with chest pain." -F "original=Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain." -F "hypothesis=patient surfers from hypertension and diabetes he was admitted to they hospital with cheats pain"
  4. $ curl -X POST "http://localhost:8000/cer/" -F "reference=Patient suffers from hypertension and diabetes. He was admitted to the hospital with chest pain." -F "original=Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain." -F "hypothesis=patient surfers from hypertension and diabetes he was admitted to they hospital with cheats pain"

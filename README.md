- Run FastAPI server:
   $ uvicorn main:app --reload

- API call request (cURL):
  1. $ curl -X POST "http://localhost:8000/spell-correct/" -F "Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain."
  2. $ curl -X POST "http://localhost:8000/wer/" -F "reference=Patient suffers from hypertension and diabetes. He was admitted to the hospital with chest pain." -F "original=Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain." -F "hypothesis=patient surfers from hypertension and diabetes he was admitted to they hospital with cheats pain"
  3. $ curl -X POST "http://localhost:8000/cer/" -F "reference=Patient suffers from hypertension and diabetes. He was admitted to the hospital with chest pain." -F "original=Patint sufers from hypertensoin and dibetes. He was admited to the hosptal with chets pain." -F "hypothesis=patient surfers from hypertension and diabetes he was admitted to they hospital with cheats pain"

# gaqqie-rainbow: a library for providers to access the quantum computer cloud platform gaqqie-sky in gaqqie suite

**This is a beta version.**

[![License](https://img.shields.io/github/license/gaqqie/gaqqie-rainbow.svg?style=flat)](https://opensource.org/licenses/Apache-2.0)


## What is **gaqqie-rainbow**?

**gaqqie-rainbow** is a library for providers to access the quantum computer cloud platform **gaqqie-sky** in **gaqqie** suite.  
For more information on **gaqqie**, see [this](https://github.com/gaqqie/gaqqie).


## Installation

```bash
pip install gaqqie-rainbow
```


## How to use gaqqie-rainbow

The currently supported quantum programming language is Qiskit.

```python
import json

from qiskit import Aer, execute
from qiskit.assembler import disassemble
from qiskit.qobj import QasmQobj

from gaqqie_rainbow import Gaqqie
from gaqqie_rainbow.rest import Result


url = "https://<api-id>.execute-api.<region>.amazonaws.com/<stage>" # rewrite to the endpoint URL of the provier API
app = Gaqqie(url)


@app.receive_job(device_name="qiskit_simulator", interval=10)
def receive_job(job):
    job_id = job.id
    print(f"receive_job job_id={job_id}")

    # parse circuit
    qobj_json = json.loads(job.instructions)
    qobj = QasmQobj.from_dict(qobj_json)
    circuit = disassemble(qobj)

    # execute circuit
    backend = Aer.get_backend("qasm_simulator")
    aer_job = execute(circuit[0][0], backend)

    # parse result
    result = aer_job.result()
    print(f"result      job_id={job_id}, counts={result.get_counts()}")
    result_dict = result.to_dict()
    result_dict["backend_name"] = job.device_name
    result_json = json.dumps(result_dict, indent=2)

    # register result
    job_result = Result(job_id=job_id, status="SUCCEEDED", results=result_json)
    response = app.register_result(job_result)


app.join()
```

Sample output:
```
receive_job job_id=6abff77e-4fda-4880-b3a5-ea8f49ff7cf0
result      job_id=6abff77e-4fda-4880-b3a5-ea8f49ff7cf0, counts={'00': 482, '11': 542}
```


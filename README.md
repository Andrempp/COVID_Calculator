#COVID-19 in Portugal: predictability of hospitalization, ICU and respiratory-assistance needs

In the context of our work, the following clinical decision support system with graphical facilities was produced.

## Installation:

Python 3+

All dependencies defined in **requirements.txt**. You can install them by:

```
$ conda config --append channels conda-forge
$ conda create --name <env> --file requirements.txt
$ conda activate <env>
```

## Usage:

After installing the required dependencies and activating your freshly created environment you should be able to run our app. 

You can see our interface for the clinical decision support system by running and accessing http://127.0.0.1:8050/:

```
$ python main.py
```

You can test our solution by filling the following fields of the patient profile:
* Stage at which the patient is, namely, after testing positive, after hospitalization, or after ICU internment.
* Age
* Gender
* Comorbidities

Press "RUN QUERY", and the probabilities of the various events will be shown, with the distinction of which classifier made them.


---

 Please cite: contributions currently under review, contact Rui Henriques (rmch@tecnico.ulisboa.pt) or Rafael Costa (rs.costa@fct.unl.pt) to obtain the updated reference.

 Guidelines to access data are available upon request.

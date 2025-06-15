# Rio de Janeiro bus prediction

**Data Mining Course (CPS833) at PESC UFRJ.**

This project aims to predict the future location of buses in Rio de Janeiro based on historical location and schedule data.

## Model

The model is based on identifying historical patterns to predict the future location of buses.
We use historical location and time data for buses in Rio de Janeiro to find past records that have similar characteristics to the current ones, such as route and approximate location.

From these records, we select points that have a similar movement behavior and calculate the median of the future location coordinates,
to provide a prediction of where the bus will be at a future time.

This method allows a prediction based on actual observed patterns, increasing the accuracy of the predictions.

## Techs

- PostgreSQL
- SQLAlchemy (Python)
- Python 3.x

## **Setting Up Your Environment**

```
python -m venv .venv
```

```
.venv\Scripts\activate
```

## Install Dependencies

```
pip install -r requirements.txt
```
